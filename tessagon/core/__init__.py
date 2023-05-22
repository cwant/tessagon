import re

# A couple of general purpose functions for manipulating
# camel case class names and snake case function/method names.
# (Mostly used for some questionable dynamic method creation ...).
# TODO: setup demos to use this


def class_name_to_method_name(class_name, prefix=''):
    method_name = prefix
    method_name += re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower()
    return method_name


def class_to_method_name(cls, prefix=''):
    # E.g., if cls is HexTessagon and prefix is 'whatever_',
    # this function returns 'whatever_hex_tessagon'
    return class_name_to_method_name(cls.__name__, prefix)


def method_name_to_class_name(method_name):
    return ''.join(word.title() for word in method_name.split('_'))
