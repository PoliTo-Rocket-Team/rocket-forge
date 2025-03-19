from numpy import *
import pyvista as pv
from rocketforge.utils.logger import logger

def plot_3D(x, R, a, b, delta, NC, t_w, t_eOvt_w = 4.0, radius_resolution=1):
    plotter = pv.Plotter(title="Regenerative cooling channels")
    global export_stl
    export_stl = False

    global channel_resolution, rib_resolution
    channel_resolution = max([1, int(180/NC * max(a / (a + delta)))])
    rib_resolution = max([1, int(channel_resolution * max(delta/a))])

    phi = a / (R + t_w + b/2)
    phi_d = delta / (R + t_w + b/2)
    global len_phi
    len_phi = len(phi)
    alpha = zeros((len_phi, NC * (rib_resolution + channel_resolution)))

    # Angles
    for k in range(int(NC)):
        for i in range(len_phi):
            alpha[i,(rib_resolution + channel_resolution)*k:(rib_resolution + channel_resolution)*k + channel_resolution] = linspace(
                -phi[i] / 2 + k * 2 * pi / NC,
                 phi[i] / 2 + k * 2 * pi / NC,
                 channel_resolution + 1)[:channel_resolution]
            alpha[i, (rib_resolution + channel_resolution)*k+channel_resolution:(rib_resolution + channel_resolution)*(k+1)] = linspace(
                phi[i] / 2 + k * 2 * pi / NC,
                phi[i] / 2 + phi_d[i] + k * 2 * pi / NC,
                rib_resolution + 1)[:rib_resolution]

    # The points (arrays of 3 x,y,z values) are put along one dimension of an array.
    # The arrays is a series of "slices" of the engine along the axial direction.
    # Each slice consists of three circles: inner, middle, outer.
    # The points are ordered going along the inner circle, then the middle circle, then the outer circle.
    # At the end of the outer circle, the next slice starts from the inner circle again.
    radii = [R, R + t_w, R + t_w + b, R + b + (1 + t_eOvt_w) * t_w]
    y_coords = [r[:, newaxis] * sin(alpha) for r in radii]
    z_coords = [r[:, newaxis] * cos(alpha) for r in radii]
    x_broadcasted = broadcast_to(x[:, newaxis], (len_phi, NC * (rib_resolution + channel_resolution)))
    points = concatenate([
        stack((x_broadcasted, y, z), axis=-1) for y, z in zip(y_coords, z_coords)
    ], axis=1).reshape(-1, 3)

    # Offsets
    global r_offset, x_offset, last_face_offset
    r_offset = NC * (rib_resolution + channel_resolution) # Index offset along the radial direction
    x_offset = len(radii) * r_offset # Index offset along the axial direction
    last_face_offset = (len_phi - 1) * x_offset

    # Inner wall
    inner_wall_faces = generate_inner_wall_mesh()
    inner_wall_pd = pv.PolyData(points, inner_wall_faces)
    if not inner_wall_pd.is_manifold: logger.warning("Inner wall mesh is not watertight.")
    inner_wall = plotter.add_mesh(inner_wall_pd, color="#727472", opacity=1, show_edges=False, line_width=2, backface_culling=True)

    # Ribs
    ribs_faces = generate_ribs_mesh()
    ribs_pd = pv.PolyData(points, ribs_faces)
    if not ribs_pd.is_manifold: logger.warning("Ribs mesh is not watertight.")
    ribs = plotter.add_mesh(ribs_pd, color="#727472", opacity=1, show_edges=False, line_width=2, backface_culling=True)

    # Outer wall
    outer_wall_faces = generate_outer_wall_mesh()
    outer_wall_pd = pv.PolyData(points, outer_wall_faces)
    if not outer_wall_pd.is_manifold: logger.warning("Outer wall mesh is not watertight.")
    outer_wall = plotter.add_mesh(outer_wall_pd, color="#727472", opacity=1, show_edges=False, line_width=2, backface_culling=True)

    # Channels
    channels_faces = generate_channels_mesh()
    channels_pd = pv.PolyData(points, channels_faces)
    if not channels_pd.is_manifold: logger.warning("Channels mesh is not watertight.")
    channels = plotter.add_mesh(channels_pd, color="#D95319", opacity=0.7, show_edges=False, line_width=2, backface_culling=True)

    plotter.add_checkbox_button_widget(
        lambda flag: outer_wall.SetVisibility(flag),
        value=True,
        position=(5.0, 162),
        size=25,
        border_size=3,
        color_on='orange',
        color_off='grey',
        background_color='grey',
    )
    plotter.add_text(
        'Outer wall',
        position=(35, 162),
        color='white',
        shadow=True,
        font_size=8,
    )

    plotter.add_checkbox_button_widget(
        lambda flag: ribs.SetVisibility(flag),
        value=True,
        position=(5.0, 132),
        size=25,
        border_size=3,
        color_on='orange',
        color_off='grey',
        background_color='grey',
    )
    plotter.add_text(
        'Ribs',
        position=(35, 132),
        color='white',
        shadow=True,
        font_size=8,
    )

    plotter.add_checkbox_button_widget(
        lambda flag: channels.SetVisibility(flag),
        value=True,
        position=(5.0, 102),
        size=25,
        border_size=3,
        color_on='orange',
        color_off='grey',
        background_color='grey',
    )
    plotter.add_text(
        'Channels',
        position=(35, 102),
        color='white',
        shadow=True,
        font_size=8,
    )

    plotter.add_checkbox_button_widget(
        lambda flag: inner_wall.SetVisibility(flag),
        value=True,
        position=(5.0, 72),
        size=25,
        border_size=3,
        color_on='orange',
        color_off='grey',
        background_color='grey',
    )
    plotter.add_text(
        'Inner wall',
        position=(35, 72),
        color='white',
        shadow=True,
        font_size=8,
    )

    plotter.add_checkbox_button_widget(
        lambda flag: plotter.enable_parallel_projection() if flag else plotter.disable_parallel_projection(),
        value=False,
        position=(5.0, 42),
        size=25,
        border_size=3,
        color_on='orange',
        color_off='grey',
        background_color='grey',
    )
    plotter.add_text(
        'Parallel projection',
        position=(35, 42),
        color='white',
        shadow=True,
        font_size=8,
    )

    def set_export_stl(flag):
        global export_stl
        export_stl = flag
    plotter.add_checkbox_button_widget(
        set_export_stl,
        value=False,
        position=(5.0, 12),
        size=25,
        border_size=3,
        color_on='orange',
        color_off='grey',
        background_color='grey',
    )
    plotter.add_text(
        'Export STL file (output.stl) when closing',
        position=(35, 12),
        color='white',
        shadow=True,
        font_size=8,
    )

    plotter.enable_anti_aliasing()
    plotter.set_background("#242424")
    plotter.add_axes(color="#fafafa")
    plotter.show()
    if export_stl:
        engine_faces = generate_single_engine_mesh()
        engine_pd = pv.PolyData(points, engine_faces)
        if not engine_pd.is_manifold: logger.warning("Engine mesh is not watertight.")
        engine_pd.save("output.stl")


def generate_inner_wall_mesh():
    faces = []
    # Top inner wall cap
    for i in range(r_offset):
        next_i = (i + 1) % r_offset # Wrap around for closed loop
        faces.extend([
            4,                      # Quad (4 vertices)
            i,                      # Current point on first circle
            i +      1 * r_offset,  # Corresponding point on second circle
            next_i + 1 * r_offset,  # Next point on second circle
            next_i                  # Corresponding point on first circle
        ])
    # Inner wall
    for j in range(len_phi - 1):
        for i in range(r_offset):
            next_i = (i + 1) % r_offset  # Wrap around for closed loop
            faces.extend([
                4,                          # Quad (4 vertices)
                i +      j * x_offset,      # Current point on first circle
                next_i + j * x_offset,      # Next point on first circle
                next_i + (j+1) * x_offset,  # Corresponding point on first circle of next slice
                i +      (j+1) * x_offset   # Previous point on first circle of next slice
            ])
    # Bottom inner wall cap
    for i in range(r_offset):
        next_i = (i + 1) % r_offset # Wrap around for closed loop
        faces.extend([
            4,                                     # Quad (4 vertices)
            i + last_face_offset,                  # Current point on first circle
            next_i + last_face_offset,             # Next point on first circle
            next_i + r_offset + last_face_offset,  # Corresponding point on second circle
            i + r_offset + last_face_offset        # Previous point on second circle
        ])
    # Outer wall
    for j in range(len_phi - 1):
        for i in range(r_offset):
            next_i = (i + 1) % r_offset
            faces.extend([
                4,                                         # Quad (4 vertices)
                i +      1 * r_offset + j * x_offset,      # Current point on second circle
                i +      1 * r_offset + (j+1) * x_offset,  # Corresponding point on second circle of next slice
                next_i + 1 * r_offset + (j+1) * x_offset,  # Next point on second circle of next slice
                next_i + 1 * r_offset + j * x_offset       # Corresponding point on second circle
            ])
    return faces

def generate_ribs_mesh():
    faces = []
    # Top ribs cap
    for j in range(channel_resolution, r_offset, rib_resolution + channel_resolution):
        for i in range(rib_resolution):
            next_i = (j + i + 1) % r_offset  # Wrap around for closed loop
            faces.extend([
                4,                      # Quad (4 vertices)
                j + i  + 1 * r_offset,  # Current point on second circle
                j + i  + 2 * r_offset,  # Corresponding point on third circle
                next_i + 2 * r_offset,  # Next point on third circle
                next_i + 1 * r_offset   # Corresponding point on second circle
            ])
    for k in range(len_phi - 1):
        for j in range(0, r_offset, rib_resolution + channel_resolution):
            # Side surface of the ribs
            faces.extend([
                4,                                                         # Quad (4 vertices)
                j + 1 * r_offset + k * x_offset,                           # Current point on second circle
                j + 2 * r_offset + k * x_offset,                           # Corresponding point on third circle
                j + 2 * r_offset + (k+1) * x_offset,                       # Corresponding point on third circle of next slice
                j + 1 * r_offset + (k+1) * x_offset,                       # Corresponding point on second circle of next slice
                4,                                                         # Quad (4 vertices)
                j + channel_resolution + 1 * r_offset + k * x_offset,      # Current point on second circle
                j + channel_resolution + 1 * r_offset + (k+1) * x_offset,  # Corresponding point on second circle of next slice
                j + channel_resolution + 2 * r_offset + (k+1) * x_offset,  # Corresponding point on third circle
                j + channel_resolution + 2 * r_offset + k * x_offset       # Corresponding point on third circle of current slice
            ])
            # Bottom surface of the rib
            for i in range(rib_resolution):
                next_i = (j + channel_resolution + i + 1) % r_offset
                faces.extend([
                    4,                                                            # Quad (4 vertices)
                    j + channel_resolution + i + 1 * r_offset + k * x_offset,     # Current point on second circle
                    next_i +                     1 * r_offset + k * x_offset,     # Next point on second circle
                    next_i +                     1 * r_offset + (k+1) * x_offset, # Corresponding point on second circle of next slice
                    j + channel_resolution + i + 1 * r_offset + (k+1) * x_offset  # Previous point on second circle of next slice
                ])
            # Top surface of the rib
            for i in range(rib_resolution):
                next_i = (j + channel_resolution + i + 1) % r_offset
                faces.extend([
                    4,                                                             # Quad (4 vertices)
                    j + channel_resolution + i + 2 * r_offset + k * x_offset,      # Current point on third circle
                    j + channel_resolution + i + 2 * r_offset + (k+1) * x_offset,  # Corresponding point on third circle of next slice
                    next_i +                     2 * r_offset + (k+1) * x_offset,  # Next point on third circle of next slice
                    next_i +                     2 * r_offset + k * x_offset       # Corresponding point on third circle of current slice
                ])

    # Bottom ribs cap
    for j in range(channel_resolution, r_offset, rib_resolution + channel_resolution):
        for i in range(rib_resolution):
            next_i = (j + i + 1) % r_offset  # Wrap around for closed loop
            faces.extend([
                4,                                         # Quad (4 vertices)
                j + i +  1 * r_offset + last_face_offset,  # Current point on second circle
                next_i + 1 * r_offset + last_face_offset,  # Next point on second circle
                next_i + 2 * r_offset + last_face_offset,  # Corresponding point on third circle
                j + i +  2 * r_offset + last_face_offset   # Previous point on third circle
            ])
    return faces

def generate_outer_wall_mesh():
    faces = []
    # Top inner wall cap
    for i in range(r_offset):
        next_i = (i + 1) % r_offset # Wrap around for closed loop
        faces.extend([
            4,                      # Quad (4 vertices)
            i +      2 * r_offset,  # Current point on third circle
            i +      3 * r_offset,  # Corresponding point on fourth circle
            next_i + 3 * r_offset,  # Next point on fourth circle
            next_i + 2 * r_offset   # Corresponding point on third circle
        ])
    # Inner wall
    for j in range(len_phi - 1):
        for i in range(r_offset):
            next_i = (i + 1) % r_offset
            faces.extend([
                4,                                         # Quad (4 vertices)
                i +      2 * r_offset + j * x_offset,      # Current point on third circle
                next_i + 2 * r_offset + j * x_offset,      # Next point on third circle
                next_i + 2 * r_offset + (j+1) * x_offset,  # Corresponding point on third circle of next slice
                i +      2 * r_offset + (j+1) * x_offset   # Previous point on third circle of next slice
            ])
    # Bottom inner wall cap
    for i in range(r_offset):
        next_i = (i + 1) % r_offset # Wrap around for closed loop
        faces.extend([
            4,                                         # Quad (4 vertices)
            i +      2 * r_offset + last_face_offset,  # Current point on third circle
            next_i + 2 * r_offset + last_face_offset,  # Next point on third circle
            next_i + 3 * r_offset + last_face_offset,  # Corresponding point on fourth circle
            i +      3 * r_offset + last_face_offset   # Previous point on fourth circle
        ])
    # Outer wall
    for j in range(len_phi - 1):
        for i in range(r_offset):
            next_i = (i + 1) % r_offset
            faces.extend([
                4,                                         # Quad (4 vertices)
                i +      3 * r_offset + j * x_offset,      # Current point on fourth circle
                i +      3 * r_offset + (j+1) * x_offset,  # Corresponding point on fourth circle of next slice
                next_i + 3 * r_offset + (j+1) * x_offset,  # Next point on fourth circle
                next_i + 3 * r_offset + j * x_offset       # Corresponding point on fourth circle of previous slice
            ])
    return faces

def generate_channels_mesh():
    faces = []
    for j in range(0, r_offset, rib_resolution + channel_resolution):
        for i in range(channel_resolution):
            next_i = (j + i + 1) % r_offset  # Wrap around for closed loop
            faces.extend([
                4,                      # Quad (4 vertices)
                j + i  + 1 * r_offset,  # Current point on second circle
                j + i  + 2 * r_offset,  # Corresponding point on third circle
                next_i + 2 * r_offset,  # Next point on third circle
                next_i + 1 * r_offset   # Corresponding point on second circle
            ])
    for k in range(len_phi - 1):
        for j in range(0, r_offset, rib_resolution + channel_resolution):
            # Side surfaces of the channel
            faces.extend([
                4,                                                         # Quad (4 vertices)
                j + 1 * r_offset + k * x_offset,                           # Current point on second circle
                j + 1 * r_offset + (k+1) * x_offset,                       # Corresponding point on second circle of next slice
                j + 2 * r_offset + (k+1) * x_offset,                       # Corresponding point on third circle
                j + 2 * r_offset + k * x_offset,                           # Corresponding point on third circle of previous slice
                4,                                                         # Quad (4 vertices)
                j + channel_resolution + 1 * r_offset + k * x_offset,      # Current point on second circle
                j + channel_resolution + 2 * r_offset + k * x_offset,      # Corresponding point on third circle
                j + channel_resolution + 2 * r_offset + (k+1) * x_offset,  # Corresponding point on third circle of next slice
                j + channel_resolution + 1 * r_offset + (k+1) * x_offset   # Corresponding point on second circle
            ])
            # Bottom and top surfaces of the channel
            for i in range(channel_resolution):
                next_i = (j + i + 1) % r_offset
                faces.extend([
                    4,                                         # Quad (4 vertices)
                    j + i  + 1 * r_offset + k * x_offset,      # Current point on second circle
                    next_i + 1 * r_offset + k * x_offset,      # Next point on second circle
                    next_i + 1 * r_offset + (k+1) * x_offset,  # Corresponding point on second circle of next slice
                    j + i  + 1 * r_offset + (k+1) * x_offset,  # Previous point on middle circle
                    4,                                         # Quad (4 vertices)
                    j + i  + 2 * r_offset + k * x_offset,      # Current point on third circle
                    j + i  + 2 * r_offset + (k+1) * x_offset,  # Corresponding point on third circle of next slice
                    next_i + 2 * r_offset + (k+1) * x_offset,  # Next point on third circle of next slice
                    next_i + 2 * r_offset + k * x_offset       # Corresponding point on third circle of previous slice
                ])
    for j in range(0, r_offset, rib_resolution + channel_resolution):
        for i in range(channel_resolution):
            next_i = (j + i + 1) % r_offset  # Wrap around for closed loop
            faces.extend([
                4,                                         # Quad (4 vertices)
                j + i +  1 * r_offset + last_face_offset,  # Current point on second circle
                next_i + 1 * r_offset + last_face_offset,  # Next point on second circle
                next_i + 2 * r_offset + last_face_offset,  # Corresponding point on third circle
                j + i +  2 * r_offset + last_face_offset   # Previous point on third circle
            ])
    return faces

def generate_single_engine_mesh():
    faces = []
    # Top inner wall cap
    for i in range(r_offset):
        next_i = (i + 1) % r_offset # Wrap around for closed loop
        faces.extend([
            4,                  # Quad (4 vertices)
            i,                  # Current point on first circle
            i + r_offset,       # Corresponding point on second circle
            next_i + r_offset,  # Next point on second circle
            next_i              # Corresponding point on first circle
        ])
    # Top ribs cap
    for j in range(channel_resolution, r_offset, rib_resolution + channel_resolution):
        for i in range(rib_resolution):
            next_i = (j + i + 1) % r_offset  # Wrap around for closed loop
            faces.extend([
                4,                      # Quad (4 vertices)
                j + i  + 1 * r_offset,  # Current point on second circle
                j + i  + 2 * r_offset,  # Corresponding point on third circle
                next_i + 2 * r_offset,  # Next point on third circle
                next_i + 1 * r_offset   # Corresponding point on second circle
            ])
    # Top outer wall cap
    for i in range(r_offset):
        next_i = (i + 1) % r_offset # Wrap around for closed loop
        faces.extend([
            4,                      # Quad (4 vertices)
            i +      2 * r_offset,  # Current point on third circle
            i +      3 * r_offset,  # Corresponding point on fourth circle
            next_i + 3 * r_offset,  # Next point on fourth circle
            next_i + 2 * r_offset   # Corresponding point on third circle
        ])
    # Exterior surface of the engine
    for k in range(len_phi - 1):
        for j in range(0, r_offset, rib_resolution + channel_resolution):
            # Side surface of the channel
            faces.extend([
                4,                                                         # Quad (4 vertices)
                j + 1 * r_offset + k * x_offset,                           # Current point on second circle
                j + 2 * r_offset + k * x_offset,                           # Corresponding point on third circle
                j + 2 * r_offset + (k+1) * x_offset,                       # Corresponding point on third circle of next slice
                j + 1 * r_offset + (k+1) * x_offset,                       # Corresponding point on second circle
                4,                                                         # Quad (4 vertices)
                j + channel_resolution + 1 * r_offset + k * x_offset,      # Current point on second circle
                j + channel_resolution + 1 * r_offset + (k+1) * x_offset,  # Corresponding point on second circle of next slice
                j + channel_resolution + 2 * r_offset + (k+1) * x_offset,  # Corresponding point on third circle
                j + channel_resolution + 2 * r_offset + k * x_offset       # Corresponding point on third circle of previous slice
            ])
            # Bottom surface of the channel
            for i in range(channel_resolution):
                next_i = (j + i + 1) % r_offset
                faces.extend([
                    4,                                         # Quad (4 vertices)
                    j + i  + 1 * r_offset + k * x_offset,      # Current point on second circle
                    j + i  + 1 * r_offset + (k+1) * x_offset,  # Corresponding point on second circle of next slice
                    next_i + 1 * r_offset + (k+1) * x_offset,  # Next point on second circle of next slice
                    next_i + 1 * r_offset + k * x_offset       # Corresponding point on second circle of previous slice
                ])
            # Top surface of the rib (channel?)
            for i in range(rib_resolution):
                next_i = (j + i + 1) % r_offset
                faces.extend([
                    4,                                         # Quad (4 vertices)
                    j + i +  2 * r_offset + k * x_offset,      # Current point on third circle
                    next_i + 2 * r_offset + k * x_offset,      # Next point on third circle
                    next_i + 2 * r_offset + (k+1) * x_offset,  # Corresponding point on third circle of next slice
                    j + i +  2 * r_offset + (k+1) * x_offset   # Previous point on third circle
                ])
    # Interior surface of the engine
    for j in range(len_phi - 1):
        for i in range(r_offset):
            next_i = (i + 1) % r_offset
            faces.extend([
                4,                          # Quad (4 vertices)
                i + j * x_offset,           # Current point on first circle
                next_i + j * x_offset,      # Next point on first circle
                next_i + (j+1) * x_offset,  # Corresponding point on first circle of next slice
                i + (j+1) * x_offset,       # Previous point on first circle
            ])
    # Exterior surface of the engine
    for j in range(len_phi - 1):
        for i in range(r_offset):
            next_i = (i + 1) % r_offset
            faces.extend([
                4,                                         # Quad (4 vertices)
                i +      3 * r_offset + j * x_offset,      # Current point on fourth circle
                i +      3 * r_offset + (j+1) * x_offset,  # Corresponding point on fourth circle of next slice
                next_i + 3 * r_offset + (j+1) * x_offset,  # Next point on fourth circle
                next_i + 3 * r_offset + j * x_offset       # Corrresponding point on fourth circle of previous slice
            ])

    # Bottom outer wall cap
    for i in range(r_offset):
        next_i = (i + 1) % r_offset # Wrap around for closed loop
        faces.extend([
            4,                                         # Quad (4 vertices)
            i +      2 * r_offset + last_face_offset,  # Current point on third circle
            next_i + 2 * r_offset + last_face_offset,  # Next point on third circle
            next_i + 3 * r_offset + last_face_offset,  # Corresponding point on fourth circle
            i +      3 * r_offset + last_face_offset   # Previous point on fourth circle
        ])
    # Bottom ribs cap
    for j in range(channel_resolution, r_offset, rib_resolution + channel_resolution):
        for i in range(rib_resolution):
            next_i = (j + i + 1) % r_offset  # Wrap around for closed loop
            faces.extend([
                4,                                         # Quad (4 vertices)
                j + i +  1 * r_offset + last_face_offset,  # Current point on second circle
                next_i + 1 * r_offset + last_face_offset,  # Next point on second circle
                next_i + 2 * r_offset + last_face_offset,  # Corresponding point on third circle
                j + i +  2 * r_offset + last_face_offset   # Previous point on third circle
            ])
    # Bottom inner wall cap
    for i in range(r_offset):
        next_i = (i + 1) % r_offset # Wrap around for closed loop
        faces.extend([
            4,                                     # Quad (4 vertices)
            i + last_face_offset,                  # Current point on first circle
            next_i + last_face_offset,             # Next point on first circle
            next_i + r_offset + last_face_offset,  # Corresponding point on second circle
            i + r_offset + last_face_offset        # Previous point on second circle
        ])
    return faces