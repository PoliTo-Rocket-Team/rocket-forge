# Design Parameters
thrust = None # Thrust over time
mdot = None # Mass flow rate
MR = None # Mixture Ratio

# Engine Mass Estimation
chamber_mass = None # Thrust chamber mass 
prop_mass = None # Propellant mass
tanks_mass = None # k0 + kt * prop_mass # Dry tanks and feed system mass

# Tanks Sizing Parameters
ox_rho = None # Oxidizer density
fuel_rho = None # Fuel density
r_ox = None # Oxidizer tank radius
r_fuel = None # Fuel tank radius
exc_ox = None # Excess percentage of oxidizer tank volume
exc_fuel = None # Excess percentage of fuel tank volume

# Engine Parameters
Re = None # Nozzle exit radius
dry_inertia = None # Dry engine inertia
engine_CoG_dry = None # Dry engine center of gravity
ox_tank_pos = None # Position of oxidizer tank
fuel_tank_pos = None # Position of fuel tank

# Rocket Parameters
rocket_mass = None # Rocket mass (without engine)
engine_position = None # Engine position
rocket_radius = None # Rocket radius
rocket_inertia = None # Rocket inertia (without engine) 
drag = None # Rocket drag coefficient over Mach
rocket_CoG_dry = None # Rocket center of gravity (without engine)
nose_length = None # Nose length
nfins = None # Number of fins
root_chord = None # Root chord of fins
tip_chord = None # Tip chord of fins
span = None # Span of fins
fins_position = None # Fins position
sweep_length = None # Fins sweep length

# Main Parachute Parameters
main_cd_s = None
main_trigger = None
main_sampling_rate = None
main_lag = None
main_noise = None

# Drogue Parachute Parameters
drogue_cd_s = None
drogue_trigger = None
drogue_sampling_rate = None
drogue_lag = None
drogue_noise = None

# Environment Parameters
year = None
month = None
day = None
hour = None
latitude = None
longitude = None
elevation = None
env = None

# Rail Parameters
rail_length = None
inclination = None
heading = None

# Simulation Parameters
from rocketpy import LiquidMotor, Rocket, Flight
engine : LiquidMotor = None
rocket : Rocket = None
flight : Flight = None