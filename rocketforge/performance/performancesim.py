from tabulate import tabulate
from dataclasses import dataclass

@dataclass
class Quantity():
    name: str = None
    value: float = None
    uom: str = None

class PerformanceSimOutput:
    def __init__(self,
                 cstar=None,                 cstar_uom="m/s",
                 Isp_sl=None,                Isp_sl_uom="s",
                 Isp_opt=None,               Isp_opt_uom="s",
                 Isp_vac=None,               Isp_vac_uom="s",
                 Isp_vac_eq=None,            Isp_vac_eq_uom="s",
                 Isp_vac_fr=None,            Isp_vac_fr_uom="s",
                 c_sl=None,                  c_sl_uom="m/s",
                 c_opt=None,                 c_opt_uom="m/s",
                 c_vac=None,                 c_vac_uom="m/s",
                 CF_sl=None,
                 CF_opt=None,
                 CF_vac=None, 
                 pressure=None,              pressure_uom="bar",
                 temperature=None,           temperature_uom="K",
                 density=None,               density_uom="kg/m^3",
                 heat_capacity=None,         heat_capacity_uom="J/kg-K",
                 viscosity=None,             viscosity_uom="millipoise",
                 thermal_conductivity=None,  thermal_conductivity_uom="mcal/cm-K-s",
                 prandtl=None,
                 gamma=None,
                 mach=None,
                 sonic_velocity=None,        sonic_velocity_uom="m/s",
                 enthalpy=None,              enthalpy_uom="kJ/kg"
                 ):
        self.cstar = Quantity(name="Characteristic Velocity", value=cstar, uom=cstar_uom)
        self.Isp = {
            "SL": Quantity(name="Sea Level Specific Impulse", value=Isp_sl, uom=Isp_sl_uom),
            "opt": Quantity(name="Optimum Expansion Specific Impulse", value=Isp_opt, uom=Isp_opt_uom),
            "vac": Quantity(name="Vacuum Specific Impulse", value=Isp_vac, uom=Isp_vac_uom),
            "vac_eq": Quantity(name="Vacuum Specific Impulse (Equilibrium)", value=Isp_vac_eq, uom=Isp_vac_eq_uom),
            "vac_fr": Quantity(name="Vacuum Specific Impulse (Frozen)", value=Isp_vac_fr, uom=Isp_vac_fr_uom)
        }
        self.c = {
            "SL": Quantity(name="Sea Level Effective Exhaust Velocity", value=c_sl, uom=c_sl_uom),
            "opt": Quantity(name="Optimum Expansion Effective Exhaust Velocity", value=c_opt, uom=c_opt_uom),
            "vac": Quantity(name="Vacuum Effective Exhaust Velocity", value=c_vac, uom=c_vac_uom)
        }
        self.CF = {
            "SL": Quantity(name="Sea Level Thrust Coefficient", value=CF_sl),
            "opt": Quantity(name="Optimum Expansion Thrust Coefficient", value=CF_opt),
            "vac": Quantity(name="Vacuum Thrust Coefficient", value=CF_vac)
        }

        self.pressure = Quantity(name="Pressure", value=pressure, uom=pressure_uom)
        self.temperature = Quantity(name="Temperature", value=temperature, uom=temperature_uom)
        self.density = Quantity(name="Density", value=density, uom=density_uom)
        self.heat_capacity = Quantity("Heat Capacity", value=heat_capacity, uom=heat_capacity_uom)
        self.viscosity = Quantity(name="Viscosity", value=viscosity, uom=viscosity_uom)
        self.thermal_conductivity = Quantity(name="Thermal Conductivity", value=thermal_conductivity, uom=thermal_conductivity_uom)
        self.prandtl = Quantity(name="Prandtl Number", value=prandtl)
        self.gamma = Quantity(name="Gamma", value=gamma)
        self.mach = Quantity(name="Mach Number", value=mach)
        self.sonic_velocity = Quantity(name="Sonic Velocity", value=sonic_velocity, uom=sonic_velocity_uom)
        self.enthalpy = Quantity(name="Enthalpy", value=enthalpy, uom=enthalpy_uom)

    def get_performance(self):
        headers = ["Parameter",            "SL",                          "Opt",                         "Vac",                         "Unit"]
        results = [
            ["Charateristic Velocity",     f"{self.cstar.value:.2f}",     f"{self.cstar.value:.2f}",     f"{self.cstar.value:.2f}",     self.cstar.uom],
            ["Effective Exhaust Velocity", f"{self.c['SL'].value:.2f}",   f"{self.c['opt'].value:.2f}",  f"{self.c['vac'].value:.2f}",  self.c['SL'].uom],
            ["Specific Impulse",           f"{self.Isp['SL'].value:.2f}", f"{self.Isp['opt'].value:.2f}", f"{self.Isp['vac'].value:.2f}", self.Isp['SL'].uom],
            ["Thrust Coefficient",         f"{self.CF['SL'].value:.5f}",  f"{self.CF['opt'].value:.5f}", f"{self.CF['vac'].value:.5f}", self.CF['SL'].uom]
        ]
        return tabulate(results, headers, numalign="right", tablefmt="plain")

    def get_thermodynamics(self):
        i = len(self.pressure.value)
        headers = ["Parameter", "Chamber", "Throat"] + [f"{x / (i - 1) * 100:.2f}%" for x in range(1,i-1)] + ["Exit", "Unit"]
        results = [[[self.pressure.name] +              self.pressure.value +              [self.pressure.uom]],
                   [[self.temperature.name] +           self.temperature.value +           [self.temperature.uom]],
                   [[self.density.name] +               self.density.value +               [self.density.uom]],
                   [[self.heat_capacity.name] +         self.heat_capacity.value +         [self.heat_capacity.uom]],
                   [[self.viscosity.name] +             self.viscosity.value +             [self.viscosity.uom]],
                   [[self.thermal_conductivity.name] +  self.thermal_conductivity.value +  [self.thermal_conductivity.uom]],
                   [[self.prandtl.name] +               self.prandtl.value +               [self.prandtl.uom]],
                   [[self.gamma.name] +                 self.gamma.value +                 [self.gamma.uom]],
                   [[self.mach.name] +                  self.mach.value +                  [self.mach.uom]],
                   [[self.sonic_velocity.name] +        self.sonic_velocity.value +        [self.sonic_velocity.uom]],
                   [[self.enthalpy.name] +              self.enthalpy.value +              [self.enthalpy.uom]]        
        ]
        return tabulate(results, headers, numalign="right", tablefmt="plain")


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

    def __repr__(self):
        optimizations = {
            0: "Mixture ratio from input",
            1: "Maximize Isp (vac)",
            2: "Maximize Isp (opt)",
            3: "Maximize Isp (SL)"
        }
        inlet_conditions = {
            0: "Contraction area ratio",
            1: "Infinite area combustor"
        }
        exit_conditions = {
            0: "Expansion area ratio",
            1: "Pressure ratio",
            2: "Exit pressure"
        }
        inletcond = self.inlet_condition.value if self.inlet_condition_type == 0 else "" #TODO: maybe not needed if None 
        table = [["Oxidizer:",         self.oxidizer,                                "Fuel:",                    self.fuel],
                 ["Chamber Pressure",   self.chamber_pressure.value,                  "",                         self.chamber_pressure.uom],
                 ["Mixture Ratio",      self.mixture_ratio.value,                     "",                         self.mixture_ratio.uom],
                 ["Optimization Mode",  optimizations[self.optimization_mode],        "",                         ""],
                 ["Inlet Condition",    inlet_conditions[self.inlet_condition_type],  inletcond,                  ""],
                 ["Exit Condition",     exit_conditions[self.exit_condition_type],    self.exit_condition.value,  self.exit_condition.uom],
                 ["Nominal Thrust",     self.nominal_thrust.value,                    "",                         self.nominal_thrust.uom],
                 ["at",                 self.design_external_pressure.value,          "",                         self.design_external_pressure.uom],
        ]
        return tabulate(table, numalign="right", tablefmt="plain")
    
