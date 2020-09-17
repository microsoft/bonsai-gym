import sys
import logging

from microsoft_bonsai_api.simulator.client import BonsaiClientConfig
from bonsai_gym import GymSimulator3
from gym.envs.registration import register

log = logging.getLogger("gym_simulator")
log.setLevel(logging.DEBUG)

# frozenlake
ENVIRONMENT = "FrozenLake-no-slip-v0"

# Map types: 4x4 or 8x8.
MAP_4x4 = "4x4"
MAP_8x8 = "8x8"

# Whether or not choose the non-deterministic states.
IS_SLIPPERY = False

MAX_EPISODE_LENGTH = 200

# Register a custom environment for frozen lake with deterministic states
register(
    id=ENVIRONMENT,
    entry_point="gym.envs.toy_text:FrozenLakeEnv",
    kwargs={"map_name": MAP_4x4, "is_slippery": IS_SLIPPERY},
    tags={"wrapper_config.TimeLimit.max_episode_steps": 100},
    reward_threshold=0.78,
)


class FrozenLake(GymSimulator3):
    environment_name = ENVIRONMENT
    simulator_name = "frozenlake_simulator"

    BOTTOM_BOUNDARY = 11
    GO_DOWN_INDEX = 0
    REACH_GOAL_INDEX = 1

    def __init__(self, brain):
        super(FrozenLake, self).__init__(brain, iteration_limit=MAX_EPISODE_LENGTH)
        self._concept_index = 1

    def gym_to_state(self, observation):
        state = {"current_pos": observation}
        return state

    def action_to_gym(self, actions):
        return actions["command"]

    # called during episode_start() to reset the gym environment and retrieve
    # the initial state. we add some additional setup here.
    def gym_episode_start(self, parameters):
        observation = super(FrozenLake, self).gym_episode_start(parameters)

        # unpack config value
        if "concept_index" in parameters:
            self._concept_index = parameters["concept_index"]

        # print out which concept we're running for this episode
        if self._concept_index == self.GO_DOWN_INDEX:
            log.info("Simulator is running for concept go_down. ")
        elif self._concept_index == self.REACH_GOAL_INDEX:
            log.info("Simulator is running for concept reach_goal. ")
        else:
            raise RuntimeError("No concept index is found.")

        return observation

    # called during simulate() to single step the gym simulation. we add
    # some additional reward shaping here.
    def gym_simulate(self, gym_action):
        observation, reward, done, info = super(FrozenLake, self).gym_simulate(
            gym_action
        )

        # base done & reward on the current concept
        if self._concept_index == self.GO_DOWN_INDEX:
            if gym_action == 1:
                reward = 10
            else:
                reward = -10
            done = done or (observation > self.BOTTOM_BOUNDARY)

        elif self._concept_index == self.REACH_GOAL_INDEX:
            pass

        else:
            raise RuntimeError("No concept index is found.")

        return observation, reward, done, info


if __name__ == "__main__":
    # create a brain, openai-gym environment, and simulator
    config = BonsaiClientConfig(argv=sys.argv)
    sim = FrozenLake(config)
    sim.run_gym()
