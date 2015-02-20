Pyphen
======

Pyphen is a pure Python module to hyphenate text using existing Hunspell
hyphenation dictionaries.

https://github.com/Kozea/Pyphen

This module is a fork of python-hyphenator, written by Wilbert Berendsen.

https://code.google.com/p/python-hyphenator/

Many dictionaries are included in pyphen, they come from the LibreOffice git
repository and are distributed under GPL, LGPL and/or MPL. See the
dictionaries and the libreoffice's repository for more details.

http://cgit.freedesktop.org/libreoffice/dictionaries/tree/

Usage:

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
>>>

Features:

* 100% pure Python with no dependencies
* a lot of included dictionaries
* caches dict files and hyphenated words
* supports nonstandard hyphenation patterns

License:

Pyphen is released under the GPL 2.0+/LGPL 2.1+/MPL 1.1 tri-license.
See COPYING.GPL, COPYING.LGPL and COPYING.MPL for more details.
