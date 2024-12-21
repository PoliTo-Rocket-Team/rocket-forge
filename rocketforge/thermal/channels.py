from numpy import *
import pyvista as pv


def plot_3D(x, R, a, b, delta, NC, t_w):
    phi = a / (R + t_w + b/2)
    phi_d = delta / (R + t_w + b/2)
    ntheta = 180
    theta = linspace(0, 2*pi, ntheta)
    alpha = zeros((len(phi), 5))
    x_channels = tile(x, (5, 1)).T

    X = outer(x, ones((1, ntheta)))
    Y_inner = outer(R, cos(theta))
    Z_inner = outer(R, sin(theta))
    Y_outer = outer(R + t_w, cos(theta))
    Z_outer = outer(R + t_w, sin(theta))

    plotter = pv.Plotter(title="Regenerative cooling channels")
    plotter.add_mesh(pv.StructuredGrid(X, Y_inner, Z_inner), color="#727472")
    plotter.add_mesh(pv.StructuredGrid(X, Y_outer, Z_outer), color="#727472")

    for k in range(int(NC)):
        for i in range(len(phi)):
            alpha[i, :] = linspace((2*k - 1) * pi / NC, (2*k + 1) * pi / NC, 5)

        z_inner = (R)[:, newaxis] * cos(alpha)
        z_outer = (R + t_w)[:, newaxis] * cos(alpha)
        y_inner = (R)[:, newaxis] * sin(alpha)
        y_outer = (R + t_w)[:, newaxis] * sin(alpha)

        plotter.add_mesh(pv.StructuredGrid(
            c_[x_channels[-1, :], x_channels[-1, :]], 
            c_[y_inner[-1, :], y_outer[-1, :]],
            c_[z_inner[-1, :], z_outer[-1, :]],
        ), color="#727472")
        plotter.add_mesh(pv.StructuredGrid(
            c_[x_channels[0, :], x_channels[0, :]], 
            c_[y_inner[0, :], y_outer[0, :]],
            c_[z_inner[0, :], z_outer[0, :]],
        ), color="#727472")

    for k in range(int(NC)):
        for i in range(len(phi)):
            alpha[i, :] = linspace(-phi[i] / 2 + k * 2 * pi / NC, phi[i] / 2 + k * 2 * pi / NC, 5)

        z_inner = (R + t_w)[:, newaxis] * cos(alpha)
        z_outer = (R + t_w + b)[:, newaxis] * cos(alpha)
        y_inner = (R + t_w)[:, newaxis] * sin(alpha)
        y_outer = (R + t_w + b)[:, newaxis] * sin(alpha)

        plotter.add_mesh(pv.StructuredGrid(
            x_channels[:, :5],
            c_[y_inner[:, 0], y_outer[:, 0], y_outer[:, -1], y_inner[:, -1], y_inner[:, 0]],
            c_[z_inner[:, 0], z_outer[:, 0], z_outer[:, -1], z_inner[:, -1], z_inner[:, 0]],
        ), color="#D95319", opacity=0.5)
        plotter.add_mesh(pv.StructuredGrid(
            c_[x_channels[-1, :], x_channels[-1, :]], 
            c_[y_inner[-1, :], y_outer[-1, :]],
            c_[z_inner[-1, :], z_outer[-1, :]],
        ), color="#D95319", opacity=0.5)
        plotter.add_mesh(pv.StructuredGrid(
            c_[x_channels[0, :], x_channels[0, :]], 
            c_[y_inner[0, :], y_outer[0, :]],
            c_[z_inner[0, :], z_outer[0, :]],
        ), color="#D95319", opacity=0.5)

    for k in range(int(NC)):
        for i in range(len(phi)):
            alpha[i, :] = linspace(phi[i] / 2 + k * 2 * pi / NC, phi[i] / 2 + phi_d[i] + k * 2 * pi / NC, 5)

        z_inner = (R + t_w)[:, newaxis] * cos(alpha)
        z_outer = (R + t_w + b)[:, newaxis] * cos(alpha)
        y_inner = (R + t_w)[:, newaxis] * sin(alpha)
        y_outer = (R + t_w + b)[:, newaxis] * sin(alpha)

        plotter.add_mesh(pv.StructuredGrid(
            x_channels[:, :5],
            c_[y_inner[:, 0], y_outer[:, 0], y_outer[:, -1], y_inner[:, -1], y_inner[:, 0]],
            c_[z_inner[:, 0], z_outer[:, 0], z_outer[:, -1], z_inner[:, -1], z_inner[:, 0]],
        ), color="#727472")
        plotter.add_mesh(pv.StructuredGrid(
            c_[x_channels[-1, :], x_channels[-1, :]], 
            c_[y_inner[-1, :], y_outer[-1, :]],
            c_[z_inner[-1, :], z_outer[-1, :]],
        ), color="#727472")
        plotter.add_mesh(pv.StructuredGrid(
            c_[x_channels[0, :], x_channels[0, :]], 
            c_[y_inner[0, :], y_outer[0, :]],
            c_[z_inner[0, :], z_outer[0, :]],
        ), color="#727472")

    plotter.set_background('#242424')
    plotter.add_axes(color="#fafafa")

    plotter.show()
