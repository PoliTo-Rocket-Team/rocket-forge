%% Delivered performance
disp('Computing delivered performance...')

% Characteristic velocity
cstar_d = z_c * cstar;

% Mass flow
m_d = pc * At / cstar_d;
m_f_d = m_d / (MR + 1);
m_ox_d = m_f_d * MR;

% Specific impulse
Fe = Ae / m_d;
Is_vac_d = z_c * z_n * Is_vac;
Is_opt_d = Is_vac_d - Fe * pe / 9.80655;
Is_SL_d = Is_vac_d - Fe * pSL / 9.80655;

% Thrust coefficient
CF_vac_d = Is_vac_d * 9.80655 / cstar_d;
CF_opt_d = Is_opt_d * 9.80655 / cstar_d;
CF_SL_d = Is_SL_d * 9.80655 / cstar_d;

% Chamber thrust
T_vac_d = CF_vac_d * At * pc;
T_opt_d = CF_opt_d * At * pc;
T_SL_d = CF_SL_d * At * pc;
