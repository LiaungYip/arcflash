# Copyright 2022, Li-aung Yip - https://www.penwatch.net
# Licensed under the MIT License. Refer LICENSE.txt.


import unittest

from arcflash.ieee_1584.calculation import Calculation
from arcflash.ieee_1584.cubicle import Cubicle
from arcflash.ieee_1584.units import ureg, kA, kV, ms, mm, inch, dimensionless, J_per_sq_cm


class TestExampleCalcs(unittest.TestCase):
    def test_annex_D1_calc(self):
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
        T_arc_max = 197 * ms
        T_arc_min = 223 * ms

        # Do all calculations
        calc_max = Calculation(cubicle, I_bf, "full")
        calc_max.calculate_I_arc()
        calc_max.calculate_E_AFB(T_arc_max)

        calc_min = Calculation(cubicle, I_bf, "reduced")
        calc_min.calculate_I_arc()
        calc_min.calculate_E_AFB(T_arc_min)

        # Step 1
        self.assertAlmostEqual(calc_max.I_arc_600, 11.117 * kA, 3)  # D.9
        self.assertAlmostEqual(calc_max.I_arc_2700, 12.816 * kA, 3)  # D.11
        self.assertAlmostEqual(calc_max.I_arc_14300, 14.116 * kA, 3)  # D.13

        # Step 2
        self.assertAlmostEqual(calc_max.I_arc, 12.979 * kA, 3)  # D.17

        # Step 3
        self.assertAlmostEqual(cubicle.width_1, 27.632 * inch, 3)  # D.19
        self.assertAlmostEqual(cubicle.height_1, 45 * inch, 3)  # D.20
        self.assertAlmostEqual(cubicle.EES, 36.316 * inch, 3)  # D.21
        self.assertAlmostEqual(cubicle.CF, 1.284 * dimensionless, 3)  # D.22

        # Step 4
        self.assertAlmostEqual(calc_max.E_600, 8.652 * J_per_sq_cm, 3)  # D.24
        self.assertAlmostEqual(calc_max.E_2700, 11.977 * J_per_sq_cm, 3)  # D.26
        self.assertAlmostEqual(calc_max.E_14300, 13.367 * J_per_sq_cm, 3)  # D.28

        # Step 5
        self.assertAlmostEqual(calc_max.E, 12.152 * J_per_sq_cm, 3)  # D.32

        # Step 6
        self.assertAlmostEqual(calc_max.AFB_600, 1285 * mm, 0)  # D.34
        self.assertAlmostEqual(calc_max.AFB_2700, 1591 * mm, 0)  # D.36
        self.assertAlmostEqual(calc_max.AFB_14300, 1707 * mm, 0)  # D.38

        # Step 7
        self.assertAlmostEqual(calc_max.AFB, 1606 * mm, 0)  # D.42

        # Step 8
        self.assertAlmostEqual(cubicle.VarCF, 0.047 * dimensionless, 3)  # D.43
        self.assertAlmostEqual(1 - 0.5 * cubicle.VarCF, 0.977 * dimensionless, 3)  # D.44

        # Step 9
        self.assertAlmostEqual(calc_min.I_arc_600, 10.856 * kA, 3)  # D.45
        self.assertAlmostEqual(calc_min.I_arc_2700, 12.515 * kA, 3)  # D.46
        self.assertAlmostEqual(calc_min.I_arc_14300, 13.786 * kA, 3)  # D.47

        # Step 10
        self.assertAlmostEqual(calc_min.I_arc, 12.675 * kA, 3)  # D.51

        # Step 11
        self.assertAlmostEqual(calc_min.E_600, 8.980 * J_per_sq_cm, 3)  # D.54
        self.assertAlmostEqual(calc_min.E_2700, 13.018 * J_per_sq_cm, 3)  # D.56
        self.assertAlmostEqual(calc_min.E_14300, 15.602 * J_per_sq_cm, 3)  # D.58

        # Step 12
        self.assertAlmostEqual(calc_min.E, 13.343 * J_per_sq_cm, 3)  # D.62

        # Step 13
        self.assertAlmostEqual(calc_min.AFB_600, 1316 * mm, 0)  # D.64
        self.assertAlmostEqual(calc_min.AFB_2700, 1678 * mm, 0)  # D.66
        self.assertAlmostEqual(calc_min.AFB_14300, 1884 * mm, 0)  # D.68

        # Step 14
        self.assertAlmostEqual(calc_min.AFB, 1704 * mm, 0)  # D.72

    def test_annex_D1_calc_unit_conversion(self):
        # This is exactly the same as test_annex_D2_calc above, but with the input units changed.
        # The intent of this test is to ensure that units are correctly converted (by `pint`) throughout the code.
        # Input data for the low voltage calculation example, from Annex D.2

        # Input data for the high voltage calculation example, from Annex D.1
        cubicle = Cubicle(
            V_oc=4160000 * ureg.millivolt,
            EC="VCB",
            G=0.104 * ureg.metre,
            D=914400 * ureg.micrometre,
            height=1.143 * ureg.metre,
            width=0.000762 * ureg.kilometre,
            depth=508000 * ureg.micrometre,
        )
        I_bf = 15000000 * ureg.milliamp
        T_arc_max = 0.197 * ureg.second
        T_arc_min = 223000 * ureg.microsecond

        # Do all calculations
        calc_max = Calculation(cubicle, I_bf, "full")
        calc_max.calculate_I_arc()
        calc_max.calculate_E_AFB(T_arc_max)

        calc_min = Calculation(cubicle, I_bf, "reduced")
        calc_min.calculate_I_arc()
        calc_min.calculate_E_AFB(T_arc_min)

        # Step 1
        self.assertAlmostEqual(calc_max.I_arc_600, 11.117 * kA, 3)  # D.9
        self.assertAlmostEqual(calc_max.I_arc_2700, 12.816 * kA, 3)  # D.11
        self.assertAlmostEqual(calc_max.I_arc_14300, 14.116 * kA, 3)  # D.13

        # Step 2
        self.assertAlmostEqual(calc_max.I_arc, 12.979 * kA, 3)  # D.17

        # Step 3
        self.assertAlmostEqual(cubicle.width_1, 27.632 * inch, 3)  # D.19
        self.assertAlmostEqual(cubicle.height_1, 45 * inch, 3)  # D.20
        self.assertAlmostEqual(cubicle.EES, 36.316 * inch, 3)  # D.21
        self.assertAlmostEqual(cubicle.CF, 1.284 * dimensionless, 3)  # D.22

        # Step 4
        self.assertAlmostEqual(calc_max.E_600, 8.652 * J_per_sq_cm, 3)  # D.24
        self.assertAlmostEqual(calc_max.E_2700, 11.977 * J_per_sq_cm, 3)  # D.26
        self.assertAlmostEqual(calc_max.E_14300, 13.367 * J_per_sq_cm, 3)  # D.28

        # Step 5
        self.assertAlmostEqual(calc_max.E, 12.152 * J_per_sq_cm, 3)  # D.32

        # Step 6
        self.assertAlmostEqual(calc_max.AFB_600, 1285 * mm, 0)  # D.34
        self.assertAlmostEqual(calc_max.AFB_2700, 1591 * mm, 0)  # D.36
        self.assertAlmostEqual(calc_max.AFB_14300, 1707 * mm, 0)  # D.38

        # Step 7
        self.assertAlmostEqual(calc_max.AFB, 1606 * mm, 0)  # D.42

        # Step 8
        self.assertAlmostEqual(cubicle.VarCF, 0.047 * dimensionless, 3)  # D.43
        self.assertAlmostEqual(1 - 0.5 * cubicle.VarCF, 0.977 * dimensionless, 3)  # D.44

        # Step 9
        self.assertAlmostEqual(calc_min.I_arc_600, 10.856 * kA, 3)  # D.45
        self.assertAlmostEqual(calc_min.I_arc_2700, 12.515 * kA, 3)  # D.46
        self.assertAlmostEqual(calc_min.I_arc_14300, 13.786 * kA, 3)  # D.47

        # Step 10
        self.assertAlmostEqual(calc_min.I_arc, 12.675 * kA, 3)  # D.51

        # Step 11
        self.assertAlmostEqual(calc_min.E_600, 8.980 * J_per_sq_cm, 3)  # D.54
        self.assertAlmostEqual(calc_min.E_2700, 13.018 * J_per_sq_cm, 3)  # D.56
        self.assertAlmostEqual(calc_min.E_14300, 15.602 * J_per_sq_cm, 3)  # D.58

        # Step 12
        self.assertAlmostEqual(calc_min.E, 13.343 * J_per_sq_cm, 3)  # D.62

        # Step 13
        self.assertAlmostEqual(calc_min.AFB_600, 1316 * mm, 0)  # D.64
        self.assertAlmostEqual(calc_min.AFB_2700, 1678 * mm, 0)  # D.66
        self.assertAlmostEqual(calc_min.AFB_14300, 1884 * mm, 0)  # D.68

        # Step 14
        self.assertAlmostEqual(calc_min.AFB, 1704 * mm, 0)  # D.72

    def test_annex_D2_calc(self):
        # Input data for the low voltage calculation example, from Annex D.2
        cubicle = Cubicle(
            V_oc=0.48 * kV,
            EC="VCB",
            G=32 * mm,
            D=609.6 * mm,
            height=610 * mm,
            width=610 * mm,
            depth=254 * mm,
        )
        I_bf = 45.0 * kA
        T_arc_max = 61.3 * ms
        T_arc_min = 319 * ms

        # Do all calculations
        calc_max = Calculation(cubicle, I_bf, "full")
        calc_max.calculate_I_arc()
        calc_max.calculate_E_AFB(T_arc_max)

        calc_min = Calculation(cubicle, I_bf, "reduced")
        calc_min.calculate_I_arc()
        calc_min.calculate_E_AFB(T_arc_min)

        # Step 1
        self.assertAlmostEqual(calc_max.I_arc_600, 32.449 * kA, 3)  # D.82

        # Step 2
        self.assertAlmostEqual(calc_max.I_arc, 28.793 * kA, 3)  # D.84

        # Step 3
        self.assertAlmostEqual(cubicle.width_1, 24.016 * inch, 3)  # D.86
        self.assertAlmostEqual(cubicle.height_1, 24.016 * inch, 3)  # D.87
        self.assertAlmostEqual(cubicle.EES, 24.016 * inch, 3)  # D.88
        self.assertAlmostEqual(cubicle.CF, 1.085 * dimensionless, 3)  # D.89

        # Step 4 / Step 5
        self.assertAlmostEqual(calc_max.E, 11.585 * J_per_sq_cm, 3)  # D.91

        # Step 6 / Step 7
        self.assertAlmostEqual(calc_max.AFB, 1029 * mm, 0)  # D.95

        # Step 8
        self.assertAlmostEqual(cubicle.VarCF, 0.247 * dimensionless, 3)  # D.96
        self.assertAlmostEqual(1 - 0.5 * cubicle.VarCF, 0.877 * dimensionless, 3)  # D.97

        # Step 9
        self.assertAlmostEqual(calc_min.I_arc, 25.244 * kA, 3)  # D.99

        # Step 10 / Step 11
        self.assertAlmostEqual(calc_min.E, 53.156 * J_per_sq_cm, 3)  # D.103

        # Step 12 / Step 13
        self.assertAlmostEqual(calc_min.AFB, 2669 * mm, 0)  # D.106

    def test_annex_D2_calc_unit_conversion(self):
        # This is exactly the same as test_annex_D2_calc above, but with the input units changed.
        # The intent of this test is to ensure that units are correctly converted (by `pint`) throughout the code.
        # Input data for the low voltage calculation example, from Annex D.2
        cubicle = Cubicle(
            V_oc=480 * ureg.volt,
            EC="VCB",
            G=0.032 * ureg.metre,
            D=0.0006096 * ureg.kilometre,
            height=610000 * ureg.micrometre,
            width=610000 * ureg.micrometre,
            depth=254000 * ureg.micrometre,
        )
        I_bf = 45000 * ureg.ampere
        T_arc_max = 0.0613 * ureg.second
        T_arc_min = 319000 * ureg.microsecond

        # Do all calculations
        calc_max = Calculation(cubicle, I_bf, "full")
        calc_max.calculate_I_arc()
        calc_max.calculate_E_AFB(T_arc_max)

        calc_min = Calculation(cubicle, I_bf, "reduced")
        calc_min.calculate_I_arc()
        calc_min.calculate_E_AFB(T_arc_min)

        # Step 1
        self.assertAlmostEqual(calc_max.I_arc_600, 32.449 * kA, 3)  # D.82

        # Step 2
        self.assertAlmostEqual(calc_max.I_arc, 28.793 * kA, 3)  # D.84

        # Step 3
        self.assertAlmostEqual(cubicle.width_1, 24.016 * inch, 3)  # D.86
        self.assertAlmostEqual(cubicle.height_1, 24.016 * inch, 3)  # D.87
        self.assertAlmostEqual(cubicle.EES, 24.016 * inch, 3)  # D.88
        self.assertAlmostEqual(cubicle.CF, 1.085 * dimensionless, 3)  # D.89

        # Step 4 / Step 5
        self.assertAlmostEqual(calc_max.E, 11.585 * J_per_sq_cm, 3)  # D.91

        # Step 6 / Step 7
        self.assertAlmostEqual(calc_max.AFB, 1029 * mm, 0)  # D.95

        # Step 8
        self.assertAlmostEqual(cubicle.VarCF, 0.247 * dimensionless, 3)  # D.96
        self.assertAlmostEqual(1 - 0.5 * cubicle.VarCF, 0.877 * dimensionless, 3)  # D.97

        # Step 9
        self.assertAlmostEqual(calc_min.I_arc, 25.244 * kA, 3)  # D.99

        # Step 10 / Step 11
        self.assertAlmostEqual(calc_min.E, 53.156 * J_per_sq_cm, 3)  # D.103

        # Step 12 / Step 13
        self.assertAlmostEqual(calc_min.AFB, 2669 * mm, 0)  # D.106


if __name__ == '__main__':
    unittest.main()
