import dataclasses
from enum import Enum
from typing import Dict, Optional, Union

from microsoft_bonsai_api.simulator.client import (BonsaiClient,
                                                   BonsaiClientConfig)
from microsoft_bonsai_api.simulator.generated.models import (
    SimulatorInterface, SimulatorState)


class BonsaiEventType(Enum):
    IDLE = "Idle"
    EPISODE_START = "EpisodeStart"
    EPISODE_STEP = "EpisodeStep"
    EPISODE_FINISH = "EpisodeFinish"


@dataclasses.dataclass
class BonsaiEvent:
    event_type: BonsaiEventType
    event_content: Optional[Dict[str, Union[str, dict]]]


class BonsaiConnector:
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
        print(f'created session with session_id {self.registered_session.session_id}')
        self.sequence_id = 1

    @staticmethod
    def validate_state(state):
        allowed_types = [str, int, float]
        for key, val in state.items():
            if not any(isinstance(val, type_) for type_ in allowed_types):
                raise TypeError(f"Type of state variable not supported: {type(val)}")

    def next_event(self, gym_state):
        """Poll the Bonsai platform for the next event and advance the state."""
        self.validate_state(gym_state)
        sim_state = SimulatorState(
            sequence_id=self.sequence_id,
            state=gym_state,
            halted=gym_state.get('halted', False),
        )
        event = self.client.session.advance(
            workspace_name=self.workspace,
            session_id=self.registered_session.session_id,
            body=sim_state,
        )
        self.sequence_id = event.sequence_id
        if event.type == 'Idle':
            return BonsaiEvent(BonsaiEventType.IDLE, {})
        elif event.type == 'EpisodeStart':
            return BonsaiEvent(BonsaiEventType.EPISODE_START, event.episode_start.config)
        elif event.type == 'EpisodeStep':
            return BonsaiEvent(BonsaiEventType.EPISODE_STEP, event.episode_step.action)
        elif event.type == 'EpisodeFinish':
            return BonsaiEvent(BonsaiEventType.EPISODE_FINISH, event.episode_finish.reason)
        elif event.type == 'Unregister':
            raise RuntimeError(
                "Simulator Session unregistered by platform because of ",
                event.unregister.details,
            )

    def close_session(self):
        self.client.session.delete(
            workspace_name=self.workspace,
            session_id=self.registered_session.session_id,
        )
