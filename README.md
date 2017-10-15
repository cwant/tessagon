# tessagon
Now there is no excuse not to tessellate your favorite 2D manifolds with triangles or hexagons or whatever.

![Animation of tessellated torii](https://raw.githubusercontent.com/cwant/tessagon/master/documentation/images/tessagon_demo.gif)

## How it works

Three things are needed to use tessagon to tessellate the surface of a 2D-manifold (or more accurately, a patch on a 2D-manifold in 3-space):

* Tessagon provides a bunch of classes (subclasses of a class called `Tessagon`) that will tessellate a portion of UV-space with mesh patterns. Parameters provide the details of the bounds in UV-space, the resolution of the tiling, whether the tiling is cyclic, whether it is rotated, etc. These classes are in the `tessagon.types` module.
* The programmer must provide a function that maps UV-space into 3-dimensional space that is defined on the tiled domain. There are some demo functions in `tessagon.misc.shapes`.
* Finally, an adaptor is chosen to create a mesh in a supported 3D software package. Currently only Blender is supported, with the adaptor `BlenderAdaptor` from the module `tessagon.adaptors.blender`.

## Tessagon classes

Additional tessagon classes can be added by deconstructing how a tessellation fits within a rectangular patch in the plane (check out the ASCII art in each source file in `tessagon.types`). The current `Tessagon` subclasses include:

### `HexTessagon`
### `TriTessagon`
### `RhombusTessagon`
### `OctoTessagon`
### `HexTriTessagon` (Star of David)
### `HexSquareTriTessagon`
### `SquareTessagon`
### `PythagoreanTessagon`
### `BrickTessagon`
### `DodecaTessagon`
