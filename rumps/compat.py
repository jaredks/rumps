# -*- coding: utf-8 -*-

import sys

PY2 = sys.version_info[0] == 2

if not PY2:
    binary_type = bytes
    text_type = str
    string_types = (str,)

    iteritems = lambda d: iter(d.items())

    import collections.abc as collections_abc

else:
    binary_type = ()
    text_type = unicode
    string_types = (str, unicode)

    iteritems = lambda d: d.iteritems()

    import collections as collections_abc
