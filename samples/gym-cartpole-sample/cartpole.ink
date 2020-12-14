inkling "2.0"

using Number

type SimState {
    position: Number.Float32,
    velocity: Number.Float32,
    angle: Number.Float32,
    rotation: Number.Float32,
    _gym_reward: number,
    _gym_terminal: number
}

type GameState {
    position: Number.Float32,
    velocity: Number.Float32,
    angle: Number.Float32,
    rotation: Number.Float32,
}

type Action {
    command: Number.Int8<Left=0, Right=1>
}

type CartPoleConfig {
    episode_length: Number.Int8,
    deque_size: Number.UInt8
}

function Reward(ss: SimState) {
    return ss._gym_reward
}

function Terminal(ss: SimState) {
    return ss._gym_terminal
}

simulator CartpoleSimulator(action: Action, config: CartPoleConfig): SimState {
}

graph (input: GameState): Action {

    concept balance(input): Action {
        curriculum {
            reward Reward
            terminal Terminal
            source CartpoleSimulator
            lesson balancing {
                scenario {
                    episode_length: -1,
                    deque_size: 1
                }
            }
        }
    }
    output balance
}
