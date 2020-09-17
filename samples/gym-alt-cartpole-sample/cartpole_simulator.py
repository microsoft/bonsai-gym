import sys
import logging
from microsoft_bonsai_api.simulator.client import BonsaiClientConfig
from bonsai_gym import GymSimulator3

log = logging.getLogger("gym_simulator")
log.setLevel(logging.DEBUG)


class CartPole(GymSimulator3):
    environment_name = "CartPole-v0"
    simulator_name = "cartpole_simulator"

    def gym_to_state(self, observation):
        state = {
            "position": observation[0],
            "velocity": observation[1],
            "angle": observation[2],
            "rotation": observation[3],
        }
        return state

    # in order to test non-zero based ranges, the inkling file for cartpole has
    # been modified to use arbitrary integers for the actions (not just 0/1)
    # to properly test that the backend is producing the correct outputs.
    # To test this properly, I'm overloading the simulator's accessor to
    # the action to convert to the 0/1 numbers that the openai gym is expecting
    def action_to_gym(self, inkling_action):
        action = inkling_action["command"]
        if action == 17:
            # convert 17 to 0
            action = 0
        elif action == 41:
            # convert 41 to 1
            action = 1
        else:
            # anything else is an error
            raise RuntimeError("Received invalid action: %s", action)
        return action


if __name__ == "__main__":
    # create a brain, openai-gym environment, and simulator
    config = BonsaiClientConfig(argv=sys.argv)
    sim = CartPole(config)
    sim.run_gym()
