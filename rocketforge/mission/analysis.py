import rocketforge.mission.config as config
from rocketpy import Fluid, LiquidMotor, CylindricalTank, MassFlowRateBasedTank
from rocketpy import Environment
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

    config.engine.add_tank(tank=oxidizer_tank, position=config.ox_tank_pos)
    config.engine.add_tank(tank=fuel_tank, position=config.fuel_tank_pos)
