inkling "2.0"

experiment {
    max_step_per_concept: "1000000"
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

simulator LunarLanderSimulator(action: LanderAction, config: LunarLanderConfig): GameState {
}

graph (input: GameState): LanderAction {
    concept Land(input): LanderAction {
        curriculum {
            source LunarLanderSimulator
        }
    }
    output Land
}
