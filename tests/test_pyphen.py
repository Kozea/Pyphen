"""

Pyphen Tests
============

Tests can be launched with Pytest.

"""


from pathlib import Path

import pytest

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


def test_dict_from_filename():
    """Test a dict open from filename."""
    dic_path = Path(__file__).parents[1] / 'pyphen' / 'dictionaries' / 'hyph_fr.dic'
    dic = pyphen.Pyphen(filename=str(dic_path))
    assert dic.inserted('bonjour') == 'bon-jour'


def test_dict_from_path():
    """Test a dict open from path."""
    dic_path = Path(__file__).parents[1] / 'pyphen' / 'dictionaries' / 'hyph_fr.dic'
    dic = pyphen.Pyphen(filename=dic_path)
    assert dic.inserted('bonjour') == 'bon-jour'


def test_dict_with_microsoft_cp1251_encoding(tmp_path):
    """Test a dict whose declared encoding is not a Python codec name."""
    dic_path = tmp_path / 'hyph_bg_BG.dic'
    dic_path.write_bytes('microsoft-cp1251\nч1н\n'.encode('cp1251'))
    dic = pyphen.Pyphen(filename=dic_path, cache=False)
    assert dic.inserted('речник') == 'реч-ник'


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
    assert pyphen.language_fallback('sr-Latn') == 'sr_Latn'
    assert pyphen.language_fallback('SR-LATN') == 'sr_Latn'
    assert pyphen.language_fallback('sr-Cyrl') == 'sr'
    assert pyphen.language_fallback('fr-Latn-FR') == 'fr'
    assert pyphen.language_fallback('en-US_variant1-x') == 'en_US'


def test_register(tmp_path):
    """Test dictionary registration."""
    path = tmp_path / 'hyph_custom.dic'
    path.write_text('UTF-8\nhyp1hen')
    try:
        pyphen.LANGUAGES['en_XX'] = path
        assert pyphen.Pyphen(lang='en_XX').inserted('hyphen') == 'hyp-hen'
        assert pyphen.Pyphen(lang='EN_XX-test').inserted('hyphen') == 'hyp-hen'
        assert pyphen.Pyphen(lang='en').inserted('hyphen') == 'hy-phen'
    finally:
        pyphen.LANGUAGES.pop('en_XX', None)


def test_lowercase_expansion():
    """Positions refer to the input, not its longer lowercase form."""
    dic = pyphen.Pyphen(lang='en_GB')
    word = 'İstanbul'
    lower = word.lower()
    for _ in range(2):
        assert dic.positions(lower) == [6]
        assert dic.positions(word) == [5]
        assert dic.inserted(word) == 'İstan-bul'
        assert tuple(dic.iterate(word)) == (('İstan', 'bul'),)
        assert dic.inserted(lower) == 'i\u0307stan-bul'
        assert dic.wrap(word, 6) == ('İstan-', 'bul')
    assert dic.hd.positions(word) == [6]


def test_lowercase_expansion_limits():
    """Both minima count characters in the original word."""
    assert pyphen.Pyphen(lang='en_GB', left=6).positions('İstanbul') == []
    assert pyphen.Pyphen(lang='en_GB', right=3).positions('İstanbul') == [5]
    assert pyphen.Pyphen(lang='en_GB', right=4).positions('İstanbul') == []


def test_lowercase_expansion_boundaries(tmp_path):
    """Do not split a character whose lowercase form has two characters."""
    path = tmp_path / 'hyph_custom.dic'
    path.write_text('UTF-8\na1i1\u03071b1i1\u03071c\n', encoding='utf-8')
    dic = pyphen.Pyphen(filename=path, left=1, right=1)
    assert dic.positions('aİbİc') == [1, 2, 3, 4]
    assert dic.inserted('aİbİc') == 'a-İ-b-İ-c'
    assert dic.positions('ai\u0307bi\u0307c') == [1, 2, 3, 4, 5, 6]


def test_lowercase_expansion_alternative(tmp_path):
    """Translate replacement offsets and lengths without changing the cache."""
    path = tmp_path / 'hyph_custom.dic'
    path.write_text('UTF-8\n.ai\u0307b1c./x=y,2,3\n', encoding='utf-8')
    dic = pyphen.Pyphen(filename=path, left=1, right=1)
    for _ in range(2):
        lower_positions = dic.positions('ai\u0307bc')
        assert lower_positions == [4]
        assert lower_positions[0].data == ('x=y', -3, 3)
        positions = dic.positions('aİbc')
        assert positions == [3]
        assert positions[0].data == ('x=y', -2, 2)
        assert dic.inserted('aİbc') == 'ax-yc'
        assert tuple(dic.iterate('aİbc')) == (('ax', 'yc'),)
        assert dic.inserted('AİBC') == 'AX-YC'


@pytest.mark.parametrize('alternative', ['3,2', '2,1'])
def test_lowercase_expansion_partial_alternative(tmp_path, alternative):
    """A replacement cannot remove only part of a lowercase expansion."""
    path = tmp_path / 'hyph_custom.dic'
    path.write_text(
        f'UTF-8\n.ai\u0307b1c./x=y,{alternative}\n', encoding='utf-8')
    dic = pyphen.Pyphen(filename=path, left=1, right=0)
    assert dic.positions('ai\u0307bc') == [4]
    assert dic.positions('aİbc') == []


def test_contextual_lowercase(tmp_path):
    """Keep whole-word lowercasing, including the Greek final sigma."""
    path = tmp_path / 'hyph_custom.dic'
    path.write_text('UTF-8\n\u03bf1ς\n', encoding='utf-8')
    dic = pyphen.Pyphen(filename=path, left=1, right=1)
    assert dic.inserted('ΟΣ') == '\u039f-Σ'
    assert dic.inserted('İΟΣ') == 'İΟ-Σ'


def test_lowercase_expansion_internal_boundary(tmp_path):
    """A lowercase-only boundary must not become a different input boundary."""
    path = tmp_path / 'hyph_custom.dic'
    path.write_text('UTF-8\nai1\u0307b\n', encoding='utf-8')
    dic = pyphen.Pyphen(filename=path, left=1, right=1)
    assert dic.positions('ai\u0307b') == [2]
    assert dic.positions('aİb') == []
    assert dic.inserted('aİb') == 'aİb'
    assert tuple(dic.iterate('aİb')) == ()


def test_lowercase_expansion_before_alternative(tmp_path):
    """An expansion before the replacement shifts both range boundaries."""
    path = tmp_path / 'hyph_custom.dic'
    path.write_text('UTF-8\n.i\u0307ab1c./x=y,4,1\n', encoding='utf-8')
    dic = pyphen.Pyphen(filename=path, left=1, right=1)
    assert dic.positions('İabc') == [3]
    assert dic.positions('İabc')[0].data == ('x=y', -1, 1)
    assert dic.inserted('İabc') == 'İax-yc'
    assert tuple(dic.iterate('İabc')) == (('İax', 'yc'),)
