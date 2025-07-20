# Script to investigate anomalous calculation results.
# See https://github.com/rwl/arcflash/issues/1 .

from arcflash.ieee_1584.calculation import Calculation
from arcflash.ieee_1584.cubicle import Cubicle

from arcflash.ieee_1584.units import kA, kV, ms, mm, J_per_sq_cm

if __name__ == '__main__':

    for x in range(4160, 15010, 10):
        T_arc = 197 * ms
        I_bf = 15 * kA

        HV_cubicle = Cubicle(
            V_oc=x / 1000.0 * kV,
            EC="VCBB",
            G=104 * mm,
            D=914.4 * mm,
            height=1143 * mm,
            width=762 * mm,
            depth=508 * mm, )

        calc_max = Calculation(HV_cubicle, I_bf, "full")
        calc_max.calculate_I_arc()
        calc_max.calculate_E_AFB(T_arc)

        calc_min = Calculation(HV_cubicle, I_bf, "reduced")
        calc_min.calculate_I_arc()
        calc_min.calculate_E_AFB(T_arc)

        print(f"{HV_cubicle.V_oc.m_as(kV)}\t{I_bf.m_as(kA)}\t{calc_max.I_arc.m_as(kA)}\t{calc_max.E.m_as(J_per_sq_cm)}\t{calc_min.I_arc.m_as(kA)}\t{calc_min.E.m_as(J_per_sq_cm)}")
