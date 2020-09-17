inkling "2.0"

using Number

type GameState {
    character: Number.Int8<0 .. 5>
}

type Action {
    move: Number.Int8<0, 1>,
    write: Number.Int8<0, 1>,
    char: Number.Int8<0 .. 4>
}

type CopyConfig {
    episode_length: -1,
    deque_size: 1
}

simulator tapecopy_simulator(action: Action, config: CopyConfig): GameState {
}

graph (input: GameState): Action {
    concept copy_string(input): Action {
        curriculum {
            source tapecopy_simulator
        }
    }
    output copy_string
}
