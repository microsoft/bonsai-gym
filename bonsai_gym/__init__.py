"""
The bonsai-gym-common package contains the classes necessary for using OpenAI
gym as a simulator for Bonsai BRAIN.
"""

# pyright: reportUnusedImport=false

from .gym_simulator import GymSimulator
try:
    from .gym_simulator3 import GymSimulator3
except ImportError:
    # TODO: remove once we have a way to publish SDK3
    pass
from .luminance_gym_simulator import LuminanceGymSimulator
from .version import __version__
