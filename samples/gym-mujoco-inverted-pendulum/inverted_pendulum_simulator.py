import os
import sys
import time
import requests
import json
import argparse
from typing import Dict, Any
import logging

from microsoft_bonsai_api.simulator.client import BonsaiClient, BonsaiClientConfig
from microsoft_bonsai_api.simulator.generated.models import SimulatorInterface, SimulatorState, SimulatorSessionResponse
from bonsai_gym import GymSimulator3

log = logging.getLogger("gym_simulator")
log.setLevel(logging.INFO)

# Runner global variables 
# "http://localhost:5000/v1/prediction"
URL = "http://localhost"
PREDICTION_PATH = "/v1/prediction"
HEADERS = {
  "Content-Type": "application/json"
}


class MujocoPendulum(GymSimulator3):

    # Environment name, from openai-gym
    environment_name = "InvertedDoublePendulum-v4"

    # simulator name from Inkling
    simulator_name = "Mujoco_InvertedDoublePendulum_Simulator"

    
    def gym_to_state(self, next_state):
                
        state = {
            "pos": float(next_state[0]),
            "sin_hinge1": float(next_state[1]),
            "sin_hinge2": float(next_state[2]),
            "cos_hinge1": float(next_state[3]),
            "cos_hinge2": float(next_state[4]),
            "velocity": float(next_state[5]),
            "ang_velocity1": float(next_state[6]),
            "ang_velocity2": float(next_state[7]),
            "constraint1": float(next_state[8]),
            "constraint2": float(next_state[9]),
            "constraint3": float(next_state[10])
        }

        return state


    def action_to_gym(self, brain_action):

        gym_action = [brain_action['input_force']]
        log.debug("gym_action is %s ", gym_action )

        return gym_action        



def train(args):

    config_client = BonsaiClientConfig(args)
    render = False if args.headless else True

    sim_model = MujocoPendulum(config_client, iteration_limit = 0, skip_frame = 1, render = render)
    sim_model.run_gym()


def run(args):

    url = URL + ':' + str(args.port) if args.port else URL + ':5000'
    # Build the endpoint reference
    endpoint = url + PREDICTION_PATH  

    log.info("Endpoint used to connect to the brain is %s ", endpoint )    

    config_client = BonsaiClientConfig(args)
    render = True    

    sim_model = MujocoPendulum(config_client, iteration_limit = 0, skip_frame = 1, render = render)
    bonsai_state = sim_model.episode_start({})  

    try:
        while True:

            # Send states to brain for getting actions
            try:
                response = requests.post(
                            endpoint,
                            data = json.dumps(bonsai_state),
                            headers = HEADERS
                        )
                
            except BaseException as err:
                log.debug(f"HTTP Post error ({err})")
                break

            # Extract the JSON response
            prediction = response.json()

            #Send actions to sim for next step
            bonsai_state = sim_model.episode_step(prediction)

            log.debug("Bonsai_state is %s ", bonsai_state )

            #Stop the run if mujoco is returning terminal is True
            if bonsai_state["_gym_terminal"] ==1.0:
                sim_model.episode_finish("End episode one") 
                break


    except BaseException as err:
        log.critical(f"Runner stopped because {type(err).__name__}: {err}")        

    
def parse_kw_args(args):
    """
    Parse keyword args into a dictionary
    """
    retval = {}
    preceded_by_key = False
    for arg in args:
        if arg.startswith('--'):
            if '=' in arg:
                key = arg.split('=')[0][2:]
                value = arg.split('=')[1]
                retval[key] = value
            else:
                key = arg[2:]
                preceded_by_key = True
        elif preceded_by_key:
            retval[key] = arg
            preceded_by_key = False

    return retval    


def main(argv):

    parser = argparse.ArgumentParser(exit_on_error=False)
             
    parser.add_argument(
        '--debug', help='debug.', action='store_true')       
    parser.add_argument(
        '--run', help='run with docker.', action='store_true')     
    parser.add_argument(
        '--port', help='run on port.', type=int)             
    parser.add_argument(
        '--headless', help='Render', action='store_true')    

    args = parser.parse_args()  

    if args.debug: 
        log.setLevel(logging.DEBUG)

    if args.run:
        runner = run(args)
    else:
        trainer = train(args)

if __name__ == '__main__':

    #Init logging
    main(sys.argv)    