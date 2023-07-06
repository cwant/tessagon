class BaseAdaptor:
    ADAPTOR_OPTIONS = []

    def __init__(self, **kwargs):
        self.face_order = kwargs.get('face_order')
