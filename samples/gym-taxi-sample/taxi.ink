inkling "2.0"

using Number

type GameState {
    location: Number.Int16<0 .. 499>
}

type Action {
    command: Number.Int8<0 .. 5>
}

type TaxiConfig {
    deque_size: 1
}

simulator taxi_simulator(action: Action, config: TaxiConfig): GameState {
}

graph (input: GameState): Action {
    concept taxi_service(input): Action {
        curriculum {
            source taxi_simulator
        }
    }
    output taxi_service
}
