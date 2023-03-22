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

kV = ureg.kilovolt

kA = ureg.kiloampere

J_per_sq_cm = ureg.joule / (ureg.centimetre ** 2)
cal_per_sq_cm = ureg.calorie / (ureg.centimetre ** 2)

deg = ureg.degree  # Useful when doing phasor arithmetic
