import rocketforge.mission.config as config
from rocketpy import Fluid, LiquidMotor, CylindricalTank, MassFlowRateBasedTank
from rocketpy import Environment, Rocket, Flight
from datetime import datetime
from numpy import pi


def set_environment():
    # Environment Definition
    date = datetime(config.year, config.month, config.day, config.hour)
    env = Environment(latitude=config.latitude, longitude=config.longitude, elevation=config.elevation)
    env.set_date(date=date, timezone="UTC")
    env.set_atmospheric_model(type="Forecast", file="GFS")
    config.env = env


def set_engine():
    # Fluids Definition
    ox = Fluid(name="oxidizer", density=config.ox_rho)
    fuel = Fluid(name="fuel", density=config.fuel_rho)
    pressurizer = Fluid(name="pressurizer", density=1)

    # Tanks Sizing
    ox_mass = config.prop_mass * config.MR / (1 + config.MR)
    ox_mdot = config.mdot * config.MR / (1 + config.MR)
    height_ox = config.exc_ox * ox_mass / config.ox_rho / (pi * config.r_ox**2)
    height_fuel = config.exc_fuel * ox_mass / config.MR / config.fuel_rho / (pi * config.r_fuel**2)
    tanks_shape_ox = CylindricalTank(radius=config.r_ox, height=height_ox)
    tanks_shape_fuel = CylindricalTank(radius=config.r_fuel, height=height_fuel)

    # Tanks Definition
    oxidizer_tank = MassFlowRateBasedTank(
        name="oxidizer tank",
        geometry=tanks_shape_ox,
        flux_time=ox_mass / ox_mdot * 0.99,
        initial_liquid_mass=ox_mass,
        initial_gas_mass=0,
        liquid_mass_flow_rate_in=0,
        liquid_mass_flow_rate_out=ox_mdot,
        gas_mass_flow_rate_in=0,
        gas_mass_flow_rate_out=0,
        liquid=ox,
        gas=pressurizer,
    )
    fuel_tank = MassFlowRateBasedTank(
        name="fuel tank",
        geometry=tanks_shape_fuel,
        flux_time=ox_mass / ox_mdot * 0.99,
        initial_liquid_mass=ox_mass / config.MR,
        initial_gas_mass=0.0,
        liquid_mass_flow_rate_in=0,
        liquid_mass_flow_rate_out=ox_mdot / config.MR,
        gas_mass_flow_rate_in=0,
        gas_mass_flow_rate_out=0,
        liquid=fuel,
        gas=pressurizer,
    )

    # Engine Definition
    config.engine = LiquidMotor(
        thrust_source=config.thrust,
        dry_mass=config.chamber_mass + config.tanks_mass,
        dry_inertia=config.dry_inertia,
        nozzle_radius=config.Re,
        center_of_dry_mass_position=config.engine_CoG_dry,
        nozzle_position=0,
        burn_time=ox_mass / ox_mdot * 0.99,
        coordinate_system_orientation="nozzle_to_combustion_chamber",
    )

    # Add Tanks
    config.engine.add_tank(tank=oxidizer_tank, position=config.ox_tank_pos)
    config.engine.add_tank(tank=fuel_tank, position=config.fuel_tank_pos)

    # Add Engine to Rocket
    try:
        config.rocket.add_motor(config.engine, position=config.engine_position)
    except Exception:
        pass


def set_rocket():
    # Rocket Definition
    config.rocket = Rocket(
        mass=config.rocket_mass,
        radius=config.rocket_radius,
        inertia=config.rocket_inertia,
        power_off_drag=config.drag,
        power_on_drag=config.drag,
        center_of_mass_without_motor=config.rocket_CoG_dry,
        coordinate_system_orientation="nose_to_tail",
    )
    config.rocket.add_motor(config.engine, position=config.engine_position)

    # Add Rocket Nose Cone
    config.rocket.add_nose(
        length=config.nose_length,
        kind=config.nose_kind,
        position=0,
    )


def add_fins():
    # Add trapezoidal fins
    config.rocket.add_trapezoidal_fins(
        n=config.nfins,
        root_chord=config.root_chord,
        tip_chord=config.tip_chord,
        span=config.span,
        position=config.fins_position,
        sweep_length=config.sweep_length,
    )


def add_parachute():
    # Add Parachute
    config.rocket.add_parachute(
        name=config.parachute,
        cd_s=config.cd_s,
        trigger=config.trigger,
        sampling_rate=config.sampling_rate,
        lag=config.lag,
        noise=config.noise,
    )


def simulate():
    # Simulate flight
    config.flight = Flight(
        rocket=config.rocket,
        environment=config.env,
        rail_length=config.rail_length,
        inclination=config.inclination,
        heading=config.heading,
    )
    # Print Environment Data
    config.env.prints.gravity_details()
    config.env.prints.launch_site_details()
    config.env.prints.atmospheric_model_details()
    config.env.prints.atmospheric_conditions()
    config.env.prints.print_earth_details()
    # Print Engine Data
    config.engine.prints.nozzle_details()
    config.engine.prints.motor_details()
    # Print Rocket Data
    config.rocket.prints.inertia_details()
    config.rocket.prints.rocket_geometrical_parameters()
    config.rocket.prints.rocket_aerodynamics_quantities()
    config.rocket.prints.parachute_data()
    # Print Flight Data
    config.flight.prints.initial_conditions()
    config.flight.prints.surface_wind_conditions()
    config.flight.prints.launch_rail_conditions()
    config.flight.prints.out_of_rail_conditions()
    config.flight.prints.burn_out_conditions()
    config.flight.prints.apogee_conditions()
    config.flight.prints.events_registered()
    config.flight.prints.impact_conditions()
    config.flight.prints.stability_margin()
    config.flight.prints.maximum_values()
    config.flight.prints.numerical_integration_settings()


def plot_trajectory():
    config.flight.plots.trajectory_3d()


def draw_rocket():
    config.rocket.draw()


def plot_all():
    config.flight.plots.trajectory_3d()
    config.flight.plots.linear_kinematics_data()
    config.flight.plots.flight_path_angle_data()
    config.flight.plots.attitude_data()
    config.flight.plots.angular_kinematics_data()
    config.flight.plots.aerodynamic_forces()
    config.flight.plots.rail_buttons_forces()
    config.flight.plots.energy_data()
    config.flight.plots.fluid_mechanics_data()
    config.flight.plots.stability_and_control_data()
    config.flight.plots.pressure_rocket_altitude()
    config.flight.plots.pressure_signals()


def plot_all_rocket():
    config.rocket.plots.all()


def plot_all_engine():
    config.engine.plots.all()
