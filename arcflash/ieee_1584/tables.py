# Copyright 2022, Li-aung Yip - https://www.penwatch.net
# Licensed under the MIT License. Refer LICENSE.txt.
#
# The "raw table texts" below have been copy-pasted out of IEEE 1584-2018.
# The main changes made are:
#   * Replace the unicode minus sign ("−", U+2212) with the normal ASCII dash character,
#   * Insert commas to separate values.
#   * Change all voltages from V to kV.

import csv

table_1_raw = """E.C., Voc, k1, k2, k3, k4, k5, k6, k7, k8, k9, k10
VCB, 0.6, -0.04287, 1.035, -0.083, 0, 0, -4.783E-09, 1.962E-06, -0.000229, 0.003141, 1.092
VCB, 2.7, 0.0065, 1.001, -0.024, -1.557E-12, 4.556E-10, -4.186E-08, 8.346E-07, 5.482E-05, -0.003191, 0.9729
VCB, 14.3, 0.005795, 1.015, -0.011, -1.557E-12, 4.556E-10, -4.186E-08, 8.346E-07, 5.482E-05, -0.003191, 0.9729
VCBB, 0.6, -0.017432, 0.98, -0.05, 0, 0, -5.767E-09, 2.524E-06, -0.00034, 0.01187, 1.013
VCBB, 2.7, 0.002823, 0.995, -0.0125, 0, -9.204E-11, 2.901E-08, -3.262E-06, 0.0001569, -0.004003, 0.9825
VCBB, 14.3, 0.014827, 1.01, -0.01, 0, -9.204E-11, 2.901E-08, -3.262E-06, 0.0001569, -0.004003, 0.9825
HCB, 0.6, 0.054922, 0.988, -0.11, 0, 0, -5.382E-09, 2.316E-06, -0.000302, 0.0091, 0.9725
HCB, 2.7, 0.001011, 1.003, -0.0249, 0, 0, 4.859E-10, -1.814E-07, -9.128E-06, -0.0007, 0.9881
HCB, 14.3, 0.008693, 0.999, -0.02, 0, -5.043E-11, 2.233E-08, -3.046E-06, 0.000116, -0.001145, 0.9839
VOA, 0.6, 0.043785, 1.04, -0.18, 0, 0, -4.783E-09, 1.962E-06, -0.000229, 0.003141, 1.092
VOA, 2.7, -0.02395, 1.006, -0.0188, -1.557E-12, 4.556E-10, -4.186E-08, 8.346E-07, 5.482E-05, -0.003191, 0.9729
VOA, 14.3, 0.005371, 1.0102, -0.029, -1.557E-12, 4.556E-10, -4.186E-08, 8.346E-07, 5.482E-05, -0.003191, 0.9729
HOA, 0.6, 0.111147, 1.008, -0.24, 0, 0, -3.895E-09, 1.641E-06, -0.000197, 0.002615, 1.1
HOA, 2.7, 0.000435, 1.006, -0.038, 0, 0, 7.859E-10, -1.914E-07, -9.128E-06, -0.0007, 0.9981
HOA, 14.3, 0.000904, 0.999, -0.02, 0, 0, 7.859E-10, -1.914E-07, -9.128E-06, -0.0007, 0.9981"""

table_2_raw = """E.C., k1, k2, k3, k4, k5, k6, k7
VCB, 0, -0.0000014269, 0.000083137, -0.0019382, 0.022366, -0.12645, 0.30226
VCBB, 1.138e-06, -6.0287e-05, 0.0012758, -0.013778, 0.080217, -0.24066, 0.33524
HCB, 0, -3.097e-06, 0.00016405, -0.0033609, 0.033308, -0.16182, 0.34627
VOA, 9.5606E-07, -5.1543E-05, 0.0011161, -0.01242, 0.075125, -0.23584, 0.33696
HOA, 0, -3.1555e-06, 0.0001682, -0.0034607, 0.034124, -0.1599, 0.34629"""

table_3_raw = """600 V, k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12, k13
VCB, 0.753364, 0.566, 1.752636, 0, 0, -4.783E-09, 0.000001962, -0.000229, 0.003141, 1.092, 0, -1.598, 0.957
VCBB, 3.068459, 0.26, -0.098107, 0, 0, -5.767E-09, 0.000002524, -0.00034, 0.01187, 1.013, -0.06, -1.809, 1.19
HCB, 4.073745, 0.344, -0.370259, 0, 0, -5.382E-09, 0.000002316, -0.000302, 0.0091, 0.9725, 0, -2.03, 1.036
VOA, 0.679294, 0.746, 1.222636, 0, 0, -4.783E-09, 0.000001962, -0.000229, 0.003141, 1.092, 0, -1.598, 0.997
HOA, 3.470417, 0.465, -0.261863, 0, 0, -3.895E-09, 0.000001641, -0.000197, 0.002615, 1.1, 0, -1.99, 1.04"""

table_4_raw = """2700 V, k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12, k13
VCB, 2.40021, 0.165, 0.354202, -1.557E-12, 4.556E-10, -4.186E-08, 8.346E-07, 5.482E-05, -0.003191, 0.9729, 0, -1.569, 0.9778
VCBB, 3.870592, 0.185, -0.736618, 0, -9.204E-11, 2.901E-08, -3.262E-06, 0.0001569, -0.004003, 0.9825, 0, -1.742, 1.09
HCB, 3.486391, 0.177, -0.193101, 0, 0, 4.859E-10, -1.814E-07, -9.128E-06, -0.0007, 0.9881, 0.027, -1.723, 1.055
VOA, 3.880724, 0.105, -1.906033, -1.557E-12, 4.556E-10, -4.186E-08, 8.346E-07, 5.482E-05, -0.003191, 0.9729, 0, -1.515, 1.115
HOA, 3.616266, 0.149, -0.761561, 0, 0, 7.859E-10, -1.914E-07, -9.128E-06, -0.0007, 0.9981, 0, -1.639, 1.078"""

table_5_raw = """14 300 V, k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12, k13
VCB, 3.825917, 0.11, -0.999749, -1.557E-12, 4.556E-10, -4.186E-08, 8.346E-07, 5.482E-05, -0.003191, 0.9729, 0, -1.568, 0.99
VCBB, 3.644309, 0.215, -0.585522, 0, -9.204E-11, 2.901E-08, -3.262E-06, 0.0001569, -0.004003, 0.9825, 0, -1.677, 1.06
HCB, 3.044516, 0.125, 0.245106, 0, -5.043E-11, 2.233E-08, -3.046E-06, 0.000116, -0.001145, 0.9839, 0, -1.655, 1.084
VOA, 3.405454, 0.12, -0.93245, -1.557E-12, 4.556E-10, -4.186E-08, 8.346E-07, 5.482E-05, -0.003191, 0.9729, 0, -1.534, 0.979
HOA, 2.04049, 0.177, 1.005092, 0, 0, 7.859E-10, -1.914E-07, -9.128E-06, -0.0007, 0.9981, -0.05, -1.633, 1.151"""

table_7_raw = """Box type, E.C., b1, b2, b3
Typical, VCB, -0.000302, 0.03441, 0.4325
Typical, VCBB, -0.0002976, 0.032, 0.479
Typical, HCB, -0.0001923, 0.01935, 0.6899
Shallow, VCB, 0.002222, -0.02556, 0.6222
Shallow, VCBB, -0.002778, 0.1194, -0.2778
Shallow, HCB, -0.0005556, 0.03722, 0.4778"""

# This table typed manually.
# This is a combination of table 8 and table 10.
# Headers and equipment class names shortened for brevity.
# G is typical busbar gap in mm.
# bh, bw, and bd are enclosure (box) height, width, and depth in mm.
# D is working distance in mm.
#
# LV equipment with "shallow" depth <= 8 inches - set to 100 mm.
# LV equipment with "deep" depth > 8 inches - set to 250 mm.
# Precise depths don't matter, only whether the enclosure is "shallow" or "deep".
table_8_10_raw ="""Equipment class, G, bh, bw, bd, D
15kV Switchgear,                152.0, 1143.0, 762.0, 762.0, 914.4
15kV MCC, 152,                  914.4,  914.4, 914.4, 914.4, 914.4
5kV Switchgear,                 104.0,  914.4, 914.4, 914.4, 914.4
5kV Switchgear (2),             104.0, 1143.0, 762.0, 762.0, 914.4
5kV MCC,                        104.0,  660.4, 660.4, 660.4, 914.4
LV Switchgear,                   32.0,  508.0, 508.0, 508.0, 609.6
LV MCC (Shallow),                25.0,  355.6, 304.8, 100.0, 457.2
LV Panelboard (Shallow),         25.0,  355.6, 304.8, 100.0, 457.2
LV MCC,                          25.0,  355.6, 304.8, 250.0, 457.2
LV Panelboard,                   25.0,  355.6, 304.8, 250.0, 457.2
Cable Junction Box (Shallow),    13.0,  355.6, 304.8, 100.0, 457.2
Cable Junction Box,              13.0,  355.6, 304.8, 250.0, 457.2
"""


def convert_to_table(raw, table_no):
    assert "−" not in raw  # check that all Unicode minus signs (U+2212) have been removed

    lines = raw.splitlines()
    c = csv.reader(lines, skipinitialspace=True)

    header_row = c.__next__()

    if table_no in (2, 3, 4, 5, 8):
        no_of_key_fields = 1
    elif table_no in (1, 7):
        no_of_key_fields = 2
    else:
        raise ValueError

    val_names = header_row[no_of_key_fields:]

    table = dict()
    for row in c:
        if table_no in (2, 3, 4, 5, 8):
            key = row[0]
        elif table_no == 1:
            key = (row[0], float(row[1]),)
        elif table_no == 7:
            key = (row[0], row[1],)
        else:
            key = None  # Should never happen

        raw_vals = row[no_of_key_fields:]
        float_vals = [float(v) for v in raw_vals]
        vals = dict(zip(val_names, float_vals))

        table[key] = vals

    return table


table_1 = convert_to_table(table_1_raw, 1)
table_2 = convert_to_table(table_2_raw, 2)
table_3 = convert_to_table(table_3_raw, 3)
table_4 = convert_to_table(table_4_raw, 4)
table_5 = convert_to_table(table_5_raw, 5)
table_7 = convert_to_table(table_7_raw, 7)
table_8_10 = convert_to_table(table_8_10_raw, 8)
