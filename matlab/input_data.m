disp('Loading input file...')

% Load input file (TODO)

% Chamber
Oxidizer = 'LOX';
Fuel = 'CH4';
MR = 2.9;
pc = 4000000;
pSL = 101325;
N = 10; % number of rocketcea stations

% Geometry
epsilon = 2.7;
epsc = 8;
At = 0.000872;
theta_ex = 8 * pi / 180;
Le = 0.05344;

Ae = At * epsilon;
re = sqrt(Ae / pi);
rt = sqrt(At / pi);

% Multiphase coefficients
Cs = 0; % Condensed phase heat capacity
Z = 0; % Mass fraction of condensed phase at nozzle exit

% Propellant empirical coefficients (TODO)
h0 = 0;
a = 1;
b = 1;