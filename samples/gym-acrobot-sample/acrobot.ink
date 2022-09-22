inkling "2.0"

using Number


type SimState {
    cos_theta0: number,
    sin_theta0: number,
    cos_theta1: number,
    sin_theta1: number,
    theta0_dot: number,
    theta1_dot: number,
    _gym_reward: number,
    _gym_terminal: number
}

type GameState {
    cos_theta0: number,
    sin_theta0: number,
    cos_theta1: number,
    sin_theta1: number,
    theta0_dot: number,
    theta1_dot: number
}

type Action {
    command: Number.Int8<Left = 0, Center = 1, Right = 2>
}

type AcrobotConfig {
    deque_size: 1
}

function Reward(ss: SimState) {
    return ss._gym_reward
}

function Terminal(ss: SimState) {
    return ss._gym_terminal
}

simulator AcrobotSimulator(action: Action, config: AcrobotConfig): SimState {
}

graph (input: GameState): Action {
    concept Height(input): Action {
        curriculum {
            reward Reward
            terminal Terminal
            source AcrobotSimulator
            lesson first_lesson {
                scenario {
                    deque_size: 1
                }
            }            
        }
    }
    output Height
}
