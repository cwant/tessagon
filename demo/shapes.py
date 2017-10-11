from math import sin, cos, pi

def general_torus(r1, r2, u, v):
  x = (r1 + r2*cos(v*2*pi))*cos(u*2*pi)
  y = (r1 + r2*cos(v*2*pi))*sin(u*2*pi)
  z = r2*sin(v*2*pi)
  return [x, y, z]

def warp_var(v, factor):
  # For any factor, maps 0-->0, 1-->1
  # factor = 0 is identity
  # factor > 0 for a wee pinch at v = 1/2
  h = 2 * (v - 0.5)
  i = h + factor*h**3
  return 0.5*(1.0 + i / (1.0 + factor))

def torus(u, v):
  r1 = 5.0
  r2 = 1.0
  return general_torus(r1, r2, u, warp_var(v, 0.2))

def other_torus(u, v):
  return torus(v, u)

def general_cylinder(r, h, u, v):
  x = r*cos(u*2*pi)
  y = r*sin(u*2*pi)
  z = h*(v - 0.5)
  return [x, y, z]

def cylinder(u, v):
  r = 5.0
  h = 5.0
  return general_cylinder(r, h, u, v)

def general_mobius(r, h, u, v):
   
  offset = h*(v-0.5)*sin(u*pi)
  x = (r + offset)*cos(u*2*pi)
  y = (r + offset)*sin(u*2*pi)
  z = h*(v-0.5)*cos(u*pi)
  return [x, y, z]

def mobius(u, v):
  r = 5.0
  h = 2.0
  return general_mobius(r, h, v, u)

def plane(u, v):
  return [u, v, 0]
