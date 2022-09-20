inkling "2.0"

#using Goal - OPTIONAL
using Goal
using Math
using Number

#Action Space Box(-1.0, 1.0, (1,), float32)
#action 0 Force applied on the cart -1 1 slider slide Force (N)
#Observation Shape (11,)
#Observation High [inf inf inf inf inf inf inf inf inf inf inf]
#Observation Low [-inf -inf -inf -inf -inf -inf -inf -inf -inf -inf -inf]

#0 - position of the cart along the linear surface - position (m)
#1 - sine of the angle between the cart and the first pole - sin(hinge)
#2 - sine of the angle between the two poles - sin(hinge2)
#3 - cosine of the angle between the cart and the first pole - cos(hinge)
#4 - cosine of the angle between the two poles - cos(hinge2)
#5 - velocity of the cart - velocity (m/s)
#6 - angular velocity of the angle between the cart and the first pole - angular velocity (rad/s)
#7 - angular velocity of the angle between the two poles - angular velocity (rad/s)
#8 - constraint force - 1 - Force (N) - see https://mujoco.readthedocs.io/en/latest/computation.html
#9 - constraint force - 2 - Force (N)
#10 - constraint force - 3 - Force (N)

#Import gym.make("InvertedDoublePendulum-v4")

function Reward(gs: MujocoState) {
    return gs._gym_reward
}

function Terminal(gs: MujocoState) {
    return gs._gym_terminal
}

const max_position = 100 #m
const max_speed = 100 #m/s
const max_ang_speed = 100 #rad/s
const max_constraint = 100 #N

type MujocoState {
    pos: Number.Float32,
    sin_hinge1: Number.Float32,
    sin_hinge2: Number.Float32,
    cos_hinge1: Number.Float32,
    cos_hinge2: Number.Float32,
    velocity: Number.Float32,
    ang_velocity1: Number.Float32,
    ang_velocity2: Number.Float32,
    constraint1: Number.Float32,
    constraint2: Number.Float32,
    constraint3: Number.Float32,
    _gym_reward: number,
    _gym_terminal: number
}

type ObservableState {

    pos: Number.Float32,
    sin_hinge1: Number.Float32,
    sin_hinge2: Number.Float32,
    cos_hinge1: Number.Float32,
    cos_hinge2: Number.Float32,
    velocity: Number.Float32,
    ang_velocity1: Number.Float32,
    ang_velocity2: Number.Float32,
    constraint1: Number.Float32,
    constraint2: Number.Float32,
    constraint3: Number.Float32,
}

type MujocoAction {
    action: Number.Float32<-1 .. 1>[1],
}

type SimAction {
    input_force: Number.Float32<-1 .. 1>,
}

type SimConfig {
    deque_size: Number.UInt8
}

function TransformState(State: MujocoState): ObservableState {

    return {
        pos: State.pos,
        sin_hinge1: State.sin_hinge1,
        sin_hinge2: State.sin_hinge2,
        cos_hinge1: State.cos_hinge1,
        cos_hinge2: State.cos_hinge2,
        velocity: State.velocity,
        ang_velocity1: State.ang_velocity1,
        ang_velocity2: State.ang_velocity2,
        constraint1: State.constraint1,
        constraint2: State.constraint2,
        constraint3: State.constraint3,
    }
}

function TransformAction(State: SimAction): MujocoAction {

    var command: Number.Float32<-1 .. 1>[1] = [State.input_force]

    return {
        action: command
    }
}

simulator Mujoco(action: MujocoAction, config: SimConfig): MujocoState {
}

graph (input: ObservableState): SimAction {

    concept StayUp(input): SimAction {
        curriculum {
            source Mujoco
            reward Reward
            terminal Terminal
            state TransformState
            action TransformAction
            lesson first_lesson {
                scenario {
                    deque_size: 2
                }
            }
        }
    }
}
