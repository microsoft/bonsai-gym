inkling "2.0"

using Number

type GameState {
    current_pos: Number.Int8<0 .. 15>,
}

type SimState {
    current_pos: Number.Int8<0 .. 15>,
    _gym_reward: number,
    _gym_terminal: Number.Bool
}

type Action {
    command: Number.UInt8<Up = 0, Down = 1, Left = 2, Right = 3>
}

type FrozenLakeConfig {
    deque_size: 1
}

simulator FrozenlakeSimulator(action: Action, config: FrozenLakeConfig): SimState {
}

function Reward(State: SimState) {

    return State._gym_reward
}

function Terminal(State: SimState) {

    return State._gym_terminal
}

graph (input: GameState): Action {
    concept GoalPosition(input): Action {
        curriculum {
            source FrozenlakeSimulator
            reward Reward
            terminal Terminal
        }
    }
    output GoalPosition
}
