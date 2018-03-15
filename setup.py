from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tessagon',
    version='0.4',
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
    keywords='tesselation tiling modeling',
    packages=find_packages(exclude=['tests', 'demo', 'wire_skin.py']),
    python_requires='~=3.5'
)
