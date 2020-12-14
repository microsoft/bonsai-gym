inkling "2.0"

using Number


type SimState {
    location: Number.Int16<0 .. 499>,
    _gym_reward: number,
    _gym_terminal: number
}

type GameState {
    location: Number.Int16<0 .. 499>,
}

type Action {
    command: Number.Int8<0 .. 5>
}

type TaxiConfig {
    deque_size: 1
}

function Reward(ss: SimState) {
    return ss._gym_reward
}

function Terminal(ss: SimState) {
    return ss._gym_terminal
}

simulator taxi_simulator(action: Action, config: TaxiConfig): SimState {
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
