from numpy import *
import pyvista as pv


def plot_3D(x, R, a, b, delta, NC, t_w):
    chamber_color = "#727472"
    coolant_color = "#D95319"

    phi = a / (R + t_w + b/2)
    phi_d = phi * delta / a
    ntheta = 180 * 5
    theta = linspace(0, 2*pi, ntheta)
    alpha = zeros((len(phi), 5))
    x_channels = tile(x, (5, 1)).T

    plotter = pv.Plotter(title="Regenerative cooling channels")

    X = outer(x, ones((1, ntheta)))
    X0 = outer([x[0], x[0]], ones((1, ntheta)))
    Xe = outer([x[-1], x[-1]], ones((1, ntheta)))

    Y_inner = outer(R, cos(theta))
    Z_inner = outer(R, sin(theta))
    inner = plotter.add_mesh(pv.StructuredGrid(X, Y_inner, Z_inner), color=chamber_color)

    Y_inner_ext = outer(R + t_w, cos(theta))
    Z_inner_ext = outer(R + t_w, sin(theta))
    inner_ext = plotter.add_mesh(pv.StructuredGrid(X, Y_inner_ext, Z_inner_ext), color=chamber_color)

    Y0_inner = outer([R[0], R[0] + t_w], cos(theta))
    Z0_inner = outer([R[0], R[0] + t_w], sin(theta))
    inner0 = plotter.add_mesh(pv.StructuredGrid(X0, Y0_inner, Z0_inner), color=chamber_color)

    Ye_inner = outer([R[-1], R[-1] + t_w], cos(theta))
    Ze_inner = outer([R[-1], R[-1] + t_w], sin(theta))
    innere = plotter.add_mesh(pv.StructuredGrid(Xe, Ye_inner, Ze_inner), color=chamber_color)

    Y_outer_int = outer(R + t_w + b, cos(theta))
    Z_outer_int = outer(R + t_w + b, sin(theta))
    outer_int = plotter.add_mesh(pv.StructuredGrid(X, Y_outer_int, Z_outer_int), color=chamber_color)

    Y_outer = outer(R + 5 * t_w + b, cos(theta))
    Z_outer = outer(R + 5 * t_w + b, sin(theta))
    outerc = plotter.add_mesh(pv.StructuredGrid(X, Y_outer, Z_outer), color=chamber_color)

    Y0_outer = outer([R[0] + t_w + b[0], R[0] + 5 * t_w + b[0]], cos(theta))
    Z0_outer = outer([R[0] + t_w + b[0], R[0] + 5 * t_w + b[0]], sin(theta))
    outer0 = plotter.add_mesh(pv.StructuredGrid(X0, Y0_outer, Z0_outer), color=chamber_color)

    Ye_outer = outer([R[-1] + t_w + b[-1], R[-1] + 5 * t_w + b[-1]], cos(theta))
    Ze_outer = outer([R[-1] + t_w + b[-1], R[-1] + 5 * t_w + b[-1]], sin(theta))
    outere = plotter.add_mesh(pv.StructuredGrid(Xe, Ye_outer, Ze_outer), color=chamber_color)

    # Cooling channels
    channels = []
    for k in range(int(NC)):
        for i in range(len(phi)):
            alpha[i, :] = linspace(-phi[i] / 2 + k * 2 * pi / NC, phi[i] / 2 + k * 2 * pi / NC, 5)

        z_inner = (R + t_w)[:, newaxis] * cos(alpha)
        z_outer = (R + t_w + b)[:, newaxis] * cos(alpha)
        y_inner = (R + t_w)[:, newaxis] * sin(alpha)
        y_outer = (R + t_w + b)[:, newaxis] * sin(alpha)

        c = plotter.add_mesh(pv.StructuredGrid(
            x_channels[:, :5],
            c_[y_inner[:, 0], y_outer[:, 0], y_outer[:, -1], y_inner[:, -1], y_inner[:, 0]],
            c_[z_inner[:, 0], z_outer[:, 0], z_outer[:, -1], z_inner[:, -1], z_inner[:, 0]],
        ), color=coolant_color, opacity=0.5)
        ce = plotter.add_mesh(pv.StructuredGrid(
            c_[x_channels[-1, :], x_channels[-1, :]], 
            c_[y_inner[-1, :], y_outer[-1, :]],
            c_[z_inner[-1, :], z_outer[-1, :]],
        ), color=coolant_color, opacity=0.5)
        c0 = plotter.add_mesh(pv.StructuredGrid(
            c_[x_channels[0, :], x_channels[0, :]], 
            c_[y_inner[0, :], y_outer[0, :]],
            c_[z_inner[0, :], z_outer[0, :]],
        ), color=coolant_color, opacity=0.5)
        channels.append(c)
        channels.append(c0)
        channels.append(ce)

    # Ribs
    ribs = []
    for k in range(int(NC)):
        for i in range(len(phi)):
            alpha[i, :] = linspace(phi[i] / 2 + k * 2 * pi / NC, phi[i] / 2 + phi_d[i] + k * 2 * pi / NC, 5)

        z_inner = (R + t_w)[:, newaxis] * cos(alpha)
        z_outer = (R + t_w + b)[:, newaxis] * cos(alpha)
        y_inner = (R + t_w)[:, newaxis] * sin(alpha)
        y_outer = (R + t_w + b)[:, newaxis] * sin(alpha)

        r = plotter.add_mesh(pv.StructuredGrid(
            x_channels[:, :5],
            c_[y_inner[:, 0], y_outer[:, 0], y_outer[:, -1], y_inner[:, -1], y_inner[:, 0]],
            c_[z_inner[:, 0], z_outer[:, 0], z_outer[:, -1], z_inner[:, -1], z_inner[:, 0]],
        ), color=chamber_color)
        re = plotter.add_mesh(pv.StructuredGrid(
            c_[x_channels[-1, :], x_channels[-1, :]], 
            c_[y_inner[-1, :], y_outer[-1, :]],
            c_[z_inner[-1, :], z_outer[-1, :]],
        ), color=chamber_color)
        r0 = plotter.add_mesh(pv.StructuredGrid(
            c_[x_channels[0, :], x_channels[0, :]], 
            c_[y_inner[0, :], y_outer[0, :]],
            c_[z_inner[0, :], z_outer[0, :]],
        ), color=chamber_color)
        ribs.append(r)
        ribs.append(r0)
        ribs.append(re)

    def toggle_inner(flag):
        inner.SetVisibility(flag)
        inner_ext.SetVisibility(flag)
        inner0.SetVisibility(flag)
        innere.SetVisibility(flag)

    def toggle_ribs(flag):
        for rib in ribs:
            rib.SetVisibility(flag)

    def toggle_channels(flag):
        for channel in channels:
            channel.SetVisibility(flag)

    def toggle_outer(flag):
        outer_int.SetVisibility(flag)
        outerc.SetVisibility(flag)
        outer0.SetVisibility(flag)
        outere.SetVisibility(flag)

    def toggle_parallel(flag):
        if flag:
            plotter.enable_parallel_projection()
        else:
            plotter.disable_parallel_projection()

    plotter.add_checkbox_button_widget(
        toggle_inner,
        value=True,
        position=(5.0, 132),
        size=25,
        border_size=3,
        color_on='orange',
        color_off='grey',
        background_color='grey',
    )

    plotter.add_text(
        'Toggle inner wall',
        position=(35, 132),
        color='white',
        shadow=True,
        font_size=8,
    )

    plotter.add_checkbox_button_widget(
        toggle_outer,
        value=True,
        position=(5.0, 102),
        size=25,
        border_size=3,
        color_on='orange',
        color_off='grey',
        background_color='grey',
    )

    plotter.add_text(
        'Toggle outer wall',
        position=(35, 102),
        color='white',
        shadow=True,
        font_size=8,
    )

    plotter.add_checkbox_button_widget(
        toggle_ribs,
        value=True,
        position=(5.0, 72),
        size=25,
        border_size=3,
        color_on='orange',
        color_off='grey',
        background_color='grey',
    )

    plotter.add_text(
        'Toggle ribs',
        position=(35, 72),
        color='white',
        shadow=True,
        font_size=8,
    )

    plotter.add_checkbox_button_widget(
        toggle_channels,
        value=True,
        position=(5.0, 42),
        size=25,
        border_size=3,
        color_on='orange',
        color_off='grey',
        background_color='grey',
    )

    plotter.add_text(
        'Toggle channels',
        position=(35, 42),
        color='white',
        shadow=True,
        font_size=8,
    )

    plotter.add_checkbox_button_widget(
        toggle_parallel,
        value=False,
        position=(5.0, 12),
        size=25,
        border_size=3,
        color_on='orange',
        color_off='grey',
        background_color='grey',
    )

    plotter.add_text(
        'Parallel projection',
        position=(35, 12),
        color='white',
        shadow=True,
        font_size=8,
    )

    plotter.set_background('#242424')

    plotter.show()
