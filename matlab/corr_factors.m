%% Compute correction factors
disp('Computing correction factors...')

% Finite reaction rate combustion factor
er1 = 0.34 - 0.34 * Is_vac_frozen / Is_vac;
er2 = max(0, 0.021 - 0.01 * log(pc / 2 / 10^6));
z_r = (1 - er1) * (1 - er2);

% Multi-phase loss factor
z_zw = 1 - Z * Cs / we^2 * (Tc - Te * (1 + log(Tc / Te)));
z_zt = 1 - Z / 2;
z_z = 0.2 * z_zw + 0.8 * z_zt;

% Friction loss factor
z_f = 0.997732 - 0.403077 * (pc * rt) ^ (-0.5598);

% Divergence loss factor
alpha = atan((re - rt) / Le);
z_d = 0.5 * (1 + cos((alpha + theta_ex) / 2));

% Drag correction factor
z_drag = z_r * z_f * z_z;

% Nozzle correction factor
z_n = z_f * z_d * z_z;

% Chamber correction factor
z_c = z_r;