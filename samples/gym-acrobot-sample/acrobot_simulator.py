import argparse
import logging

from bonsai_gym import GymSimulator3

log = logging.getLogger("gym_simulator")
log.setLevel(logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument("--headless", action="store_true", default=False)


class Acrobot(GymSimulator3):
    # Environment name, from openai-gym
    environment_name = "Acrobot-v1"

    # simulator name from Inkling
    simulator_name = "AcrobotSimulator"

    # convert openai gym observation to our state type
    def gym_to_state(self, observation):
        state = {
            "cos_theta0": observation[0],
            "sin_theta0": observation[1],
            "cos_theta1": observation[2],
            "sin_theta1": observation[3],
            "theta0_dot": observation[4],
            "theta1_dot": observation[5],
        }
        return state

    # convert our action type into openai gym action
    def action_to_gym(self, action):
        return action["command"]


if __name__ == "__main__":
    # create a brain, openai-gym environment, and simulator
    args, _ = parser.parse_known_args()
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
    sim = Acrobot(iteration_limit=500, headless=headless)
    sim.run_gym()
