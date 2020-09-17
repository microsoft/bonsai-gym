inkling "2.0"

using Number

type GameState {
    current_sum: number<0 .. 31 step 1>,
    dealer_card: number<0 .. 10 step 1>,
    usable_ace: number<0, 1>
}

type Action {
    command: Number.Int8<Stay = 0, Hit = 1>
}

type BlackJackConfig {
    episode_length: -1,
    deque_size: 1
}

simulator blackjack_simulator(action: Action, config: BlackJackConfig): GameState {
}

graph (input: GameState): Action {
    concept high_score(input): Action {
        curriculum {
            source blackjack_simulator
        }
    }
    output high_score
}
