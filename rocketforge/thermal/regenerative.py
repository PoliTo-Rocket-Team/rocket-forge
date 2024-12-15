from numpy import *
import matplotlib.pyplot as plt
import rocketforge.thermal.config as config
import rocketforge.performance.config as pconf
import rocketforge.geometry.convergent as convergent
import rocketforge.geometry.top as top
import rocketforge.geometry.conical as conical
from rocketforge.thermal.heat_flux import bartz
from rocketprops.rocket_prop import get_prop


class Regen():
    def run(self):
        P = get_prop(config.coolant)
        X, Y = get_geometry()

        L_tot = config.L_c + config.L_e
        x = linspace(0.0, L_tot, config.n_stations)
        R = interp(x, X, Y)
        A = pi * R**2.0
        A_w = 2.0 * pi * R * L_tot / config.n_stations

        M = generate_profile(x, 0.0, 1.0, config.M_e, R)
        Pr = generate_profile(x, config.Pr_0, config.Pr_t, config.Pr_e, R)
        gamma = generate_profile(x, config.gamma, config.gamma, config.gamma_e, R)

        b = generate_profile(x, config.b1, config.b2, config.b3, R)
        C = 2.0 * pi * (R + config.t_w + b / 2.0)
        if config.NC:
            NC = config.NC
            if config.a1:
                a = generate_profile(x, config.a1, config.a2, config.a3, R)
                delta = C / NC - a
            else:
                delta = generate_profile(x, config.d1, config.d2, config.d3, R)
                a = C / NC - delta
        else:
            a = generate_profile(x, config.a1, config.a2, config.a3, R)
            delta = generate_profile(x, config.d1, config.d2, config.d3, R)
            NC = C / (a + delta)
        d_e = 2.0 * a * b / (a + b)
        p = linspace(config.pcoOvpc * pconf.pc, config.p_ci, config.n_stations)

        T_aw = (
            config.T_c
            * (1.0 + Pr**0.33 * (gamma - 1.0) / 2.0 * M**2.0)
            / (1.0 + (gamma - 1.0) / 2.0 * M**2.0)
        )

        T_wg = full(config.n_stations, config.T_ci)
        T_wc = full(config.n_stations, config.T_ci)
        T_c = full(config.n_stations, config.T_ci)
        cp_c = [P.CpAtTdegR(T_c[i] * 1.8) * 4186.8 for i in range(config.n_stations)]
        mu_c = zeros(config.n_stations)
        lambda_c = zeros(config.n_stations)

        iter = 0
        while True:
            iter += 1

            h = bartz(M, A, gamma, T_wg)
            q = h * (T_aw - T_wg)
            
            dT_c = q * A_w / config.m_dot_c / cp_c
            for i in reversed(range(config.n_stations)):
                if i != config.n_stations - 1:
                    T_c[i] = T_c[i + 1] + dT_c[i]
            
            for i in range(config.n_stations):
                cp_c[i] = P.CpAtTdegR(T_c[i] * 1.8) * 4186.8
                mu_c[i] = P.Visc_compressed(T_c[i] * 1.8, p[i] / 6894.75728) / 10.0
                lambda_c[i] = P.CondAtTdegR(T_c[i] * 1.8) * 1.72958

            Re_c = config.m_dot_c / a / b / NC * d_e / mu_c
            Pr_c = mu_c * cp_c / lambda_c
            Nu = 0.023 * Re_c**0.8 * Pr_c**0.4
            h_c = Nu * lambda_c / d_e
            h_c0 = h_c

            for i in range(config.max_iter):
                xi = sqrt(2.0 * h_c / delta / config.lambda_w) * b
                eta_f = a / (a + delta) + 2.0 * b / (a + delta) * tanh(xi) / xi
                hc_old = h_c
                h_c = h_c0 * eta_f
                if all(abs((hc_old - h_c)/hc_old) < 0.01):
                    break

            T_wc = T_c + q / h_c
            T_wg_new = T_wc + q * config.t_w / config.lambda_w

            if all(abs((T_wg - T_wg_new) / T_wg) < 0.05) or iter == config.max_iter:
                T_wg = T_wg_new
                break

            T_wg = (1.0 - config.stability) * T_wg + config.stability * T_wg_new
        
        self.x = x
        self.T_wg = T_wg
        self.T_wc = T_wc
        self.T_c = T_c
        self.q = q
        self.a = a
        self.b = b
        self.delta = delta
        self.X = X
        self.Y = Y

    def plot_T(self):
        _, ax = plt.subplots()
        ax.plot(self.x, self.T_wg, label="Twg")
        ax.plot(self.x, self.T_wc, label="Twc")
        ax.plot(self.x, self.T_c, label="Tc")
        ax.set_xlabel("x [m]")
        ax.set_ylabel("Temperature [K]")
        ax.grid()
        ax.legend(loc="upper right")
        axt = ax.twinx()
        axt.plot(self.X, self.Y, color="black", label="Thrust chamber contour")
        axt.set_ylabel("Radius [m]")
        axt.axis([0, max(self.x), 0, max(self.x)])
        axt.legend(loc="upper left")
        plt.title("Temperature distribution")
        plt.show()

    def plot_q(self):
        _, ax = plt.subplots()
        ax.plot(self.x, self.q / 1000, label="Heat flux")
        ax.set_xlabel("x [m]")
        ax.set_ylabel("Heat flux [kW/m^2]")
        ax.grid()
        ax.legend(loc="upper right")
        axt = ax.twinx()
        axt.plot(self.X, self.Y, color="black", label="Thrust chamber contour")
        axt.set_ylabel("Radius [m]")
        axt.axis([0, max(self.x), 0, max(self.x)])
        axt.legend(loc="upper left")
        plt.title("Heat flux distribution")
        plt.show()

    def plot_g(self):
        _, ax = plt.subplots()
        ax.plot(self.x, self.a, label="a")
        ax.plot(self.x, self.b, label="b")
        ax.plot(self.x, self.delta, label="delta")
        ax.set_xlabel("x [m]")
        ax.set_ylabel("Length [m]")
        ax.grid()
        ax.legend(loc="upper right")
        ax.axis([0, max(self.x), 0, 1.5 * max([max(self.a), max(self.b), max(self.delta)])])
        axt = ax.twinx()
        axt.plot(self.X, self.Y, color="black", label="Thrust chamber contour")
        axt.set_ylabel("Radius [m]")
        axt.axis([0, max(self.x), 0, max(self.x)])
        axt.legend(loc="upper left")
        plt.title("Cooling channels")
        plt.show()

    def details(self):
        pass


def get_geometry():
    XC, YC = convergent.get(
        pconf.At,
        config.R1OvRt,
        config.L_c,
        radians(config.b),
        config.R2OvR2max,
        pconf.epsc,
    )
    if config.shape == 0:
        XD, YD = conical.get(
            pconf.At,
            config.RnOvRt,
            pconf.eps,
            config.L_e,
            radians(config.theta)
        )
    else:
        XD, YD = top.get(
            pconf.At,
            config.RnOvRt,
            config.L_e,
            radians(config.thetan),
            radians(config.thetae),
            pconf.eps,
        )
    X = concatenate([XC, XD]) + config.L_c
    Y = concatenate([YC, YD])
    return X, Y


def generate_profile(x, y_c, y_t, y_e, R):
    R_t = sqrt(pconf.At / pi)
    R_e = R_t * sqrt(pconf.eps)
    R_c = R_t * sqrt(pconf.epsc)
    return piecewise(
        x,
        [
            x <= config.L_c,
            x > config.L_c,
        ],
        [
            lambda _: y_c * (R[x <= config.L_c] - R_t) / (R_c - R_t) + y_t * (R_c - R[x <= config.L_c]) / (R_c - R_t),
            lambda _: y_t * (R_e - R[x > config.L_c]) / (R_e - R_t) + y_e * (R[x > config.L_c] - R_t) / (R_e - R_t),
        ],
    )
