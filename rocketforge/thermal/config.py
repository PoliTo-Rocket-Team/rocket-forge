# Global thermal analysis variables

# Cooling methods
regen = False
rad = False
film = False

# Regenerative cooling parameters
## Coolant parameters
coolant = None
m_dot_c = None
T_ci = None
p_ci = None

## Enable pressure drops
enable_dp = None

## Wall properties
lambda_w = None
t_w = None

## Channels geometry
a1 = 1.0e-3
a2 = 1.0e-3
a3 = 1.0e-3
b1 = 1.0e-3
b2 = 1.0e-3
b3 = 1.0e-3
d1 = 1.0e-3
d2 = 1.0e-3
d3 = 1.0e-3
NC = 100

## Chamber geometry
shape = None
L_cyl = None
L_c = None
L_e = None
RnOvRt = None
R1OvRt = None
R2OvR2max = None
b = None
theta = None
thetan = None
thetae = None

## Thermodynamic properties
gamma = None
gamma_e = None
Pr_0 = None
Pr_t = None
Pr_e = None
mu_0 = None
cp_0 = None
T_c = None
M_e = None

## Advanced options
pcoOvpc = 1.2
n_stations = 200
max_iter = 200
tuning_factor = 1.0
stability = 0.5
absolute_roughness = 0.00025
dp_method = 0

# Radiation cooling parameters
eps_w = None

# Film cooling parameters
oxfilm = 0.0
fuelfilm = 0.0