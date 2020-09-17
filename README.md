# Bonsai Gym Common

A python library for integrating Bonsai BRAIN with Open AI Gym environments.

## Bonsai Gym Common

A python library for integrating Bonsai BRAIN with Open AI Gym environments.

## Installation

Install the latest from github.

**NOTE** - The bonsai-gym located on pypi is an older release that we no longer support. We have no plans to publish this to ypi

`$ pip install git+https://github.com/microsoft/bonsai-gym`

## Usage

Once installed, import `bonsai_gym` in order to access
base class `GymSimulator3`, which implements all of the
environment-independent Bonsai SDK integrations necessary to
train a Bonsai BRAIN to play an OpenAI Gym simulator.

```python
    import gym

    from bonsai_gym import GymSimulator

    class CartPoleSimulator(GymSimulator):
        # Perform cartpole-specific integrations here.
```

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
