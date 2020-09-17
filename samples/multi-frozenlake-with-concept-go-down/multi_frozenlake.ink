inkling "2.0"

using Number

type GameState {
    current_pos: Number.Int8<0 .. 15>
}

experiment {
    backend_type: "pdp-core",
    random_seed: "20",
    num_workers: "3",
    env_runners_per_sampler: "3"
}

type Action {
    command: Number.Int8<Left = 0, Down = 1, Right = 2, Up = 3>
}

type FrozenLakeConfig {
    deque_size: 1,
    concept_index: number<0, 1>
}

simulator frozenlake_simulator(action: Action, config: FrozenLakeConfig): GameState {
}

graph (input: GameState): Action {
    concept go_down(input): Action {
        experiment {
            set_properties_num: "5",
            steps_per_set_properties: "1000",
            max_step_per_concept: "5000"
        }
        curriculum {
            source frozenlake_simulator
            lesson train_go_down {
                scenario {
                    concept_index: 0
                }
            }
        }
    }

    concept reach_goal(input, go_down): Action {
        experiment {
            max_step_per_concept: "5000"
        }
        curriculum {
            source frozenlake_simulator
            lesson train_reach_goal {
                scenario {
                    concept_index: 1
                }
            }
        }
    }

    output reach_goal
}
