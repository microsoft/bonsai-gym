import dataclasses
from enum import Enum
from typing import Dict, Optional, Union

from microsoft_bonsai_api.simulator.client import BonsaiClient, BonsaiClientConfig
from microsoft_bonsai_api.simulator.generated.models import (
    SimulatorInterface,
    SimulatorState,
)

from bonsai_gym.logger import log


class BonsaiEventType(Enum):
    IDLE = "Idle"
    EPISODE_START = "EpisodeStart"
    EPISODE_STEP = "EpisodeStep"
    EPISODE_FINISH = "EpisodeFinish"


@dataclasses.dataclass
class BonsaiEvent:
    event_type: BonsaiEventType
    event_content: Optional[Dict[str, Union[str, dict]]]

    def __repr__(self):
        return f"{self.event_type}: {self.event_content}"


class BonsaiConnector:
    """
    Class that allows communications between Bonsai and Simulation.

    The class initialized by passing the simulation interface as a
    JSON-serializable dictionary. The dictionary must contain the ``name`` of
    the sim and the ``timeout`` in seconds as an ``int``.
    """

    def __init__(self, sim_interface, *, verbose=False):
        client_config = BonsaiClientConfig(enable_logging=verbose)
        self.workspace = client_config.workspace
        self.client = BonsaiClient(client_config)
        self.verbose = verbose

        reg_info = SimulatorInterface(
            simulator_context=client_config.simulator_context,
            **sim_interface,
        )
        self.registered_session = self.client.session.create(
            workspace_name=self.workspace,
            body=reg_info,
        )
        log.info(
            f"Created session with session_id {self.registered_session.session_id}"
        )
        self.sequence_id = 1

    @staticmethod
    def validate_state(state):
        """
        Validate the state.

        The serialization of the state works only on builtin types.

        TODO: consider whether nested list/dict should be evaluated
        """
        allowed_types = (bool, dict, float, int, list)

        def has_invalid_type(x):
            """
            Return False when x is not an allowed type.

            We need to use ``type`` instead of ``isinstance`` because of:
            https://github.com/Azure/msrest-for-python/issues/257
            """
            return type(x) not in allowed_types

        for val in state.values():
            if has_invalid_type(val):
                raise TypeError(f"Type of state variable not supported: {type(val)}")
            if isinstance(val, list):
                for item in val:
                    if has_invalid_type(item):
                        raise TypeError(f"Element in list not supported: {type(val)}")
            elif isinstance(val, dict):
                for nested_val in val.values():
                    if has_invalid_type(nested_val):
                        raise TypeError(f"Element in dict not supported: {type(val)}")

    def next_event(self, gym_state) -> BonsaiEvent:
        """Poll the Bonsai platform for the next event and advance the state."""
        self.validate_state(gym_state)
        sim_state = SimulatorState(
            sequence_id=self.sequence_id,
            state=gym_state,
            halted=gym_state.get("halted", False),
        )
        event = self.client.session.advance(
            workspace_name=self.workspace,
            session_id=self.registered_session.session_id,
            body=sim_state,
        )
        self.sequence_id = event.sequence_id
        if event.type == "Idle":
            return BonsaiEvent(BonsaiEventType.IDLE, {})
        elif event.type == "EpisodeStart":
            return BonsaiEvent(
                BonsaiEventType.EPISODE_START, event.episode_start.config
            )
        elif event.type == "EpisodeStep":
            return BonsaiEvent(BonsaiEventType.EPISODE_STEP, event.episode_step.action)
        elif event.type == "EpisodeFinish":
            return BonsaiEvent(
                BonsaiEventType.EPISODE_FINISH, event.episode_finish.reason
            )
        elif event.type == "Unregister":
            raise RuntimeError(
                "Simulator Session unregistered by platform because of ",
                event.unregister.details,
            )
        raise TypeError(f"Unknown event type. Received {event.type}")

    def close_session(self):
        """Unregister gracefully the sim from Bonsai."""
        log.debug("Closing session...")
        self.client.session.delete(
            workspace_name=self.workspace,
            session_id=self.registered_session.session_id,
        )
