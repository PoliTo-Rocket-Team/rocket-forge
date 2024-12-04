from tabulate import tabulate
from dataclasses import dataclass
from rocketcea.cea_obj_w_units import CEA_Obj
from rocketforge.utils.conversions import pressure_uom, thrust_uom
from rocketforge.performance.mixtureratio import optimizemr, optimizermr_at_pe

@dataclass
class Quantity():
    name: str = None
    value: float = None
    uom: str = None

class PerformanceSimOutput:
    def __init__(self,
                 cstar=None,                 cstar_uom="m/s",
                 eps=None,
                 exp_p_ratio=None,
                 pe=None,                    pe_uom="bar",
                 mr=None,
                 mr_s=None,
                 alpha=None,
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
                 At = None,                  At_uom="m^2",
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
        self.eps = Quantity(name="Expansion Area Ratio", value=eps)
        self.exp_p_ratio = Quantity(name="Expansion Pressure Ratio", value=exp_p_ratio)
        self.pe = Quantity(name="Exit Pressure", value=pe, uom=pe_uom)
        self.mr = Quantity(name="Mixture Ratio", value=mr)
        self.mr_s = Quantity(name="Mixture Ratio (stoichiometric)", value=mr_s)
        self.alpha = Quantity(name="Alpha (oxidizer excess coefficient)", value=alpha)
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

        self.At = Quantity(name="Throat Area", value=At, uom=At_uom)
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
        output1 = tabulate(results, headers, numalign="right", tablefmt="plain")

        table = [[self.eps.name,          self.eps.value,          ""],
                 [self.exp_p_ratio.name,  self.exp_p_ratio.value,  ""],
                 [self.pe.name,           self.pe.value,           self.pe.uom],
                 [self.mr.name,           self.mr.value,           ""],
                 [self.mr_s.name,         self.mr_s.value,         ""],
                 [self.alpha.name,        self.alpha.value,        ""]
        ]
        output2 = tabulate(table, numalign="right", tablefmt="plain", floatfmt=".3f")
        return output1 + 2*"\n" + output2

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
        self.inlet_condition = Quantity(
            name="Inlet Condition",
            value=float(inlet_condition_value) if inlet_condition_value is not None else None)
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

        inletcond = self.inlet_condition.value if self.inlet_condition_type == 0 else "" # Not really needed but keeps consistency with other empty cells
        exituom = self.exit_condition.uom if self.exit_condition_type == 2 else ""
        table = [["Oxidizer:",          self.oxidizer,                                "Fuel:",                    self.fuel],
                 ["Chamber Pressure",   self.chamber_pressure.value,                  "",                         self.chamber_pressure.uom],
                 ["Mixture Ratio",      self.mixture_ratio.value,                     "",                         self.mixture_ratio.uom],
                 ["Optimization Mode",  optimizations[self.optimization_mode],        "",                         ""],
                 ["Inlet Condition",    inlet_conditions[self.inlet_condition_type],  inletcond,                  ""],
                 ["Exit Condition",     exit_conditions[self.exit_condition_type],    self.exit_condition.value,  exituom],
                 ["Nominal Thrust",     self.nominal_thrust.value,                    "",                         self.nominal_thrust.uom],
                 ["at",                 self.design_external_pressure.value,          "",                         self.design_external_pressure.uom],
        ]
        return tabulate(table, numalign="right", tablefmt="plain")

    def simulation_run(self, i=2, fr=0, fat=0) -> PerformanceSimOutput:
        try:
            pamb = 101325 # Assuming standard atmospheric pressure in Pa
            pc = self.chamber_pressure.value * pressure_uom(self.chamber_pressure.uom)
            mr = self.mixture_ratio.value
            epsc = self.inlet_condition.value
            optimization_mode = self.optimization_mode
            exit_condition_type = self.exit_condition_type

            C = CEA_Obj(
                oxName = self.oxidizer,
                fuelName = self.fuel,
                fac_CR = epsc,
                cstar_units = "m/s",
                pressure_units = "Pa",
                temperature_units = "K",
                sonic_velocity_units="m/s",
                enthalpy_units="kJ/kg",
                density_units="kg/m^3",
                specific_heat_units="J/kg-K")

            mr_s = C.getMRforER(ERphi=1)

            if optimization_mode == 0: # MR from input
                mr, alpha, eps, pe = self.get_params_from_mr_input(pc, mr_s, C)
            elif exit_condition_type == 0: # Expansion area ratio
                mr, alpha, eps, pe = self.get_params_from_area_ratio(pc, mr_s, C)
            else: # Pressure conditions
                mr, alpha, eps, pe = self.get_params_from_pe_input(pc, mr_s, C)

            # Characteristic velocity
            cstar = C.get_Cstar(Pc=pc, MR=mr)
            # Exit pressure
            pe = pc / C.get_PcOvPe(Pc=pc, MR=mr, eps=eps, frozen=fr, frozenAtThroat=fat)
            pe_output = pe / pressure_uom("bar") # from Pa to bar
            # Vacuum specific impulse
            Isp_vac = C.get_Isp(Pc=pc, MR=mr, eps=eps, frozen=fr, frozenAtThroat=fat)
            # Vacuum specific impulse (equilibrium)
            Isp_vac_eq = C.get_Isp(Pc=pc, MR=mr, eps=eps)
            # Vacuum specific impulse (frozen)
            Isp_vac_fr = C.get_Isp(Pc=pc, MR=mr, eps=eps, frozen=1)
            # Sea level specific impulse
            Isp_sl = C.estimate_Ambient_Isp(Pc=pc, MR=mr, eps=eps, Pamb=pamb, frozen=fr, frozenAtThroat=fat)[0]
            # Optimum expansion specific impulse
            Isp_opt = C.estimate_Ambient_Isp(Pc=pc, MR=mr, eps=eps, Pamb=pe, frozen=fr, frozenAtThroat=fat)[0]
            # Effective exhaust velocities
            c_vac = Isp_vac * 9.80655
            c_sl = Isp_sl * 9.80655
            c_opt = Isp_opt * 9.80655
            # Thrust coefficients
            CF_opt, CF_sl, mode = C.get_PambCf(Pamb=pamb, Pc=pc, MR=mr, eps=eps)
            CF_vac = c_vac / cstar
            # Temperature
            Tc, Tt, Te = C.get_Temperatures(Pc=pc, MR=mr, eps=eps, frozen=fr, frozenAtThroat=fat)
            # Density
            rhoc, rhot, rhoe = C.get_Densities(Pc=pc, MR=mr, eps=eps, frozen=fr, frozenAtThroat=fat)
            # Chamber transport properties
            cpc, muc, lc, Prc = C.get_Chamber_Transport(Pc=pc, MR=mr, eps=eps, frozen=fr)
            # Sonic velocity
            ac, at, ae = C.get_SonicVelocities(Pc=pc, MR=mr, eps=eps, frozen=fr, frozenAtThroat=fat)
            # Enthalpy
            Hc, Ht, He = C.get_Enthalpies(Pc=pc, MR=mr, eps=eps, frozen=fr, frozenAtThroat=fat)
            # Thrust
            thrust = self.nominal_thrust.value * thrust_uom(self.nominal_thrust.uom)
            # Throat area
            At = (thrust * cstar) / (c_sl * pc)
            # Thermodynamic properties initialization
            p = [pc / 100000]
            T = [Tc]
            rho = [rhoc]
            cp = [cpc]
            mu = [muc]
            l = [lc]
            Pr = [Prc]
            gamma = [0]
            M = [0]
            a = [ac]
            H = [Hc]
            # Thermodynamic properties calculations
            for x in range(i):
                x = 1 + x * (eps - 1) / (i - 1)
                p.append(pc / 100000 / C.get_PcOvPe(Pc=pc, MR=mr, eps=x, frozen=fr, frozenAtThroat=fat))
                T.append(C.get_Temperatures(Pc=pc, MR=mr, eps=x, frozen=fr, frozenAtThroat=fat)[2])
                rho.append(C.get_Densities(Pc=pc, MR=mr, eps=x, frozen=fr, frozenAtThroat=fat)[2])
                cp.append(C.get_Exit_Transport(Pc=pc, MR=mr, eps=x, frozen=fr, frozenAtThroat=fat)[0])
                mu.append(C.get_Exit_Transport(Pc=pc, MR=mr, eps=x, frozen=fr, frozenAtThroat=fat)[1])
                l.append(C.get_Exit_Transport(Pc=pc, MR=mr, eps=x, frozen=fr, frozenAtThroat=fat)[2])
                Pr.append(C.get_Exit_Transport(Pc=pc, MR=mr, eps=x, frozen=fr, frozenAtThroat=fat)[3])
                gamma.append(C.get_exit_MolWt_gamma(Pc=pc, MR=mr, eps=x, frozen=fr, frozenAtThroat=fat)[1])
                M.append(C.get_MachNumber(Pc=pc, MR=mr, eps=x, frozen=fr, frozenAtThroat=fat))
                a.append(C.get_SonicVelocities(Pc=pc, MR=mr, eps=x, frozen=fr, frozenAtThroat=fat)[2])
                H.append(C.get_Enthalpies(Pc=pc, MR=mr, eps=x, frozen=fr, frozenAtThroat=fat)[2])

            return PerformanceSimOutput(cstar=cstar,
                                        eps=eps,
                                        exp_p_ratio=pc/pe,
                                        pe=pe_output,
                                        mr=mr,
                                        mr_s=mr_s,
                                        alpha=alpha,
                                        Isp_sl=Isp_sl,
                                        Isp_opt=Isp_opt,
                                        Isp_vac=Isp_vac,
                                        Isp_vac_eq=Isp_vac_eq,
                                        Isp_vac_fr=Isp_vac_fr,
                                        c_sl=c_sl,
                                        c_opt=c_opt,
                                        c_vac=c_vac,
                                        CF_sl=CF_sl,
                                        CF_opt=CF_opt,
                                        CF_vac=CF_vac,
                                        pressure=p,
                                        At=At,
                                        temperature=T,
                                        density=rho,
                                        heat_capacity=cp,
                                        viscosity=mu,
                                        thermal_conductivity=l,
                                        prandtl=Pr,
                                        gamma=gamma,
                                        mach=M,
                                        sonic_velocity=a,
                                        enthalpy=H)
        except Exception as err:
            return str(err) # FIXME: shouldn't have different type returns for same function (use Union or RuntimeError)

    def get_params_from_mr_input(self, pc, mr_s, C):
        if self.mixture_ratio.uom == "O/F":
            mr = self.mixture_ratio.value
            alpha = mr / mr_s
        elif self.mixture_ratio.uom == "alpha":
            alpha = self.mixture_ratio.value
            mr = alpha * mr_s

        if self.exit_condition_type == 0: # Expansion Area Ratio
            eps = self.exit_condition.value
            pe = pc / C.get_PcOvPe(Pc=pc, MR=mr, eps=eps)
        elif self.exit_condition_type == 1: # Pressure Ratio
            eps = C.get_eps_at_PcOvPe(Pc=pc, MR=mr, PcOvPe=self.exit_condition.value)
            pe = pc / self.exit_condition.value
        elif self.exit_condition_type == 2: # Exit Pressure
            pe = self.exit_condition.value * pressure_uom(self.exit_condition.uom)
            eps = C.get_eps_at_PcOvPe(Pc=pc, MR=mr, PcOvPe=pc / pe)
        return mr, alpha, eps, pe

    def get_params_from_area_ratio(self, pc, mr_s, C):
        eps = self.exit_condition.value
        mr = optimizemr(C, pc, eps, self.optimization_mode)
        alpha = mr / mr_s
        pe = pc / C.get_PcOvPe(Pc=pc, MR=mr, eps=eps)
        return mr, alpha, eps, pe

    def get_params_from_pressure_conditions(self, pc, mr_s, C):
        if self.exit_condition_type == 1: # Pressure Ratio
            pe = pc / self.exit_condition.value
        elif self.exit_condition_type == 2: # Exit Pressure
            pe = self.exit_condition.value * pressure_uom(self.exit_condition.uom)

        mr = optimizermr_at_pe(C, pc, pe, self.optimization_mode)
        eps = C.get_eps_at_PcOvPe(Pc=pc, MR=mr, PcOvPe=pc / pe)
        alpha = mr / mr_s
        return mr, alpha, eps, pe

# Passing parameters to the function as kwargs overrides inputs from the engine definition frame
def generate_sim_input(initial_frame = None, nested_frame = None, **kwargs) -> PerformanceSimInput:
    nested_mr = kwargs.get('nested_mr', None)
    nested_pc = kwargs.get('nested_pc', None)
    nested_epsc = kwargs.get('nested_epsc', None)
    nested_eps = kwargs.get('nested_eps', None)

    # Get mixture ratio
    if nested_mr is None:
        mixture_ratio, mixture_ratio_uom = initial_frame.get_mixture_ratio()
    else:
        mixture_ratio = nested_mr
        mixture_ratio_uom = nested_frame.rows[0]["unit_dropdown"].get()

    # Get chamber pressure
    if nested_pc is None:
        chamber_pressure, chamber_pressure_uom = initial_frame.get_chamber_pressure()
    else:
        chamber_pressure = nested_pc
        chamber_pressure_uom = nested_frame.rows[1]["unit_dropdown"].get()

    # Get inlet condition
    if nested_epsc is None:
        inlet_condition_type, inlet_condition_value = initial_frame.get_inlet_condition()
    else:
        inlet_condition_type = 0 if nested_frame.rows[2]["unit_dropdown"].get() == "Contraction Area Ratio (Ac/At)" else 1 #TODO this sucks
        inlet_condition_value = nested_epsc

    # Get exit condition
    if nested_eps is None:
        exit_condition_type, exit_condition_value, exit_condition_uom = initial_frame.get_exit_condition()
    else:
        exit_condition_value = nested_eps
        exit_condition_type, exit_condition_uom = nested_frame.get_exit_type_and_uom()

    return PerformanceSimInput(
        oxidizer=initial_frame.oxoptmenu.get(),
        fuel=initial_frame.fueloptmenu.get(),
        chamber_pressure=chamber_pressure,
        chamber_pressure_uom=chamber_pressure_uom,
        mixture_ratio=mixture_ratio,
        mixture_ratio_uom=mixture_ratio_uom,
        optimization_mode=initial_frame.optimizationmode.get(),
        inlet_condition_type=inlet_condition_type,
        inlet_condition_value=inlet_condition_value,
        exit_condition_type=exit_condition_type,
        exit_condition_value=exit_condition_value,
        exit_condition_uom=exit_condition_uom,
        nominal_thrust=initial_frame.thrustentry.get(),
        nominal_thrust_uom=initial_frame.thrustuom.get(),
        design_external_pressure=initial_frame.thrustentry2.get(),
        design_external_pressure_uom=initial_frame.thrustuom2.get())
