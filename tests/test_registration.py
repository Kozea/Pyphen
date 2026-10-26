"""Tests for registering application-provided hyphenation dictionaries."""

import pytest

import pyphen


@pytest.fixture(autouse=True)
def isolated_registration(monkeypatch):
    """Keep dictionary registrations and caches local to each test."""
    monkeypatch.setattr(pyphen, 'LANGUAGES', pyphen.LANGUAGES.copy())
    monkeypatch.setattr(
        pyphen, 'LANGUAGES_LOWERCASE', pyphen.LANGUAGES_LOWERCASE.copy())
    monkeypatch.setattr(pyphen, 'hdcache', pyphen.hdcache.copy())


@pytest.fixture
def dictionary_path(tmp_path):
    """Create a small, synthetic dictionary with one hyphenation point."""
    path = tmp_path / 'hyph_custom.dic'
    path.write_text('UTF-8\nhy1phen\n', encoding='utf-8')
    return path


@pytest.mark.parametrize('as_string', [False, True])
def test_register_filename(dictionary_path, as_string):
    """Accept both Path and string filenames through the public API."""
    filename = str(dictionary_path) if as_string else dictionary_path

    pyphen.register('xx', filename)

    assert 'register' in pyphen.__all__
    assert pyphen.LANGUAGES['xx'] == dictionary_path
    assert pyphen.Pyphen(lang='xx').inserted('hyphen') == 'hy-phen'
    assert pyphen.Pyphen(lang='xx_YY').inserted('hyphen') == 'hy-phen'


def test_register_locale_normalization(dictionary_path):
    """Use normal case-insensitive language lookup and variant fallback."""
    pyphen.register('xX-Test', dictionary_path)

    assert pyphen.language_fallback('XX_test_variant') == 'xX_Test'
    assert pyphen.Pyphen(lang='xx-TEST-variant').inserted('hyphen') == 'hy-phen'


def test_register_overrides_only_matching_locale(dictionary_path):
    """Replace the canonical locale without changing its parent language."""
    original_base = pyphen.LANGUAGES['en']
    original_instance = pyphen.Pyphen(lang='en_US')

    pyphen.register('EN-us', dictionary_path)

    assert pyphen.LANGUAGES['en_US'] == dictionary_path
    assert pyphen.LANGUAGES['en'] == original_base
    assert 'EN_us' not in pyphen.LANGUAGES
    replacement = pyphen.Pyphen(lang='en-US')
    assert replacement.inserted('hyphen') == 'hy-phen'
    assert replacement.hd is not original_instance.hd


def test_register_replacement_applies_to_new_instances(dictionary_path, tmp_path):
    """Keep existing instances usable after replacing a registration."""
    pyphen.register('xx', dictionary_path)
    original = pyphen.Pyphen(lang='xx')
    replacement_path = tmp_path / 'hyph_replacement.dic'
    replacement_path.write_text('UTF-8\nhyp1hen\n', encoding='utf-8')

    pyphen.register('XX', replacement_path)

    assert pyphen.Pyphen(lang='xx').inserted('hyphen') == 'hyp-hen'
    assert original.inserted('hyphen') == 'hy-phen'


def test_register_relative_path_survives_chdir(dictionary_path, tmp_path, monkeypatch):
    """Resolve relative filenames when registering them."""
    monkeypatch.chdir(tmp_path)
    pyphen.register('xx', dictionary_path.name)
    other_directory = tmp_path / 'other'
    other_directory.mkdir()
    monkeypatch.chdir(other_directory)

    assert pyphen.Pyphen(lang='xx').inserted('hyphen') == 'hy-phen'


def test_register_empty_language(dictionary_path):
    """Reject an empty language code without changing the registry."""
    original = pyphen.LANGUAGES.copy()

    with pytest.raises(ValueError, match='Language code must not be empty'):
        pyphen.register('', dictionary_path)

    assert pyphen.LANGUAGES == original


def test_register_defers_dictionary_loading(tmp_path):
    """Read the registered file when a hyphenation instance is constructed."""
    path = tmp_path / 'not-created-yet.dic'
    pyphen.register('xx', path)
    path.write_text('UTF-8\nhy1phen\n', encoding='utf-8')

    assert pyphen.Pyphen(lang='xx').inserted('hyphen') == 'hy-phen'
