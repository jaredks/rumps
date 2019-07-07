# -*- coding: utf-8 -*-

try:
    PY2 = True
    text_type = unicode
    string_types = basestring

    iteritems = lambda d: d.iteritems()
except NameError:
    PY2 = False
    text_type = str
    string_types = (str,)

    iteritems = lambda d: iter(d.items())
