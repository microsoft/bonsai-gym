inkling "2.0"
using Number

type SimState{
    view: number[512],
    _gym_reward: number,
    _gym_terminal: Number.Bool
}

type GameState {
    view: number[512],
}

function Reward(State: SimState) {

    return State._gym_reward
}

function Terminal(State: SimState) {

    return State._gym_terminal
}


const ThrottleMin = -1.0
const ThrottleMax = 1.0

type RacerAction {
    steer: number<ThrottleMin .. ThrottleMax>,
    gas: number<ThrottleMin .. ThrottleMax>,
    apply_break: number<ThrottleMin .. ThrottleMax>
}

simulator CarRacingSimulator(action: RacerAction): SimState {
}

graph (input: GameState): RacerAction {
    concept Drive(input): RacerAction {
        curriculum {
            source CarRacingSimulator
            reward Reward
            terminal Terminal
        }
    }
    output Drive
}
