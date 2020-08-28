from bonsai_ai import Luminance
from bonsai_gym.gym_simulator import GymSimulator


class LuminanceGymSimulator(GymSimulator):
    # Downsample rate. Subclasses can override.
    downsample = 1
    env_width = 1
    env_height = 1

    def episode_finish(self):
        print("Episode {} reward: {}".format(self.episode_count, self.episode_reward))

    def gym_to_state(self, observation):
        """
        Calculates the luminance of the values for the image and
        performs nice preprocessing.
        """

        R = observation[:, :, 0]
        G = observation[:, :, 1]
        B = observation[:, :, 2]
        # Calculates weighted apparent brightness values
        # according to https://en.wikipedia.org/wiki/Relative_luminance
        observation = 0.2126 * R + 0.7152 * G + 0.0722 * B

        # Normalize the observations.
        observation /= 255.0

        # should be replaced with tranformed
        observation = observation[:: self.downsample, :: self.downsample]

        observation = observation.ravel().tolist()

        return {
            "observation": Luminance(
                int(self.env_width / self.downsample),
                int(self.env_height / self.downsample),
                observation,
            )
        }
