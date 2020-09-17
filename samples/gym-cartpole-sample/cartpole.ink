inkling "2.0"

using Number
experiment {
    num_workers: "3",
    env_runners_per_sampler: "2"
}

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
        experiment {
            random_seed: "42"
        }
        curriculum {
            source CartpoleSimulator
        }
    }
    output Balance
}
