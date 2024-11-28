class PerformanceSimData:
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
                 outlet_condition_type=None,
                 outlet_condition_value=None,
                 outlet_condition_value_uom=None
                ):
        self.oxidizer = oxidizer
        self.fuel = fuel
        self.chamber_pressure = chamber_pressure
        self.chamber_pressure_uom = chamber_pressure_uom
        self.mixture_ratio = mixture_ratio
        self.mixture_ratio_uom = mixture_ratio_uom
        self.optimization_mode = optimization_mode
        self.inlet_condition_type = inlet_condition_type
        self.inlet_condition_value = inlet_condition_value
        self.outlet_condition_type  = outlet_condition_type 
        self.outlet_condition_value = outlet_condition_value
        self.outlet_condition_value_uom = outlet_condition_value_uom
