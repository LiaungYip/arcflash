# About

This is a Python library for doing arc flash calculations.

This includes:

* AC arc flash calculations to IEEE 1584 (for 3-phase AC systems, 208 V - 15,000 V)

Future planned efforts will include:

* AC arc flash calculations using the Lee method, for 3-phase AC systems above 15,000 V.
* DC arc flash calculations using the Doan and Ammerman methods

Not currently included:

* Any user interface for running calculations
* Any integrations with power system studies software

# Why did I write this?

There are many arc flash calculator software packages and spreadsheets in the wild.

The spreadsheets are done with Excel formulas or VBA code, both of which are difficult to write, maintain, and verify.
Spreadsheets also have the problem that they are hard to protect from inadvertent changes over time, which can lead to
errors in calculations.

The software packages are usually closed-source commercial software, whose workings can't be independently verified.

Therefore, my contribution to this field is an arc flash calculator library whose workings are **easy to understand**
and **easy to verify**.

# Verification

The engineers using this library must be **confident** that it will produce correct results.

1. The `ieee_1584` module includes unit tests which replicate the example calculations from Annex D1 and D2 of IEEE
   1584, checking that all intermediate calculations, and final calculated results, **exactly** match the examples in
   the standard. These calculations are verified to as many significant figures as are shown in the standard.

2. As far as possible, I have written the calculator code so that it obviously corresponds to the way the formulas are
   set out in the printed documents (standards, papers, etc.) It should (hopefully) be obvious from visual inspection
   that the formulas are correct.

3. Basic checks are included to help check if calculation parameters are within applicable bounds.

4. The `ieee_1584` module includes 144,000 "additional test cases" which were calculated from the "official" IEEE
   1584-2018 calculator spreadsheets, available at link [1].

   The 144,000 cases involve every combination of a number of possibilities for each input variable.

   The operation of the `ieee_1584` python code for each of the 144,000 cases is then verified against the official
   spreadsheet results to within (at most) 0.1%.

    * Note 2022-02-14:

      There are currently some errors in the spreadsheet `IEEE ExcelCalculator_V 2.6.6_M_mm_08_29_2019.xlsm`. I have
      attempted to contact the spreadsheet author(s) about this. Details are in the `additional_test_cases` folder.

# Units

The first version of this package (2022-02-22) required data to be entered in specific units of mm, kA, kV and J/cm². This left users vulnerable to unit conversion mishaps (e.g. entering times in sec instead of ms), which would result in severe calculation errors.

As of the second major version of this package (2023-03-21) the code has been converted to use [pint](https://pint.readthedocs.io/en/stable/) for automatic unit tracking in calculations. This allows users to enter data in whatever unit they want (e.g. mm, metres, or inches) - the data will be automatically converted to the right unit.

A unit test has been added which uses the exact same data as the example from Annex D2 of the standard, but with different input units (e.g. 480 V instead of 0.48 kV, and 610000 micrometres instead of 610 mm) to ensure the unit conversion code works correctly.

Note that some formulas in IEEE 1584 use a factor of 1 mm = 0.03937 inch, which is a truncated value and thus introduces a small unit conversion error. I have chosen to match the printed text of IEEE 1584 exactly, rather than use the actual conversion factor of 5/127 (approx. 0.03937007874015748).

# License

This software is released under the MIT License.

# Disclaimer

Users of the software should note the disclaimer included in the MIT License.

In short - if you don't know what you are doing with this software - consult with an electrical engineer who does.

# References

[1] : https://ieee-dataport.org/open-access/arc-flash-ie-and-iarc-calculators