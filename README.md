**WIP - documentation currently in development, more to come**

# tessagon
Now there is no excuse not to tessellate your favorite 2D manifolds with triangles or hexagons or whatever.

![Animation of tessellated torii](https://raw.githubusercontent.com/cwant/tessagon/master/documentation/images/tessagon_demo.gif)

(Individual images from the above gif are below.)

## TL;DR

Check out the repository and look in the `demo` directory.

* **Blender**: you'll find a blender file and `tessagon_blender_demo.py` which creates the meshes in the demo. The demo has examples of each tessagon class, and an example that uses tessagon with one of my other projects, ![wire_skin](https://github.com/cwant/wire_skin).
* **VTK**: Take a look at `tessagon_vtk_demo.py` for a script that creates all of the current tessagon classes.

## How it works

Three things are needed to use tessagon to tessellate the surface of a 2D-manifold (or more accurately, a patch on a 2D-manifold in 3-space):

* Tessagon provides a bunch of classes (subclasses of a class called `Tessagon`) that will tessellate a portion of UV-space with mesh patterns. Parameters provide the details of the bounds in UV-space, the resolution of the tiling, whether the tiling is cyclic, whether a cyclic domain "twists" (think a topological identification space, like a Mobius strip or a Klein bottle), whether it is rotated, etc. These classes are in the `tessagon.types` module.
* The programmer must provide a function that maps UV-space into 3-dimensional space that is defined on the tiled domain. There are some demo functions in `tessagon.misc.shapes`.
* Finally, an adaptor is chosen to create a mesh in a supported 3D software package. Currently only Blender and VTK are supported:
  * adaptor `BlenderAdaptor` from the module `tessagon.adaptors.blender`
  * adaptor `VtkAdaptor` from the module `tessagon.adaptors.vtk`

The reader should check out the demos, but here is some very basic usage using blender:

```python
from tessagon.types.hex_tessagon import HexTessagon
from tessagon.adaptors.blender_adaptor import BlenderAdaptor

def my_func(u,v):
  return [u, v, u**2 + v**2]
  
options = {
    'function': my_func,
    'u_range': [0.0, 1.0],
    'v_range': [0.0, 1.0],
    'u_num': 8,
    'v_num': 20,
    'u_cyclic': False,
    'v_cyclic': False,
    'adaptor_class' : BlenderAdaptor
  }
tessagon = HexTessagon(**options)

bmesh = tessagon.create_mesh()

# Do something with the bmesh ...
```

## Tessagon classes

Additional tessagon classes can be added by deconstructing how a tessellation fits within a rectangular patch in the plane (check out the ASCII art in each source file in `tessagon.types`). The current `Tessagon` subclasses include:

### `HexTessagon`
![HexTessagon](https://raw.githubusercontent.com/cwant/tessagon/master/documentation/images/hex_tessagon.png)

### `TriTessagon`
![TriTessagon](https://raw.githubusercontent.com/cwant/tessagon/master/documentation/images/tri_tessagon.png)

### `RhombusTessagon`
![RhombusTessagon](https://raw.githubusercontent.com/cwant/tessagon/master/documentation/images/rhombus_tessagon.png)

### `OctoTessagon`
![OctoTessagon](https://raw.githubusercontent.com/cwant/tessagon/master/documentation/images/octo_tessagon.png)

### `HexTriTessagon` (Star of David)
![HexTriTessagon](https://raw.githubusercontent.com/cwant/tessagon/master/documentation/images/hex_tri_tessagon.png)

### `HexSquareTriTessagon`
![HexSquareTriTessagon](https://raw.githubusercontent.com/cwant/tessagon/master/documentation/images/hex_square_tri_tessagon.png)

### `SquareTessagon`
![SquareTessagon](https://raw.githubusercontent.com/cwant/tessagon/master/documentation/images/square_tessagon.png)

### `PythagoreanTessagon`
![PythagoreanTessagon](https://raw.githubusercontent.com/cwant/tessagon/master/documentation/images/pythagorean_tessagon.png)

### `BrickTessagon`
![BrickTessagon](https://raw.githubusercontent.com/cwant/tessagon/master/documentation/images/brick_tessagon.png)

### `DodecaTessagon`
![DodecaTessagon](https://raw.githubusercontent.com/cwant/tessagon/master/documentation/images/dodeca_tessagon.png)

## Usage and Options

Each tessagon class is initialized with number of keyword options, e.g.:

```
from tessagon.types.dodeca_tessagon import DodecaTessagon
from tessagon.adaptors.vtk_adaptor import VtkAdaptor
tessagon = DodecaTessagon(function=my_func,
                          u_range=[0.0, 1.0],
                          v_range=[0.0, 1.0],
                          u_num=8,
                          v_num=20,
                          u_cyclic=True,
                          v_cyclic=False,
                          adaptor_class=VtkAdaptor)
poly_data = tessagon.create_mesh()
```
The `create_mesh()` method creates a tessellated mesh using your provided function and the tile type corresponding to the tessagon class used. The chosen adaptor dictates the 3D data type the mesh will be (for the `BlenderAdaptor` the output is `BMesh`, for the `VTKAdaptor` the output is `vtkPolyData`).

Here are the options:

* `function`: the function to be used to generate the geometry. This is a function that takes two arguments (`u`, `v`) and returns a list of three items (`x`, `y`, `z`)
* `u_range`: a list with two items indicating the minimum and maximum values for u (the first argument to the function passed);
* `v_range`: a list with two items indicating the minimum and maximum values for v (the second argument to the function passed);
* `u_num`: the number of tiles to be created in the u-direction;
* `v_num`: the number of tiles to be created in the v-direction;
* `u_cyclic`: a boolean indicating whether the u-direction is cyclic (wraps around to the beginning again;
* `v_cyclic`: a boolean indicating whether the v-direction is cyclic;
