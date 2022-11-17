import pytest

import bonsai_gym.bonsai_connector
from bonsai_gym.gym_simulator3 import GymSimulator3


class AcrobotSim(GymSimulator3):
    environment_name = "Acrobot-v1"
    simulator_name = "AcrobotSim"

    def action_to_gym(self, action):
        return action["command"]

    def gym_to_state(self, obs):
        return {
            "cos_theta0": obs[0],
            "sin_theta0": obs[1],
            "cos_theta1": obs[2],
            "sin_theta1": obs[3],
            "theta0_dot": obs[4],
            "theta1_dot": obs[5],
        }


@pytest.fixture
def gymsimulator3(mocker):
    mocker.patch.object(
        bonsai_gym.bonsai_connector.BonsaiConnector, "__init__", return_value=None
    )
    return AcrobotSim(headless=True)


def test_episode_start(gymsimulator3):
    assert not gymsimulator3.episode_start({})["halted"]


def test_get_interface(gymsimulator3):
    interface = {
        "name": "AcrobotSim",
        "timeout": 60,
    }
    assert gymsimulator3.get_interface() == interface


def test_episode_step(gymsimulator3):
    gymsimulator3.episode_start({})
    action = {"command": 0}
    assert not gymsimulator3.episode_step(action)["halted"]


def test_episode_finish(gymsimulator3):
    gymsimulator3.episode_start({})
    assert gymsimulator3.episode_finish("stopped") is None
