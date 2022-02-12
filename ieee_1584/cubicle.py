# Copyright 2022, Li-aung Yip - https://www.penwatch.net
# Licensed under the MIT License. Refer LICENSE.txt.


from ieee_1584.tables import table_2, table_7


class Cubicle:
    # The Cubicle class encapsulates physical parameters of equipment that do not change with current (kA) or time (ms).
    def __init__(self, V_oc: float, EC: str, G: float, D: float, height: float, width: float, depth: float):
        # Assign input data

        self.V_oc = V_oc
        self.EC = EC
        self.G = G
        self.D = D
        self.height = height
        self.width = width
        self.depth = depth

        # Initialise placeholders
        self.enclosure_type = None
        self.VarCF = None
        self.width_1 = None
        self.height_1 = None
        self.EES = None
        self.CF = None

        # Calculate dependent variables and do basic input checking
        self.calc_VarCf()
        self.calc_CF()
        self.check_model_bounds()
        self.sanity_check()

    def check_model_bounds(self):
        # ref IEEE 1584-2018 s4.2 "Range of model"
        # Applying the IEEE 1584-2018 model outside these ranges _WILL_ give incorrect results.

        assert 0.208 <= self.V_oc <= 15

        if self.V_oc <= 0.600:  # low voltage
            assert 6.35 <= self.G <= 76.2
        else:  # high voltage
            assert 19.05 <= self.G <= 254

        assert self.D >= 305

        assert self.width >= 4 * self.G  # Width of enclosure should be at least four times the busbar gap

        assert self.EC in ("VCB", "VCBB", "HCB", "HOA", "VOA",)

    def sanity_check(self):
        assert 0.0 <= self.CF <= 2.0

    def calc_VarCf(self):
        # Arcing current variation correction factor.
        # The equation under Equation 2. (Equation 2a?)
        V_oc = self.V_oc

        k = table_2[self.EC]

        v = + k["k1"] * V_oc ** 6 \
            + k["k2"] * V_oc ** 5 \
            + k["k3"] * V_oc ** 4 \
            + k["k4"] * V_oc ** 3 \
            + k["k5"] * V_oc ** 2 \
            + k["k6"] * V_oc ** 1 \
            + k["k7"]

        self.VarCF = v

    def calc_CF(self):
        # Enclosure size correction factor.
        if self.EC in ("HOA", "VOA",):
            # Open air configurations HOA / VOA do not require a box size correction factor.
            self.CF = 1.00
            return

        if (self.V_oc < 0.6) and (self.height < 508) and (self.width < 508) and (self.depth <= 203.2):
            self.enclosure_type = "Shallow"
        else:
            self.enclosure_type = "Typical"

        constants = {
            "VCB": (4, 20,),
            "VCBB": (10, 24,),
            "HCB": (10, 22),
        }
        A, B = constants[self.EC]

        # Equation 11 / 12
        def eq_11_12(dim):
            y1 = dim - 660.4
            y2 = (self.V_oc + A) / B
            dim_1 = (660.4 + (y1 * y2)) / 25.4
            return dim_1

        # Table 6
        # The special case in this table appears to be height_1 for the VCBB configuration.

        mm_to_in = 0.03937

        width_1 = None
        w = self.width
        if w < 508:
            if self.enclosure_type == "Typical":
                width_1 = 20
            elif self.enclosure_type == "Shallow":
                width_1 = mm_to_in * w
        elif 508 <= w <= 660.4:
            width_1 = mm_to_in * w
        elif 660.4 <= w <= 1244.6:
            width_1 = eq_11_12(w)
        elif 1244.6 < w:
            width_1 = eq_11_12(1244.6)

        height_1 = None
        h = self.height
        if h < 508:
            if self.enclosure_type == "Typical":
                height_1 = 20
            elif self.enclosure_type == "Shallow":
                height_1 = mm_to_in * h
        elif 508 <= h <= 660.4:
            height_1 = mm_to_in * h
        elif 660.4 <= h <= 1244.6:
            if self.EC == "VCB":
                height_1 = mm_to_in * h
            elif self.EC in ("VCBB", "HCB",):
                height_1 = eq_11_12(h)
        elif 1244.6 < h:
            height_1 = 49

        # Equation 13
        EES = (height_1 + width_1) / 2
        if self.enclosure_type == "Typical":
            assert EES >= 20  # "For typical box enclosures, the minimum value of EES is 20."

        # save calculation details for unit test purposes
        self.height_1 = height_1
        self.width_1 = width_1
        self.EES = EES

        # Equation 14 / 15
        key = (self.enclosure_type, self.EC)
        b = table_7[key]
        x1 = + b["b1"] * EES ** 2 \
             + b["b2"] * EES \
             + b["b3"]

        if self.enclosure_type == "Typical":
            self.CF = x1
        elif self.enclosure_type == "Shallow":
            self.CF = 1 / x1

    def pretty_print(self):
        return f"""Cubicle parameters:
        
V_oc (nominal voltage)          = {self.V_oc:.3f} kV
D (working distance)            = {self.D:.1f} mm
G (busbar gap)                  = {self.G:.1f} mm
EC (electrode configuration)    = {self.EC}

Box dimensions:
    height  = {self.height:.1f} mm
    width   = {self.width:.1f} mm
    depth   = {self.depth:.1f} mm
    
Enclosure correction factor
    enclosure_type  = {self.enclosure_type}
    height_1        = {self.height_1:.1f} inch
    width_1         = {self.width_1:.1f} inch
    EES             = {self.EES:.1f} inch
    CF              = {self.CF:.3f}
"""
