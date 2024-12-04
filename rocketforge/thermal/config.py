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

## Wall properties
lambda_w = None
t_w = None

## Channels geometry
a1 = None
a2 = None
a3 = None
b1 = None
b2 = None
b3 = None
d1 = None
d2 = None
d3 = None
NC = None

## Chamber geometry
shape = None
L_cyl = None
L_c = None
L_e = None
A_t = None
eps = None
eps_c = None
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
c_star = None
p_c = None
T_c = None
M_e = None

## Advanced options
pcoOvpc = None
n_stations = None
max_iter = None
tuning_factor = None
stability = None

# Radiation cooling parameters
eps_w = None

# Film cooling parameters
oxfilm = 0.0
fuelfilm = 0.0