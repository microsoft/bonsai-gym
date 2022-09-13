# OpenAI Gym DSSAT Agriculture Sample

Fertilization and irrigation are two of the most important factors in agriculture. This sample demonstrates how to use Bonsai to train a model to optimize these factors for a crop.

This sample uses the [Decision Support System for Agrotechnology Transfer (DSSAT)](https://dssat.net/) with the [OpenAI Gym](https://github.com/openai/gym) interface provided by [gym_dssat_pdi_project](https://gitlab.inria.fr/rgautron/gym_dssat_pdi).

For more information about DSSAT and the reinforcement learning scenarios provided by gym_dssat_pdi_project, see [gym-DSSAT: a crop model turned into a Reinforcement Learning environment](https://arxiv.org/abs/2207.03270).

## Creating the Bonsai simulator

Before starting, you will need the following:
1. An Azure subscription and Bonsai workspace. See [Account setup](https://docs.microsoft.com/bonsai/guides/account-setup) for more information.
1. You must set up the Bonsai CLI. See [Get started with the Bonsai CLI](https://docs.microsoft.com/bonsai/cli) for more information. You will also need to run the [bonsai configure](https://docs.microsoft.com/bonsai/cli/configure) command to use the CLI with your Bonsai workspace.
1. You must have Docker installed on your local machine. The community edition of Docker is available for [Windows](https://docs.docker.com/docker-for-windows/install), [Linux](https://docs.docker.com/engine/install), and [MacOS](https://docs.docker.com/docker-for-mac/install).

We will use the gym_dssat_pdi_project to create a base container image with the tag `gym-dssat:debian-bullseye`:
1. Clone https://gitlab.inria.fr/rgautron/gym_dssat_pdi.git
1. Open folder `gym_dssat_pdi\docker_recipes`
1. Modify Dockerfile_Debian_Bullseye, changing `https://gac.udc.es/~emilioj/bullseye.tgz` to `http://burgas.des.udc.es/gym-dssat/tarballs/bullseye.tgz` (apparently this file has been moved)
1. Build with: `docker build -t "gym-dssat:debian-bullseye" -f Dockerfile_Debian_Bullseye .`
1. Test with: `docker run -it --rm gym-dssat:debian-bullseye`

If this is working, you should see a series of fertilizing outputs with final output that looks like this:

```sh
mean of yields: 8444.814610883532 kg/ha
variance of yields: 280080.59325247107 kg/ha
16/16 multiprocess_trial
16/16 multiprocess_trial_hard_reset
```

Next, we need to create a container image for the Bonsai simulator:
1. Clone this repository and check out the gym-dssat-agriculture-sample branch. You can do so with the command `git clone -b gym-dssat-agriculture-sample https://github.com/microsoft/bonsai-gym.git`
1. Open this folder (`bonsai-gym\samples\gym-dssat-agriculture-sample`)
1. Build with: `docker build -t gym-dssat-bonsai:latest .`
1. Set your SIM_ACCESS_KEY, SIM_WORKSPACE, and SIM_ACR_PATH system environment variables according to your [Bonsai workspace info](https://docs.microsoft.com/bonsai/cookbook/get-workspace-info#option-1-use-the-bonsai-ui)
1. Test with: `docker run -it --rm -e SIM_ACCESS_KEY -e SIM_WORKSPACE gym-dssat-bonsai:latest`
1. Test that the resulting unmanaged simulator registers with Bonsai and can be used with a Bonsai brain
    * Create a new empty brain in your Bonsai workspace
    * Paste in the Inkling source code from [dssat.ink](dssat.ink)
    * Click the train button and select the unmanaged simulator DSSATSimulator
    * Let it run for a little bit and verify that you see episode activity in the Bonsai workspace and in the unmanaged simulator console output

Finally, we will push the container image to our Azure Container Registry and create a managed simulator:
1. Tag with: `docker tag gym-dssat-bonsai:latest $env:SIM_ACR_PATH/gym-dssat-bonsai:latest`
    * This assumes that you are using a Powershell console. If that is not the case, you can replace `$env:SIM_ACR_PATH` in this step and the following steps with the ACR path from your workspace info.
1. Log in to your Azure container reistry with: `az acr login -n $env:SIM_ACR_PATH`
1. Push with: `docker push $env:SIM_ACR_PATH/gym-dssat-bonsai:latest`
1. Create Bonsai sim with: `bonsai simulator package container create --name dssat --image-uri $env:SIM_ACR_PATH/gym-dssat-bonsai:latest --cores-per-instance 1 --memory-in-gb-per-instance 1 --os-type Linux --max-instance-count 25`
1. Add a package statement to the Inkling brain that you previously created for testing the unmanaged simulator. It should look like this:
    ```inkling
    simulator Simulator(action: Action, config: Config): SimState {
        package "dssat" # <-- Add this line
    }
    ```
1. Click the Train button. After a couple minutes, you should see multiple simulators registered and in use and episodes running in the Simulator (Live) pane of the Bonsai workspace. If you leave it running for a couple hours, the training graph should show hundreds of thousands of iterations completed and rising values for episode reward