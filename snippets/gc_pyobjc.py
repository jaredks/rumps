# -*- coding: utf-8 -*-
"""
snippets.gc_pyobjc
~~~~~~~~~~~~~~~~~~

Test integrity of garbage collection.

"""

from __future__ import print_function

import AppKit
import gc
import objc
import weakref


class PyObjCObject(AppKit.NSObject):
    pass


class PythonObject(object):
    pass


def test_1():
    """Check that an instance of NSObject eventually garbage collects
    """
    a = AppKit.NSObject.alloc().init()
    ref = objc.WeakRef(a)
    assert ref() is a

    del a
    print('after del', ref())

    gc.collect()
    print('after gc.collect', ref())

    objc.recycleAutoreleasePool()
    print('after objc.recycleAutoreleasePool', ref())

    assert ref() is None


def test_2():
    """Check that an instance of a NSObject subclass eventually garbage
    collects.
    """
    pyobjc = PyObjCObject.alloc().init()
    ref = objc.WeakRef(pyobjc)
    assert ref() is pyobjc

    del pyobjc
    print('after del', ref())

    gc.collect()
    print('after gc.collect', ref())

    objc.recycleAutoreleasePool()
    print('after objc.recycleAutoreleasePool', ref())

    assert ref() is None


def test_3():
    """Check that garbage collector eventually collects both,

      * an instance of a NSObject subclass (a)
      * an instance of a standard python class (b)

    when the following occurs,

      * the b references a
      * a is subsequently deleted
      * b is subsequently deleted

    """
    pyobjc = PyObjCObject.alloc().init()
    py = PythonObject()
    py.pyobjc = pyobjc

    pyobjc_ref = objc.WeakRef(pyobjc)
    assert pyobjc_ref() is pyobjc

    py_ref = weakref.ref(py)
    assert py_ref() is py

    del pyobjc
    del py
    print('after del', pyobjc_ref(), py_ref())

    gc.collect()
    print('after gc.collect', pyobjc_ref(), py_ref())

    objc.recycleAutoreleasePool()
    print('after objc.recycleAutoreleasePool', pyobjc_ref(), py_ref())

    assert pyobjc_ref() is None
    assert py_ref() is None


def test_4():
    """Check that garbage collector *does not** eventually collect either,

      * an instance of a NSObject subclass (a)
      * an instance of a standard python class (b)

    when the following occurs,

      * a references b
      * b references a
      * a is subsequently deleted
      * b is subsequently deleted

    """
    a = PyObjCObject.alloc().init()
    b = PythonObject()
    a.b = b
    b.a = a

    ref_a = objc.WeakRef(a)
    ref_b = weakref.ref(b)
    assert ref_a() is a
    assert ref_b() is b

    del a
    del b
    print('after del', ref_a(), ref_b())

    gc.collect()
    print('after gc.collect', ref_a(), ref_b())

    objc.recycleAutoreleasePool()
    print('after objc.recycleAutoreleasePool', ref_a(), ref_b())

    assert ref_a() is not None
    assert ref_b() is not None


def test_5():
    """Check that garbage collector eventually collects both,

      * an instance of a standard python class (a)
      * an instance of a standard python class (b)

    when the following occurs,

      * a references b
      * b references a
      * a is subsequently deleted
      * b is subsequently deleted

    """
    a = PythonObject()
    b = PythonObject()
    a.b = b
    b.a = a

    ref_a = weakref.ref(a)
    ref_b = weakref.ref(b)
    assert ref_a() is a
    assert ref_b() is b

    del a
    del b
    print('after del', ref_a(), ref_b())

    gc.collect()
    print('after gc.collect', ref_a(), ref_b())

    objc.recycleAutoreleasePool()
    print('after objc.recycleAutoreleasePool', ref_a(), ref_b())

    assert ref_a() is None
    assert ref_b() is None


def test_6():
    """Check that garbage collector eventually collects both,

      * an instance of a NSObject subclass (a)
      * an instance of a standard python class (b)

    when the following occurs,

      * a weak-references b
      * b references a
      * a is subsequently deleted
      * b is subsequently deleted

    """
    a = PyObjCObject.alloc().init()
    b = PythonObject()
    a.b = weakref.ref(b)
    b.a = a

    ref_a = objc.WeakRef(a)
    ref_b = weakref.ref(b)
    assert ref_a() is a
    assert ref_b() is b

    del a
    del b
    print('after del', ref_a(), ref_b())

    gc.collect()
    print('after gc.collect', ref_a(), ref_b())

    objc.recycleAutoreleasePool()
    print('after objc.recycleAutoreleasePool', ref_a(), ref_b())

    assert ref_a() is None
    assert ref_b() is None


def test_7():
    """Check that garbage collector eventually collects both,

      * an instance of a NSObject subclass (a)
      * an instance of a standard python class (b)

    when the following occurs,

      * a references b
      * b weak-references a
      * a is subsequently deleted
      * b is subsequently deleted

    """
    a = PyObjCObject.alloc().init()
    b = PythonObject()
    a.b = b
    b.a = objc.WeakRef(a)

    ref_a = objc.WeakRef(a)
    ref_b = weakref.ref(b)
    assert ref_a() is a
    assert ref_b() is b

    del a
    del b
    print('after del', ref_a(), ref_b())

    gc.collect()
    print('after gc.collect', ref_a(), ref_b())

    objc.recycleAutoreleasePool()
    print('after objc.recycleAutoreleasePool', ref_a(), ref_b())

    assert ref_a() is None
    assert ref_b() is None


def test_8():
    """Check that garbage collector *does not** eventually collect either,

      * an instance of a NSObject subclass (a)
      * an instance of a NSObject subclass (b)

    when the following occurs,

      * a references b
      * b references a
      * a is subsequently deleted
      * b is subsequently deleted

    """
    a = PyObjCObject.alloc().init()
    b = PyObjCObject.alloc().init()
    a.b = b
    b.a = a

    ref_a = objc.WeakRef(a)
    ref_b = objc.WeakRef(b)
    assert ref_a() is a
    assert ref_b() is b

    del a
    del b
    print('after del', ref_a(), ref_b())

    gc.collect()
    print('after gc.collect', ref_a(), ref_b())

    objc.recycleAutoreleasePool()
    print('after objc.recycleAutoreleasePool', ref_a(), ref_b())

    assert ref_a() is not None
    assert ref_b() is not None


if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
    test_4()
    test_5()
    test_6()
    test_7()
    test_8()
    # TODO: check if cleaned up when cycle python objs, each having ref to ns object
