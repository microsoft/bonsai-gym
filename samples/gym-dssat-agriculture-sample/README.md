# OpenAI Gym DSSAT Agriculture Sample

Fertilization and irrigation are two of the most important factors in agriculture. This sample demonstrates how to use Bonsai to train a model to optimize these factors for a crop.

This sample uses the [Decision Support System for Agrotechnology Transfer (DSSAT)](https://dssat.net/) with the [OpenAI Gym](https://gym.openai.com/) interface provided by [gym_dssat_pdi_project](https://gitlab.inria.fr/rgautron/gym_dssat_pdi).

For more information about DSSAT and the reinforcement learning scenarios provided by gym_dssat_pdi_project, see [gym-DSSAT: a crop model turned into a Reinforcement Learning environment](https://arxiv.org/abs/2207.03270).

## Creating the Bonsai simulator

We must use the gym_dssat_pdi_project to create a base container image with the tag `gym-dssat:debian-bullseye`:
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
?? i don't have this folder, but can generate it by cloning the bonsai-gym repo (that should be a step)
?? then opening with vscode and switching to your branch, then it is generated (shown?)
?? I know there is a command line way to do this as well with git, but need to look that up.
1. Open this folder (`bonsai-gym\samples\gym-dssat-agriculture-sample`)
1. Build with: `docker build -t gym-dssat-bonsai:latest .`
1. Set your SIM_ACCESS_KEY and SIM_WORKSPACE system environment variables according to your Bonsai workspace.
1. Test with: `docker run -it --rm -e SIM_ACCESS_KEY -e SIM_WORKSPACE gym-dssat-bonsai:latest`. Test that the resulting unmanaged simulator can be used with a Bonsai brain.

Finally, we will push the container image to our Azure Container Registry and create a managed simulator:
1. Tag with: `docker tag gym-dssat-bonsai:latest $env:SIM_ACR_PATH/gym-dssat-bonsai:latest`. (This assumes Powershell and that you have set the SIM_ACR_PATH environment variable to your ACR name.)
1. Log in with: `az acr login -n $env:SIM_ACR_PATH`.
1. Push with: `docker push $env:SIM_ACR_PATH/gym-dssat-bonsai:latest`.
1. Create Bonsai sim with: `bonsai simulator package container create --name dssat --image-uri $env:SIM_ACR_PATH/gym-dssat-bonsai:latest --cores-per-instance 1 --memory-in-gb-per-instance 1 --os-type Linux --max-instance-count 25`.
