inkling "2.0"

using Number

type GameState {
    position: number,
    velocity: number,
    angle: number,
    rotation: number
}

type Action {
    command: Number.Int8<17, 41>
}

type CartPoleConfig {
    episode_length: -1,
    deque_size: 1
}

simulator cartpole_simulator(action: Action, config: CartPoleConfig): GameState {
}

graph (input: GameState): Action {
    concept balance(input): Action {
        curriculum {
            source cartpole_simulator
        }
    }
    output balance
}
