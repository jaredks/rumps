# -*- coding: utf-8 -*-

import pytest

from rumps.utils import ListDict


class TestListDict(object):
    def test_clear(self):
        ld = ListDict()

        ld[1] = 11
        ld['b'] = 22
        ld[object()] = 33
        assert len(ld) == 3

        ld.clear()
        assert len(ld) == 0
        assert ld.items() == []
