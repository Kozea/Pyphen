---
layout: default
title: Pyphen
permalink: /
---

Presentation
------------

Pyphen is a pure Python module to hyphenate text using included or external
Hunspell hyphenation dictionaries.


Usage
-----

{% highlight python %}
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
{% endhighlight %}


Features
--------

- 100% pure Python with no dependencies
- a lot of included dictionaries
- caches dict files and hyphenated words
- supports nonstandard hyphenation patterns


Included Dictionaries
---------------------

The dictionaries included in LibreOffice are distributed with Pyphen:

- Afrikaans
- Bulgarian
- Catalan
- Croatian
- Czech
- Danish
- Dutch
- English (Great-Britain and United-States)
- Estonian
- French
- Galician
- German (Austria, Germany and Switzerland)
- Greek
- Hungarian
- Icelandic
- Italian
- Lithuanian
- Latvian
- Norwegian (Bokmål and Nynorsk)
- Polish
- Portuguese (Brazil and Portugal)
- Romanian
- Russian
- Serbian (cyrillic and latin)
- Slovak
- Slovenian
- Spanish
- Swedish
- Telugu
- Ukrainian
- Zulu


Download
--------

{% assign releases = site.github.releases | where:"draft",false | sort:"created_at" | reverse %}
{% assign latest_release = releases[0] %}

Latest version of Pyphen is {{ latest_release.tag_name }}, released on
{{ latest_release.created_at | date: "%B %-d, %Y" }}.

Pyphen is [available on PyPI](http://pypi.python.org/pypi/Pyphen/). To
install, just type `pip install pyphen` as superuser.

Pyphen is also packaged for ArchLinux, CentOS, Gentoo, Fedora and Mageia.

If you want the development version, take a look at the
[git repository on GitHub]({{ site.github.repository_url }}), or clone it
thanks to `git clone git://github.com/Kozea/Pyphen.git`.

You can also download
[the Pyphen package of the git repository]({{ site.github.repository_url }}/tarball/master).


Contribute
----------

Features, bugs, hacks, documentation, tests, dictionaries? Fork us on
[GitHub]({{ site.github.repository_url }}), or chat with us on IRC (`##kozea`
on Freenode).


License
-------

Pyphen is a friendly fork of the unmaintained
[python-hyphenator](https://code.google.com/p/python-hyphenator/) module.

Pyphen is released under the GPL 2.0+ ~ LGPL 2.1+ ~ MPL 1.1 tri-license. See
`COPYING.GPL`, `COPYING.LGPL` and `COPYING.MPL` for more details.

The dictionaries included in Pyphen come from the LibreOffice’s git repository
and are distributed under GPL, LGPL and/or MPL. See the dictionaries and
[LibreOffice's repository](http://cgit.freedesktop.org/libreoffice/dictionaries/tree/)
for more details.
