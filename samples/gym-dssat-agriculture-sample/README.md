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
1. Test with: `docker run gym-dssat:debian-bullseye`

If this is working, you should see a series of fertilizing outputs with final output that looks like this:

```sh
mean of yields: 8444.814610883532 kg/ha
variance of yields: 280080.59325247107 kg/ha
16/16 multiprocess_trial
16/16 multiprocess_trial_hard_reset
```

