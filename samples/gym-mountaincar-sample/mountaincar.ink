inkling "2.0"

using Number

function Reward(gs: GameState) {
    return gs._gym_reward
}

function Terminal(gs: GameState) {
    return gs._gym_terminal
}

type GameState {
    x_position: number,
    x_velocity: number,
    _gym_reward: number,
    _gym_terminal: number
}

type Action {
    command: Number.Int8<Left = 0, Stop = 1, Right = 2>
}

type MountainCarConfig {
    episode_length: -1,
    deque_size: 1
}

simulator MountainCarSimulator(action: Action, config: MountainCarConfig): GameState {
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
