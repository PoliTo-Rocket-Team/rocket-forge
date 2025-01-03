import rocketforge.thermal.config as tconf
from main                       import RocketForge
from configparser               import ConfigParser
from rocketforge.utils.helpers  import update_entry
from tkinter                    import filedialog


def save_config(self: RocketForge):
    self.statuslabel.configure(text="Status: saving configuration file...")
    self.statuslabel.update()

    try:
        config = ConfigParser()
        config["InitialData"] = {
            "name": self.initialframe.enginenameentry.get(),
            "chamber_pressure": self.initialframe.pcentry.get(),
            "chamber_pressure_uom": self.initialframe.pcuom.get(),
            "oxidizer": self.initialframe.oxvar.get(),
            "fuel": self.initialframe.fuelvar.get(),
            "mixture_ratio": self.initialframe.mrentry.get(),
            "mixture_ratio_uom": self.initialframe.mruom.get(),
            "expansion_area_ratio": self.initialframe.epsentry.get(),
            "expansion_pressure_ratio": self.initialframe.peratioentry.get(),
            "exit_pressure": self.initialframe.peentry.get(),
            "exit_pressure_uom": self.initialframe.peuom.get(),
            "exit_condition": self.initialframe.exitcondition.get(),
            "mixture_ratio_optimization": self.initialframe.optimizationmode.get(),
            "inlet_conditions": self.initialframe.inletcondition.get(),
            "contraction_ratio": self.initialframe.epscentry.get(),
            "thrust": self.initialframe.thrustentry.get(),
            "thrust_uom": self.initialframe.thrustuom.get(),
            "ambient_pressure": self.initialframe.thrustentry2.get(),
            "ambient_pressure_uom": self.initialframe.thrustuom2.get(),
        }
        tf = self.performanceframe.thermodynamicframe
        config["Performance"] = {
            "flow_model": tf.frozenflow.get(),
            "number_of_stations": tf.stationsentry.get(),
        }
        gf = self.geometryframe
        config["Geometry"] = {
            "throat_area": gf.throatareaentry.get(),
            "throat_area_uom": gf.throatareauom.get(),
            "shape": gf.shape.get(),
            "divergent_length": gf.divergentlengthentry.get(),
            "divergent_length_uom": gf.divergentlengthuom.get(),
            "theta_e": gf.thetaexentry.get(),
            "theta_e_uom": gf.thetaexuom.get(),
            "rnovrt": gf.rnovrtentry.get(),
            "theta_n": gf.thetanentry.get(),
            "theta_n_uom": gf.thetanuom.get(),
            "r1ovrt": gf.r1ovrtentry.get(),
            "chamber_length": gf.chamberlengthentry.get(),
            "chamber_length_uom": gf.chamberlengthuom.get(),
            "contraction_angle": gf.bentry.get(),
            "contraction_angle_uom": gf.buom.get(),
            "r2ovr2max": gf.r2ovr2maxentry.get(),
            "cselected": gf.cselected.get(),
            "cle": gf.cleentry.get(),
            "cle_uom": gf.cleuom.get(),
            "clf": gf.clfentry.get(),
            "ctheta": gf.cthetaentry.get(),
            "ctheta_uom": gf.cthetauom.get(),
        }
        thf = self.thermalframe
        config["Thermal"] = {
            "enable_regen": thf.regenvar.get(),
            "coolant": thf.coolant.get(),
            "coolant_flow_rate": thf.mdotcentry.get(),
            "coolant_flow_rate_uom": thf.mdotcuom.get(),
            "coolant_Ti": thf.tcientry.get(),
            "coolant_Ti_uom": thf.tciuom.get(),
            "coolant_pi": thf.pcientry.get(),
            "coolant_pi_uom": thf.pciuom.get(),
            "pressure_drops": thf.dp.get(),
            "inner_wall": thf.tentry.get(),
            "inner_wall_uom": thf.tuom.get(),
            "wall_conductivity": thf.kentry.get(),
            "number_of_channels": tconf.NC,
            "channels_ac": tconf.a1,
            "channels_at": tconf.a2,
            "channels_ae": tconf.a3,
            "channels_bc": tconf.b1,
            "channels_bt": tconf.b2,
            "channels_be": tconf.b3,
            "adv_pinj/pc": tconf.pcoOvpc,
            "adv_stations": tconf.n_stations,
            "adv_max_iter": tconf.max_iter,
            "adv_tuning": tconf.tuning_factor,
            "adv_stability": tconf.stability,
            "adv_abs_roughness": tconf.absolute_roughness,
            "adv_friction_method": tconf.dp_method,
            "t_eOvt_w": tconf.t_eOvt_w,
            "enable_rad": thf.radvar.get(),
            "eps_w": thf.radepsentry.get(),
            "enable_film": thf.filmvar.get(),
            "fuel_film": thf.fuelfilm.get(),
            "ox_film": thf.oxfilm.get(),
        }
        ttf = self.tanksframe
        config["Tanks"] = {
            "mass_flow_rate": ttf.mdotentry.get(),
            "mass_flow_rate_uom": ttf.mdotuom.get(),
            "prop_mass": ttf.mpentry.get(),
            "prop_mass_uom": ttf.mpuom.get(),
            "mixture_ratio": ttf.mrentry.get(),
            "k0": ttf.k0entry.get(),
            "k0_uom": ttf.k0uom.get(),
            "kt": ttf.ktentry.get(),
            "rho_ox": ttf.oxrhoentry.get(),
            "rho_ox_uom": ttf.oxrhouom.get(),
            "r_ox": ttf.oxrentry.get(),
            "r_ox_uom": ttf.oxruom.get(),
            "exc_ox": ttf.oxexcentry.get(),
            "pos_ox": ttf.oxxentry.get(),
            "pos_ox_uom": ttf.oxxuom.get(),
            "rho_fuel": ttf.fuelrhoentry.get(),
            "rho_fuel_uom": ttf.fuelrhouom.get(),
            "r_fuel": ttf.fuelrentry.get(),
            "r_fuel_uom": ttf.fuelruom.get(),
            "exc_fuel": ttf.fuelexcentry.get(),
            "pos_fuel": ttf.fuelxentry.get(),
            "pos_fuel_uom":ttf.fuelxuom.get(),
        }

        with open(filedialog.asksaveasfilename(defaultextension=".rf"), "w") as f:
            config.write(f)

    except Exception:
        pass

    self.statuslabel.configure(text="Status: idle")
    self.statuslabel.update()


def load_config(self: RocketForge):
    self.statuslabel.configure(text="Status: loading configuration file...")
    self.statuslabel.update()

    try:
        config = ConfigParser()
        config.read(filedialog.askopenfilename(title="Load configuration file", filetypes=(("Rocket Forge files", "*.rf"), ("all files", "*.*"))))

        idf = self.initialframe

        update_entry(idf.enginenameentry, config.get("InitialData", "name"))
        update_entry(idf.pcentry, config.get("InitialData", "chamber_pressure"))
        idf.pcuom.set(config.get("InitialData", "chamber_pressure_uom"))
        idf.oxvar.set(config.get("InitialData", "oxidizer"))
        idf.fuelvar.set(config.get("InitialData", "fuel"))
        update_entry(idf.mrentry, config.get("InitialData", "mixture_ratio"))
        idf.mruom.set(config.get("InitialData", "mixture_ratio_uom"))
        update_entry(idf.epsentry, config.get("InitialData", "expansion_area_ratio"))
        update_entry(idf.peratioentry, config.get("InitialData", "expansion_pressure_ratio"))
        update_entry(idf.peentry, config.get("InitialData", "exit_pressure"))
        idf.peuom.set(config.get("InitialData", "exit_pressure_uom"))
        idf.exitcondition.set(config.get("InitialData", "exit_condition"))
        idf.optimizationmode.set(config.get("InitialData", "mixture_ratio_optimization"))
        idf.inletcondition.set(config.get("InitialData", "inlet_conditions"))
        update_entry(idf.epscentry, config.get("InitialData", "contraction_ratio"))
        update_entry(idf.thrustentry, config.get("InitialData", "thrust"))
        idf.thrustuom.set(config.get("InitialData", "thrust_uom"))
        update_entry(idf.thrustentry2, config.get("InitialData", "ambient_pressure"))
        idf.thrustuom2.set(config.get("InitialData", "ambient_pressure_uom"))

        tf = self.performanceframe.thermodynamicframe

        tf.frozenflow.set(config.get("Performance", "flow_model"))
        update_entry(tf.stationsentry, config.get("Performance", "number_of_stations"))

        gf = self.geometryframe

        gf.shape.set(config.get("Geometry", "shape"))
        gf.change_shape(config.get("Geometry", "shape"))

        update_entry(gf.throatareaentry, config.get("Geometry", "throat_area"))
        gf.throatareauom.set(config.get("Geometry", "throat_area_uom"))
        update_entry(gf.divergentlengthentry, config.get("Geometry", "divergent_length"))
        gf.divergentlengthuom.set(config.get("Geometry", "divergent_length_uom"))
        update_entry(gf.thetaexentry, config.get("Geometry", "theta_e"))
        gf.thetaexuom.set(config.get("Geometry", "theta_e_uom"))
        update_entry(gf.thetanentry, config.get("Geometry", "theta_n"))
        gf.thetanuom.set(config.get("Geometry", "theta_n_uom"))
        update_entry(gf.rnovrtentry, config.get("Geometry", "rnovrt"))
        update_entry(gf.r1ovrtentry, config.get("Geometry", "r1ovrt"))
        update_entry(gf.r2ovr2maxentry, config.get("Geometry", "r2ovr2max"))
        update_entry(gf.chamberlengthentry, config.get("Geometry", "chamber_length"))
        gf.chamberlengthuom.set(config.get("Geometry", "chamber_length_uom"))
        update_entry(gf.bentry, config.get("Geometry", "contraction_angle"))
        gf.buom.set(config.get("Geometry", "contraction_angle_uom"))
        gf.cselected.set(config.get("Geometry", "cselected"))
        update_entry(gf.cleentry, config.get("Geometry", "cle"))
        gf.cleuom.set(config.get("Geometry", "cle_uom"))
        update_entry(gf.clfentry, config.get("Geometry", "clf"))
        update_entry(gf.cthetaentry, config.get("Geometry", "ctheta"))
        gf.cthetauom.set(config.get("Geometry", "ctheta_uom"))

        thf = self.thermalframe
        thf.regenvar.set(config.get("Thermal", "enable_regen"))
        thf.coolant.set(config.get("Thermal", "coolant"))
        update_entry(thf.mdotcentry, config.get("Thermal", "coolant_flow_rate"))
        thf.mdotcuom.set(config.get("Thermal", "coolant_flow_rate_uom"))
        update_entry(thf.tcientry, config.get("Thermal", "coolant_Ti"))
        thf.tciuom.set(config.get("Thermal", "coolant_Ti_uom"))
        update_entry(thf.pcientry, config.get("Thermal", "coolant_pi"))
        thf.pciuom.set(config.get("Thermal", "coolant_pi_uom"))
        thf.dp.set(config.get("Thermal", "pressure_drops"))
        update_entry(thf.tentry, config.get("Thermal", "inner_wall"))
        thf.tuom.set(config.get("Thermal", "inner_wall_uom"))
        update_entry(thf.kentry, config.get("Thermal", "wall_conductivity"))
        tconf.NC = int(float(config.get("Thermal", "number_of_channels")))
        tconf.a1 = float(config.get("Thermal", "channels_ac"))
        tconf.a2 = float(config.get("Thermal", "channels_at"))
        tconf.a3 = float(config.get("Thermal", "channels_ae"))
        tconf.b1 = float(config.get("Thermal", "channels_bc"))
        tconf.b2 = float(config.get("Thermal", "channels_bt"))
        tconf.b3 = float(config.get("Thermal", "channels_be"))
        tconf.pcoOvpc = float(config.get("Thermal", "adv_pinj/pc"))
        tconf.n_stations = int(float(config.get("Thermal", "adv_stations")))
        tconf.max_iter = int(float(config.get("Thermal", "adv_max_iter")))
        tconf.tuning_factor = float(config.get("Thermal", "adv_tuning"))
        tconf.stability = float(config.get("Thermal", "adv_stability"))
        tconf.absolute_roughness = float(config.get("Thermal", "adv_abs_roughness"))
        tconf.dp_method = int(float(config.get("Thermal", "adv_friction_method")))
        tconf.t_eOvt_w = float(config.get("Thermal", "t_eOvt_w"))
        thf.radvar.set(config.get("Thermal", "enable_rad"))
        update_entry(thf.radepsentry, config.get("Thermal", "eps_w"))
        thf.filmvar.set(config.get("Thermal", "enable_film"))
        update_entry(thf.fuelfilm, config.get("Thermal", "fuel_film"))
        update_entry(thf.oxfilm, config.get("Thermal", "ox_film"))

        ttf = self.tanksframe

        update_entry(ttf.mdotentry, config.get("Tanks", "mass_flow_rate"))
        ttf.mdotuom.set(config.get("Tanks", "mass_flow_rate_uom"))
        update_entry(ttf.mpentry, config.get("Tanks", "prop_mass"))
        ttf.mpuom.set(config.get("Tanks", "prop_mass_uom"))
        update_entry(ttf.mrentry, config.get("Tanks", "mixture_ratio"))
        update_entry(ttf.k0entry, config.get("Tanks", "k0"))
        ttf.k0uom.set(config.get("Tanks", "k0_uom"))
        update_entry(ttf.ktentry, config.get("Tanks", "kt"))
        update_entry(ttf.oxrhoentry, config.get("Tanks", "rho_ox"))
        ttf.oxrhouom.set(config.get("Tanks", "rho_ox_uom"))
        update_entry(ttf.oxrentry, config.get("Tanks", "r_ox"))
        ttf.oxruom.set(config.get("Tanks", "r_ox_uom"))
        update_entry(ttf.oxexcentry, config.get("Tanks", "exc_ox"))
        update_entry(ttf.oxxentry, config.get("Tanks", "pos_ox"))
        ttf.oxxuom.set(config.get("Tanks", "pos_ox_uom"))
        update_entry(ttf.fuelrhoentry, config.get("Tanks", "rho_fuel"))
        ttf.fuelrhouom.set(config.get("Tanks", "rho_fuel_uom"))
        update_entry(ttf.fuelrentry, config.get("Tanks", "r_fuel"))
        ttf.fuelruom.set(config.get("Tanks", "r_fuel_uom"))
        update_entry(ttf.fuelexcentry, config.get("Tanks", "exc_fuel"))
        update_entry(ttf.fuelxentry, config.get("Tanks", "pos_fuel"))
        ttf.fuelxuom.set(config.get("Tanks", "pos_fuel_uom"))

    except Exception:
        pass

    self.statuslabel.configure(text="Status: idle")
    self.statuslabel.update()