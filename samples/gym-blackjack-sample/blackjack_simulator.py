import logging
import sys

from microsoft_bonsai_api.simulator.client import BonsaiClientConfig

from bonsai_gym import GymSimulator3

log = logging.getLogger("gym_simulator")
log.setLevel(logging.DEBUG)


class BlackJack(GymSimulator3):
    environment_name = "Blackjack-v0"
    simulator_name = "blackjack_simulator"

    # convert openai gym observation to our state type
    def gym_to_state(self, observation):
        state = {
            "current_sum": int(observation[0]),
            "dealer_card": int(observation[1]),
            "usable_ace": int(observation[2]),
        }
        return state

    # convert our action type into openai gym action
    def action_to_gym(self, action):
        return action["command"]


if __name__ == "__main__":
    # create a brain, openai-gym environment, and simulator
    config = BonsaiClientConfig(argv=sys.argv)
    sim = BlackJack(config)
    sim.run_gym()
