from arcflash.ieee_1584.calculation import Calculation
from arcflash.ieee_1584.cubicle import Cubicle
from arcflash.ieee_1584.equations import intermediate_AFB_from_E, interpolate
from arcflash.ieee_1584.units import kV, Q_


def multistep_E_and_AFB(c: Cubicle, calc_steps: list[Calculation]) -> (Q_, Q_):
    # Calculates the total energy and total arc flash boundary for a multi-step calculation.
    #
    # E.g. for example, if there are 2 calculation time steps -
    # Step 1: calculation for I_bf = 10kA for T = 0.100 sec -> E = 10 J/cm², AFB = 1,000 mm
    # Step 2: calculation for I_bf = 5kA for T = 0.200 sec -> E = 2 J/cm², AFB = 500 mm
    #
    # The total energy is just the sum of energy at each step: total_E = 10 + 2 = 12 J/cm².
    #
    # The arc flash boundary, however, is non-linear with energy and so needs special treatment.
    #
    # For HV, intermediate AFB's are worked out from the intermediate E values at 600, 2700, and 14300 V.
    #
    # So we need to calculate the sum of E_600, E_2700, and E_14300 across all steps, then calculate the intermediate
    # AFB values AFB_600, AFB_2700, and AFB_14300.
    #
    # The final AFB is then interpolated from the intermediate AFB's.
    #
    # For LV, there are no intermediate values / interpolation so we can just work out the AFB based on total_E.

    total_E = sum([c.E for c in calc_steps])

    if c.vlevel == "HV":
        total_E_600 = sum([c.E_600 for c in calc_steps])
        total_E_2700 = sum([c.E_2700 for c in calc_steps])
        total_E_14300 = sum([c.E_14300 for c in calc_steps])

        AFB_600 = intermediate_AFB_from_E(c, 0.600 * kV, total_E_600)
        AFB_2700 = intermediate_AFB_from_E(c, 2.700 * kV, total_E_2700)
        AFB_14300 = intermediate_AFB_from_E(c, 14.300 * kV, total_E_14300)

        total_AFB = interpolate(c, AFB_600, AFB_2700, AFB_14300)

    else:
        total_AFB = intermediate_AFB_from_E(c, c.V_oc, total_E)

    return total_E, total_AFB
