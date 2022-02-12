# Copyright 2022, Li-aung Yip - https://www.penwatch.net
# Licensed under the MIT License. Refer LICENSE.txt.

from math import log10, sqrt

from ieee_1584.cubicle import Cubicle
from ieee_1584.tables import table_1, table_3, table_4, table_5


def I_arc_intermediate(c: Cubicle, V_oc: float, I_bf: float):
    # Equation 1
    assert V_oc in (0.6, 2.7, 14.3,)

    k = table_1[(c.EC, V_oc,)]

    x1 = + k["k1"] \
         + k["k2"] * log10(I_bf) \
         + k["k3"] * log10(c.G)

    x2 = + k["k4"] * I_bf ** 6 \
         + k["k5"] * I_bf ** 5 \
         + k["k6"] * I_bf ** 4 \
         + k["k7"] * I_bf ** 3 \
         + k["k8"] * I_bf ** 2 \
         + k["k9"] * I_bf ** 1 \
         + k["k10"]

    I_a = (10 ** x1) * x2

    return I_a


def I_arc_min(c: Cubicle, I_arc: float):
    # Equation 2
    return I_arc * (1 - 0.5 * c.VarCF)


def E_AFB_intermediate(c: Cubicle, V_oc: float, I_arc: float, I_bf: float, T: float, I_arc_600: float = None):
    # Note that equations (3, 4, 5, 6) for incident energy "E", and (7, 8, 9, 10) for arc flash boundary "AFB", are
    # closely related.
    #
    # In fact, Eq 3 is simply an algebraic rearrangement of Eq 7.
    #
    #   * "E" is the energy for a fixed distance "D".
    #   * "AFB" is the distance for a fixed energy 1.2 cal/cm².
    #
    # Since both "E" and "AFB" are calculated using the same variables, it makes sense to calculate both at the same
    # time.
    #
    # Note the funny number "50/12.552" in Eq 3/4/5/6 turns into the magic number 20 in Eq 7/8/9/10.
    # 1.2 cal/cm² × 4.184 J/cal = 5.0208 J/cm²
    # 50 / 12.552 * 5.0208 = 20 (exact)
    #
    # Also note that "k12" has the same role as the "distance exponent, x" did in IEEE 1584-2002.
    # That is, k12 determines the falloff of energy with distance.

    assert (V_oc <= 0.6) or (V_oc in (0.6, 2.7, 14.3,))

    if V_oc <= 0.6:
        k = table_3[c.EC]
    elif V_oc == 2.7:
        k = table_4[c.EC]
    elif V_oc == 14.3:
        k = table_5[c.EC]
    else:
        k = None

    x1 = 12.552 / 50 * T

    x2 = k["k1"] + k["k2"] * log10(c.G)

    if I_arc_600 is None:  # HV case. Eqs 3, 4, 5
        x3_num = k["k3"] * I_arc
    else:  # LV case. Eq 6.
        x3_num = k["k3"] * I_arc_600

    x3_den = + k["k4"] * I_bf ** 7 \
             + k["k5"] * I_bf ** 6 \
             + k["k6"] * I_bf ** 5 \
             + k["k7"] * I_bf ** 4 \
             + k["k8"] * I_bf ** 3 \
             + k["k9"] * I_bf ** 2 \
             + k["k10"] * I_bf

    x3 = x3_num / x3_den

    x4 = + k["k11"] * log10(I_bf) \
         + k["k13"] * log10(I_arc) \
         + log10(1 / c.CF)

    x5 = k["k12"] * log10(c.D)

    # Equations 3, 4, 5, 6
    E = x1 * 10 ** (x2 + x3 + x4 + x5)

    # Equations 7, 8, 9, 10
    x6_num = x2 + x3 + x4 - log10(20 / T)
    x6_den = - k["k12"]  # note -ve sign
    x6 = x6_num / x6_den
    AFB = 10 ** x6

    assert E >= 0
    assert AFB >= 0

    return E, AFB


def interpolate(c: Cubicle, x_600, x_2700, x_14300):
    V_oc = c.V_oc

    # Eq 16, Eq 19, Eq 22
    x1 = (((x_2700 - x_600) / 2.1) * (V_oc - 2.7)) + x_2700
    # Eq 17, Eq 20, Eq 23
    x2 = (((x_14300 - x_2700) / 11.6) * (V_oc - 14.3)) + x_14300
    # Eq 18, Eq 21, Eq 24
    x3 = ((x1 * (2.7 - V_oc)) / 2.1) + ((x2 * (V_oc - 0.6)) / 2.1)

    if 0.600 < V_oc <= 2.7:
        return x3
    elif V_oc > 2.7:
        return x2


def I_arc_final_LV(c: Cubicle, I_arc_600, I_bf):
    # Equation 25
    V_oc = c.V_oc
    x1 = (0.6 / V_oc) ** 2
    x2 = 1 / (I_arc_600 ** 2)
    x3 = (0.6 ** 2 - V_oc ** 2) / (0.6 ** 2 * I_bf ** 2)
    x4 = sqrt(x1 * (x2 - x3))
    return 1 / x4
