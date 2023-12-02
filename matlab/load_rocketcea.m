% Run rocketcea
disp('Running rocketcea...')
pystr = sprintf('../python/rocketcea.py %s %s %f %f %f %f %f %d', Oxidizer, Fuel, pc, MR, epsilon, epsc, At, N);
x = pyrunfile(pystr, "x");

% Output (TODO)
Te = double(x(1));
Tc = double(x(2));
we = double(x(3));

clear x