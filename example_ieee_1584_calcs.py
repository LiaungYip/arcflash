from ieee_1584.calculation import Calculation
from ieee_1584.cubicle import Cubicle

if __name__ == '__main__':
    # IEEE 1584-2018 "D.1 Sample arc-flash incident energy calculation for a medium-voltage system"
    print("Medium voltage example")
    I_bf = 15.0
    cubicle = Cubicle(4.16, "VCB", 104, 914.4, 1143, 762, 508)
    calc = Calculation(cubicle, I_bf)
    calc.calculate_I_arc()
    # Pass the values of calc.I_arc_max and calc.I_arc_min out to external software to determine clearing times T
    T_arc_max = 197
    T_arc_min = 223
    calc.calculate_E_AFB(T_arc_max, T_arc_min)
    print(cubicle.pretty_print())
    print(calc.pretty_print())

    if calc.E_max > calc.E_min:
        print("The maximum arcing current case was highest energy.")
    else:
        print("The minimum arcing current case was highest energy.")

    # IEEE 1584-2018 "D.2 Sample arc-flash incident energy calculation for a low-voltage system"
    print("Low voltage example")
    I_bf = 45.0
    cubicle = Cubicle(V_oc=0.48, EC="VCB", G=32, D=609.6, height=610, width=610, depth=254)
    calc = Calculation(cubicle, I_bf)
    calc.calculate_I_arc()
    # Pass the values of calc.I_arc_max and calc.I_arc_min out to external software to determine clearing times T
    T_arc_max = 61.3
    T_arc_min = 319
    calc.calculate_E_AFB(T_arc_max, T_arc_min)
    print(cubicle.pretty_print())
    print(calc.pretty_print())
