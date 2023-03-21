# Copyright 2022, Li-aung Yip - https://www.penwatch.net
# Licensed under the MIT License. Refer LICENSE.txt.


from ieee_1584.tables import table_2, table_7
from ieee_1584.units import Q_, kV, mm, inch, dimensionless


class Cubicle:
    # The Cubicle class encapsulates physical parameters of equipment that do not change with current (kA) or time (ms).
    def __init__(self, V_oc: Q_, EC: str, G: Q_, D: Q_, height: Q_, width: Q_, depth: Q_):
        # Check units
        assert V_oc.check('[electric_potential]')
        assert G.check('[length]')
        assert D.check('[length]')
        assert height.check('[length]')
        assert width.check('[length]')
        assert depth.check('[length]')

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

        if 0.600 * kV < self.V_oc <= 15.000 * kV:
            self.vlevel = "HV"
        elif self.V_oc <= 0.600 * kV:
            self.vlevel = "LV"

    def check_model_bounds(self) -> None:
        # ref IEEE 1584-2018 s4.2 "Range of model"
        # Applying the IEEE 1584-2018 model outside these ranges _WILL_ give incorrect results.

        assert 0.208 * kV <= self.V_oc <= 15 * kV

        if self.V_oc <= 0.600 * kV:  # low voltage
            assert 6.35 * mm <= self.G <= 76.2 * mm
        else:  # high voltage
            assert 19.05 * mm <= self.G <= 254 * mm

        assert self.D >= 305 * mm

        assert self.width >= 4 * self.G  # Width of enclosure should be at least four times the busbar gap

        assert self.EC in ("VCB", "VCBB", "HCB", "HOA", "VOA",)

    def sanity_check(self) -> None:
        assert 0.0 * dimensionless <= self.CF <= 3.0 * dimensionless

    def calc_VarCf(self) -> None:
        # Arcing current variation correction factor.
        # The equation under Equation 2. (Equation 2a?)

        # Specifically need V_oc to be in kV for this formula
        _V_oc = self.V_oc.m_as(kV)

        k = table_2[self.EC]

        v = + k["k1"] * _V_oc ** 6 \
            + k["k2"] * _V_oc ** 5 \
            + k["k3"] * _V_oc ** 4 \
            + k["k4"] * _V_oc ** 3 \
            + k["k5"] * _V_oc ** 2 \
            + k["k6"] * _V_oc ** 1 \
            + k["k7"]

        self.VarCF = v * dimensionless

    def calc_CF(self) -> None:
        # Enclosure size correction factor.
        if self.EC in ("HOA", "VOA",):
            # Open air configurations HOA / VOA do not require a box size correction factor.
            self.CF = 1.00 * dimensionless
            return

        if (self.V_oc < 0.6 * kV) and (self.height < 508 * mm) and (self.width < 508 * mm) \
                and (self.depth <= 203.2 * mm):
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
        def eq_11_12(dim) -> Q_:
            _V_oc = self.V_oc.m_as(kV)
            _dim = dim.m_as(mm)

            y1 = _dim - 660.4
            y2 = (_V_oc + A) / B
            dim_1 = (660.4 + (y1 * y2)) / 25.4
            return dim_1 * inch

        # Table 6
        # The special case in this table appears to be height_1 for the VCBB configuration.

        # The actual conversion from mm to inch (according to `frink`) is:
        # mm -> inch = 5 / 127 (approx. 0.03937007874015748)
        #
        # However to match the printed text of IEEE 1584-2018, we must use the factor 0.03937 that is printed in the
        # standard.
        mm_to_in = 0.03937

        width_1 = None
        w = self.width
        if w < 508 * mm:
            if self.enclosure_type == "Typical":
                width_1 = 20 * inch
            elif self.enclosure_type == "Shallow":
                width_1 = mm_to_in * w.m_as(mm) * inch
        elif 508 * mm <= w <= 660.4 * mm:
            width_1 = mm_to_in * w.m_as(mm) * inch
        elif 660.4 * mm <= w <= 1244.6 * mm:
            width_1 = eq_11_12(w)
        elif 1244.6 * mm < w:
            width_1 = eq_11_12(1244.6 * mm)

        height_1 = None
        h = self.height
        if h < 508 * mm:
            if self.enclosure_type == "Typical":
                height_1 = 20 * inch
            elif self.enclosure_type == "Shallow":
                height_1 = mm_to_in * h.m_as(mm) * inch
        elif 508 * mm <= h <= 660.4 * mm:
            height_1 = mm_to_in * h.m_as(mm) * inch
        elif 660.4 * mm <= h <= 1244.6 * mm:
            if self.EC == "VCB":
                height_1 = mm_to_in * h.m_as(mm) * inch
            elif self.EC in ("VCBB", "HCB",):
                height_1 = eq_11_12(h)
        elif 1244.6 * mm < h:
            if self.EC == "VCB":
                height_1 = 49 * inch
            elif self.EC in ("VCBB", "HCB",):
                height_1 = eq_11_12(1244.6 * mm)

        # Equation 13
        EES = ((height_1 + width_1) / 2).to(inch)
        if self.enclosure_type == "Typical":
            assert EES >= 19.999 * inch  # "For typical box enclosures, the minimum value of EES is 20."
            # Relax the criteria from ">= 20" to ">= 19.999" to allow for the imprecise conversion factor of 1 mm =
            # 0.03937 inch that is printed in the text of IEEE 1584-2018.

        # save calculation details for unit test purposes
        self.height_1 = height_1
        self.width_1 = width_1
        self.EES = EES

        # Equation 14 / 15
        key = (self.enclosure_type, self.EC)
        b = table_7[key]
        _EES = EES.m_as(inch)
        x1 = + b["b1"] * _EES ** 2 \
             + b["b2"] * _EES \
             + b["b3"]

        if self.enclosure_type == "Typical":
            self.CF = x1 * dimensionless
        elif self.enclosure_type == "Shallow":
            self.CF = 1 / x1 * dimensionless

    def pretty_print(self) -> str:
        return f"""Cubicle parameters:
        
V_oc (nominal voltage)          = {self.V_oc:.3f~P}
D (working distance)            = {self.D:.1f~P}
G (busbar gap)                  = {self.G:.1f~P}
EC (electrode configuration)    = {self.EC}

Box dimensions:
    height  = {self.height:.1f~P}
    width   = {self.width:.1f~P}
    depth   = {self.depth:.1f~P}
    
Enclosure correction factor
    enclosure_type  = {self.enclosure_type}
    height_1        = {self.height_1:.1f~P}
    width_1         = {self.width_1:.1f~P}
    EES             = {self.EES:.1f~P}
    CF              = {self.CF:.3f~P}
"""
