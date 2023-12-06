if cea == 1
    % Run rocketcea
    disp('Running rocketcea...')
    pystr = sprintf('../python/rocketcea-matlab.py %s %s %f %f %f %f %f %d', Oxidizer, Fuel, pc, MR, epsilon, epsc, At, N);
    x = pyrunfile(pystr, "x");

    % Output
    p = double(x{1});
    Temp = double(x{2});
    rho = double(x{3});
    cp = double(x{4});
    mu = double(x{5});
    l = double(x{6});
    Pr = double(x{7});
    gamma = double(x{8});
    M = double(x{9});
    a = double(x{10});
    H = double(x{11});
    cstar = double(x(12));
    m = double(x(13));
    mf = double(x(14));
    mox = double(x(15));
    we = double(x(16));
    Is_SL = double(x(17));
    Is_opt = double(x(18));
    Is_vac = double(x(19));
    Is_vac_frozen = double(x(20));
    CF_SL = double(x(21));
    CF_opt = double(x(22));
    CF_vac = double(x(23));
    T_sl = double(x(24));
    T_opt = double(x(25));
    T_vac = double(x(26));

    clear x

    Te = Temp(end);
    Tc = Temp(1);
    pe = p(end);

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