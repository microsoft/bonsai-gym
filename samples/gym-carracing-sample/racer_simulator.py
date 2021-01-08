import sys
import logging
from microsoft_bonsai_api.simulator.client import BonsaiClientConfig
import gym
from bonsai_gym import GymSimulator3
from typing import List
import torch
import torchvision.models as models
import numpy as np

log = logging.getLogger("gym_simulator")
log.setLevel(logging.DEBUG)

SKIP_FRAME = 2


class CarRacer(GymSimulator3):
    environment_name = "CarRacing-v0"
    simulator_name = "CarRacingSimulator"

    def gym_to_state(self, obs):
        state = {"view": torch_featurizer(obs)}
        return state

    def action_to_gym(self, actions):
        steer = np.clip(actions["steer"], -1.0, 1.0)
        gas = np.clip(actions["gas"], -1.0, 1.0)
        apply_break = np.clip(actions["apply_break"], -1.0, 1.0)
        return np.asarray([steer, gas, apply_break])


def torch_featurizer(x: np.ndarray) -> List[float]:

    model_ft = models.resnet18(pretrained=True)
    # convert to torch tensor, shape: [h, w, c]
    x_tensor = torch.Tensor(x.copy())
    # get the features from the penultimate layer of the pretrained model
    feature_extractor = torch.nn.Sequential(*list(model_ft.children())[:-1])
    # need to convert to shape [b, c, h, w]
    # first convert from [h, w, c] -> [b, h, w, c] -> [b, c, h, w]
    output_features = feature_extractor(x_tensor.unsqueeze(0).permute(0, 3, 1, 2))

    return torch.flatten(output_features).tolist()


if __name__ == "__main__":
    # create a brain, openai-gym environment, and simulator
    config = BonsaiClientConfig(argv=sys.argv)
    sim = CarRacer(config, skip_frame=SKIP_FRAME)
    sim.run_gym()
