inkling "2.0"

using Number


type SimState {
    x_position: number,
    x_velocity: number,
    _gym_reward: number,
    _gym_terminal: number
}

type GameState {
    x_position: number,
    x_velocity: number,
}

type Action {
    command: Number.Int8<Left = 0, Stop = 1, Right = 2>
}

type MountainCarConfig {
    episode_length: -1,
    deque_size: 1
}


function Reward(ss: SimState) {
    return ss._gym_reward
}

function Terminal(ss: SimState) {
    return ss._gym_terminal
}

simulator MountainCarSimulator(action: Action, config: MountainCarConfig): SimState {
}

graph (input: GameState): Action {
    concept HighScore(input): Action {
        curriculum {
            reward Reward
            terminal Terminal
            source MountainCarSimulator
        }
    }
    output HighScore
}
