from math import sqrt, log, atan, cos, pi


def correction_factors(pc, eps, At, Le, theta_ex, Is_v, Is_v_fr, Tc, Te, we, Z, Cs):
    # Geometry
    Ae = At * eps
    re = sqrt(Ae / pi)
    rt = sqrt(At / pi)

    # Finite reaction rate combustion factor
    er1 = 0.34 - 0.34 * Is_v_fr / Is_v
    er2 = max(0, 0.021 - 0.01 * log(pc / 2 / 10**6))
    z_r = (1 - er1) * (1 - er2)

    # Multi-phase loss factor
    z_zw = 1 - Z * Cs / we**2 * (Tc - Te * (1 + log(Tc / Te)))
    z_zt = 1 - Z / 2
    z_z = 0.2 * z_zw + 0.8 * z_zt

    # Divergence loss factor
    alpha = atan((re - rt) / Le)
    z_d = 0.5 * (1 + cos((alpha + theta_ex) / 2))

    # Friction loss factor
    # Coefficients from NASA SP8120 Boundary Layer Loss Recommendation
    a = 0.13956490814036465
    b = 0.4839954048378114
    c = -1.5290708783162201
    d = 1.8872208607881908
    e = 1.2281287531868839
    f = 1.1165014352424605
    g = 0.08873349847277191
    pxd = 2 * pc * rt * 0.00014503773800722 * 39.37007874
    loss = g*eps/pxd + (c + d * log(e + eps*f))/( a + b*log(pxd))
    z_f = (100.0 - loss) / 100.0

    # Nozzle correction factor
    z_n = z_f * z_d * z_z

    # Overall correction factor
    z_overall = z_n * z_r

    return z_r, z_n, z_overall, z_f, z_d, z_z