inkling "2.0"

using Number

type GameState {
    position: Number.Float32,
    velocity: Number.Float32,
    angle: Number.Float32,
    rotation: Number.Float32
}

type Action {
    command: Number.Int8<Left = 0, Right = 1>
}

type CartPoleConfig {
    episode_length: -1,
    deque_size: 1
}

simulator CartpoleSimulator(action: Action, config: CartPoleConfig): GameState {
}

graph (input: GameState): Action {
    concept Balance(input): Action {
        curriculum {
            source CartpoleSimulator
        }
    }
    output Balance
}
