inkling "2.0"

using Number

type GameState {
    current_pos: number<0 .. 63 step 1>
}

type Action {
    command: Number.Int8<Up = 0, Down = 1, Left = 2, Right = 3>
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
