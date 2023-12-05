%% Compute correction factors
disp('Computing correction factors...')

% Finite reaction rate combustion factor
er1 = (h0 / rt)^a * (pSL / pc)^b * log10(re /rt);
er2 = max(0, 0.021 - 0.01 * log(pc / 2 / 10^6));
z_r = (1 - er1) * (1 - er2);

% Multi-phase loss factor
z_zw = 1 - Z * Cs / we^2 * (Tc - Te * (1 + log(Tc / Te)));
z_zt = 1 - Z / 2;
z_z = 0.2 * z_zw + 0.8 * z_zt;

% Divergence loss factor
alpha = atan((re - rt) / Le);
z_d = 0.5 * (1 + cos((alpha + theta_ex) / 2));

% Drag correction factor
z_drag = z_r * z_f * z_z;

% Nozzle correction factor
z_n = z_f * z_d * z_z;

% Chamber correction factor
z_c = z_r;