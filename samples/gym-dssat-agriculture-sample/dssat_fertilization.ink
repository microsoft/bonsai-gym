inkling "2.0"

using Number
using Math
using Goal

type Mode number<uninitialized = 0, fertilization = 1, irrigation = 2, all = 3>

type ObservableState {
    # Observation variables
    cumsumfert: number<0..20000>, # cumulative nitrogen fertilizer applications (kg/ha)
    dap: number<0..366>, # days after planting
    dtt: number<0..100>, # growing degree days for current day (C/d)
    ep: number<0..50>, # actual plant transpiration rate (mm/d)
    grnwt: number<0..50000>, # grain weight dry matter (kg/ha)'
    istage: number<1..9 step 1>, # DSSAT maize growing stage (index in order 7, 8, 9, 1, 2, 3, 4, 5 ,6)
    nstres: number<0..1>, # index of plant nitrogen stress (unitless)
    swfac: number<0..1>, # index of plant water stress (unitless)
    topwt: number<0..50000>, # above the ground population biomass (kg/ha)
    vstage: number<0..30>, # vegetative growth stage (number of leaves)
    xlai: number<0..10>, # plant population leaf area index (m2_leaf/m2_soil)

    # Additional variables from internal environment state
    cleach: number<0..20000>, # cumulative nitrate leaching (kg/ha)

    # Config variables
    mode: Mode, # mode that was set up by the lesson config

    # Context variables
    # Not sure how to hook up the context variables so they would be reported by the sim...
    #sat: number<0..1>[9], # volumetric soil water content in soil layers at saturation - (cm3 [water] / cm3 [soil])
    #dul: number<0..1>[9], # volumetric soil water content in soil layers at drained -  upper limit (cm3 [water] / cm3 [soil])
    #ll: number<0..1>[9], # volumetric soil water content in soil layers at lower limit - (cm3 [water] / cm3 [soil])
    #dlayr: number<0..1000>[9], # thickness of for soil layers (cm)
}

type SimState extends ObservableState {
    _gym_reward: number,
    _gym_terminal: number
}

type Action {
    anfer: number<0 .. 200>, # nitrogen to fertilize for current day (kg/ha)
}

type Config {
    mode: Mode
}

function Reward(ss: SimState) {
    return ss._gym_reward
}

function Terminal(ss: SimState) {
    return ss._gym_terminal
}

simulator Simulator(action: Action, config: Config): SimState {
    package "dssat"
}

graph (input: ObservableState): Action {

    concept Fertilize(input): Action {
        curriculum {
            source Simulator
            reward Reward
            terminal Terminal

            lesson balancing {
                scenario {
                    mode: Mode.fertilization
                }
            }
        }
    }
    output Fertilize
}
