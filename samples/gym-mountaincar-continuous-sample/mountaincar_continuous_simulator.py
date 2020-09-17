import sys
import numpy
import logging
from microsoft_bonsai_api.simulator.client import BonsaiClientConfig
from bonsai_gym import GymSimulator3

log = logging.getLogger("gym_simulator")
log.setLevel(logging.DEBUG)


SKIP_FRAME = 6


class MountainCarContinuous(GymSimulator3):
    environment_name = "MountainCarContinuous-v0"
    simulator_name = "MountainCarSimulator"

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
    sim = MountainCarContinuous(config, skip_frame=SKIP_FRAME)
    sim.run_gym()
