###

# MSFT Bonsai 
# Copyright 2021 Microsoft
# This code is licensed under MIT license (see LICENSE for details)

# Bipedal Walker sample demonstrating usage of the Machine Teaching strategy
# of curriculum learning using manual lessons to gradually introduce harder
# episodes to promote better learning.

# easy lesson - learn to gait without obstacles
# hard lesson - learn to gait with obstacles varying height and spacing

###

inkling "2.0"
using Number

# Range of actions easily defined as constants
const ThrottleMin = -1.0
const ThrottleMax = 1.0

# Simulator State from OpenAI gym framework
type GameState {
    hull_ang: number,
    hull_ang_vel: number,
    x_velocity: number,
    y_velocity: number,
    leg_1_hip_angle: number,
    leg_1_hip_speed: number,
    leg_1_knee_angle: number,
    leg_1_knee_speed: number,
    leg_1_contact: number,
    leg_2_hip_angle: number,
    leg_2_hip_speed: number,
    leg_2_knee_angle: number,
    leg_2_knee_speed: number,
    leg_2_contact: number,
    lidar0: number,
    lidar1: number,
    lidar2: number,
    lidar3: number,
    lidar4: number,
    lidar5: number,
    lidar6: number,
    lidar7: number,
    lidar8: number,
    lidar9: number,
    _gym_reward: number,
    _gym_terminal: number
}

# Observable state as input to brain to make next decision
type ObservableState {
    hull_ang: number,
    hull_ang_vel: number,
    x_velocity: number,
    y_velocity: number,
    leg_1_hip_angle: number,
    leg_1_hip_speed: number,
    leg_1_knee_angle: number,
    leg_1_knee_speed: number,
    leg_1_contact: number,
    leg_2_hip_angle: number,
    leg_2_hip_speed: number,
    leg_2_knee_angle: number,
    leg_2_knee_speed: number,
    leg_2_contact: number,
    lidar0: number,
    lidar1: number,
    lidar2: number,
    lidar3: number,
    lidar4: number,
    lidar5: number,
    lidar6: number,
    lidar7: number,
    lidar8: number,
    lidar9: number,
}

# Array actions for leg 1 and leg 2
# 0th element - hip joint
# 1st element - knee joint
type WalkerAction {
    leg_1_torque: number<ThrottleMin .. ThrottleMax>[2],
    leg_2_torque: number<ThrottleMin .. ThrottleMax>[2],
}

# Stump Track - stump_height, obstacle_spacing
# Hexagon Track - poly_shape array of 12
type BipedalWalkerConfig {
    stump_height: number<0.0 .. 3.0>,
    obstacle_spacing: number<0.0 .. 6.0>,
    poly_shape: number<0 .. 4>[12],
}

# Reward function from OpenAI gym
function Reward(gs: GameState) {
    return gs._gym_reward
}

# Terminal function from OpenAI gym
# Terminate if hull falls on ground or hits obstacles
function Terminal(gs: GameState) {
    return gs._gym_terminal
}

simulator BipedalWalkerSimulator(action: WalkerAction, config: BipedalWalkerConfig): GameState {
    #package "BipedalWalkerSim"
}

graph (input: ObservableState): WalkerAction {
    concept Run(input): WalkerAction {
        curriculum {
            reward Reward
            terminal Terminal
            source BipedalWalkerSimulator

            # Specify NN architecture using algorithm hints
            # https://docs.microsoft.com/en-us/bonsai/inkling/advanced/algorithm
            algorithm {
                Algorithm: "SAC",
                QHiddenLayers: [
                {
                    Size: 400,
                    Activation: "relu"
                },
                {
                    Size: 300,
                    Activation: "relu"
                }
                ],
                PolicyHiddenLayers: [
                {
                    Size: 400,
                    Activation: "relu"
                },
                {
                    Size: 300,
                    Activation: "tanh"
                }
                ]
            }
            
            # Increase NPIL to match literature paper *crucial*
            training {
                NoProgressIterationLimit: 20000000,
                EpisodeIterationLimit: 2000,
            }
            
            # First learn the task of walking
            lesson easy_course {
                scenario {
                    stump_height: 0,
                    obstacle_spacing: 0,
                }
                training {
                    # Specify minimum reward threshold for success
                    LessonRewardThreshold: 230,
                }
            }
            
            # If successful within NPIL iterations, transition to episodes
            # with obstacles varying stump height and spacing
            lesson hard_course {
                scenario {
                    stump_height: number<0 .. 3>,
                    obstacle_spacing: number<0 .. 6>,
                }
                training {
                    LessonRewardThreshold: 230,
                }
            }
        }
    }
    output Run
}