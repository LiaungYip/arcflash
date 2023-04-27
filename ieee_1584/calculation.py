# Copyright 2022, Li-aung Yip - https://www.penwatch.net
# Licensed under the MIT License. Refer LICENSE.txt.

from ieee_1584.cubicle import Cubicle
from ieee_1584.equations import I_arc_intermediate, I_arc_min, interpolate, I_arc_final_LV, intermediate_E, \
    intermediate_AFB_from_E

from ieee_1584.units import Q_, kV, cal_per_sq_cm, sec, kA


class Calculation:
    def __init__(self, c: Cubicle, I_bf: Q_, full_or_reduced: str):
        # "full" means the full value of I_arc is used.
        # "reduced" means that I_arc_min is used, e.g. that the arcing current variation factor VarCF is used.
        #
        # I have called these "full"/"reduced" to avoid confusion with "max"/"min" which mean e.g.
        # "maximum fault operating scenario" and "minimum fault operating scenario" in context.

        assert I_bf.check('[current]')

        if (0.208 * kV <= c.V_oc <= 0.600 * kV) and not (0.500 * kA <= I_bf <= 106.000 * kA):
            raise ValueError(f"I_bf out of range for LV calculation. I_bf = {I_bf:.3f~P} is outside the range 500 A to 106 kA.")
        elif (0.600 * kV < c.V_oc <= 15.000 * kV) and not (0.200 * kA <= I_bf <= 65.000 * kA):
            raise ValueError(f"I_bf out of range for HV calculation. I_bf = {I_bf:.3f~P} is outside the range 200 A to 65 kA.")

        assert full_or_reduced in ("full", "reduced",)

        self.c = c
        self.I_bf = I_bf

        self.AFB_14300 = None
        self.AFB_2700 = None
        self.AFB_600 = None
        self.AFB = None
        self.E_14300 = None
        self.E_2700 = None
        self.E_600 = None
        self.E = None
        self.I_arc_14300 = None
        self.I_arc_2700 = None
        self.I_arc_600 = None
        self.I_arc = None
        self.T_arc = None

        self.full_or_reduced = full_or_reduced

        self.vlevel = "DEPRECATED"  # voltage level attribute has been moved to the Cubicle class.

    def calculate_I_arc(self) -> None:
        if self.c.vlevel == "HV":
            I_arc_600_full = I_arc_intermediate(self.c, 0.600 * kV, self.I_bf)
            I_arc_2700_full = I_arc_intermediate(self.c, 2.700 * kV, self.I_bf)
            I_arc_14300_full = I_arc_intermediate(self.c, 14.300 * kV, self.I_bf)
            if self.full_or_reduced == "full":
                self.I_arc_600 = I_arc_600_full
                self.I_arc_2700 = I_arc_2700_full
                self.I_arc_14300 = I_arc_14300_full
                self.I_arc = interpolate(self.c, self.I_arc_600, self.I_arc_2700, self.I_arc_14300)

            else:
                self.I_arc_600 = I_arc_min(self.c, I_arc_600_full)
                self.I_arc_2700 = I_arc_min(self.c, I_arc_2700_full)
                self.I_arc_14300 = I_arc_min(self.c, I_arc_14300_full)
                self.I_arc = interpolate(self.c, self.I_arc_600, self.I_arc_2700, self.I_arc_14300)

        elif self.c.vlevel == "LV":
            self.I_arc_600 = I_arc_intermediate(self.c, 0.600 * kV, self.I_bf)
            I_arc_full = I_arc_final_LV(self.c, self.I_arc_600, self.I_bf)

            if self.full_or_reduced == "full":
                self.I_arc = I_arc_full
            else:
                self.I_arc = I_arc_min(self.c, I_arc_full)

    def calculate_E_AFB(self, T_arc: Q_) -> None:
        assert T_arc.check('[time]')

        self.T_arc = T_arc.to(sec)

        if self.c.vlevel == "HV":
            # Max
            self.E_600 = intermediate_E(self.c, 0.600 * kV, self.I_arc_600, self.I_bf, self.T_arc)
            self.E_2700 = intermediate_E(self.c, 2.700 * kV, self.I_arc_2700, self.I_bf, self.T_arc)
            self.E_14300 = intermediate_E(self.c, 14.300 * kV, self.I_arc_14300, self.I_bf, self.T_arc)
            self.AFB_600 = intermediate_AFB_from_E(self.c, 0.600 * kV, self.E_600)
            self.AFB_2700 = intermediate_AFB_from_E(self.c, 2.700 * kV, self.E_2700)
            self.AFB_14300 = intermediate_AFB_from_E(self.c, 14.300 * kV, self.E_14300)

            self.E = interpolate(self.c, self.E_600, self.E_2700, self.E_14300)
            self.AFB = interpolate(self.c, self.AFB_600, self.AFB_2700, self.AFB_14300)

        elif self.c.vlevel == "LV":
            # Note I_arc_600_max, **not** I_arc_600_min, even in a "min" calculation.
            self.E = intermediate_E(self.c, self.c.V_oc, self.I_arc, self.I_bf, self.T_arc, self.I_arc_600)
            self.AFB = intermediate_AFB_from_E(self.c, self.c.V_oc, self.E)

    def pretty_print(self) -> str:
        return \
            f"""Let I_bf = {self.I_bf:.3f~P}

Calculated:

I_arc = {self.I_arc:.3f~P} ({self.full_or_reduced})

Then, with T_arc = {self.T_arc:.1f~P}:

E = {self.E:.3f~P} or {self.E.to(cal_per_sq_cm):.3f~P}
AFB = {self.AFB:.0f~P}
"""
