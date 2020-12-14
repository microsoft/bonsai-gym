inkling "2.0"
using Number

function Reward(gs: GameState) {
    return gs._gym_reward
}

function Terminal(gs: GameState) {
    return gs._gym_terminal
}

type GameState {
    position: Number.Float32,
    velocity: Number.Float32,
    angle: Number.Float32,
    rotation: Number.Float32,
    _gym_reward: number,
    _gym_terminal: number
}

type Action {
    command: Number.Int8<Left=0, Right=1>
}

type CartPoleConfig {
    episode_length: Number.Int8,
    deque_size: Number.UInt8
}

simulator cartpole_simulator(action: Action, config: CartPoleConfig): GameState {
}

graph (input: GameState): Action {

    concept balance(input): Action {
        curriculum {
            reward Reward
            terminal Terminal
            source cartpole_simulator
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
