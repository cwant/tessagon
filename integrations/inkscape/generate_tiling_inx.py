#!/usr/bin/env python
"""
Read in tiling.inx.in input file and inject Tessagon tiling types
(to stdout).
"""
import os
import sys

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(THIS_DIR + '/../..')

from tessagon.core.tessagon_discovery import TessagonDiscovery  # noqa E402


class InxGenerate:
    def run(self):
        with open(THIS_DIR + '/tiling.inx.in') as f:
            for line in f:
                sys.stdout.write(line)
                if "Autogenerated tiling types start" in line:
                    self.dump_tilings()

    def dump_tilings(self):
        # Create tiling menu with items in nice order
        find_tilings = TessagonDiscovery()
        tilings = find_tilings.with_classification('regular').to_list() + \
            find_tilings.with_classification('archimedean').to_list() + \
            find_tilings.with_classification('laves').to_list() + \
            find_tilings.with_classification('non_edge').to_list() + \
            find_tilings.with_classification('non_convex').to_list()

        template = '        <option value="{}">{}</option>\n'
        for tiling_class in tilings:
            metadata = tiling_class.metadata
            sys.stdout.write(template.format(tiling_class.__name__,
                                             metadata.name))


if __name__ == "__main__":
    InxGenerate().run()
