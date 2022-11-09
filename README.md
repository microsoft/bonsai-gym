# Bonsai Gym

A python library for integrating Bonsai brains with Open AI Gym environments.

## Bonsai Gym

A python library for integrating Bonsai BRAIN with Open AI Gym environments.

## Installation

```bash
$ pip install git+https://github.com/microsoft/bonsai-gym
```

**NOTE** - The bonsai-gym located on pypi is an older release that we no longer support. We have no plans to publish this to pypi


## Usage

Once installed, import `bonsai_gym` in order to access
the class `GymSimulator3`, which implements all of the
environment-independent Bonsai SDK integrations necessary to
train a Bonsai BRAIN to play an OpenAI Gym simulator.

See [CartPole sample](samples/gym-cartpole-sample/cartpole_simulator.py)

```python
import logging
from bonsai_gym import GymSimulator3

log = logging.getLogger("gym_simulator")
log.setLevel(logging.DEBUG)


class CartPole(GymSimulator3):
    # Environment name, from openai-gym
    environment_name = "CartPole-v0"

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
```

## Running Simulator

Simulators need two environment variables set to be able to attach to the platform.

The first is `SIM_ACCESS_KEY`. You can create one from the `Account Settings` page.
You have one chance to copy the key once it has been created. Make sure you don't enter
the ID.

The second is `SIM_WORKSPACE`. You can find this in the URL after `/workspaces/` once
you are logged in to the platform.

There is also an optional `SIM_API_HOST` key, but if it is not set it will default to `https://api.bons.ai`.

If you're launching your simulator from the command line, make sure that you have these two
environment variables set. If you like, you could use the following example script:

```sh
export SIM_WORKSPACE=<your-workspace-id>
export SIM_ACCESS_KEY=<your-access-key>
python3 my_sim.py
```

## Rewards and Terminals

The `GymSimulator3` class automatically appends the gym reward and gym terminal to the state extracted from the environment with the keys named `_gym_reward` and `_gym_terminal` respectively. You can use these [rewards and terminals](https://docs.microsoft.com/en-us/bonsai/inkling/advanced/reward-terminal-functions) in your Inkling definition using Inkling functions. See the example Inklings in the `samples` directory to see a standard implementation.

# Contributing

This project welcomes contributions and suggestions. Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
