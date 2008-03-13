from distutils.core import setup

longdesc = """
Python text hyphenator
======================

hyphenator is a pure Python module to hyphenate text using existing hyphenation
dictionaries, like those used by OpenOffice.org.

Usage:

>>> from hyphenator import Hyphenator
>>> h = Hyphenator("/usr/share/myspell/hyph_nl_NL.dic")
>>> h.inserted('lettergrepen')
u'let-ter-gre-pen'
>>> h.wrap('autobandventieldopje', 11)
('autoband-', 'ventieldopje')
>>> for pair in h.iterate('Amsterdam'):
...     print pair
...
('Amster', 'dam')
('Am', 'sterdam')
>>>

Features:

* 100% pure Python
* caches dict files and hyphenated words
* supports nonstandard hyphenation patterns

License:

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""

classifiers = [
'Development Status :: 3 - Alpha',
'Intended Audience :: Developers',
'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
'Programming Language :: Python',
'Topic :: Text Processing',
'Topic :: Text Processing :: Linguistic',
]

setup(
    name = 'hyphenator',
    version = '0.5.1',
    py_modules = ['hyphenator'],
    author = 'Wilbert Berendsen',
    author_email = 'wbsoft@xs4all.nl',
    url = 'http://python-hyphenator.googlecode.com/',
    description = 'Pure Python module to hyphenate text using existing dictionaries',
    long_description = longdesc,
    classifiers = classifiers,
)
