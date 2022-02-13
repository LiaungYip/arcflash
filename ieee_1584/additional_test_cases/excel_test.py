# Copyright 2022, Li-aung Yip - https://www.penwatch.net
# Licensed under the MIT License. Refer LICENSE.txt.

# This is a very quick and nasty script that drives the official IEEE 1584 calculation spreadsheet(s) in order to
# get the spreadsheets' calculation results for ~ 150,000 input scenarios.
#
# Requirements:
#  * Be running on Windows with Microsoft Excel installed
#  * pywin32 module
#  * Have copies of the IEEE 1584 calculator spreadsheets
#
# Note that (as of the time of writing) one of the calculation spreadsheets has incorrect formulas in it. See the
# "Error in IEEE 1584 spreadsheet" folder. I have attempted to contact the spreadsheet's authors about this.
#
# It helps to trim down the spreadsheet to remove all formula cells except the row we are using (row 12).
# This makes the process about 3x faster.
# You can unprotect the spreadsheets by editing the internal XML files (Google will be your friend.)

import csv
import os.path
import time

import win32com.client as win32com_client  # from pywin32

from test_case_generator import scenarios_iter, no_of_scenarios

# Place the spreadsheets in the same folder as this script
filename_spreadsheet_max = r"IEEE ExcelCalculator_V 2.6.6__mm_08_29_2019 - trimmed.xlsm"
# filename_spreadsheet_min = r"IEEE ExcelCalculator_V 2.6.6_M_mm_08_29_2019 - trimmed.xlsm"
filename_spreadsheet_min = r"IEEE ExcelCalculator_V 2.6.6_M_mm_08_29_2019 - trimmed corrected.xlsm"

cwd = os.getcwd()
path_spreadsheet_max = os.path.join(cwd, filename_spreadsheet_max)
path_spreadsheet_min = os.path.join(cwd, filename_spreadsheet_min)

assert os.path.exists(path_spreadsheet_max) and os.path.isfile(path_spreadsheet_max)
assert os.path.exists(path_spreadsheet_min) and os.path.isfile(path_spreadsheet_min)

# Output file
csv_out_file = "ieee_1584_spreadsheet_results.csv"


try:
    # Use this version for development (uses existing instance of Excel, generates/caches static bindings)
    # with win32com_client.gencache.EnsureDispatch("Excel.Application") as app:

    # Use this version for production (opens a new instance of Excel)
    app =  win32com_client.Dispatch("Excel.Application")
    # Open workbooks and acquire relevant cell ranges.
    # Note output cells are at different addresses on the max spreadsheet vs. the min spreadsheet

    wb_max = app.Workbooks.Open(path_spreadsheet_max)
    ws_max = wb_max.Sheets["Calculate Table"]
    input_cells_max = ws_max.Range("A12:H12,K12")  # 9 cells: EC, V_oc, I_bf, G, D, T, width, height, depth.
    output_cells_max = ws_max.Range("IK12,IO12,IP12")  # 3 cells: I_arc (kA), E (J/cm²), and Arc Flash Boundary (mm)

    wb_min = app.Workbooks.Open(path_spreadsheet_min)
    # original spreadsheet
    # ws_min = wb_min.Sheets["Calculate Table"]
    # input_cells_min = ws_min.Range("A12:H12,K12")  # 9 cells: EC, V_oc, I_bf, G, D, T, width, height, depth.
    # output_cells_min = ws_min.Range("IU12,IY12,IZ12")  # 3 cells: I_arc (kA), E (J/cm²), and Arc Flash Boundary (mm)
    # corrected spreadsheet
    ws_min = wb_min.Sheets["Calculate Table - Corrected"]
    input_cells_min = ws_min.Range("A11:H11,K11")  # 9 cells: EC, V_oc, I_bf, G, D, T, width, height, depth.
    output_cells_min = ws_min.Range("BT11,BX11,BY11")  # 3 cells: I_arc (kA), E (J/cm²), and Arc Flash Boundary (mm)

    # Put excel into speed mode
    # https://stackoverflow.com/questions/12391786/effect-of-screen-updating/12405808
    app.Visible = False
    app.ScreenUpdating = False
    app.EnableEvents = False

    EC_numbers = {
        "VCB": 1,
        "VCBB": 2,
        "HCB": 3,
        "VOA": 4,
        "HOA": 5,
    }

    # Open CSV file and write header row
    fh = open(csv_out_file, mode="w", newline="")
    w = csv.writer(fh, dialect="excel")
    header = ['EC', 'V_oc', 'I_bf', 'G', 'D', 'T', 'width', 'height', 'depth', 'I_arc_max', 'E_joules_max', 'AFB_max',
              'I_arc_min', 'E_joules_min', 'AFB_min']
    w.writerow(header)

    t_start = time.time()

    for n, scenario in enumerate(scenarios_iter):
        if n % 100 == 0 and n != 0:
            t_now = time.time()
            avg_time = (time.time() - t_start) / n  # sec
            time_left = (no_of_scenarios - n) * avg_time
            print(
                f"{n}/{no_of_scenarios} ({n / no_of_scenarios * 100:.1f}%), averaging {avg_time * 1000:.1f} ms/scenario, {time_left / 60:.0f} min remaining")

        # if n > 20:
        #     break

        # Unpack scenario values
        EC, V_oc, I_bf, G, D, T, width, height, depth = scenario

        # Translate electrode configuration to the numbers used by the spreadsheet, i.e. "VCB" -> 1
        EC_number = EC_numbers[EC]

        # Translate depth in mm to either "Shallow" or "Typical"
        if depth <= 203.2:
            depth_text = "Shallow(<=8 inch)"
        else:
            depth_text = "Typical"

        # Disable calculation while changing input data cells
        ws_max.EnableCalculation = False
        ws_min.EnableCalculation = False

        # Put new values into spreadsheet
        spreadsheet_input_values = (EC_number, V_oc, I_bf, G, D, T, width, height, depth_text,)

        for cell, val in zip(input_cells_max, spreadsheet_input_values):
            cell.Value = val

        for cell, val in zip(input_cells_min, spreadsheet_input_values):
            cell.Value = val

        # Trigger calculation
        ws_max.EnableCalculation = True
        ws_min.EnableCalculation = True

        # Get numbers out of spreadsheet
        I_arc_max, E_joules_max, AFB_max = [cell.Value for cell in output_cells_max.Cells]
        I_arc_min, E_joules_min, AFB_min = [cell.Value for cell in output_cells_min.Cells]

        # Format to 5 significant figures
        # (this didn't work very well)
        # results = tuple(f"{x:.5g}" for x in (I_arc_max, E_joules_max, AFB_max, I_arc_min, E_joules_min, AFB_min,))

        # Give me as much precision as Excel can give me

        results = (I_arc_max, E_joules_max, AFB_max, I_arc_min, E_joules_min, AFB_min,)

        csv_row = scenario + results
        w.writerow(csv_row)

    t_end = time.time()
    t_elapsed = t_end - t_start

    print(f"time: {t_elapsed} to process {n} scenarios. Averaged {t_elapsed / n * 1000:.3f} ms/scenario.")

    fh.close()

    # Undo speed mode
    app.Visible = True
    app.ScreenUpdating = True
    app.EnableEvents = True

finally:
    # Close Excel
    app.DisplayAlerts = False  # Suppress "Save changes to file?" dialogs.
    app.Quit()
