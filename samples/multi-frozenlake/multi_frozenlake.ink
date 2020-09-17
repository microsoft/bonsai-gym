inkling "2.0"

using Number

experiment {
    backend_type: "pdp-core",
    random_seed: "20",
    set_properties_num: "20",
    steps_per_set_properties: "1000",
    max_step_per_concept: "20000",
    num_workers: "3",
    env_runners_per_sampler: "3"
}

type GameState {
    current_pos: Number.Int8<0 .. 15>
}

type Action {
    command: Number.Int8<Left = 0, Down = 1, Right = 2, Up = 3>
}

type FrozenLakeConfig {
    deque_size: 1
}

simulator frozenlake_simulator(action: Action, config: FrozenLakeConfig): GameState {
}

graph (input: GameState): Action {
    concept subconcept_A(input): Action {
        experiment {
            concept_termination_condition: "2"
        }
        curriculum {
            source frozenlake_simulator
        }
    }

    concept subconcept_B(input): Action {
        curriculum {
            source frozenlake_simulator
        }
    }

    concept final_concept(input, subconcept_A, subconcept_B): Action {
        experiment {
            set_properties_num: "10",
            steps_per_set_properties: "100"
        }
        curriculum {
            source frozenlake_simulator
        }
    }
    output final_concept
}
