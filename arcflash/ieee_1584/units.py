import pint

ureg = pint.UnitRegistry()
ureg.default_format = "~P"

Q_ = pint.Quantity

dimensionless = ureg.dimensionless

inch = ureg.inch
m = ureg.metre
mm = ureg.millimetre

sec = ureg.second
ms = ureg.millisecond

V = ureg.volt
kV = ureg.kilovolt

A = ureg.ampere
kA = ureg.kiloampere

J_per_sq_cm = ureg.joule / (ureg.centimetre ** 2)
cal_per_sq_cm = ureg.calorie / (ureg.centimetre ** 2)

deg = ureg.degree  # Useful when doing phasor arithmetic

ohm = ureg.ohm
