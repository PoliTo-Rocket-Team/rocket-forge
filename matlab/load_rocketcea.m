if cea == 1
    % Run rocketcea
    disp('Running rocketcea...')
    pystr = sprintf('../python/rocketcea-matlab.py %s %s %f %f %f %f %f %d', Oxidizer, Fuel, pc, MR, epsilon, epsc, At, N);
    x = pyrunfile(pystr, "x");

    % Output (TODO)
    Te = double(x(1));
    Tc = double(x(2));
    we = double(x(3));
    cstar = double(x(4));
    Is_vac = double(x(5));
    pe = double(x(6));
    Is_vac_frozen = double(x(7));
    clear x
    
else
    % Load rocketcea input file (TODO)
    disp('Rocketcea is disabled. Loading preexisting data...')
    Te = 2523.94;
    Tc = 3370.19;
    we = 1094.74 * 2.20581;
    cstar = 1859.64182;
    Is_vac = 292.0319;
    pe = 327862.74;
    Is_vac_frozen = 284.28542;
    
end