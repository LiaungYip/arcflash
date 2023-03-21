from ieee_1584.calculation import Calculation
from ieee_1584.cubicle import Cubicle

from ieee_1584.units import kA, kV, ms, mm, inch, dimensionless, J_per_sq_cm

if __name__ == '__main__':
    # IEEE 1584-2018 "D.1 Sample arc-flash incident energy calculation for a medium-voltage system"
    print("Medium voltage example")
    I_bf = 15.0 * kA
    cubicle = Cubicle(
        V_oc=4.16 * kV,
        EC="VCB",
        G=104 * mm,
        D=914.4 * mm,
        height=1143 * mm,
        width=762 * mm,
        depth=508 * mm, )
    calc = Calculation(cubicle, I_bf)
    calc.calculate_I_arc()
    # Pass the values of calc.I_arc_max and calc.I_arc_min out to external software to determine clearing times T
    T_arc_max = 197 * ms
    T_arc_min = 223 * ms
    calc.calculate_E_AFB(T_arc_max, T_arc_min)
    print(cubicle.pretty_print())
    print(calc.pretty_print())

    if calc.E_max > calc.E_min:
        print("The maximum arcing current case was highest energy.")
    else:
        print("The minimum arcing current case was highest energy.")

    # IEEE 1584-2018 "D.2 Sample arc-flash incident energy calculation for a low-voltage system"
    print("Low voltage example")
    I_bf = 45.0 * kA
    cubicle = Cubicle(
        V_oc=0.48 * kV,
        EC="VCB",
        G=32 * mm,
        D=609.6 * mm,
        height=610 * mm,
        width=610 * mm,
        depth=254 * mm, )
    calc = Calculation(cubicle, I_bf)
    calc.calculate_I_arc()
    # Pass the values of calc.I_arc_max and calc.I_arc_min out to external software to determine clearing times T
    T_arc_max = 61.3 * ms
    T_arc_min = 319 * ms
    calc.calculate_E_AFB(T_arc_max, T_arc_min)
    print(cubicle.pretty_print())
    print(calc.pretty_print())
