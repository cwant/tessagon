# tessagon
Now there is no excuse not to tessellate your favorite 2D manifolds with triangles or hexagons or whatever.

![Animation of tessellated torii](https://raw.githubusercontent.com/cwant/tessagon/master/documentation/images/tessagon_demo.gif)

(Individual images from the above gif are below.)

## TL;DR

Check out the repository and look in the `demo` directory. There you'll find a blender file and `tessagon_blender_demo.py` which creates the meshes in the demo.

## How it works

Three things are needed to use tessagon to tessellate the surface of a 2D-manifold (or more accurately, a patch on a 2D-manifold in 3-space):

* Tessagon provides a bunch of classes (subclasses of a class called `Tessagon`) that will tessellate a portion of UV-space with mesh patterns. Parameters provide the details of the bounds in UV-space, the resolution of the tiling, whether the tiling is cyclic, whether it is rotated, etc. These classes are in the `tessagon.types` module.
* The programmer must provide a function that maps UV-space into 3-dimensional space that is defined on the tiled domain. There are some demo functions in `tessagon.misc.shapes`.
* Finally, an adaptor is chosen to create a mesh in a supported 3D software package. Currently only Blender is supported, with the adaptor `BlenderAdaptor` from the module `tessagon.adaptors.blender`.

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
