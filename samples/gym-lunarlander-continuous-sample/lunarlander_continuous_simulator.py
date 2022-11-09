import logging
import sys

import numpy
from microsoft_bonsai_api.simulator.client import BonsaiClientConfig

from bonsai_gym import GymSimulator3

log = logging.getLogger("gym_simulator")
log.setLevel(logging.DEBUG)


class LunarLanderContinuous(GymSimulator3):
    environment_name = "LunarLanderContinuous-v2"
    simulator_name = "LunarLanderSimulator"

    def gym_to_state(self, observation):
        state = {
            "x_position": observation[0],
            "y_position": observation[1],
            "x_velocity": observation[2],
            "y_velocity": observation[3],
            "angle": observation[4],
            "rotation": observation[5],
            "left_leg": observation[6],
            "right_leg": observation[7],
        }
        return state

    # As an Estimator, return as a numpy array.
    def action_to_gym(self, actions):
        engine1 = numpy.clip(actions["engine1"], -1.0, 1.0)
        engine2 = numpy.clip(actions["engine2"], -1.0, 1.0)
        return numpy.asarray([engine1, engine2])


if __name__ == "__main__":
    # create a brain, openai-gym environment, and simulator
    config = BonsaiClientConfig(argv=sys.argv)
    sim = LunarLanderContinuous(config)
    sim.run_gym()
