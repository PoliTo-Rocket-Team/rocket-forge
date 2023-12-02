if cea == 1
    % Run rocketcea
    disp('Running rocketcea...')
    pystr = sprintf('../python/rocketcea-matlab.py %s %s %f %f %f %f %f %d', Oxidizer, Fuel, pc, MR, epsilon, epsc, At, N);
    x = pyrunfile(pystr, "x");

    % Output (TODO)
    Te = double(x(1));
    Tc = double(x(2));
    we = double(x(3));
    
    clear x
    
else
    % Load rocketcea input file (TODO)
    disp('Rocketcea is disabled. Loading preexisting data...')
    Te = 2554.31;
    Tc = 3370.19;
    we = 1094.74 * 2.20581;
end