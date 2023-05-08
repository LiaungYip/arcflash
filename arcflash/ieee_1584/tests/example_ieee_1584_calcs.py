from arcflash.ieee_1584.calculation import Calculation
from arcflash.ieee_1584.cubicle import Cubicle

from arcflash.ieee_1584.units import kA, kV, ms, mm

if __name__ == '__main__':
    # IEEE 1584-2018 "D.1 Sample arc-flash incident energy calculation for a medium-voltage system"
    print("Medium voltage example")
    HV_I_bf = 15.0 * kA
    HV_cubicle = Cubicle(
        V_oc=4.16 * kV,
        EC="VCB",
        G=104 * mm,
        D=914.4 * mm,
        height=1143 * mm,
        width=762 * mm,
        depth=508 * mm, )

    HV_calc_max = Calculation(HV_cubicle, HV_I_bf, "full")
    HV_calc_max.calculate_I_arc()

    HV_calc_min = Calculation(HV_cubicle, HV_I_bf, "reduced")
    HV_calc_min.calculate_I_arc()

    # Pass the values of calc.I_arc_max and calc.I_arc_min out to external software to determine clearing times T
    HV_T_arc_max = 197 * ms
    HV_T_arc_min = 223 * ms

    HV_calc_max.calculate_E_AFB(HV_T_arc_max)
    HV_calc_min.calculate_E_AFB(HV_T_arc_min)

    print(HV_cubicle.pretty_print())
    print(HV_calc_max.pretty_print())
    print(HV_calc_min.pretty_print())

    if HV_calc_max.E > HV_calc_min.E:
        print("The maximum arcing current case was highest energy.")
    else:
        print("The minimum arcing current case was highest energy.")

    # IEEE 1584-2018 "D.2 Sample arc-flash incident energy calculation for a low-voltage system"
    print("Low voltage example")
    LV_I_bf = 45.0 * kA
    LV_cubicle = Cubicle(
        V_oc=0.48 * kV,
        EC="VCB",
        G=32 * mm,
        D=609.6 * mm,
        height=610 * mm,
        width=610 * mm,
        depth=254 * mm, )

    LV_calc_max = Calculation(LV_cubicle, LV_I_bf, "full")
    LV_calc_max.calculate_I_arc()

    LV_calc_min = Calculation(LV_cubicle, LV_I_bf, "reduced")
    LV_calc_min.calculate_I_arc()

    # Pass the values of calc.I_arc_max and calc.I_arc_min out to external software to determine clearing times T
    LV_T_arc_max = 61.3 * ms
    LV_T_arc_min = 319 * ms

    LV_calc_max.calculate_E_AFB(LV_T_arc_max)
    LV_calc_min.calculate_E_AFB(LV_T_arc_min)

    print(LV_cubicle.pretty_print())
    print(LV_calc_max.pretty_print())
    print(LV_calc_min.pretty_print())

    if LV_calc_max.E > LV_calc_min.E:
        print("The maximum arcing current case was highest energy.")
    else:
        print("The minimum arcing current case was highest energy.")
