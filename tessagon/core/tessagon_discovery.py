import importlib
from tessagon.core import class_name_to_method_name

# Note that ALL is ordered in an ideal way (regular, archimedean, ...)
ALL = ['SquareTessagon',
       'HexTessagon',
       'TriTessagon',

       'OctaTessagon',
       'HexTriTessagon',
       'HexSquareTriTessagon',
       'DodecaTessagon',
       'SquareTriTessagon',
       'SquareTri2Tessagon',
       'DodecaTriTessagon',
       'BigHexTriTessagon',

       'RhombusTessagon',
       'FloretTessagon',
       'DissectedSquareTessagon',
       'DissectedTriangleTessagon',
       'DissectedHexQuadTessagon',
       'DissectedHexTriTessagon',
       'PentaTessagon',
       'Penta2Tessagon',

       'PythagoreanTessagon',
       'BrickTessagon',
       'WeaveTessagon',
       'HexBigTriTessagon',
       'ZigZagTessagon',
       'ValemountTessagon',
       'CloverdaleTessagon',
       'HokusaiParallelogramsTessagon',
       'SlatsTessagon',

       'StanleyParkTessagon',
       'IslamicHexStarsTessagon',
       'IslamicStarsCrossesTessagon',

       'HokusaiHashesTessagon']


class TessagonDiscovery:
    def __init__(self, **kwargs):
        self.names = kwargs.get('names', ALL)
        self._classes = None

    @property
    def classes(self):
        if self._classes is None:
            self._classes = []
            for name in self.names:
                klass = self.__class__.get_class(name, verify=False)
                self._classes.append(klass)

        return self._classes

    def count(self):
        return len(self.names)

    def to_list(self):
        return self.classes

    def inverse(self):
        other_names = list(set(ALL) - set(self.names))
        return TessagonDiscovery(names=other_names)

    def __add__(self, other):
        new_names = list(set(self.names) | set(other.names))
        return TessagonDiscovery(names=new_names)

    def __sub__(self, other):
        new_names = list(set(self.names) - set(other.names))
        return TessagonDiscovery(names=new_names)

    def with_color_patterns(self):
        results = []
        for klass in self.classes:
            if klass.metadata is None:
                continue
            if klass.metadata.has_color_patterns:
                results.append(klass.__name__)
        return TessagonDiscovery(names=results)

    def with_classification(self, classification):
        results = []
        for klass in self.classes:
            if klass.metadata is None:
                continue
            if klass.metadata.has_classification(classification):
                results.append(klass.__name__)
        return TessagonDiscovery(names=results)

    @classmethod
    def get_class(cls, class_name, verify=True):
        if verify and (class_name not in ALL):
            raise ValueError(class_name + ' is not recognized by Tessagon')

        module_name = class_name_to_method_name(class_name)
        module_path = 'tessagon.types.{}'.format(module_name)
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
