# About

This is a Python library for doing arc flash calculations.

This includes:

* AC arc flash calculations to IEEE 1584 (for 3-phase AC systems, 208 V - 15,000 V)

Future planned efforts will include:

* AC arc flash calculations using the Lee method, for 3-phase AC systems above 15,000 V.
* DC arc flash calculations using the Doan and Ammerman methods

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

2. The `ieee_1584` module includes a number of additional test cases which were calculated from the "official" IEEE
   1584-2018 calculator spreadsheet, available at link [1]. These results are verified to 2 decimal places, the
   precision shown by the spreadsheet.

3. As far as possible, I have written the calculator code so that it obviously corresponds to the way the formulas are
   set out in the printed documents (standards, papers, etc.) It should (hopefully) be obvious from visual inspection
   that the formulas are correct.

4. Basic checks are included to help check if calculation parameters are within applicable bounds.

Note that

# Unit conventions

* All distances are in units of mm.
* All currents are in units of kA.
* All voltages are in units of kV.
* All incident energies are in J/cm², except where they are specifically labelled as cal/cm².

Note: My personal preference is normally to either a) use a calculator system that automatically tracks/converts units,
or b) to use SI base units (metres, amps, volts) in calculations. Those are usually the best way to avoid unit\
conversion traps.

However, all the formulas in IEEE 1584 are in terms of mm, kA, and kV, so I have maintained that convention here.

# License

This software is released under the MIT License.

# Disclaimer

Users of the software should note the disclaimer included in the MIT License.

In short - if you don't know what you are doing with this software - consult with an electrical engineer who does.