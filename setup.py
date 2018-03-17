from setuptools import setup, find_packages

long_description = '''
===========================================
tessagon: tessellation / tiling with python
===========================================

Tessellate your favorite 3D surfaces (technically, 2D manifolds) with
triangles, hexagons, or a number of other curated tiling types!

Please visit the Github repository for documentation:

`<https://github.com/cwant/tessagon>`_

Either checkout the code from the Github project, or install via pip::

    python3 -m pip install tessagon

or::

    pip3 install tessagon

'''[1:-1]

setup(
    name='tessagon',
    version='0.4.2',
    description='Tessellate your favorite 2D manifolds with triangles, ' +
    'hexagons, and other interesting patterns.',
    long_description=long_description,
    url='https://github.com/cwant/tessagon',
    author='Chris Want',
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Manufacturing',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: Apache Software License',
                 'Natural Language :: English',
                 'Programming Language :: Python :: 3 :: Only',
                 'Topic :: Artistic Software',
                 'Topic :: Multimedia :: Graphics :: 3D Modeling',
                 'Topic :: Scientific/Engineering :: Mathematics',
                 'Topic :: Scientific/Engineering :: Visualization'],
    keywords='tesselation tiling modeling blender vtk',
    packages=find_packages(exclude=['tests', 'demo', 'wire_skin.py']),
    python_requires='~=3.5'
)
