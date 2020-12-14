# Inkling code for driving a car up a mountain.
# Simulator source code:
# https://github.com/BonsaiAI/bonsai-sdk/blob/master/samples/openai-gym/gym-mountaincar-continuous-sample/mountaincar_continuous_simulator.py

inkling "2.0"

function Reward(gs: GameState) {
    return gs._gym_reward
}

function Terminal(gs: GameState) {
    return gs._gym_terminal
}

type GameState {
    x_position: number,
    x_velocity: number,
    _gym_reward: number,
    _gym_terminal: number
}

const ThrottleMin = -1.0
const ThrottleMax = 1.0
type Action {
    command: number<ThrottleMin .. ThrottleMax>
}

type MountainCarConfig {
    deque_size: -1
}

simulator MountainCarSimulator(action: Action, config: MountainCarConfig): GameState {
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
