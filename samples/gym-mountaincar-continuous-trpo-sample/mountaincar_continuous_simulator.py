import sys
import numpy
import logging
from microsoft_bonsai_api.simulator.client import BonsaiClientConfig
from bonsai_gym import GymSimulator3
from gym.envs.registration import register

log = logging.getLogger("gym_simulator")
log.setLevel(logging.DEBUG)

EPISODE_LIMIT = 6000
SKIP_FRAME = 4

register(
    id="TRPO-MountainCarContinuous-v0",
    entry_point="gym.envs.classic_control:Continuous_MountainCarEnv",
    tags={"wrapper_config.TimeLimit.max_episode_steps": 6000},
    reward_threshold=90.0,
)


class MountainCarContinuous(GymSimulator3):
    environment_name = "TRPO-MountainCarContinuous-v0"
    simulator_name = "mountaincar_continuous_simulator"

    def gym_to_state(self, observation):
        state = {"x_position": observation[0], "x_velocity": observation[1]}
        return state

    # As an Estimator, continuous mountaincar returns the command
    # as a numpy array.
    def action_to_gym(self, actions):
        # return actions['command']
        return numpy.asarray([actions["command"]])


if __name__ == "__main__":
    # create a brain, openai-gym environment, and simulator
    config = BonsaiClientConfig(argv=sys.argv)
    sim = MountainCarContinuous(
        config, iteration_limit=EPISODE_LIMIT, skip_frame=SKIP_FRAME
    )
    sim.run_gym()
