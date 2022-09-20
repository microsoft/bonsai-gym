
# OpenAI Gym - Mujoco (https://mujoco.org/) - Double inverted Pendulum


The agent controls the force applied on the cart (Box[-1,1]) and receives the states of the environment. 
'''
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
'''

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
python3 frozenlake_simulator.py
```



## Questions about Inkling?

See our [Inkling Guide](https://docs.microsoft.com/en-us/bonsai/inkling/) for help.
