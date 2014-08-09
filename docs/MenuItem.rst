MenuItem
========

.. autoclass:: rumps.MenuItem
   :members:
   :inherited-members:

   .. method:: d[key]

      Return the item of d with key `key`. Raises a ``KeyError`` if key is not in the map.

   .. method:: d[key] = value

      Set `d[key]` to `value` if `key` does not exist in d. `value` will be converted to a `MenuItem` object if not one already.

   .. method:: del d[key]

      Remove `d[key]` from d. Raises a ``KeyError`` if `key` is not in the map.
