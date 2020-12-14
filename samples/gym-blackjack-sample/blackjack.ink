inkling "2.0"

using Number

type SimState {
    current_sum: number<0 .. 31 step 1>,
    dealer_card: number<0 .. 10 step 1>,
    usable_ace: number<0, 1>,
    _gym_reward: number,
    _gym_terminal: number
}

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

function Reward(ss: SimState) {
    return ss._gym_reward
}

function Terminal(ss: SimState) {
    return ss._gym_terminal
}

simulator blackjack_simulator(action: Action, config: BlackJackConfig): SimState {
}

graph (input: GameState): Action {
    concept high_score(input): Action {
        curriculum {
            reward Reward
            terminal Terminal
            source blackjack_simulator
        }
    }
    output high_score
}
