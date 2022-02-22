# Copyright 2022, Li-aung Yip - https://www.penwatch.net
# Licensed under the MIT License. Refer LICENSE.txt.

from ieee_1584.cubicle import Cubicle
from ieee_1584.equations import I_arc_intermediate, I_arc_min, interpolate, I_arc_final_LV, intermediate_E, \
    intermediate_AFB_from_E


class Calculation:
    def __init__(self, c: Cubicle, I_bf: float):
        self.c = c
        self.I_bf = I_bf

        self.AFB_14300_max = None
        self.AFB_14300_min = None
        self.AFB_2700_max = None
        self.AFB_2700_min = None
        self.AFB_600_max = None
        self.AFB_600_min = None
        self.AFB_max = None
        self.AFB_min = None
        self.E_14300_max = None
        self.E_14300_min = None
        self.E_2700_max = None
        self.E_2700_min = None
        self.E_600_max = None
        self.E_600_min = None
        self.E_max = None
        self.E_min = None
        self.I_arc_14300_max = None
        self.I_arc_14300_min = None
        self.I_arc_2700_max = None
        self.I_arc_2700_min = None
        self.I_arc_600_max = None
        self.I_arc_600_min = None
        self.I_arc_max = None
        self.I_arc_min = None
        self.T_arc_max = None
        self.T_arc_min = None

        self.vlevel = "DEPRECATED"  # voltage level attribute has been moved to the Cubicle class.

    def calculate_I_arc(self):
        # Calculates I_arc and also the reduced I_arc_min
        if self.c.vlevel == "HV":
            self.I_arc_600_max = I_arc_intermediate(self.c, 0.600, self.I_bf)
            self.I_arc_2700_max = I_arc_intermediate(self.c, 2.700, self.I_bf)
            self.I_arc_14300_max = I_arc_intermediate(self.c, 14.300, self.I_bf)
            self.I_arc_max = interpolate(self.c, self.I_arc_600_max, self.I_arc_2700_max, self.I_arc_14300_max)

            self.I_arc_600_min = I_arc_min(self.c, self.I_arc_600_max)
            self.I_arc_2700_min = I_arc_min(self.c, self.I_arc_2700_max)
            self.I_arc_14300_min = I_arc_min(self.c, self.I_arc_14300_max)
            self.I_arc_min = interpolate(self.c, self.I_arc_600_min, self.I_arc_2700_min, self.I_arc_14300_min)

        elif self.c.vlevel == "LV":
            self.I_arc_600_max = I_arc_intermediate(self.c, 0.600, self.I_bf)
            self.I_arc_max = I_arc_final_LV(self.c, self.I_arc_600_max, self.I_bf)

            # self.I_arc_min = self.I_arc_max * self.c.VarCF
            self.I_arc_min = I_arc_min(self.c, self.I_arc_max)

    def calculate_E_AFB(self, T_arc_max: float, T_arc_min: float):

        self.T_arc_max = T_arc_max
        self.T_arc_min = T_arc_min

        if self.c.vlevel == "HV":
            # Max
            self.E_600_max = intermediate_E(self.c, 0.600, self.I_arc_600_max, self.I_bf, self.T_arc_max)
            self.E_2700_max = intermediate_E(self.c, 2.700, self.I_arc_2700_max, self.I_bf, self.T_arc_max)
            self.E_14300_max = intermediate_E(self.c, 14.300, self.I_arc_14300_max, self.I_bf, self.T_arc_max)
            self.AFB_600_max = intermediate_AFB_from_E(self.c, 0.600, self.E_600_max)
            self.AFB_2700_max = intermediate_AFB_from_E(self.c, 2.700, self.E_2700_max)
            self.AFB_14300_max = intermediate_AFB_from_E(self.c, 14.300, self.E_14300_max)

            self.E_max = interpolate(self.c, self.E_600_max, self.E_2700_max, self.E_14300_max)
            self.AFB_max = interpolate(self.c, self.AFB_600_max, self.AFB_2700_max, self.AFB_14300_max)

            # Min
            self.E_600_min = intermediate_E(self.c, 0.600, self.I_arc_600_min, self.I_bf, self.T_arc_min)
            self.E_2700_min = intermediate_E(self.c, 2.700, self.I_arc_2700_min, self.I_bf, self.T_arc_min)
            self.E_14300_min = intermediate_E(self.c, 14.300, self.I_arc_14300_min, self.I_bf, self.T_arc_min)
            self.AFB_600_min = intermediate_AFB_from_E(self.c, 0.600, self.E_600_min)
            self.AFB_2700_min = intermediate_AFB_from_E(self.c, 2.700, self.E_2700_min)
            self.AFB_14300_min = intermediate_AFB_from_E(self.c, 14.300, self.E_14300_min)

            self.E_min = interpolate(self.c, self.E_600_min, self.E_2700_min, self.E_14300_min)
            self.AFB_min = interpolate(self.c, self.AFB_600_min, self.AFB_2700_min, self.AFB_14300_min)

        elif self.c.vlevel == "LV":
            self.E_max = intermediate_E(self.c, self.c.V_oc, self.I_arc_max, self.I_bf, self.T_arc_max,
                                        self.I_arc_600_max)
            self.E_min = intermediate_E(self.c, self.c.V_oc, self.I_arc_min, self.I_bf, self.T_arc_min,
                                        self.I_arc_600_max)  # Note I_arc_600_max, **not** I_arc_600_min.
            self.AFB_max = intermediate_AFB_from_E(self.c, self.c.V_oc, self.E_max)
            self.AFB_min = intermediate_AFB_from_E(self.c, self.c.V_oc, self.E_min)

    def pretty_print(self):
        return \
            f"""Let I_bf = {self.I_bf:.3f} kA

Calculated:

I_arc_max = {self.I_arc_max:.3f} kA
I_arc_min = {self.I_arc_min:.3f} kA

Then, with T_arc_max = {self.T_arc_max:.1f} ms and T_arc_min = {self.T_arc_min:.1f} ms:

E_max = {self.E_max:.3f} J/cm² or {self.E_max / 4.184:.3f} cal/cm²
AFB_max = {self.AFB_max:.0f} mm

E_min = {self.E_min:.3f} J/cm² or {self.E_min / 4.184:.3f} cal/cm²
AFB_min = {self.AFB_min:.0f} mm
"""
