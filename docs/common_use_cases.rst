Common Use Cases
================

Pyphen has been created for WeasyPrint and many common use cases can thus be
found in `its repository`_.

.. _its repository: https://github.com/Kozea/WeasyPrint


.. code-block:: python

   >>> import pyphen
   >>> pyphen.language_fallback('nl_NL_variant1')
   'nl_NL'
   >>> 'nl_NL' in pyphen.LANGUAGES
   True
   >>> dic = pyphen.Pyphen(lang='nl_NL')
   >>> dic.inserted('lettergrepen')
   'let-ter-gre-pen'
   >>> dic.wrap('autobandventieldopje', 11)
   ('autoband-', 'ventieldopje')
   >>> for pair in dic.iterate('Amsterdam'):
   ...     print(pair)
   ...
   ('Amster', 'dam')
   ('Am', 'sterdam')


Registering a Custom Dictionary
--------------------------------

Applications can register their own Hunspell hyphenation dictionaries before
creating hyphenation instances:

.. code-block:: python

   import pyphen

   pyphen.register('xx', '/path/to/hyph_xx.dic')
   dictionary = pyphen.Pyphen(lang='xx')

Both string filenames and ``pathlib.Path`` objects are accepted. Relative paths
are resolved when registered, so later working-directory changes do not affect
the registered file.

Language codes are case-insensitive and accept either hyphens or underscores.
Normal language fallback applies: registering ``xx`` also makes it available
for a request such as ``xx_YY``. Registering a specific regional code replaces
only that code; its parent language and other regions remain unchanged.

Registrations affect newly created instances. Existing instances retain their
dictionaries. Dictionary caching still follows the ``cache`` argument of
``Pyphen``; use ``cache=False`` to reread a file whose contents have changed.
