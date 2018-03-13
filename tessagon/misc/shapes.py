from math import sin, cos, sqrt, pi


def plane(u, v):
    # u_cyclic = False, v_cyclic = False
    return [u, v, 0]


def other_plane(u, v):
    # u_cyclic = False, v_cyclic = False
    return [v, u, 0]


def general_torus(r1, r2, u, v):
    x = (r1 + r2*cos(v*2*pi))*cos(u*2*pi)
    y = (r1 + r2*cos(v*2*pi))*sin(u*2*pi)
    z = r2*sin(v*2*pi)
    return [x, y, z]


def normalize_value(v):
    if (v < 0.0):
        while (v < 0.0):
            v += 1.0
    else:
        while (v > 1.0):
            v -= 1.0
    return v


def warp_var(v, factor):
    # For any factor, maps 0-->0, 1-->1
    # factor = 0 is identity
    # factor > 0 for a wee pinch at v = 1/2
    v = normalize_value(v)
    h = 2 * (v - 0.5)
    i = h + factor*h**3
    return 0.5*(1.0 + i / (1.0 + factor))


def torus(u, v):
    # u_cyclic = True, v_cyclic = True
    r1 = 5.0
    r2 = 1.0
    return general_torus(r1, r2, u, warp_var(v, 0.2))


def other_torus(u, v):
    # u_cyclic = True, v_cyclic = True
    return torus(v, u)


def general_cylinder(r, h, u, v):
    x = r*cos(u*2*pi)
    y = r*sin(u*2*pi)
    z = h*(v - 0.5)
    return [x, y, z]


def cylinder(u, v):
    # u_cyclic = True, v_cyclic = False
    r = 5.0
    h = 3.5
    return general_cylinder(r, h, u, v)


def other_cylinder(u, v):
    # u_cyclic = False, v_cyclic = True
    return cylinder(v, u)


def general_paraboloid(scale1, scale2, displace, u, v):
    return [scale1*u, scale1*v, displace + scale2 * (u**2 + v**2)]


def paraboloid(u, v):
    # u_cyclic = False, v_cyclic = False
    return general_paraboloid(4, 3, -3, u, v)


def general_one_sheet_hyperboloid(scale1, scale2, u, v):
    c = scale1 * sqrt(1 + u**2)
    v1 = 2*pi*v
    x = c * cos(v1)
    y = c * sin(v1)
    z = scale2 * u
    return [x, y, z]


def one_sheet_hyperboloid(u, v):
    # u_cyclic = False, v_cyclic = True
    return general_one_sheet_hyperboloid(3, 2, u, v)


def general_ellipsoid(r1, r2, r3, u, v):
    # u_cyclic = True, v_cyclic = False
    u1 = 2*pi*u
    v1 = pi*normalize_value(warp_var(v + 0.5, 0.8)-0.5)
    sinv1 = sin(v1)
    return [r1 * cos(u1) * sinv1, r2 * sin(u1) * sinv1, r3 * cos(v1)]


def sphere(u, v):
    return general_ellipsoid(4, 4, 4, u, v)


def general_mobius(r, h, u, v):
    offset = h*(v-0.5)*sin(u*pi)
    x = (r + offset)*cos(u*2*pi)
    y = (r + offset)*sin(u*2*pi)
    z = h*(v-0.5)*cos(u*pi)
    return [x, y, z]


def mobius(u, v):
    # u_cyclic = False, v_cyclic = True
    # u_twist = True, v_twist = False
    r = 5.0
    h = 2.0
    return general_mobius(r, h, v, u)


def other_mobius(u, v):
    # u_cyclic = True, v_cyclic = False
    # u_twist = False, v_twist = True
    return mobius(v, u)


def general_klein(scale, u, v):
    # Adapted from http://paulbourke.net/geometry/klein/
    u1 = 2*pi*normalize_value(warp_var(u + 0.5, 0.6)-0.5)
    v1 = 2*pi*normalize_value(v+0.25)

    c1 = cos(u1)
    c2 = sin(u1)
    r = 4.0 - 2.0*c1

    if u1 <= pi:
        x = 6*c1*(1.0 + c2) + r*c1*cos(v1)
        y = 16*c2 + r*c2*cos(v1)
    else:
        x = 6*c1*(1.0 + c2) + r*cos(v1+pi)
        y = 16*c2
    z = r * sin(v1)
    return [scale*x, scale*y, scale*z]


def klein(u, v):
    # u_cyclic = True, v_cyclic = True
    # u_twist = False, v_twist = True
    return general_klein(0.25, u, v)


def other_klein(u, v):
    # u_cyclic = True, v_cyclic = True
    # u_twist = True, v_twist = False
    return general_klein(0.25, v, u)
