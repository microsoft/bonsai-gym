import abc
import json
from time import time
from typing import Any, Dict

import gymnasium as gym

from bonsai_gym.bonsai_connector import BonsaiConnector, BonsaiEventType
from bonsai_gym.serializers import NumpyEncoder

from bonsai_gym.logger import log

STATE_REWARD_KEY = "_gym_reward"
STATE_TERMINAL_KEY = "_gym_terminal"


class GymSimulator3(abc.ABC):
    simulator_name = ""  # name of the simulation in the inkling file
    environment_name = ""  # name of the OpenAI Gym environment

    def __init__(
        self,
        *,
        iteration_limit: int = 0,
        skip_frame: int = 1,
        headless: bool = False,
    ) -> None:

        # create and reset the gym environment
        self._env = gym.make(
            self.environment_name, render_mode="human" if not headless else None
        )
        initial_observation, _ = self._env.reset(seed=20)

        self._set_last_state(initial_observation, 0, False)

        # optional parameters for controlling the simulation
        self._iteration_limit = iteration_limit  # default is no limit
        self._skip_frame = skip_frame  # default is to process every frame

        # book keeping for rate status
        self.iteration_count = 0
        self.episode_count = 0
        self._log_interval = 10.0  # seconds
        self._last_status = time()
        self.connector = BonsaiConnector(self.get_interface())

    #
    # These MUST be implemented by the simulator.
    #

    @abc.abstractmethod
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

    @abc.abstractmethod
    def action_to_gym(self, action) -> Any:
        """Convert an Inkling action schema into a gym action.

        Example:
            return action['command']

        :param action: A dictionary as defined in the Inkling schema.
        :return A gym action as defined in the gym environment
        """

    #
    # These MAY be implemented by the simulator.
    #

    def gym_episode_start(self, parameters):
        """
        called during episode_start() to return the initial observation
        after reseting the gym environment. clients can override this
        to provide additional initialization.
        """
        observation, _ = self._env.reset()
        log.debug("start state: " + str(observation))
        return observation

    def gym_simulate(self, gym_action):
        """
        called during simulate to single step the gym environment
        and return (observation, reward, done, info).
        clients can override this method to provide additional
        reward shaping.
        """
        observation, reward, truncated, terminated, info = self._env.step(gym_action)
        done = truncated or terminated
        return observation, reward, done, info

    def dispatch_event(self, next_event):
        if next_event.event_type == BonsaiEventType.EPISODE_START:
            self.episode_start(next_event.event_content)
        elif next_event.event_type == BonsaiEventType.EPISODE_STEP:
            self.episode_step(next_event.event_content)
        elif next_event.event_type == BonsaiEventType.EPISODE_FINISH:
            self.episode_finish(next_event.event_content)
        elif next_event.event_type == BonsaiEventType.IDLE:
            print("Idling")
        else:
            raise RuntimeError(
                f"Unexpected BonsaiEventType. Got {next_event.event_type}"
            )

    def run_gym(self):
        """
        Run the simulation until cancelled or finished
        """
        try:
            while True:
                next_event = self.connector.next_event(self.get_state())
                self.dispatch_event(next_event)
                log.debug(next_event)
        except KeyboardInterrupt:
            log.info("Terminating...")
        finally:
            self.connector.close_session()
            log.info("Simulator finished running")

    #
    # SDK3 SimulatorSession methods
    #

    def get_interface(self):
        return {
            "name": self.simulator_name,
            "timeout": 60,
        }

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
        state = self._set_last_state(observation, 0, False)
        return state

    def episode_step(self, action: Dict[str, Any]):

        # simulate
        gym_action = self.action_to_gym(action)
        rwd_accum = 0
        done = False
        i = 0
        observation = None

        for i in range(self._skip_frame):
            observation, reward, done, info = self.gym_simulate(gym_action)
            self.iteration_count += 1
            rwd_accum += reward

            log.debug(
                "step action: {} state: {} reward: {} done: {}".format(
                    str(gym_action), str(observation), str(reward), str(done)
                )
            )

            # episode limits
            if self.iteration_count >= self._iteration_limit > 0:
                done = True
                log.debug("iteration_limit reached.")
                break

        if observation is None:
            raise RuntimeError("observation found to be None.")

        # print a periodic status of iterations and episodes
        self._periodic_status_update()

        # calculate reward
        reward = rwd_accum / (i + 1)
        self.episode_reward += reward

        state = self._set_last_state(observation, reward, done)
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

    @property
    def halted(self):
        return False

    #
    # Internal methods
    #

    @staticmethod
    def _sanitize_state(state):
        """Remove non-builtin types from the state."""
        return json.loads(json.dumps(state, cls=NumpyEncoder))

    def _set_last_state(
        self, observation: Dict[str, Any], reward: float, terminal: bool
    ):
        """Store the last state of the sim."""
        state = self.gym_to_state(observation)
        state[STATE_REWARD_KEY] = reward
        state[STATE_TERMINAL_KEY] = terminal
        state["halted"] = self.halted
        self._last_state = self._sanitize_state(state)
        return self._last_state

    def _periodic_status_update(self):
        """print a periodic status update showing iterations/sec"""
        if time() - self._last_status > self._log_interval:
            log.info(
                "Episode {} is still running, "
                "reward so far is {}".format(self.episode_count, self.episode_reward)
            )
            self._last_status = time()
