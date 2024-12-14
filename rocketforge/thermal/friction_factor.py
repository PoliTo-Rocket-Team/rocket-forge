from numpy import log, real, linspace
from scipy.special import lambertw
import matplotlib.pyplot as plt


def moody(Re_c, roughness):
    """Moody (1947)"""
    return 0.0055 * (1 + (2.0 * 10**4 * roughness + 10**6 / Re_c) ** (1.0 / 3.0))


def tkachenko(Re_c, roughness):
    """Tkachenko, Mileikovskyi (2020)"""
    A0 = -0.79638 * log(roughness / 8.208 + 7.3357 / Re_c)
    A1 = Re_c * roughness + 9.3120665 * A0
    return (
        (8.128943 + A1) / (8.128943 * A0 - 0.86859209 * A1 * log(A1 / 3.7099535 / Re_c))
    ) ** 2


def colebrook_white(Re_c, roughness):
    """Colebrook-White (1937)"""
    a = 2.51 / Re_c
    b = 4 * roughness / 14.8
    return real(
        (2.0 * lambertw(log(10) / (2 * a) * 10.0 ** (b / (2 * a))) / log(10) - b / a)
        ** (-2)
    )


if __name__ == "__main__":
    # Input parameters
    Re_c = 50000
    roughness = linspace(0, 0.25, 1000)

    # Compute results
    f1 = moody(Re_c, roughness)
    f2 = tkachenko(Re_c, roughness)
    f3 = colebrook_white(Re_c, roughness)

    # Print results
    plt.plot(roughness, f1, label="Moody (1947)")
    plt.plot(roughness, f2, label="Tkachenko, Mileikovskyi (2020)")
    plt.plot(roughness, f3, label="Colebrook-White (1937)")
    plt.legend()
    plt.grid()
    plt.xlabel("Relative roughness")
    plt.ylabel("Friction factor")
    plt.show()
