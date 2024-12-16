from numpy import sqrt, pi
import rocketforge.thermal.config as config
import rocketforge.performance.config as pconf


def bartz(M, A, gamma, T_wg):
    R_t = sqrt(pconf.At / pi)
    sigma = (
        (0.5 * (T_wg / config.T_c) * (1.0 + (gamma - 1.0) / 2.0 * M**2.0) + 0.5)**(-0.68) 
        * (1.0 + (gamma - 1.0) / 2.0 * M**2.0)**(-0.12)
    )
    h_gas = (
        0.026 / (2.0 * R_t) ** 0.2
        * config.mu_0**0.2
        * config.cp_0 / config.Pr_0**0.6
        * (pconf.pc / pconf.cstar_d) ** 0.8
        * (4.0 / (config.RnOvRt + config.R1OvRt)) ** 0.1
        * (pconf.At / A) ** 0.9
        * sigma
        / config.tuning_factor
    )
    return h_gas


def rad(e, T):
    q_rad = e * 5.670374419e-8 * T**4
    return q_rad
