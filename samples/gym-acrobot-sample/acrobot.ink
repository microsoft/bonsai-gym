inkling "2.0"

using Number

function Reward(gs: GameState) {
    return gs._gym_reward
}

function Terminal(gs: GameState) {
    return gs._gym_terminal
}

type GameState {
    cos_theta0: number,
    sin_theta0: number,
    cos_theta1: number,
    sin_theta1: number,
    theta0_dot: number,
    theta1_dot: number,
    _gym_reward: number,
    _gym_terminal: number
}

type Action {
    command: Number.Int8<Left = 0, Center = 1, Right = 2>
}

type AcrobotConfig {
    deque_size: 1
}

simulator AcrobotSimulator(action: Action, config: AcrobotConfig): GameState {
}

graph (input: GameState): Action {
    concept Height(input): Action {
        curriculum {
            reward Reward
            terminal Terminal
            source AcrobotSimulator
        }
    }
    output Height
}
