# Copyright 2022, Li-aung Yip - https://www.penwatch.net
# Licensed under the MIT License. Refer LICENSE.txt.

# This compares the results from the official IEEE spreadsheet(s) to the results of the `ieee_1584` module.
#
# Some pre-generated test data is shipped with this code - see `ieee_1584_spreadsheet_results.csv`.
#
# Should you want to generate your own test cases, you might try editing `test_case_generator.py` and then running
# excel_test.py.

import csv

from ieee_1584.calculation import Calculation
from ieee_1584.cubicle import Cubicle

infile = "ieee_1584_spreadsheet_results.csv"
outfile = "comparison.csv"

with open(infile) as fh_in:
    with open(outfile, mode="w", newline="") as fh_out:
        reader = csv.DictReader(fh_in)
        writer = csv.writer(fh_out)

        header = (
            "V_oc", "EC", "G", "D", "height", "width", "depth", "I_bf", "T",
            "I_arc_max(ss)", "I_arc_max(py)", "I_arc_max(%diff)",
            "E_joules_max(ss)", "E_joules_max(py)", "E_joules_max(%diff)",
            "AFB_max(ss)", "AFB_max(py)", "AFB_max(%diff)",
            "I_arc_min(ss)", "I_arc_min(py)", "I_arc_min(%diff)",
            "E_joules_min(ss)", "E_joules_min(py)", "E_joules_min(%diff)",
            "AFB_min(ss)", "AFB_min(py)", "AFB_min(%diff)",
        )

        writer.writerow(header)

        for r in reader:
            # Convert numerical columns from strings to floats
            for k, v in r.items():
                if k != "EC":
                    r[k] = float(v)

            # Discard cases which are invalid due to busbar gap vs. enclosure width
            if r["width"] < 4 * r["G"]:
                continue

            # Do calculations
            cubicle_params = (r["V_oc"], r["EC"], r["G"], r["D"], r["height"], r["width"], r["depth"],)
            cubicle = Cubicle(*cubicle_params)
            calc = Calculation(cubicle, r["I_bf"])
            calc.calculate_I_arc()
            calc.calculate_E_AFB(r["T"], r["T"])

            # Check our calcs to official calcs
            ss_results = (
                r["I_arc_max"], r["E_joules_max"], r["AFB_max"], r["I_arc_min"], r["E_joules_min"], r["AFB_min"],)
            py_results = (calc.I_arc_max, calc.E_max, calc.AFB_max, calc.I_arc_min, calc.E_min, calc.AFB_min,)

            results = list()
            for ss, py in zip(ss_results, py_results):
                results.append(f"{ss:.5g}")
                results.append(f"{py:.5g}")
                results.append(f"{abs(1 - (ss / py)):.1%}")

            out_row = cubicle_params + (r["I_bf"], r["T"],) + tuple(results)
            writer.writerow(out_row)
