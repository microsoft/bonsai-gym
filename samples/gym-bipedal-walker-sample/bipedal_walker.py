"""
Bipedal walker sim.
"""
__copyright__ = "Copyright 2021, Microsoft Corp."

import datetime
import logging
import sys
from typing import Any, cast, Dict, List, Tuple, Union

from teachDRL.gym_flowers.envs.bipedal_walker_continuous import (
    BipedalWalkerContinuous as BipedalWalkerContinuous,
)

from microsoft_bonsai_api.simulator.client import BonsaiClientConfig
from bonsai_gym import GymSimulator3

log = logging.getLogger("bonsai_gym.gym_simulator3")
log.setLevel(logging.DEBUG)

ENVIRONMENT = "bipedal-walker-continuous-v0"
RECORD_PATH = None

logger = logging.getLogger(__name__)


class BipedalWalkerSimulator(GymSimulator3):
    environment_name = ENVIRONMENT
    simulator_name = "BipedalWalkerSimulator"

    def __init__(self, *args: Any, **kwargs: Any):
        # There is an SDK3 limitation for pulling info from self._env
        # That's why we use NB_LIDAR as opposed to custom_env.NB_LIDAR
        # and we have to do it before super().__init__()
        NB_LIDAR = 10
        nb_leg_pairs = 1

        self._fields = [
            "hull_ang",
            "hull_ang_vel",
            "x_velocity",
            "y_velocity",
            "leg_1_hip_angle",
            "leg_1_hip_speed",
            "leg_1_knee_angle",
            "leg_1_knee_speed",
            "leg_1_contact",
            "leg_2_hip_angle",
            "leg_2_hip_speed",
            "leg_2_knee_angle",
            "leg_2_knee_speed",
            "leg_2_contact",
        ] + [f"lidar{i}" for i in range(NB_LIDAR)]

        super().__init__(*args, **kwargs)
        custom_env = cast(Any, self._env)
        custom_env.env.my_init({"leg_size": "default"})

        self._parameters: Dict[str, Any] = {}
        self._timestamp = datetime.datetime.now()

        assert len(self._fields) == (4 + 5 * nb_leg_pairs * 2 + NB_LIDAR)

    def gym_to_state(
        self, observation: Tuple[Union[int, float]]
    ) -> Dict[str, Union[int, float]]:
        state = {field: observation[i] for i, field in enumerate(self._fields)}
        return state

    def action_to_gym(
        self, action: Dict[str, Union[int, float]]
    ) -> List[Union[int, float]]:
        return [
            action['leg_1_torque'][0], # hip joint 1
            action['leg_1_torque'][1], # knee joint 1
            action['leg_2_torque'][0], # hip joint 2
            action['leg_2_torque'][1], # knee joint 2
        ]

    def episode_start(self, config: Dict[str, Any]) -> Any:
        logger.info(f"Starting an episode with parameters {config}.")
        self._parameters = config
        custom_env = cast(Any, self._env)
        custom_env.env.set_environment(**config)
        return super().episode_start(config)

    def episode_finish(self, reason: str) -> None:
        return 0


if __name__ == "__main__":
    # create a brain, openai-gym environment, and simulator
    config = BonsaiClientConfig(argv=sys.argv)
    sim = BipedalWalkerSimulator(config)
    sim.run_gym()
