# Copyright 2022, Li-aung Yip - https://www.penwatch.net
# Licensed under the MIT License. Refer LICENSE.txt.

# Generates a number of test cases for input into the official IEEE 1584-2018 spreadsheets
#
# Columns required:
#  1. Configuration - an integer 1 - 5  representing the electrode configuration.
#         1 = VCB, 2 = VCBB, 3 = HCB, 4 = VOA, 5 = HOA.
#  2. Open circuit voltage, V_oc (kV)
#  3. Bolted fault current, I_bf (kA)
#  4. Electrode gap, G (mm)
#  5. Working distance, D (mm)
#  6. Arc duration, T (ms)
#  7. Box width, width (mm)
#  8. Box height, height (mm)
#  9. Box depth, a selection of either "Typical" or "Shallow(<=8 inch)".

import itertools
from math import prod

# Electrode configuration: pick one of five options.
EC = (
    "VCB",
    "VCBB",
    "HCB",
    "VOA",
    "HOA",
)

V_oc_LV = (
    0.208,  # Lower bound of validity for IEEE 1584 model
    0.400,  # New standard LV in Australia (230V single phase)
    # 0.415,  # Old standard LV in Australia (240V single phase)
    # 0.440,  # Common on mine sites with older equipment. (254V single phase)
    # 0.480,  # Common in the USA, example in IEEE annex D.2 is this voltage
    0.600,  # Upper bound of what IEEE 1584 considers LV
)

V_oc_HV = (
    0.601,  # Lower bound of what IEEE 1584 considers HV
    # 0.690,  # Common voltage for motors
    1.000,  # Common voltage for underground mining equipment, i.e. drill rigs, raise borers
    # 2.700,  # A special voltage for IEEE 1584 calculations
    # 3.300,  # Common HV motor voltage in Australia
    # 4.160,  # Common in the USA, example in IEEE 1584 Annex D.1 is this voltage
    # 6.600,  # Common HV motor voltage in Australia
    10.00,
    # 11.000,  # Common distribution voltage in Australia
    # 14.300,  # A special voltage for IEEE 1584 calculations
    15.000,  # Upper bound of validity for the IEEE 1584 model
)

# Range of validity for LV: 500 A to 106,000 A
I_bf_LV = (
    0.5,
    # 1.0,
    # 2.0,
    # 5.0,
    # 10.0,
    20.0,
    # 50.0,
    # 100.0,
    106.0,
)

# Range of validity for HV: 200 A to 65,000 A
I_bf_HV = (
    0.2,
    # 0.5,
    # 1.0,
    # 2.0,
    # 5.0,
    # 10.0,
    20.0,
    # 50.0,
    65.0,
)

# Range of validity for LV: 6.35 mm to 76.2 mm (0.25 in to 3 in)
# Special numbers are 13 mm, 25 mm, and 32 mm
# len = 6
G_LV = (
    6.35,
    # 13.0,
    25.0,
    # 32.0,
    # 50.0,
    76.2,
)

# Range of validity for HV: 19.05 mm to 254 mm (0.75 in to 10 in)
# Special numbers are 104 mm and 152 mm
G_HV = (
    19.05,
    # 25.0,
    # 50.0,
    104.0,
    152.0,
    # 200.0,
    254.0,
)

# Range of validity: over 305 mm (12 in)
# Special numbers are 18 in, 24 in, and 36 in
D = (
    305,
    457.2,
    609.6,
    914.4,
)

# Range of validity: No limit, but practical calculations limit T to 2 seconds.
# Note this is in milliseconds.
# T = (
#     # 0.01,
#     # 0.02,
#     # 0.05,
#     0.10,
#     # 0.20,
#     # 0.50,
#     1.00,
#     # 2.00,
#     # 5.00,
#     10.00,
# )

T = (
    10,
    100,
    1000,
)

# Enclosure height/width: Max 49 inches - dimensions over 49 in are treated as 49 in.
# Special numbers are 508 mm (20 in), 660.4 mm (26 in), 1244.6 mm (49 in)
width = (
    200.0,
    # 508,
    600.0,
    # 660.4,
    # 750.0,
    1000.0,
    # 1244.6,
    1500.0
)

height = width

# Enclosure depths
# If an LV enclosure is less than 203.2 mm (8 in) deep, it __might__ be treated as shallow.
depth = (
    100,
    # 203.2,
    500,
    # 1000,
)

# Generate all possible combinations of the above

LV_scenarios_iter = itertools.product(EC, V_oc_LV, I_bf_LV, G_LV, D, T, width, height, depth)
HV_scenarios_iter = itertools.product(EC, V_oc_HV, I_bf_HV, G_HV, D, T, width, height, depth)
scenarios_iter = itertools.chain(LV_scenarios_iter, HV_scenarios_iter)

# Count number of possible scenarios

no_of_LV_scenarios = prod([len(x) for x in (EC, V_oc_LV, I_bf_LV, G_LV, D, T, width, height, depth,)])
no_of_HV_scenarios = prod([len(x) for x in (EC, V_oc_HV, I_bf_HV, G_HV, D, T, width, height, depth,)])
no_of_scenarios = no_of_LV_scenarios + no_of_HV_scenarios
