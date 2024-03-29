# Copyright 2022, Li-aung Yip - https://www.penwatch.net
# Licensed under the MIT License. Refer LICENSE.txt.

import logging
from math import log10, sqrt

from arcflash.ieee_1584.cubicle import Cubicle
from arcflash.ieee_1584.tables import table_1, table_3, table_4, table_5
from arcflash.ieee_1584.units import Q_, kA, kV, ms, mm, dimensionless, J_per_sq_cm


def I_arc_intermediate(c: Cubicle, V_oc: Q_, I_bf: Q_) -> Q_:
    assert V_oc.check('[electric_potential]')
    assert I_bf.check('[current]')
    # Equation 1
    assert V_oc in (0.6 * kV, 2.7 * kV, 14.3 * kV,)

    _V_oc = V_oc.m_as(kV)
    _I_bf = I_bf.m_as(kA)
    _G = c.G.m_as(mm)

    k = table_1[(c.EC, _V_oc,)]

    x1 = + k["k1"] \
         + k["k2"] * log10(_I_bf) \
         + k["k3"] * log10(_G)

    x2 = + k["k4"] * _I_bf ** 6 \
         + k["k5"] * _I_bf ** 5 \
         + k["k6"] * _I_bf ** 4 \
         + k["k7"] * _I_bf ** 3 \
         + k["k8"] * _I_bf ** 2 \
         + k["k9"] * _I_bf ** 1 \
         + k["k10"]

    I_a = (10 ** x1) * x2

    return I_a * kA


def I_arc_min(c: Cubicle, I_arc: Q_) -> Q_:
    # Equation 2

    assert I_arc.check('[current]')
    _I_arc = I_arc.m_as(kA)
    _VarCF = c.VarCF.m_as(dimensionless)

    return _I_arc * (1 - 0.5 * _VarCF) * kA


def E_AFB_intermediate(c: Cubicle, V_oc: Q_, I_arc: Q_, I_bf: Q_, T: Q_, I_arc_600: Q_ = None) -> (Q_, Q_,):
    logging.warning(
        "Function E_AFB_intermediate() is deprecated. Use intermediate_E() and intermediate_AFB_from_E() instead.")
    E = intermediate_E(c, V_oc, I_arc, I_bf, T, I_arc_600)
    AFB = intermediate_AFB_from_E(c, V_oc, E)
    return E, AFB


def intermediate_E(c: Cubicle, V_oc: Q_, I_arc: Q_, I_bf: Q_, T: Q_, I_arc_600: Q_ = None) -> Q_:
    # Implements equations 3, 4, 5, 6 for "intermediate incident energy".

    assert V_oc.check('[electric_potential]')
    assert I_arc.check('[current]')
    assert I_bf.check('[current]')
    assert T.check('[time]')
    assert I_arc_600 is None or I_arc_600.check('[current]')

    _V_oc = V_oc.m_as(kV)
    _I_arc = I_arc.m_as(kA)
    _I_bf = I_bf.m_as(kA)
    _T = T.m_as(ms)
    if I_arc_600 is None:
        _I_arc_600 = None
    else:
        _I_arc_600 = I_arc_600.m_as(kA)
    _G = c.G.m_as(mm)
    _CF = c.CF.m_as(dimensionless)
    _D = c.D.m_as(mm)

    assert (V_oc <= 0.6 * kV) or (V_oc in (0.6 * kV, 2.7 * kV, 14.3 * kV,))

    if V_oc <= 0.6 * kV:
        k = table_3[c.EC]
    elif V_oc == 2.7 * kV:
        k = table_4[c.EC]
    elif V_oc == 14.3 * kV:
        k = table_5[c.EC]
    else:
        k = None

    x1 = 12.552 / 50 * _T

    x2 = k["k1"] + k["k2"] * log10(_G)

    if I_arc_600 is None:  # HV case. Eqs 3, 4, 5
        x3_num = k["k3"] * _I_arc
    else:  # LV case. Eq 6.
        x3_num = k["k3"] * _I_arc_600

    x3_den = + k["k4"] * _I_bf ** 7 \
             + k["k5"] * _I_bf ** 6 \
             + k["k6"] * _I_bf ** 5 \
             + k["k7"] * _I_bf ** 4 \
             + k["k8"] * _I_bf ** 3 \
             + k["k9"] * _I_bf ** 2 \
             + k["k10"] * _I_bf

    x3 = x3_num / x3_den

    x4 = + k["k11"] * log10(_I_bf) \
         + k["k13"] * log10(_I_arc) \
         + log10(1 / _CF)

    x5 = k["k12"] * log10(_D)

    # Equations 3, 4, 5, 6
    E = x1 * 10 ** (x2 + x3 + x4 + x5)

    assert E >= 0

    return E * J_per_sq_cm


def intermediate_AFB_from_E(c: Cubicle, V_oc: Q_, E: Q_) -> Q_:
    # Implements equations 7, 8, 9, 10, for "intermediate arc flash boundary", in a simpler way.
    #
    # Calculates the (intermediate) arc flash boundary, i.e. AFB_600, from the incident energy i.e. E_600 only.
    # Knowledge of T, G, I_arc, I_bf, and CF is not required, as it would be if using Eq's 7, 8, 9, 10 directly.
    # This is useful for multi-time-step calculations where there is no singular value of T, I_arc, or I_bf.
    #
    # Motivation:
    # ===========
    #
    # The IEEE 1584-2018 formulas for arc flash boundary (AFB), i.e. eq's 7, 8, 9, and 10, are pretty complicated.
    #
    # In particular, the equations for AFB requires knowledge of time T, busbar gap G, the currents I_arc and I_bf,
    # and size correction factor CF.
    #
    # This is a problem when doing multi-time-step arc flash calculations where the values of T, I_arc, and I_bf are
    # different for each time-step. What single value of I_arc would you plug into Eq 7, when I_arc is 10 kA for 100 ms,
    # then 5 kA for 900 ms, then 2 kA for 1,000 ms?
    #
    # Details:
    # ========
    #
    # Consider Eq 3 for the quantity E_600.
    #
    # First, we recognise that the relationship between incident energy E_600 (J/cm²) and distance D (mm) is simply
    # that __the energy E_600 falls off exponentially with distance D__. If we rearrange Eq 3 using exponent identities
    # we can simplify to:
    #
    #       E_600 = F * ( D ^ k12 )
    #
    # Where:
    #   * E_600 is the __intermediate__ arcing energy at V = 0.6 kV, with units of J/cm²,
    #   * F_600 is a (reasonably complicated) function of time T, busbar gap G, currents I_arc and I_bf, and size
    #     correction factor CF,
    #   * D is the distance (mm) from the fault to where E_600 has been measured.
    #   * k12 is a constant __"distance exponent"__ from Table 3, Table 4, or Table 5.
    #
    # We can calculate what F_600** would have been:
    #
    #       F_600 = E_600 / ( D ^ k12 )
    #
    # Once we know the value of F_600, we can calculate E_600' at any distance D' we like:
    #
    #       E_600' (at distance D') = F_600 * ( D' ^ k12 )
    #
    # Alternately, we can calculate the distance D' that will give a particular value of E_600'.
    #
    #       D' = (E_600' / F_600) ^ ( 1 / k12 )
    #
    # Finally note that the arc flash boundary, AFB_600, is simply the special case where E_600' is equal to exactly
    # 1.2 cal/cm². Noting that 1.2 cal/cm² * 4.184 J/cal = 5.0208 J/cm²,
    #
    #       AFB_600 = (5.0208 / F_600) ^ ( 1 / k12 )
    #
    # ** Sidenote: The physical meaning of the quantity "F_600" is that F_600 is, in some sense, the total amount of
    # energy released (i.e. Joules). (The distribution of energy is not isotropic, i.e. k12 != -2.00, so this
    # interpretation is not exact.)
    #
    # Sidenote 2: the funny number "50/12.552" in Eq 3/4/5/6 turns into the magic number 20 in Eq 7/8/9/10.
    # 1.2 cal/cm² × 4.184 J/cal = 5.0208 J/cm²
    # 50 / 12.552 * 5.0208 = 20 (exact)

    assert V_oc.check('[electric_potential]')
    assert E.check('[energy]/[area]')

    _V_oc = V_oc.m_as(kV)
    _E = E.m_as(J_per_sq_cm)
    _D = c.D.m_as(mm)

    assert (V_oc <= 0.6 * kV) or (V_oc in (0.6 * kV, 2.7 * kV, 14.3 * kV,))

    if V_oc <= 0.6 * kV:
        k = table_3[c.EC]
    elif V_oc == 2.7 * kV:
        k = table_4[c.EC]
    elif V_oc == 14.3 * kV:
        k = table_5[c.EC]
    else:
        k = None

    # After all the explanation, calculation of the (intermediate) AFB is simply 2 lines.
    F = _E / (_D ** k["k12"])
    AFB = (5.0208 / F) ** (1 / k["k12"])
    assert AFB >= 0
    return AFB * mm


def interpolate(c: Cubicle, x_600: Q_, x_2700: Q_, x_14300: Q_) -> Q_:
    _V_oc = c.V_oc.m_as(kV)

    # Eq 16, Eq 19, Eq 22
    x1 = (((x_2700 - x_600) / 2.1) * (_V_oc - 2.7)) + x_2700
    # Eq 17, Eq 20, Eq 23
    x2 = (((x_14300 - x_2700) / 11.6) * (_V_oc - 14.3)) + x_14300
    # Eq 18, Eq 21, Eq 24
    x3 = ((x1 * (2.7 - _V_oc)) / 2.1) + ((x2 * (_V_oc - 0.6)) / 2.1)

    if 0.600 < _V_oc <= 2.7:
        return x3
    elif _V_oc > 2.7:
        return x2


def I_arc_final_LV(c: Cubicle, I_arc_600: Q_, I_bf: Q_) -> Q_:
    # Equation 25

    assert I_arc_600.check('[current]')
    assert I_bf.check('[current]')

    _V_oc = c.V_oc.m_as(kV)
    _I_arc_600 = I_arc_600.m_as(kA)
    _I_bf = I_bf.m_as(kA)

    x1 = (0.6 / _V_oc) ** 2
    x2 = 1 / (_I_arc_600 ** 2)
    x3 = (0.6 ** 2 - _V_oc ** 2) / (0.6 ** 2 * _I_bf ** 2)
    x4 = sqrt(x1 * (x2 - x3))
    return 1 / x4 * kA
