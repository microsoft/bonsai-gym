inkling "2.0"

experiment {
    num_workers: "3",
    env_runners_per_sampler: "2",
    max_step_per_concept: "1000000"
}

type GameState {
    x_position: number,
    x_velocity: number
}

const throttleMin = -1.0
const throttleMax = 1.0
type Action {
    command: number<throttleMin .. throttleMax>
}

type MountainCarConfig {
    deque_size: 1
}

simulator mountaincar_continuous_simulator(action: Action, config: MountainCarConfig): GameState {
}

graph (input: GameState): Action {
    concept high_score(input): Action {
        experiment {
            random_seed: "42"
        }
        curriculum {
            algorithm {
                Algorithm: "TRPO"
            }
            source mountaincar_continuous_simulator
        }
    }
    output high_score
}
