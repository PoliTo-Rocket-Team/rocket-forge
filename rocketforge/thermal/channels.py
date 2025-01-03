from numpy import *
import pyvista as pv


def plot_3D(x, R, a, b, delta, NC, t_w, t_eOvt_w):
    plotter = pv.Plotter(title="Regenerative cooling channels")

    chamber_color = "#727472"
    coolant_color = "#D95319"

    nphi = max([2, int(180 / NC * max(a / (a + delta)))])
    nphi_d = max([2, int(nphi * max(delta / a))])
    ntheta = (nphi + nphi_d) * NC

    phi = a / (R + t_w + b/2)
    phi_c = zeros((len(phi), nphi))
    phi_d = phi * delta / a
    phi_r = zeros((len(phi_d), nphi_d))

    angles = []
    for k in range(NC):
        angles.append(linspace(k * (phi + phi_d) - phi / 2, k * (phi + phi_d) + phi / 2, nphi))
        angles.append(linspace(k * (phi + phi_d) + phi / 2, (k + 1) * (phi + phi_d) - phi / 2, nphi_d))
    theta = concatenate(angles)

    X = outer(x, ones((1, ntheta)))
    X0 = outer([x[0], x[0]], ones((1, ntheta)))
    Xe = outer([x[-1], x[-1]], ones((1, ntheta)))

    Y_inner = (R[newaxis, :] * cos(theta)).T
    Z_inner = (R[newaxis, :] * sin(theta)).T
    inner = plotter.add_mesh(pv.StructuredGrid(X, Y_inner, Z_inner), color=chamber_color)

    Y_inner_ext = ((R[newaxis, :] + t_w) * cos(theta)).T
    Z_inner_ext = ((R[newaxis, :] + t_w) * sin(theta)).T
    inner_ext = plotter.add_mesh(pv.StructuredGrid(X, Y_inner_ext, Z_inner_ext), color=chamber_color)

    Y0_inner = outer([R[0], R[0] + t_w], cos(theta[:, 0]))
    Z0_inner = outer([R[0], R[0] + t_w], sin(theta[:, 0]))
    inner0 = plotter.add_mesh(pv.StructuredGrid(X0, Y0_inner, Z0_inner), color=chamber_color)

    Ye_inner = outer([R[-1], R[-1] + t_w], cos(theta[:, -1]))
    Ze_inner = outer([R[-1], R[-1] + t_w], sin(theta[:, -1]))
    innere = plotter.add_mesh(pv.StructuredGrid(Xe, Ye_inner, Ze_inner), color=chamber_color)

    Y_outer_int = ((R + t_w + b)[newaxis, :] * cos(theta)).T
    Z_outer_int = ((R + t_w + b)[newaxis, :] * sin(theta)).T
    outer_int = plotter.add_mesh(pv.StructuredGrid(X, Y_outer_int, Z_outer_int), color=chamber_color)

    Y_outer = ((R + (t_eOvt_w + 1) * t_w + b)[newaxis, :] * cos(theta)).T
    Z_outer = ((R + (t_eOvt_w + 1) * t_w + b)[newaxis, :] * sin(theta)).T
    outerc = plotter.add_mesh(pv.StructuredGrid(X, Y_outer, Z_outer), color=chamber_color)

    Y0_outer = outer([R[0] + t_w + b[0], R[0] + (t_eOvt_w + 1) * t_w + b[0]], cos(theta[:, 0]))
    Z0_outer = outer([R[0] + t_w + b[0], R[0] + (t_eOvt_w + 1) * t_w + b[0]], sin(theta[:, 0]))
    outer0 = plotter.add_mesh(pv.StructuredGrid(X0, Y0_outer, Z0_outer), color=chamber_color)

    Ye_outer = outer([R[-1] + t_w + b[-1], R[-1] + (t_eOvt_w + 1) * t_w + b[-1]], cos(theta[:, -1]))
    Ze_outer = outer([R[-1] + t_w + b[-1], R[-1] + (t_eOvt_w + 1) * t_w + b[-1]], sin(theta[:, -1]))
    outere = plotter.add_mesh(pv.StructuredGrid(Xe, Ye_outer, Ze_outer), color=chamber_color)

    # Cooling channels
    channels = []
    for k in range(int(NC)):
        for i in range(len(phi)):
            phi_start = -phi[i] / 2 + k * 2 * pi / NC
            phi_end = phi[i] / 2 + k * 2 * pi / NC
            phi_c[i, :] = linspace(phi_start, phi_end, nphi)

        Xc = outer(x, ones((1, nphi)))

        Y_channel_inner = ((R + t_w)[newaxis, :].T * cos(phi_c))
        Z_channel_inner = ((R + t_w)[newaxis, :].T * sin(phi_c))
        c_in = plotter.add_mesh(pv.StructuredGrid(Xc, Y_channel_inner, Z_channel_inner), color=coolant_color, opacity=0.5)
        channels.append(c_in)

        Y_channel_outer = ((R + t_w + b)[newaxis, :].T * cos(phi_c))
        Z_channel_outer = ((R + t_w + b)[newaxis, :].T * sin(phi_c))
        c_out = plotter.add_mesh(pv.StructuredGrid(Xc, Y_channel_outer, Z_channel_outer), color=coolant_color, opacity=0.5)
        channels.append(c_out)

        c_left = plotter.add_mesh(pv.StructuredGrid(
            Xc[:, :2],
            c_[Y_channel_inner[:, 0], Y_channel_outer[:, 0]],
            c_[Z_channel_inner[:, 0], Z_channel_outer[:, 0]]
        ), color=coolant_color, opacity=0.5)
        channels.append(c_left)

        c_right = plotter.add_mesh(pv.StructuredGrid(
            Xc[:, :2],
            c_[Y_channel_inner[:, -1], Y_channel_outer[:, -1]],
            c_[Z_channel_inner[:, -1], Z_channel_outer[:, -1]]
        ), color=coolant_color, opacity=0.5)
        channels.append(c_right)

        z_inner = (R + t_w)[:, newaxis] * sin(phi_c)
        z_outer = (R + t_w + b)[:, newaxis] * sin(phi_c)
        y_inner = (R + t_w)[:, newaxis] * cos(phi_c)
        y_outer = (R + t_w + b)[:, newaxis] * cos(phi_c)

        x_c = (tile(x, (nphi, 1)).T)
        ce = plotter.add_mesh(pv.StructuredGrid(
            c_[x_c[-1, :], x_c[-1, :]], 
            c_[y_inner[-1, :], y_outer[-1, :]],
            c_[z_inner[-1, :], z_outer[-1, :]],
        ), color=coolant_color, opacity=0.5)
        c0 = plotter.add_mesh(pv.StructuredGrid(
            c_[x_c[0, :], x_c[0, :]], 
            c_[y_inner[0, :], y_outer[0, :]],
            c_[z_inner[0, :], z_outer[0, :]],
        ), color=coolant_color, opacity=0.5)
        channels.append(c0)
        channels.append(ce)

    # Ribs
    ribs = []
    for k in range(int(NC)):
        for i in range(len(phi_d)):
            phi_start = phi[i] / 2 + k * 2 * pi / NC
            phi_end = phi[i] / 2 + phi_d[i] + k * 2 * pi / NC
            phi_r[i, :] = linspace(phi_start, phi_end, nphi_d)

        Xr = outer(x, ones((1, nphi_d)))

        Y_channel_inner = ((R + t_w)[newaxis, :].T * cos(phi_r))
        Z_channel_inner = ((R + t_w)[newaxis, :].T * sin(phi_r))
        r_in = plotter.add_mesh(pv.StructuredGrid(Xr, Y_channel_inner, Z_channel_inner), color=chamber_color)
        ribs.append(r_in)

        Y_channel_outer = ((R + t_w + b)[newaxis, :].T * cos(phi_r))
        Z_channel_outer = ((R + t_w + b)[newaxis, :].T * sin(phi_r))
        r_out = plotter.add_mesh(pv.StructuredGrid(Xr, Y_channel_outer, Z_channel_outer), color=chamber_color)
        ribs.append(r_out)

        r_left = plotter.add_mesh(pv.StructuredGrid(
            Xr[:, :2],
            c_[Y_channel_inner[:, 0], Y_channel_outer[:, 0]],
            c_[Z_channel_inner[:, 0], Z_channel_outer[:, 0]]
        ), color=chamber_color)
        ribs.append(r_left)

        r_right = plotter.add_mesh(pv.StructuredGrid(
            Xr[:, :2],
            c_[Y_channel_inner[:, -1], Y_channel_outer[:, -1]],
            c_[Z_channel_inner[:, -1], Z_channel_outer[:, -1]]
        ), color=chamber_color)
        ribs.append(r_right)

        z_inner = (R + t_w)[:, newaxis] * sin(phi_r)
        z_outer = (R + t_w + b)[:, newaxis] * sin(phi_r)
        y_inner = (R + t_w)[:, newaxis] * cos(phi_r)
        y_outer = (R + t_w + b)[:, newaxis] * cos(phi_r)

        x_r = (tile(x, (nphi_d, 1)).T)
        re = plotter.add_mesh(pv.StructuredGrid(
            c_[x_r[-1, :], x_r[-1, :]], 
            c_[y_inner[-1, :], y_outer[-1, :]],
            c_[z_inner[-1, :], z_outer[-1, :]],
        ), color=chamber_color)
        r0 = plotter.add_mesh(pv.StructuredGrid(
            c_[x_r[0, :], x_r[0, :]], 
            c_[y_inner[0, :], y_outer[0, :]],
            c_[z_inner[0, :], z_outer[0, :]],
        ), color=chamber_color)
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
