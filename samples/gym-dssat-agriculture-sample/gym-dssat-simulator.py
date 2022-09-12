import sys
import logging
from microsoft_bonsai_api.simulator.client import BonsaiClientConfig
from bonsai_gym import GymSimulator3

log = logging.getLogger("gym_simulator")
log.setLevel(logging.DEBUG)


class GymDSSAT(GymSimulator3):
    # Environment name, from openai-gym
    environment_name = "gym_dssat_pdi:GymDssatPdi-v0"

    # Simulator name from Inkling
    simulator_name = "DSSATSimulator"

    # convert openai gym observation to our state type
    def gym_to_state(self, observation):
        print(f"observation: {observation}")
        return observation

    # convert our action type into openai gym action
    def action_to_gym(self, action):
        print(f"action: {action}")
        return action


if __name__ == "__main__":
    # create a brain, openai-gym environment, and simulator
    print("main")
    config = BonsaiClientConfig(argv=sys.argv)
    sim = GymDSSAT(config)
    sim.run_gym()
