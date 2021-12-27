Common Use Cases
================

pyphen has been created for WeasyPrint and many common use cases can thus be
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
