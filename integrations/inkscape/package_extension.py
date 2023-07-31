#!/usr/bin/env python
"""
Package Tessagon code for including in Inkscape
"""
import os
import sys
import shutil
import glob
import zipfile
import pathlib
from generate_tiling_inx import InxGenerate

# Only minify if the python_minifier package is installed
minify = False
try:
    import python_minifier
    minify = True
except ModuleNotFoundError:
    pass

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(THIS_DIR + '/../..')

from tessagon.core.tessagon_discovery import TessagonDiscovery  # noqa E402

OUTPUT_DIR = THIS_DIR + '/output/inkscape-tiling-extension'
OUTPUT_FILE = THIS_DIR + '/output/inkscape-tiling-extension.zip'

TESSAGON_DIR = THIS_DIR + '/../..'
TESSAGON_FILES = ['tessagon/*.py',
                  'tessagon/core/*.py',
                  'tessagon/adaptors/base_*.py',
                  'tessagon/adaptors/list_*.py',
                  'tessagon/adaptors/svg_*.py',
                  'tessagon/types/*.py',
                  'tessagon/types/tiles/*.py']


class PackageExtension:
    def run(self):
        self.make_output_directory()
        self.generate_tiling_inx()
        self.copy_tiling_py()
        self.copy_tessagon()
        self.zip_package()

    def make_output_directory(self):
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    def generate_tiling_inx(self):
        orig_stdout = sys.stdout
        f = open(OUTPUT_DIR + '/tiling.inx', 'w')
        sys.stdout = f
        InxGenerate().run()
        sys.stdout = orig_stdout

    def copy_tiling_py(self):
        shutil.copy(THIS_DIR + '/tiling.py', OUTPUT_DIR)

    def copy_tessagon(self):
        base_dir = OUTPUT_DIR + '/tessagon'
        if not os.path.isdir(base_dir):
            os.mkdir(base_dir)

        for pattern in TESSAGON_FILES:
            dest_dir = os.path.dirname(base_dir + '/' + pattern)
            os.makedirs(dest_dir, exist_ok=True)

            print("Copying files to {}".format(dest_dir))
            for filename in glob.glob(TESSAGON_DIR + '/' + pattern):
                output = dest_dir + '/' + os.path.basename(filename)
                if minify is True:
                    self.minify_file(filename, output)
                else:
                    shutil.copy(filename, output)

    def minify_file(self, source, destination):
        buffer = ""
        with open(source) as f:
            buffer = python_minifier.minify(f.read())

        with open(destination, "w") as f:
            f.write(buffer)

    def zip_package(self):
        directory = pathlib.Path(OUTPUT_DIR)
        with zipfile.ZipFile(OUTPUT_FILE, mode="w") as archive:
            for file_path in directory.rglob("*"):
                arcname = os.path.join('inkscape-tiling-extension',
                                       file_path.relative_to(directory))
                archive.write(file_path, arcname=arcname)


if __name__ == "__main__":
    PackageExtension().run()
