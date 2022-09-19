import argparse
import logging
from typing import Dict, Any, Union
from time import time
import random
import os


import gym
from bonsai_common import SimulatorSession
from microsoft_bonsai_api.simulator.client import BonsaiClientConfig
from microsoft_bonsai_api.simulator.generated.models import SimulatorInterface

logFormatter = "[%(asctime)s][%(levelname)s] %(message)s"
logging.basicConfig(format=logFormatter, datefmt="%Y-%m-%d %H:%M:%S")
log = logging.getLogger(__name__)
log.setLevel(level=logging.INFO)

STATE_REWARD_KEY = "_gym_reward"
STATE_TERMINAL_KEY = "_gym_terminal"


class GymSimulator3(SimulatorSession):
    simulator_name = ""  # name of the simulation in the inkling file
    environment_name = ""  # name of the OpenAI Gym environment

    def __init__(
        self, config: BonsaiClientConfig, iteration_limit: int = 0, skip_frame: int = 1,
    ) -> None:
        super(GymSimulator3, self).__init__(config)

        self.mode = 'uninitialized'
        self.init_mode('all')

        # optional parameters for controlling the simulation
        self._headless = self._check_headless()
        self._iteration_limit = iteration_limit  # default is no limit
        self._skip_frame = skip_frame  # default is to process every frame

        # book keeping for rate status
        self._log_interval = 10.0  # seconds
        self._last_status = time()
        self.episode_count = 0

    def init_mode(self, mode):
        if self.mode == mode:
            return # already in this mode

        print(f'changing mode from {self.mode} to {mode}')

        # create and reset the gym environment
        env_args = {
            'run_dssat_location': '/opt/dssat_pdi/run_dssat',
            'log_saving_path': '/dssat_pdi.log',
            'mode': mode,
            'seed': random.randint(0, 1000000),
            'random_weather': True,
            'auxiliary_file_paths': ['/opt/gym_dssat_pdi/samples/test_files/GAGR.CLI'],
        }

        self._env = gym.make(self.environment_name, **env_args)
        #self._env.seed(20)
        initial_observation = self._env.reset()

        # store initial gym state
        try:
            # initial reward = 0; initial terminal False
            state = self.gym_to_state(initial_observation)
        except NotImplementedError as e:
            raise e
        self._set_last_state(state, 0, False)

        self.iteration_count = 0

        self.mode == mode

    #
    # These MUST be implemented by the simulator.
    #

    def gym_to_state(self, observation: Any) -> Dict[str, Any]:
        """Convert a gym observation into an Inkling state

        Example:
            state = {'position': observation[0],
                     'velocity': observation[1],
                     'angle':    observation[2],
                     'rotation': observation[3]}
            return state

        :param observation: gym observation, see specific gym
            environment for details.
        :return A dictionary matching the Inkling state schema.
        """
        raise NotImplementedError("No gym_to_state() implementation found.")

    def action_to_gym(self, action) -> Any:
        """Convert an Inkling action schema into a gym action.

        Example:
            return action['command']

        :param action: A dictionary as defined in the Inkling schema.
        :return A gym action as defined in the gym environment
        """
        raise NotImplementedError("No action_to_gym() implementation found.")

    #
    # These MAY be implemented by the simulator.
    #

    def gym_episode_start(self, parameters):
        """
        called during episode_start() to return the initial observation
        after reseting the gym environment. clients can override this
        to provide additional initialization.
        """
        if 'mode' in parameters:
            if parameters['mode'] == 1:
                self.init_mode('fertilization')
            elif parameters['mode'] == 2:
                self.init_mode('irrigation')
            elif parameters['mode'] == 3:
                self.init_mode('all')
        observation = self._env.reset()
        log.debug("start state: " + str(observation))
        return observation

    def gym_simulate(self, gym_action):
        """
        called during simulate to single step the gym environment
        and return (observation, reward, done, info).
        clients can override this method to provide additional
        reward shaping.
        """
        observation, reward, done, info = self._env.step(gym_action)
        print(f'reward: {reward}')
        return observation, reward, done, info

    def run_gym(self):
        """
        runs the simulation until cancelled or finished
        """
        while self.run():
            continue
        log.info("Simulator finished running")

    #
    # SDK3 SimulatorSession methods
    #

    def get_interface(self):
        return SimulatorInterface(
            name=self.simulator_name,
            timeout=60,
            simulator_context=self.get_simulator_context(),
        )

    def get_state(self):
        return self._last_state

    def episode_start(self, config: Dict[str, Any]):
        self.iteration_count = 0
        self.episode_reward = 0

        # optional configuration arguments for open-ai-gym
        if "iteration_limit" in config:
            self._iteration_limit = config["iteration_limit"]

        # initial observation
        observation = self.gym_episode_start(config)
        state = self.gym_to_state(observation)
        state = self._set_last_state(state, 0, False)
        return state

    def episode_step(self, action: Dict[str, Any]):

        # simulate
        gym_action = self.action_to_gym(action)
        rwd_accum = 0
        done = False
        i = 0
        observation = None

        for i in range(self._skip_frame):
            print(f'gym_simulate({gym_action})')
            observation, reward, done, info = self.gym_simulate(gym_action)
            print(f'-> observation: {observation}, reward: {reward}, done: {done}, info: {info}')
            if done and reward == None:
                reward = 0
                print(f'set done reward to {reward}')
            if isinstance(reward, list):
                # In the all mode (both irrigation and fertilization) the reward is a list of two values.
                # TODO: Not clear how this should be handled in Bonsai. For now, let's add them together.
                #       Perhaps we should return them in separate values or perhaps we should be using goals
                #       instead of the simulator-supplied gym rewards?
                reward = sum(reward)
                print(f'flattened reward to {reward}')
            self.iteration_count += 1
            rwd_accum += reward

            log.debug(
                "step action: {} state: {} reward: {} done: {}".format(
                    str(gym_action), str(observation), str(reward), str(done)
                )
            )

            # episode limits
            if self._iteration_limit > 0:
                if self.iteration_count >= self._iteration_limit:
                    done = True
                    log.debug("iteration_limit reached.")
                    break

            # render if not headless
            if not self._headless:
                if "human" in self._env.metadata["render.modes"]:
                    self._env.render()

        # print a periodic status of iterations and episodes
        self._periodic_status_update()

        # calculate reward
        reward = rwd_accum / (i + 1)
        self.episode_reward += reward

        # convert state and return to the server
        print(f'gym_to_state({observation})')
        state = self.gym_to_state(observation)
        print(f'-> state: {state}, reward: {reward}, done: {done}')
        state = self._set_last_state(state, reward, done)
        return state

    def episode_finish(self, reason: str):
        log.info(
            "Episode {} reward is {}".format(self.episode_count, self.episode_reward)
        )
        log.debug(
            "finish episode: "
            + str(self.episode_count)
            + " reward: "
            + str(self.episode_reward)
        )
        self.episode_count += 1
        self._last_status = time()

    def halted(self):
        return False

    #
    # Internal methods
    #

    def _set_last_state(self, state: Dict[str, Any], reward: float, terminal: bool):
        if terminal and state == None:
            print('not updating _last_state because terminal and state is None')
        else:
            self._last_state = state
        self._last_state[STATE_REWARD_KEY] = reward
        self._last_state[STATE_TERMINAL_KEY] = terminal
        return self._last_state

    def _periodic_status_update(self):
        """ print a periodic status update showing iterations/sec
        """
        if time() - self._last_status > self._log_interval:
            log.info(
                "Episode {} is still running, "
                "reward so far is {}".format(self.episode_count, self.episode_reward)
            )
            self._last_status = time()

    def _check_headless(self) -> bool:
        parser = argparse.ArgumentParser()
        parser.add_argument("--headless", action="store_true", default=False)
        args, unknown = parser.parse_known_args()
        headless = args.headless
        if headless:
            log.debug(
                "Running simulator headlessly, graphical "
                "environment will not be displayed."
            )
        else:
            log.debug(
                "Starting simulator with graphical evironment. "
                "Use --headless to disable."
            )
        return headless
