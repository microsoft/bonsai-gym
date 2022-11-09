import logging
from bonsai_gym import GymSimulator3

log = logging.getLogger("gym_simulator")
log.setLevel(logging.DEBUG)


class CartPole(GymSimulator3):
    # Environment name, from openai-gym
    environment_name = "CartPole-v1"

    # Simulator name from Inkling
    simulator_name = "CartpoleSimulator"

    # convert openai gym observation to our state type
    def gym_to_state(self, observation):
        state = {
            "position": observation[0],
            "velocity": observation[1],
            "angle": observation[2],
            "rotation": observation[3],
        }
        return state

    # convert our action type into openai gym action
    def action_to_gym(self, action):
        return action["command"]


if __name__ == "__main__":
    # create a brain, openai-gym environment, and simulator
    sim = CartPole()
    sim.run_gym()
