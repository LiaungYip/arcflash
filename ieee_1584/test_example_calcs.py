# Copyright 2022, Li-aung Yip - https://www.penwatch.net
# Licensed under the MIT License. Refer LICENSE.txt.


import unittest

from ieee_1584.calculation import Calculation
from ieee_1584.cubicle import Cubicle


class TestExampleCalcs(unittest.TestCase):
    def test_annex_D1_calc(self):
        # Input data for the high voltage calculation example, from Annex D.1
        cubicle = Cubicle(V_oc=4.16, EC="VCB", G=104, D=914.4, height=1143, width=762, depth=508)
        I_bf = 15.0
        T_arc_max = 197
        T_arc_min = 223

        # Do all calculations
        calc = Calculation(cubicle, I_bf)
        calc.calculate_I_arc()
        calc.calculate_E_AFB(T_arc_max, T_arc_min)

        # Step 1
        self.assertAlmostEqual(calc.I_arc_600_max, 11.117, 3)  # D.9
        self.assertAlmostEqual(calc.I_arc_2700_max, 12.816, 3)  # D.11
        self.assertAlmostEqual(calc.I_arc_14300_max, 14.116, 3)  # D.13

        # Step 2
        self.assertAlmostEqual(calc.I_arc_max, 12.979, 3)  # D.17

        # Step 3
        self.assertAlmostEqual(cubicle.width_1, 27.632, 3)  # D.19
        self.assertAlmostEqual(cubicle.height_1, 45, 3)  # D.20
        self.assertAlmostEqual(cubicle.EES, 36.316, 3)  # D.21
        self.assertAlmostEqual(cubicle.CF, 1.284, 3)  # D.22

        # Step 4
        self.assertAlmostEqual(calc.E_600_max, 8.652, 3)  # D.24
        self.assertAlmostEqual(calc.E_2700_max, 11.977, 3)  # D.26
        self.assertAlmostEqual(calc.E_14300_max, 13.367, 3)  # D.28

        # Step 5
        self.assertAlmostEqual(calc.E_max, 12.152, 3)  # D.32

        # Step 6
        self.assertAlmostEqual(calc.AFB_600_max, 1285, 0)  # D.34
        self.assertAlmostEqual(calc.AFB_2700_max, 1591, 0)  # D.36
        self.assertAlmostEqual(calc.AFB_14300_max, 1707, 0)  # D.38

        # Step 7
        self.assertAlmostEqual(calc.AFB_max, 1606, 0)  # D.42

        # Step 8
        self.assertAlmostEqual(cubicle.VarCF, 0.047, 3)  # D.43
        self.assertAlmostEqual(1 - 0.5 * cubicle.VarCF, 0.977, 3)  # D.44

        # Step 9
        self.assertAlmostEqual(calc.I_arc_600_min, 10.856, 3)  # D.45
        self.assertAlmostEqual(calc.I_arc_2700_min, 12.515, 3)  # D.46
        self.assertAlmostEqual(calc.I_arc_14300_min, 13.786, 3)  # D.47

        # Step 10
        self.assertAlmostEqual(calc.I_arc_min, 12.675, 3)  # D.51

        # Step 11
        self.assertAlmostEqual(calc.E_600_min, 8.980, 3)  # D.54
        self.assertAlmostEqual(calc.E_2700_min, 13.018, 3)  # D.56
        self.assertAlmostEqual(calc.E_14300_min, 15.602, 3)  # D.58

        # Step 12
        self.assertAlmostEqual(calc.E_min, 13.343, 3)  # D.62

        # Step 13
        self.assertAlmostEqual(calc.AFB_600_min, 1316, 0)  # D.64
        self.assertAlmostEqual(calc.AFB_2700_min, 1678, 0)  # D.66
        self.assertAlmostEqual(calc.AFB_14300_min, 1884, 0)  # D.68

        # Step 14
        self.assertAlmostEqual(calc.AFB_min, 1704, 0)  # D.72

    def test_annex_D2_calc(self):
        # Input data for the low voltage calculation example, from Annex D.2
        cubicle = Cubicle(V_oc=0.48, EC="VCB", G=32, D=609.6, height=610, width=610, depth=254)
        I_bf = 45.0
        T_arc_max = 61.3
        T_arc_min = 319

        # Do all calculations
        calc = Calculation(cubicle, I_bf)
        calc.calculate_I_arc()
        calc.calculate_E_AFB(T_arc_max, T_arc_min)

        # Step 1
        self.assertAlmostEqual(calc.I_arc_600_max, 32.449, 3)  # D.82

        # Step 2
        self.assertAlmostEqual(calc.I_arc_max, 28.793, 3)  # D.84

        # Step 3
        self.assertAlmostEqual(cubicle.width_1, 24.016, 3)  # D.86
        self.assertAlmostEqual(cubicle.height_1, 24.016, 3)  # D.87
        self.assertAlmostEqual(cubicle.EES, 24.016, 3)  # D.88
        self.assertAlmostEqual(cubicle.CF, 1.085, 3)  # D.89

        # Step 4 / Step 5
        self.assertAlmostEqual(calc.E_max, 11.585, 3)  # D.91

        # Step 6 / Step 7
        self.assertAlmostEqual(calc.AFB_max, 1029, 0)  # D.95

        # Step 8
        self.assertAlmostEqual(cubicle.VarCF, 0.247, 3)  # D.96
        self.assertAlmostEqual(1 - 0.5 * cubicle.VarCF, 0.877, 3)  # D.97

        # Step 9
        self.assertAlmostEqual(calc.I_arc_min, 25.244, 3)  # D.99

        # Step 10 / Step 11
        self.assertAlmostEqual(calc.E_min, 53.156, 3)  # D.103

        # Step 12 / Step 13
        self.assertAlmostEqual(calc.AFB_min, 2669, 0)  # D.106


if __name__ == '__main__':
    unittest.main()
