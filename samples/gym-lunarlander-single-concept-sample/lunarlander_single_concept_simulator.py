import logging
import sys

from bonsai_gym import GymSimulator3

log = logging.getLogger("gym_simulator")
log.setLevel(logging.DEBUG)


class LunarLander(GymSimulator3):
    environment_name = "LunarLander-v2"
    simulator_name = "lunarlander_simulator"

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

    def action_to_gym(self, inkling_action):
        return inkling_action["command"]


if __name__ == "__main__":
    # create a brain, openai-gym environment, and simulator
    sim = LunarLander()
    sim.run_gym()
