inkling "2.0"

using Number

type SimState {
    x_position: number,
    y_position: number,
    x_velocity: number,
    y_velocity: number,
    angle: number,
    rotation: number,
    left_leg: number,
    right_leg: number,
    _gym_reward: number,
    _gym_terminal: number
}

type GameState {
    x_position: number,
    y_position: number,
    x_velocity: number,
    y_velocity: number,
    angle: number,
    rotation: number,
    left_leg: number,
    right_leg: number
}

function Reward(ss: SimState) {
    return ss._gym_reward
}

function Terminal(ss: SimState) {
    return ss._gym_terminal
}

type LanderAction {
    command: Number.Int8<Off = 0, LeftEngine = 1, MainEngine = 2, RightEngine = 3>
}

type LunarLanderConfig {
    episode_length: -1,
    deque_size: 1
}

simulator lunarlander_simulator(action: LanderAction, config: LunarLanderConfig): SimState {
}

graph (input: GameState): LanderAction {
    concept land(input): LanderAction {
        curriculum {
            reward Reward
            terminal Terminal
            source lunarlander_simulator
        }
    }
    output land
}
