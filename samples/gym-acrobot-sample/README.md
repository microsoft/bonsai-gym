# OpenAI Gym Acrobot Sample
The acrobot system includes two joints and two links, where the joint between the two links is actuated. Initially, the links are hanging downwards, and the goal is to swing the end of the lower link up to a given height.

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
python3 acrobot_simulator.py
```

## Questions about Inkling?

See our [Inkling Guide](https://docs.microsoft.com/en-us/bonsai/inkling/) for help.