# -*- coding: utf-8 -*-
"""
    from werkzeug.datastructures
    ~~~~~~~~~~~~~~~~~~~~~~~

    This module provides mixins and classes with an immutable interface.

    :copyright: (c) 2014 by the Werkzeug Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

def is_immutable(self):
    raise TypeError('%r objects are immutable' % self.__class__.__name__)

class ImmutableDictMixin(object):

    """Makes a :class:`dict` immutable.

    .. versionadded:: 0.5

    :private:
    """
    _hash_cache = None

    @classmethod
    def fromkeys(cls, keys, value=None):
        instance = super(cls, cls).__new__(cls)
        instance.__init__(zip(keys, repeat(value)))
        return instance

    def __reduce_ex__(self, protocol):
        return type(self), (dict(self),)

    def _iter_hashitems(self):
        return iteritems(self)

    def __hash__(self):
        if self._hash_cache is not None:
            return self._hash_cache
        rv = self._hash_cache = hash(frozenset(self._iter_hashitems()))
        return rv

    def setdefault(self, key, default=None):
        is_immutable(self)

    def update(self, *args, **kwargs):
        is_immutable(self)

    def pop(self, key, default=None):
        is_immutable(self)

    def popitem(self):
        is_immutable(self)

    def __setitem__(self, key, value):
        is_immutable(self)

    def __delitem__(self, key):
        is_immutable(self)

    def clear(self):
        is_immutable(self)

class ImmutableDict(ImmutableDictMixin, dict):

    """An immutable :class:`dict`.

    .. versionadded:: 0.5
    """

    def __repr__(self):
        return '%s(%s)' % (
            self.__class__.__name__,
            dict.__repr__(self),
        )

    def copy(self):
        """Return a shallow mutable copy of this object.  Keep in mind that
        the standard library's :func:`copy` function is a no-op for this class
        like for any other python immutable type (eg: :class:`tuple`).
        """
        return dict(self)

    def __copy__(self):
        return self


        if self.start is None:
            return '%s */%s' % (self.units, length)
        return '%s %s-%s/%s' % (
            self.units,
            self.start,
            self.stop - 1,
            length
        )

    def __nonzero__(self):
        return self.units is not None
