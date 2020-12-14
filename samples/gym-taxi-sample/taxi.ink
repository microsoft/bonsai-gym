inkling "2.0"

using Number

function Reward(gs: GameState) {
    return gs._gym_reward
}

function Terminal(gs: GameState) {
    return gs._gym_terminal
}

type GameState {
    location: Number.Int16<0 .. 499>,
    _gym_reward: number,
    _gym_terminal: number
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
            reward Reward
            terminal Terminal
            source taxi_simulator
        }
    }
    output taxi_service
}
