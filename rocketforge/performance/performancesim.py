from dataclasses import dataclass

@dataclass
class Quantity():
    name: str = None
    value: float = None
    uom: str = None

class PerformanceSimInput:
    def __init__(self,
                 oxidizer=None,
                 fuel=None,
                 chamber_pressure=None,
                 chamber_pressure_uom=None,
                 mixture_ratio=None,
                 mixture_ratio_uom=None,
                 optimization_mode = None,
                 inlet_condition_type=None,
                 inlet_condition_value=None,
                 exit_condition_type=None,
                 exit_condition_value=None,
                 exit_condition_uom=None,
                 nominal_thrust=None,
                 nominal_thrust_uom=None,
                 design_external_pressure=None,
                 design_external_pressure_uom=None
                ):
        self.oxidizer = oxidizer
        self.fuel = fuel
        self.chamber_pressure = Quantity(name="Chamber Pressure", value=float(chamber_pressure), uom=chamber_pressure_uom)
        self.mixture_ratio = Quantity(name="Mixture Ratio", value=float(mixture_ratio), uom=mixture_ratio_uom)
        self.optimization_mode = optimization_mode # 0: Mixture ratio from input, 1: Isp (vac), 2: Isp (opt), 3: Isp (SL)
        self.inlet_condition_type = inlet_condition_type # 0: Contraction area ratio, 1: Infinite area combustor
        self.inlet_condition = Quantity(name="Inlet Condition", value=float(inlet_condition_value))
        self.exit_condition_type = exit_condition_type # 0: Expansion area ratio, 1: Pressure ratio, 2: Exit pressure 
        self.exit_condition = Quantity(name="Exit Condition", value=float(exit_condition_value), uom=exit_condition_uom)
        self.nominal_thrust = Quantity(name="Nominal Thrust", value=float(nominal_thrust), uom=nominal_thrust_uom)
        self.design_external_pressure = Quantity(name="Design External Pressure", value=float(design_external_pressure), uom=design_external_pressure_uom)

