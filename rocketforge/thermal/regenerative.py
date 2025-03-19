from numpy import *
import matplotlib.pyplot as plt
import rocketforge.thermal.config as config
import rocketforge.performance.config as pconf
import rocketforge.geometry.convergent as convergent
import rocketforge.geometry.top as top
import rocketforge.geometry.conical as conical
import rocketforge.thermal.channels as channels
from rocketforge.thermal.friction_factor import moody, tkachenko, colebrook_white
from rocketforge.thermal.heat_flux import bartz, rad
from rocketprops.rocket_prop import get_prop
from tkinter.filedialog import asksaveasfilename


class Regen():
    def run(self):
        P = get_prop(config.coolant)
        X, Y = get_geometry()

        L_tot = config.L_c + config.L_e
        self.x = linspace(0.0, L_tot, config.n_stations)
        self.R = interp(self.x, X, Y)
        A = pi * self.R**2.0
        A_w = 2.0 * pi * self.R * L_tot / config.n_stations

        M = generate_profile(self.x, 0.0, 1.0, config.M_e, self.R)
        Pr = generate_profile(self.x, config.Pr_0, config.Pr_t, config.Pr_e, self.R)
        gamma = generate_profile(self.x, config.gamma, config.gamma, config.gamma_e, self.R)

        self.set_channels()

        a = self.a
        b = self.b
        delta = self.delta

        NC = full(config.n_stations, config.NC)
        d_e = 2.0 * a * b / (a + b)

        if config.enable_dp:
            p = full(config.n_stations, config.pcoOvpc * pconf.pc)
            rho_c = zeros(config.n_stations)
            dp1 = zeros(config.n_stations)
            dp2 = zeros(config.n_stations)
            dp3 = zeros(config.n_stations)
        else:
            p = linspace(config.pcoOvpc * pconf.pc, config.p_ci, config.n_stations)

        T_aw = (
            config.T_c
            * (1.0 + Pr**0.33 * (gamma - 1.0) / 2.0 * M**2.0)
            / (1.0 + (gamma - 1.0) / 2.0 * M**2.0)
        )

        T_wg = full(config.n_stations, config.T_ci)
        T_wc = full(config.n_stations, config.T_ci)
        T_c = full(config.n_stations, config.T_ci)
        cp_c = full(config.n_stations, P.CpAtTdegR(config.T_ci * 1.8) * 4186.8)
        mu_c = zeros(config.n_stations)
        lambda_c = zeros(config.n_stations)

        iter = 0
        while True:
            iter += 1

            h = bartz(M, A, gamma, T_wg)
            q = h * (T_aw - T_wg)
            
            if config.rad:
                q_rad = full(config.n_stations, 0.0) # TODO
                q_rc = rad(config.eps_w, T_wc)
                q += q_rad - q_rc

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

            if config.enable_dp:
                for i in range(config.n_stations):
                    rho_c[i] = P.SG_compressed(T_c[i] * 1.8, p[i] / 6894.75728) * 1000.0
                u_c = Re_c * mu_c / d_e / rho_c
                roughness = config.absolute_roughness / d_e

                if config.dp_method == 0:
                    f = tkachenko(Re_c, roughness)
                elif config.dp_method == 1:
                    f = moody(Re_c, roughness)
                elif config.dp_method == 2:
                    f = colebrook_white(Re_c, roughness)

                dp1 = 0.5 * rho_c * u_c**2 * f * L_tot / config.n_stations / d_e

                for i in range(config.n_stations - 1):
                    ratio = d_e[i] / d_e[i + 1]
                    if ratio > 1.0:
                        _K = (ratio**2 - 1.0)**2
                    else:
                        _K = 0.5 - 0.167 * ratio - 0.125 * ratio**2 - 0.208 * ratio**3
                    dp2[i] = 0.5 * rho_c[i] * u_c[i]**2 * _K
                    dp3[i] = (
                        (2.0/(a[i]*b[i] + a[i+1]*b[i+1]))
                        * (1.0/(a[i+1]*b[i+1]) - 1.0/(a[i]*b[i]))
                        / rho_c[i] / NC[i]**2 * config.m_dot_c**2
                    )

                dp = dp1 + dp2 + dp3

                for i in range(config.n_stations):
                    if i != 0:
                        p[i] = p[i - 1] + dp[i]

            if all(abs((T_wg - T_wg_new) / T_wg) < 0.05) or iter == config.max_iter:
                T_wg = T_wg_new
                break

            T_wg = (1.0 - config.stability) * T_wg + config.stability * T_wg_new
        
        if config.enable_dp:
            Dp = sum(dp)

        self.T_wg = T_wg
        self.T_wc = T_wc
        self.T_c = T_c
        self.q = q
        self.X = X
        self.Y = Y

        if config.rad:
            self.q_rad = q_rad
            self.q_rc = q_rc

        if config.enable_dp:
            self.p = p
            self.dp1 = dp1
            self.dp2 = dp2
            self.dp3 = dp3
            self.Dp = Dp

    def plot_p(self):
        _, ax = plt.subplots()
        ax.plot(self.x, self.p / 100000, label="Coolant pressure")
        ax.plot(self.x, self.dp1 / 100000, label="Friction losses")
        ax.plot(self.x, self.dp2 / 100000, label="Geometric losses")
        ax.plot(self.x, self.dp3 / 100000, label="Acceleration losses")
        ax.set_xlabel("x [m]")
        ax.set_ylabel("Pressure [bar]")
        ax.grid()
        ax.legend(loc="upper right")
        axt = ax.twinx()
        axt.plot(self.X, self.Y, color="black", label="Thrust chamber contour")
        axt.set_ylabel("Radius [m]")
        axt.axis([0, max(self.x), 0, max(self.x)])
        axt.legend(loc="upper left")
        plt.title(f"Coolant Pressure (total losses: {self.Dp / 100000:.2f} bar)")
        plt.show()

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
        ax.axis([0, max(self.x), 0, 1.2 * max(self.T_wg)])
        axt.plot(self.X, self.Y, color="black", label="Thrust chamber contour")
        axt.set_ylabel("Radius [m]")
        axt.axis([0, max(self.x), 0, max(self.x)])
        axt.legend(loc="upper left")
        plt.title("Temperature distribution")
        plt.show()

    def plot_q(self):
        _, ax = plt.subplots()
        ax.plot(self.x, self.q / 1000, label="Total Heat flux")
        if config.rad:
            ax.plot(self.x, (self.q - self.q_rad + self.q_rc) / 1000, label="Convective heat flux")
            ax.plot(self.x, self.q_rad / 1000, label="Radiation heat flux")
            ax.plot(self.x, self.q_rc / 1000, label="Radiation cooling heat flux")
        ax.set_xlabel("x [m]")
        ax.set_ylabel("Heat flux [kW/m^2]")
        ax.grid()
        ax.legend(loc="upper right")
        ax.axis([0, max(self.x), 0, 1.2 * max(self.q) / 1000])
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

    def plot_3D(self):
        channels.plot_3D(self.x, self.R, self.a, self.b, self.delta, config.NC, config.t_w, config.t_eOvt_w)

    def set_a(self):
        Rt = sqrt(pconf.At / pi)
        C1 = 2.0 * pi * (Rt * sqrt(pconf.epsc) + config.t_w + config.b1 / 2.0)
        config.a1 = C1 / config.NC - config.d1
        C2 = 2.0 * pi * (Rt + config.t_w + config.b2 / 2.0)
        config.a2 = C2 / config.NC - config.d2
        C3 = 2.0 * pi * (Rt * sqrt(pconf.eps) + config.t_w + config.b3 / 2.0)
        config.a3 = C3 / config.NC - config.d3

    def set_delta(self):
        Rt = sqrt(pconf.At / pi)
        C1 = 2.0 * pi * (Rt * sqrt(pconf.epsc) + config.t_w + config.b1 / 2.0)
        config.d1 = C1 / config.NC - config.a1
        C2 = 2.0 * pi * (Rt + config.t_w + config.b2 / 2.0)
        config.d2 = C2 / config.NC - config.a2
        C3 = 2.0 * pi * (Rt * sqrt(pconf.eps) + config.t_w + config.b3 / 2.0)
        config.d3 = C3 / config.NC - config.a3

    def set_channels(self):
        self.set_delta
        self.a = generate_profile(self.x, config.a1, config.a2, config.a3, self.R)
        self.b = generate_profile(self.x, config.b1, config.b2, config.b3, self.R)
        self.delta = generate_profile(self.x, config.d1, config.d2, config.d3, self.R)

    def details(self):
        pass

    def print_g(self):
        try:
            with open(asksaveasfilename(defaultextension=".csv"), "w") as f:
                f.write(f"{self.x[0]:.7f},{self.a[0]:.7f},0\n")
                for i in range(1, len(self.x)):
                    if self.x[i] != self.x[i-1]:
                        f.write(f"{self.x[i]:.7f},{self.a[i]:.7f},0\n")
            with open(asksaveasfilename(defaultextension=".csv"), "w") as f:
                f.write(f"{self.x[0]:.7f},{self.b[0]:.7f},0\n")
                for i in range(1, len(self.x)):
                    if self.x[i] != self.x[i-1]:
                        f.write(f"{self.x[i]:.7f},{self.b[i]:.7f},0\n")
        except Exception:
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
            lambda _: (
                y_c * (R[x <= config.L_c] - R_t) / (R_c - R_t)
                + y_t * (R_c - R[x <= config.L_c]) / (R_c - R_t)
            ),
            lambda _: (
                y_e * (R[x  > config.L_c] - R_t) / (R_e - R_t)
                + y_t * (R_e - R[x  > config.L_c]) / (R_e - R_t)
            ),
        ],
    )
