# -*- coding: utf-8 -*-
# This file is part of Pyphen
#
# Copyright 2013 - Guillaume Ayoub <guillaume.ayoub@kozea.fr>
#
# This library is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyphen.  If not, see <http://www.gnu.org/licenses/>.

"""

Pyphen Tests
============

Tests can be launched with:

- Pytest (``py.test test.py``).
- Nose (``nosetests``).

"""


from __future__ import unicode_literals

import pyphen


def test_inserted():
    """Test the ``inserted`` method."""
    dic = pyphen.Pyphen(lang='nl_NL')
    assert dic.inserted('lettergrepen') == 'let-ter-gre-pen'


def test_wrap():
    """Test the ``wrap`` method."""
    dic = pyphen.Pyphen(lang='nl_NL')
    assert dic.wrap('autobandventieldopje', 11) == (
        'autoband-', 'ventieldopje')


def test_iterate():
    """Test the ``iterate`` method."""
    dic = pyphen.Pyphen(lang='nl_NL')
    assert tuple(dic.iterate('Amsterdam')) == (
        ('Amster', 'dam'), ('Am', 'sterdam'))


def test_fallback_dict():
    """Test the ``iterate`` method with a fallback dict."""
    dic = pyphen.Pyphen(lang='nl_NL-variant')
    assert tuple(dic.iterate('Amsterdam')) == (
        ('Amster', 'dam'), ('Am', 'sterdam'))


def test_missing_dict():
    """Test a missing dict."""
    try:
        pyphen.Pyphen(lang='mi_SS')
    except KeyError:
        pass
    else:  # pragma: no cover
        raise Exception('Importing a missing dict must raise a KeyError')


def test_personal_dict():
    """Test a personal dict."""
    dic = pyphen.Pyphen(lang='fr')
    assert dic.inserted('autobandventieldopje') != 'au-to-band-ven-tiel-dop-je'
    pyphen.LANGUAGES['fr'] = pyphen.LANGUAGES['nl_NL']
    dic = pyphen.Pyphen(lang='fr')
    assert dic.inserted('autobandventieldopje') == 'au-to-band-ven-tiel-dop-je'


def test_left_right():
    """Test the ``left`` and ``right`` parameters."""
    dic = pyphen.Pyphen(lang='nl_NL')
    assert dic.inserted('lettergrepen') == 'let-ter-gre-pen'
    dic = pyphen.Pyphen(lang='nl_NL', left=4)
    assert dic.inserted('lettergrepen') == 'letter-gre-pen'
    dic = pyphen.Pyphen(lang='nl_NL', right=4)
    assert dic.inserted('lettergrepen') == 'let-ter-grepen'
    dic = pyphen.Pyphen(lang='nl_NL', left=4, right=4)
    assert dic.inserted('lettergrepen') == 'letter-grepen'


def test_filename():
    """Test the ``filename`` parameter."""
    dic = pyphen.Pyphen(filename=pyphen.LANGUAGES['nl_NL'])
    assert dic.inserted('lettergrepen') == 'let-ter-gre-pen'


def test_alternative():
    """Test the alternative parser."""
    dic = pyphen.Pyphen(lang='hu', left=1, right=1)
    assert tuple(dic.iterate('kulissza')) == (
        ('kulisz', 'sza'), ('ku', 'lissza'))
    assert dic.inserted('kulissza') == 'ku-lisz-sza'


def test_upper():
    """Test uppercase."""
    dic = pyphen.Pyphen(lang='nl_NL')
    assert dic.inserted('LETTERGREPEN') == 'LET-TER-GRE-PEN'


def test_upper_alternative():
    """Test uppercase with alternative parser."""
    dic = pyphen.Pyphen(lang='hu', left=1, right=1)
    assert tuple(dic.iterate('KULISSZA')) == (
        ('KULISZ', 'SZA'), ('KU', 'LISSZA'))
    assert dic.inserted('KULISSZA') == 'KU-LISZ-SZA'


def test_all_dictionaries():
    """Test that all included dictionaries can be parsed."""
    for lang in pyphen.LANGUAGES:
        pyphen.Pyphen(lang=lang)


def test_fallback():
    """Test the language fallback algorithm."""
    assert pyphen.language_fallback('en') == 'en'
    assert pyphen.language_fallback('en_US') == 'en_US'
    assert pyphen.language_fallback('en_FR') == 'en'
    assert pyphen.language_fallback('en-Latn-US') == 'en_Latn_US'
    assert pyphen.language_fallback('en-Cyrl-US') == 'en'
    assert pyphen.language_fallback('fr-Latn-FR') == 'fr'
    assert pyphen.language_fallback('en-US_variant1-x') == 'en_US'

def test_lang_alias():
    """Test that language alias can be parsed."""
    pyphen.Pyphen(lang='ru')

def test_all_lang_aliases():
    """Test that all language aliases can be parsed."""
    for alias in pyphen.LANGUANGE_ALIASES.iterkeys():
        pyphen.Pyphen(lang=alias)

def test_multiwrap():
    """Test the ``multiwrap`` method."""
    dic = pyphen.Pyphen(lang='en')

    assert dic.multiwrap('galactic', 5) == 'galac-tic'
    assert dic.multiwrap('inter-galactic', 5) == 'inter-galac-tic'

    assert dic.inserted('floccinaucinihilipilification') ==\
            'floc-cin-aucini-hilip-il-i-fi-ca-tion'
    assert dic.multiwrap('floccinaucinihilipilification', 10) ==\
            'floccin-aucini-hilipilifi-cation'
    assert dic.inserted('Antidisestablishmentarianism') ==\
            'An-tidis-es-tab-lish-men-tar-i-an-ism'
    assert dic.multiwrap('Antidisestablishmentarianism', 10) ==\
            'Antidises-tablishmen-tarianism'

def test_hebrew():
    """ Test Hebrew dictionary."""
    dic = pyphen.Pyphen(lang='he')
    assert dic.inserted('אברא-קדברא') == 'אברא-קדברא'

def test_arabic():
    """ Test Arabic dictionary."""
    dic = pyphen.Pyphen(lang='ar')
    assert dic.inserted('عربة قطار') == 'عربة قطار'

