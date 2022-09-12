inkling "2.0"

using Number
using Math
using Goal

type ObservableState {
    dap: number
}

type SimState extends ObservableState {
    _gym_reward: number,
    _gym_terminal: number
}

type Action {
    anfer: number<0 .. 10>,
    amir: number<0 .. 10>,
}

type Config {
    noop: number,
}

function Reward(ss: SimState) {
    return ss._gym_reward
}

function Terminal(ss: SimState) {
    return ss._gym_terminal
}

simulator Simulator(action: Action, config: Config): SimState {
}

graph (input: ObservableState): Action {

    concept Fertilize(input): Action {
        curriculum {
            source Simulator
            reward Reward
            terminal Terminal

            lesson balancing {
                scenario {
                    noop: 0
                }
            }
        }
    }
    output Fertilize
}
