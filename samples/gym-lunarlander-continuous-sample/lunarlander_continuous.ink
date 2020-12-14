inkling "2.0"
using Number

type SimState{
    x_position: number,
    y_position: number,
    x_velocity: number,
    y_velocity: number,
    angle: number,
    rotation: number,
    left_leg: number,
    right_leg: number,
    _gym_reward: number,
    _gym_terminal: Number.Bool
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

function Reward(State: SimState) {

    return State._gym_reward
}

function Terminal(State: SimState) {

    return State._gym_terminal
}


const ThrottleMin = -1.0
const ThrottleMax = 1.0
type LanderAction {
    engine1: number<ThrottleMin .. ThrottleMax>,
    engine2: number<ThrottleMin .. ThrottleMax>
}

type LunarLanderConfig {
    episode_length: -1,
    deque_size: 1
}

simulator LunarLanderSimulator(action: LanderAction, config: LunarLanderConfig): SimState {
}

graph (input: GameState): LanderAction {
    concept Land(input): LanderAction {
        curriculum {
            source LunarLanderSimulator
            reward Reward
            terminal Terminal
        }
    }
    output Land
}
