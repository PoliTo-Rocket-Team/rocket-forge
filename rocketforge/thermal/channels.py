from numpy import *
import pyvista as pv
from rocketforge.utils.logger import logger

def plot_3D(x, R, a, b, delta, NC, t_w, rib_resolution=4, channel_resolution=4, radius_resolution=1):
    plotter = pv.Plotter(title="Regenerative cooling channels")
    # BUG: Diminuendo troppo NC o aumentando troppo t_w la generazione ha problemi. Credo credo cominci a non valere più l'approssimazione di piccolo angolo in phi e phi_d
    phi = a / (R + t_w + b/2)
    phi_d = delta / (R + t_w + b/2)
    # Questi non usano l'approssimazione di piccolo angolo
    # phi = 2 * arcsin(a / (2 * (R + t_w + b/2)))
    # phi_d = 2 * arcsin(delta / (2 * (R + t_w + b/2)))
    # Questi distribuiscono bene ribs e canali ma devo capire bene con che criterio
    # phi = 2 * pi * (a / (NC * (a + delta)))
    # phi_d = 2 * pi * (delta / (NC * (a + delta)))
    alpha_total = zeros((len(phi), NC * (rib_resolution + channel_resolution)))
        #), color="#D95319", opacity=0.5, backface_culling=bfc)

    for k in range(int(NC)):
        for i in range(len(phi)):
            alpha_total[i,(rib_resolution + channel_resolution)*k:(rib_resolution + channel_resolution)*k + channel_resolution] = linspace(
                -phi[i] / 2 + k * 2 * pi / NC,
                 phi[i] / 2 + k * 2 * pi / NC,
                 channel_resolution + 1)[:channel_resolution]
            alpha_total[i, (rib_resolution + channel_resolution)*k+channel_resolution:(rib_resolution + channel_resolution)*(k+1)] = linspace(
                phi[i] / 2 + k * 2 * pi / NC,
                phi[i] / 2 + phi_d[i] + k * 2 * pi / NC,
                rib_resolution + 1)[:rib_resolution]
    
    radii = [R, R + t_w, R + t_w + b]# + linspace(R + t_w, R + t_w + b, radius_resolution + 1)[:1].tolist()
    y_coords = [r[:, newaxis] * sin(alpha_total) for r in radii]
    z_coords = [r[:, newaxis] * cos(alpha_total) for r in radii]

    # The points (arrays of 3 x,y,z values) are put along one dimension of an array.
    # The arrays is a series of "slices" of the engine along the axial direction.
    # Each slice consists of three circles: inner, middle, outer.
    # The points are ordered going along the inner circle, then the middle circle, then the outer circle.
    # At the end of the outer circle, the next slice starts from the inner circle again.
    x_broadcasted = broadcast_to(x[:, newaxis], (len(phi), NC * (rib_resolution + channel_resolution)))
    points = concatenate([
        stack((x_broadcasted, y, z), axis=-1) for y, z in zip(y_coords, z_coords)
    ], axis=1).reshape(-1, 3)
    
    r_offset = NC * (rib_resolution + channel_resolution) # Index offset along the radial direction
    x_offset = len(radii) * r_offset # Index offset along the axial direction
    last_face_offset = (len(phi) - 1) * x_offset
    faces = []
    # Top wall cap
    for i in range(r_offset):
        next_i = (i + 1) % r_offset # Wrap around for closed loop
        faces.extend([
            4,                  # Quad (4 vertices)
            i,                  # Current point on inner circle
            i + r_offset,       # Corresponding point on middle circle
            next_i + r_offset,  # Next point on middle circle
            next_i              # Corresponding point on inner circle
        ])
    # Top ribs cap
    for j in range(channel_resolution, r_offset, rib_resolution + channel_resolution):
        for i in range(rib_resolution):
            next_i = (j + i + 1) % r_offset  # Wrap around for closed loop
            faces.extend([
                4,                      # Quad (4 vertices)
                j + i  + 1 * r_offset,  # Current point on middle circle
                j + i  + 2 * r_offset,  # Corresponding point on outer circle
                next_i + 2 * r_offset,  # Next point on outer circle
                next_i + 1 * r_offset   # Corresponding point on middle circle
            ])
    # Exterior surface of the engine
    for k in range(len(phi) - 1):
        for j in range(0, r_offset, rib_resolution + channel_resolution):
            # Side surface of the channel
            faces.extend([
                4,                                    # Quad (4 vertices)
                j + 1 * r_offset + k * x_offset,      # Current point on middle circle
                j + 2 * r_offset + k * x_offset,      # Corresponding point on outer circle
                j + 2 * r_offset + (k+1) * x_offset,  # Corresponding point on outer circle of next slice
                j + 1 * r_offset + (k+1) * x_offset,  # Corresponding point on middle circle of next slice
                4,                                                         # Quad (4 vertices)
                j + channel_resolution + 1 * r_offset + k * x_offset,      # Current point on middle circle
                j + channel_resolution + 1 * r_offset + (k+1) * x_offset,  # Corresponding point on middle circle of next slice
                j + channel_resolution + 2 * r_offset + (k+1) * x_offset,  # Corresponding point on outer circle
                j + channel_resolution + 2 * r_offset + k * x_offset       # Corresponding point on outer circle of current slice    
            ])
            # Bottom surface of the channel
            for i in range(channel_resolution):
                next_i = (j + i + 1) % r_offset
                faces.extend([
                    4,                                         # Quad (4 vertices)
                    j + i  + 1 * r_offset + k * x_offset,      # Current point on middle circle
                    j + i  + 1 * r_offset + (k+1) * x_offset,  # Corresponding point on middle circle of next slice
                    next_i + 1 * r_offset + (k+1) * x_offset,  # Next point on middle circle of next slice
                    next_i + 1 * r_offset + k * x_offset       # Corresponding point on middle circle of current slice
                ])
            # Top surface of the rib
            for i in range(rib_resolution):
                next_i = (j + channel_resolution + i + 1) % r_offset
                faces.extend([
                    4,                                                             # Quad (4 vertices)
                    j + channel_resolution + i + 2 * r_offset + k * x_offset,      # Current point on outer circle
                    j + channel_resolution + i + 2 * r_offset + (k+1) * x_offset,  # Corresponding point on outer circle of next slice
                    next_i + 2 * r_offset + (k+1) * x_offset,                      # Next point on outer circle of next slice
                    next_i + 2 * r_offset + k * x_offset                           # Corresponding point on outer circle of current slice
                ])
    # Interior surface of the engine
    for j in range(len(phi) - 1):
        for i in range(r_offset):
            next_i = (i + 1) % r_offset
            faces.extend([
                4,                          # Quad (4 vertices)
                i + j * x_offset,           # Current point on inner circle
                next_i + j * x_offset,      # Next point on inner circle
                next_i + (j+1) * x_offset,  # Corresponding point on inner circle of next slice
                i + (j+1) * x_offset,       # Previous point on inner circle of next slice
            ])
    # Bottom ribs cap
    for j in range(channel_resolution, r_offset, rib_resolution + channel_resolution):
        for i in range(rib_resolution):
            next_i = (j + i + 1) % r_offset  # Wrap around for closed loop
            faces.extend([
                4,                                         # Quad (4 vertices)
                j + i + r_offset + last_face_offset,       # Current point on middle circle
                next_i + r_offset + last_face_offset,      # Next point on middle circle
                next_i + 2 * r_offset + last_face_offset,  # Corresponding point on outer circle
                j + i + 2 * r_offset + last_face_offset    # Previous point on outer circle
            ])
    # Bottom wall cap
    for i in range(r_offset):
        next_i = (i + 1) % r_offset # Wrap around for closed loop
        faces.extend([
            4,                                     # Quad (4 vertices)
            i + last_face_offset,                  # Current point on inner circle
            next_i + last_face_offset,             # Next point on inner circle
            next_i + r_offset + last_face_offset,  # Correpsonding point on middle circle
            i + r_offset + last_face_offset        # Previous point on middle circle
        ])
    faces = array(faces, dtype=int64)
    engine = pv.PolyData(points, faces)
    if not engine.is_manifold: logger.warning("Mesh is not watertight.")

    faces_channels = []
    for j in range(0, r_offset, rib_resolution + channel_resolution):
        for i in range(channel_resolution):
            next_i = (j + i + 1) % r_offset  # Wrap around for closed loop
            faces_channels.extend([
                4,                      # Quad (4 vertices)
                j + i  + 1 * r_offset,  # Current point on middle circle
                j + i  + 2 * r_offset,  # Corresponding point on outer circle
                next_i + 2 * r_offset,  # Next point on outer circle
                next_i + 1 * r_offset   # Corresponding point on middle circle
            ])
    for k in range(len(phi) - 1):
        for j in range(0, r_offset, rib_resolution + channel_resolution):
            # Side surfaces of the channel
            faces_channels.extend([
                4,                                    # Quad (4 vertices)
                j + 1 * r_offset + k * x_offset,      # Current point on middle circle
                j + 1 * r_offset + (k+1) * x_offset,  # Corresponding point on middle circle of next slice
                j + 2 * r_offset + (k+1) * x_offset,  # Corresponding point on outer circle of next slice
                j + 2 * r_offset + k * x_offset,      # Corresponding point on outer circle
                4,                                                         # Quad (4 vertices)
                j + channel_resolution + 1 * r_offset + k * x_offset,      # Current point on middle circle
                j + channel_resolution + 2 * r_offset + k * x_offset,      # Corresponding point on outer circle of current slice    
                j + channel_resolution + 2 * r_offset + (k+1) * x_offset,  # Corresponding point on outer circle
                j + channel_resolution + 1 * r_offset + (k+1) * x_offset   # Corresponding point on middle circle of next slice
            ])
            # Bottom and top surfaces of the channel
            for i in range(channel_resolution):
                next_i = (j + i + 1) % r_offset
                faces_channels.extend([
                    4,                                         # Quad (4 vertices)
                    j + i  + 1 * r_offset + k * x_offset,      # Current point on middle circle
                    next_i + 1 * r_offset + k * x_offset,      # Corresponding point on middle circle of current slice
                    next_i + 1 * r_offset + (k+1) * x_offset,  # Next point on middle circle of next slice
                    j + i  + 1 * r_offset + (k+1) * x_offset, # Corresponding point on middle circle of next slice
                    4,
                    j + i  + 2 * r_offset + k * x_offset,      # Current point on middle circle
                    j + i  + 2 * r_offset + (k+1) * x_offset,  # Corresponding point on middle circle of next slice
                    next_i + 2 * r_offset + (k+1) * x_offset,  # Next point on middle circle of next slice
                    next_i + 2 * r_offset + k * x_offset       # Corresponding point on middle circle of current slice
                ])
    for j in range(0, r_offset, rib_resolution + channel_resolution):
        for i in range(channel_resolution):
            next_i = (j + i + 1) % r_offset  # Wrap around for closed loop
            faces_channels.extend([
                4,                                         # Quad (4 vertices)
                j + i + r_offset + last_face_offset,       # Current point on middle circle
                next_i + r_offset + last_face_offset,      # Next point on middle circle
                next_i + 2 * r_offset + last_face_offset,  # Corresponding point on outer circle
                j + i + 2 * r_offset + last_face_offset    # Previous point on outer circle
            ])
    faces_channels = array(faces_channels, dtype=int64)
    channels = pv.PolyData(points, faces_channels)
    if not channels.is_manifold: logger.warning("Channels mesh is not watertight.")
    plotter.add_mesh(engine, color="#727472", show_edges=False, line_width=2, backface_culling=True)
    plotter.add_mesh(channels, color="#D95319", opacity=0.7, show_edges=False, line_width=2, backface_culling=True)
    plotter.set_background('#242424')
    plotter.add_axes(color="#fafafa")
    plotter.show()

