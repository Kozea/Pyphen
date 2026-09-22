"""

Pyphen Tests
============

Tests can be launched with Pytest.

"""


import importlib.util
from pathlib import Path
from zipfile import Path as ZipPath
from zipfile import ZipFile

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


def test_dictionary_resources_from_zip(tmp_path, monkeypatch):
    """Discover and read dictionaries whose resources are not filesystem paths."""
    archive_path = tmp_path / 'dictionaries.zip'
    with ZipFile(archive_path, 'w') as archive:
        # Reverse language order to check that the short-name choice is stable.
        archive.writestr('hyph_en_US.dic', 'UTF-8\nab1cd\n')
        archive.writestr('hyph_en_GB.dic', 'UTF-8\nab1cd\n')
        archive.writestr('README.txt', 'Not a hyphenation dictionary')

    with ZipFile(archive_path) as archive:
        dictionaries = ZipPath(archive)
        monkeypatch.setattr(pyphen.resources, 'files', lambda _: dictionaries)
        spec = importlib.util.spec_from_file_location(
            'pyphen_from_zip', pyphen.__file__)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        assert set(module.LANGUAGES) == {'en', 'en_GB', 'en_US'}
        assert module.LANGUAGES['en'].name == 'hyph_en_GB.dic'
        assert module.Pyphen(lang='en').inserted('abcd') == 'ab-cd'
