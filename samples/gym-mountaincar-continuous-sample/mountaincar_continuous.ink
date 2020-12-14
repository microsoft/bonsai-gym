inkling "2.0"

type SimState {
    x_position: number,
    x_velocity: number,
    _gym_reward: number,
    _gym_terminal: number
}

type GameState {
    x_position: number,
    x_velocity: number,
}

const ThrottleMin = -1.0
const ThrottleMax = 1.0
type Action {
    command: number<ThrottleMin .. ThrottleMax>
}

type MountainCarConfig {
    deque_size: -1
}

function Reward(ss: SimState) {
    return ss._gym_reward
}

function Terminal(ss: SimState) {
    return ss._gym_terminal
}

simulator MountainCarSimulator(action: Action, config: MountainCarConfig): SimState {
}

graph (input: GameState): Action {
    concept HighScore(input): Action {
        curriculum {
            reward Reward
            terminal Terminal
            source MountainCarSimulator
        }
    }
    output HighScore
}
