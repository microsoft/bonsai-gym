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
        print(f"observation: mode {self.mode}, {observation}")
        if observation:
            if self.mode == 'fertilization':
                observation['mode'] = 1
            elif self.mode == 'irrigation':
                observation['mode'] = 2
            elif self.mode == 'all':
                observation['mode'] = 3
            else:
                observation['mode'] = 0

            if observation.get('dap', 0) == 4377089:
                # TODO: Not sure why this happens.
                print("dap is 4377089. Strange that this is the first observation. We'll reassign it to 0.")
                observation['dap'] = 0
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
