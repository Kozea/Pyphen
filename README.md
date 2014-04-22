Pyphen
======

Pyphen is a pure Python module to hyphenate text using existing *Hunspell* hyphenation dictionaries.

This module is a fork of `python-hyphenator`, written by Wilbert Berendsen at https://code.google.com/p/python-hyphenator.

Many dictionaries are included in Pyphen, they come from the *LibreOffice* git repository and are distributed under *GPL*, *LGPL* and/or *MPL*. See the dictionaries and the *LibreOffice* repository for more details: http://cgit.freedesktop.org/libreoffice/dictionaries/tree.

Usage
-----

```python
    >>> import pyphen
    >>> pyphen.language_fallback('nl_NL_variant1')
    u'nl_NL'
    >>> u'nl_NL' in pyphen.LANGUAGES
    True
    >>> dic = pyphen.Pyphen(lang='nl_NL')
    >>> dic.inserted('lettergrepen')
    u'let-ter-gre-pen'
    >>> dic.wrap('autobandventieldopje', 11)
    (u'autoband-', u'ventieldopje')
    >>> for pair in dic.iterate('Amsterdam'):
    ...     print(pair)
    (u'Amster', u'dam')
    (u'Am', u'sterdam')
    >>>
```

Features
--------

* 100% pure Python with no dependencies
* a lot of included dictionaries
* caches dict files and hyphenated words
* supports nonstandard hyphenation patterns

License
-------

Pyphen is released under the *GPL 2.0+/LGPL 2.1+/MPL 1.1* tri-license. See [COPYING.GPL](COPYING.GPL), [COPYING.LGPL](COPYING.LGPL) and [COPYING.MPL](COPYING.MPL) for more details.
