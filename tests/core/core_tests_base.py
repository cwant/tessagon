import os
import sys

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_dir + '/../../..')


class CoreTestsBase:
    pass


class FakeTessagon:
    def f(self, u, v):
        return [u, u*v, v]


class FakeAdaptor:
    pass
