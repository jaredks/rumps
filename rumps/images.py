# -*- coding: utf-8 -*-
"""
rumps.images
~~~~~~~~~~~~

xxx

"""

import AppKit

from . import utils
from .ui import _mixins


def _resolve_image_location(filename):
    """Resolve image location ahead of time."""
    try:
        utils.log('attempting to open image at {0}'.format(filename))
        with open(filename):
            pass

    # literal file path didn't work -- try to locate image based on main script path
    except IOError:
        try:
            from __main__ import __file__ as main_script_path
            main_script_path = os.path.dirname(main_script_path)
            filename = os.path.join(main_script_path, filename)
        except ImportError:
            pass
        utils.log('attempting (again) to open image at {0}'.format(filename))
        with open(filename):
            pass

    return filename


class Image(_mixins.Component):
    """xxx
    """

    DEFAULT_HEIGHT = 20
    DEFAULT_WIDTH = 20

    def __init__(self, **options):
        pass

    def _create_view(self):
        self._ns = AppKit.NSImageView.alloc().init()
        #self._ns.setImageFrameStyle_(2)

    def _init_image(self):
        self._ns_image.setScalesWhenResized_(True)
        self._ns.setImage_(self._ns_image)

    @property
    def path(self):
        return self._path

    def path_from_file(self, filename):
        """xxx"""
        filename = _resolve_image_location(filename)
        print '==>', filename

        self._ns_image = AppKit.NSImage.alloc().initByReferencingFile_(filename)
        self._init_image()

    @classmethod
    def from_file(cls, filename, **options):
        """Create an image from the given path.
        """
        dimensions = options.get('dimensions', (cls.DEFAULT_WIDTH, cls.DEFAULT_HEIGHT))
        template = options.get('template')

        obj = cls.__new__(cls)
        obj._create_view()
        obj.path_from_file(filename)
        obj.template = template
        obj.set_size(dimensions)
        return obj

    @classmethod
    def from_url(cls, url, **options):
        pass

    @property
    def template(self):
        return self._ns_image.template()

    @template.setter
    def template(self, value):
        """xxx"""
        value = bool(value)
        return self._ns_image.setTemplate_(value)

    def set_size(self, dimensions):
        """xxx"""
        self._ns_image.setSize_(dimensions)
        self._ns.setFrameSize_(dimensions)

    @property
    def width(self):
        return self._ns_image.size().width
        #return self._ns.frame().size.width

    @width.setter
    def width(self, value):
        #if getattr(self, 'auto_width', False):
        #    raise exceptions.UIError(
        #        'cannot explicitly set width when auto_width is true'
        #    )

        dimensions = AppKit.NSSize(value, self.height)
        self._ns_image.setSize_(dimensions)
        self._ns.setFrameSize_(dimensions)

        if self.parent:
            self.parent.layout()

    @property
    def height(self):
        return self._ns_image.size().height
        #return self._ns.frame().size.height

    @height.setter
    def height(self, value):
        #if getattr(self, 'auto_height', False):
        #    raise exceptions.UIError(
        #        'cannot explicitly set height when auto_height is true'
        #    )

        dimensions = AppKit.NSSize(self.width, value)
        self._ns_image.setSize_(dimensions)
        self._ns.setFrameSize_(dimensions)

        if self.parent:
            self.parent.layout()
