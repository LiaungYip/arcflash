# Copyright 2022, Li-aung Yip - https://www.penwatch.net
# Licensed under the MIT License. Refer LICENSE.txt.

import unittest

from ieee_1584.calculation import Calculation
from ieee_1584.cubicle import Cubicle
from ieee_1584.units import ureg, kA, kV, ms, mm, inch, dimensionless, J_per_sq_cm
from ieee_1584.multistep import multistep_E_and_AFB


class MultistepTest(unittest.TestCase):
    def test_annex_D1_calc_multistep(self):
        # Test that doing a calculation in 2 steps gives an identical result to doing the calculation in 1 step
        # Input data for the high voltage calculation example, from Annex D.1
        cubicle = Cubicle(
            V_oc=4.16 * kV,
            EC="VCB",
            G=104 * mm,
            D=914.4 * mm,
            height=1143 * mm,
            width=762 * mm,
            depth=508 * mm,
        )
        I_bf = 15.0 * kA

        # Total 197ms as per original example
        T_arc_max_1 = 170 * ms
        T_arc_max_2 = 27 * ms

        # Total 223 ms as per original example
        T_arc_min_1 = 200 * ms
        T_arc_min_2 = 23 * ms

        # Do all calculations
        calc_max_1 = Calculation(cubicle, I_bf, "full")
        calc_max_1.calculate_I_arc()
        calc_max_1.calculate_E_AFB(T_arc_max_1)

        calc_max_2 = Calculation(cubicle, I_bf, "full")
        calc_max_2.calculate_I_arc()
        calc_max_2.calculate_E_AFB(T_arc_max_2)

        max_E, max_AFB = multistep_E_and_AFB(cubicle, [calc_max_1, calc_max_2])

        calc_min_1 = Calculation(cubicle, I_bf, "reduced")
        calc_min_1.calculate_I_arc()
        calc_min_1.calculate_E_AFB(T_arc_min_1)

        calc_min_2 = Calculation(cubicle, I_bf, "reduced")
        calc_min_2.calculate_I_arc()
        calc_min_2.calculate_E_AFB(T_arc_min_2)

        min_E, min_AFB = multistep_E_and_AFB(cubicle, [calc_min_1, calc_min_2])

        # Step 5
        self.assertAlmostEqual(max_E, 12.152 * J_per_sq_cm, 3)  # D.32

        # Step 7
        self.assertAlmostEqual(max_AFB, 1606 * mm, 0)  # D.42

        # Step 12
        self.assertAlmostEqual(min_E, 13.343 * J_per_sq_cm, 3)  # D.62

        # Step 14
        self.assertAlmostEqual(min_AFB, 1704 * mm, 0)  # D.72


if __name__ == '__main__':
    unittest.main()
