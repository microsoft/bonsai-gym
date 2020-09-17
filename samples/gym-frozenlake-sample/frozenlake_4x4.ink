inkling "2.0"

using Number

experiment {
    random_seed: "20",
    num_workers: "3",
    env_runners_per_sampler: "2"
}

type GameState {
    current_pos: Number.Int8<0 .. 15>
}

type Action {
    command: Number.UInt8<Up = 0, Down = 1, Left = 2, Right = 3>
}

type FrozenLakeConfig {
    deque_size: 1
}

simulator FrozenlakeSimulator(action: Action, config: FrozenLakeConfig): GameState {
}

graph (input: GameState): Action {
    concept GoalPosition(input): Action {
        curriculum {
            source FrozenlakeSimulator
        }
    }
    output GoalPosition
}
