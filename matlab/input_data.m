%% Load input values
disp('Loading input values...')

% Enable rocketcea calculations 
cea = 0;                    % cea = 1: enabled, cea = 0: disabled

% Chamber
Oxidizer = 'LOX';           % Oxidizer (rocketcea notation)
Fuel = 'CH4';               % Fuel (rocketcea notation)
MR = 2.9;                   % Thruster mixture ratio
pc = 40E5;                  % Chamber pressure
pSL = 101325;               % Sea level pressure
N = 10;                     % Number of rocketcea stations

% Geometry
epsilon = 2.7;              % Supersonic area ratio
epsc = 8;                   % Contraction ratio of finite area combustor
At = 8.72E-4;               % Throat area
Ae = At * epsilon;          % Exit area
theta_n = 14.32 * pi / 180; % Initial parabola angle
theta_ex = 8 * pi / 180;    % Final parabola angle
theta_b = 35 * pi / 180;    % Contraction angle
rt = sqrt(At / pi);         % Throat radius
re = sqrt(Ae / pi);         % Exit radius
rc = 47.115E-3;             % Chamber radius
Dt = 2 * rt;                % Throat diameter
De = 2 * re;                % Exit diameter
Dc = 2 * rc;                % Chamber diameter
R1 = 24.99E-3;              % Convergent-Throat curvature
R2 = 71.72E-3;              % Chamber-convergent curvature
Rn = 6.36E-3;               % Throat-Divergent curvature
Le = 53.44E-3;              % Divergent nozzle length
Lc = 155.89E-3;             % Chamber length
Lcyl = 81.9E-3;             % Cylindrical chamber length
LeOvc15 = 1.3095;           % Relative to 15 deg cone nozzle

% Multiphase coefficients
Cs = 0;                     % Condensed phase heat capacity
Z = 0;                      % Mass fraction of condensed phase at nozzle exit

% Conversion factors
lbf = 0.22480894387096;     % 1 N = 0.22480894387096 lbf
inch = 39.37007874;         % 1 m = 39.37007874 inches
psia = 1.4503773800722E-4;  % 1 Pa = 0.00014503773800722 psia