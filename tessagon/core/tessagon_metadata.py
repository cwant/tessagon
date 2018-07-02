class TessagonMetadata:
    CLASSIFICATION_MAP = {
        'regular': 'Regular tiling',
        'archimedean': 'Archimedean tiling',
        'laves': 'Laves tiling',
        'non_edge': 'Non-edge-to-edge tiling'
    }

    def __init__(self, **kwargs):
        self._name = kwargs.get('name')
        if not self._name:
            raise ValueError('No name set')
        self._num_color_patterns = kwargs.get('num_color_patterns', 0)
        self._classification = kwargs.get('classification', 'misc')
        self._shapes = kwargs.get('shapes', [])
        self._sides = kwargs.get('sides', [])

    def name(self):
        return self._name

    def num_color_patterns(self):
        return self._num_color_patterns

    def has_color_patterns(self):
        return self._num_color_patterns > 0

    def has_shape(self, shape):
        if shape in self._shapes:
            return True
        return False

    def classification(self):
        return self._classification

    def has_classification(self, classification):
        return self._classification == classification

    def human_readable_classification(self):
        return self.__class__.CLASSIFICATION_MAP[self._classification]
