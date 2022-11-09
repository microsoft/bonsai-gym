import logging
import sys

from microsoft_bonsai_api.simulator.client import BonsaiClientConfig

from bonsai_gym import GymSimulator3

log = logging.getLogger("gym_simulator")
log.setLevel(logging.DEBUG)


SKIP_FRAME = 4


class MountainCar(GymSimulator3):
    environment_name = "MountainCar-v0"
    simulator_name = "MountainCarSimulator"

    def gym_to_state(self, observation):
        state = {"x_position": observation[0], "x_velocity": observation[1]}
        return state

    def action_to_gym(self, inkling_action):
        return inkling_action["command"]


if __name__ == "__main__":
    # create a brain, openai-gym environment, and simulator
    config = BonsaiClientConfig(argv=sys.argv)
    sim = MountainCar(config, skip_frame=SKIP_FRAME)
    sim.run_gym()
