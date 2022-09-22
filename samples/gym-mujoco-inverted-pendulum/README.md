
# OpenAI Gym - Mujoco (https://mujoco.org/) - Double inverted Pendulum

<img width="1428" alt="Mujoco" src="https://user-images.githubusercontent.com/14914357/191338828-d8ad6072-a7f4-4172-bffb-e750f96b197b.png">


The agent controls the force applied on the cart (Box[-1,1]) and receives the states of the environment. 
```sh
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
```

The simulator needs two environment variables set to be able to attach to the platform.

The first is `SIM_ACCESS_KEY`. You can create one from the `Account Settings` page.
You have one chance to copy the key once it has been created. Make sure you don't enter
the ID.

The second is `SIM_WORKSPACE`. You can find this in the URL after `/workspaces/` once
you are logged in to the platform.

If you're launching your simulator from the command line, make sure that you have these two
environment variables set. If you like, you could use the following example script:

```sh
export SIM_WORKSPACE=<your-workspace-id>
export SIM_ACCESS_KEY=<your-access-key>
python3 python inverted_pendulum_simulator.py --headless
```
Three args can be used: 

'--debug' to set the logger level to debug      
'--headless' to not render the simulator
'--run' to run the simulator using a local docker container with the trained brain
'--port' to set the port used by the docker image

## Using a trained brain in a local docker container 

For using the local trained brain add the command line argument --run. When in run mode, inverted_pendulum_simulator.py sends the HTTP request to localhost using port 5000. If you want to change this behavior, use the --port argument or edit the file to change the hostname.
      


## Questions about Inkling?

See our [Inkling Guide](https://docs.microsoft.com/en-us/bonsai/inkling/) for help.
