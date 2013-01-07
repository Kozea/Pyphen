# This file is part of Pyphen
#
# Copyright 2008 - Wilbert Berendsen <info@wilbertberendsen.nl>
# Copyright 2012 - Guillaume Ayoub <guillaume.ayoub@kozea.fr>
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

Pyphen
======

Pure Python module to hyphenate text, inspired by Ruby's Text::Hyphen.

"""

from __future__ import unicode_literals

import os
import re


__all__ = ('Pyphen', 'LANGUAGES')

# cache of per-file HyphDict objects
hdcache = {}

# precompile some stuff
parse_hex = re.compile(r'\^{2}([0-9a-f]{2})').sub
parse = re.compile(r'(\d?)(\D?)').findall

# included dictionaries
dictionaries_root = os.path.join(os.path.dirname(__file__), 'dictionaries')
LANGUAGES = dict(
    (filename[5:-4], os.path.join(dictionaries_root, filename))
    for filename in os.listdir(dictionaries_root)
    if filename.endswith('.dic'))


class AlternativeParser(object):
    """Parser of nonstandard hyphen pattern alternative.

    The instance returns a special int with data about the current position in
    the pattern when called with an odd value.

    """
    def __init__(self, pattern, alternative):
        alternative = alternative.split(',')
        self.change = alternative[0]
        if len(alternative) > 2:
            self.index = int(alternative[1])
            self.cut = int(alternative[2]) + 1
        else:
            self.index = 1
            self.cut = len(re.sub(r'[\d\.]', '', pattern)) + 1
        if pattern.startswith('.'):
            self.index += 1

    def __call__(self, value):
        self.index -= 1
        value = int(value)
        if value % 2:
            return value
        else:
            return DataInt(value, (self.change, self.index, self.cut))


class DataInt(int):
    """``int`` with some other data can be stuck to in a ``data`` attribute."""
    def __new__(cls, value, data=None, reference=None):
        """Create a new ``DataInt``.

        Call with ``reference=dataint_object`` to use the data from another
        ``DataInt``.

        """
        obj = int.__new__(cls, value)
        obj.data = reference.data if isinstance(reference, DataInt) else None
        return obj


class HyphDict(object):
    """Hyphenation patterns."""

    def __init__(self, filename):
        """Read a ``hyph_*.dic`` and parse its patterns.

        :param filename: filename of hyph_*.dic to read

        """
        self.patterns = {}

        with open(filename, 'rb') as stream:
            charset = stream.readline().strip().decode('ascii')
            if charset.startswith('charset '):
                charset = charset[8:].strip()

            for pattern in stream:
                pattern = pattern.decode(charset).strip()
                if not pattern or pattern[0] == '%':
                    continue

                # replace ^^hh with the real character
                pattern = parse_hex(
                    lambda match: unichr(int(match.group(1), 16)), pattern)

                # read nonstandard hyphen alternatives
                if '/' in pattern:
                    pattern, alternative = pattern.split('/', 1)
                    factory = AlternativeParser(pattern, alternative)
                else:
                    factory = int

                tags, values = zip(*[
                    (string, factory(i or '0'))
                    for i, string in parse(pattern)])

                # if only zeros, skip this pattern
                if max(values) == 0:
                    continue

                # chop zeros from beginning and end, and store start offset
                start, end = 0, len(values)
                while not values[start]:
                    start += 1
                while not values[end - 1]:
                    end -= 1

                self.patterns[''.join(tags)] = start, values[start:end]

        self.cache = {}
        self.maxlen = max(map(len, self.patterns.keys()))

    def positions(self, word):
        """Get a list of positions where the word can be hyphenated.

        :param word: unicode string of the word to hyphenate

        E.g. for the dutch word 'lettergrepen' this method returns ``[3, 6,
        9]``.

        Each position is a ``DataInt`` with a data attribute.

        If the data attribute is not ``None``, it contains a tuple with
        information about nonstandard hyphenation at that point: ``(change,
        index, cut)``.

        change
          a string like ``'ff=f'``, that describes how hyphenation should
          take place.

        index
          where to substitute the change, counting from the current point

        cut
          how many characters to remove while substituting the nonstandard
          hyphenation

        """
        word = word.lower()
        points = self.cache.get(word)
        if points is None:
            pointed_word = '.%s.' % word
            references = [0] * (len(pointed_word) + 1)

            for i in range(len(pointed_word) - 1):
                for j in range(
                        i + 1, min(i + self.maxlen, len(pointed_word)) + 1):
                    pattern = self.patterns.get(pointed_word[i:j])
                    if pattern:
                        offset, value = pattern
                        slice_ = slice(i + offset, i + offset + len(value))
                        references[slice_] = map(
                            max, value, references[slice_])

            points = [
                DataInt(i - 1, reference=reference)
                for i, reference in enumerate(references) if reference % 2]
            self.cache[word] = points
        return points


class Pyphen(object):
    """Hyphenation class, with methods to hyphenate strings in various ways."""

    def __init__(self, filename=None, lang=None, left=2, right=2, cache=True):
        """Create an hyphenation instance for given lang or filename.

        :param filename: filename of hyph_*.dic to read
        :param lang: lang of the included dict to use if no filename is given
        :param left: minimum number of characters of the first syllabe
        :param right: minimum number of characters of the last syllabe
        :param cache: if ``True``, use cached copy of the hyphenation patterns

        """
        if not filename:
            filename = LANGUAGES[lang]
        self.left = left
        self.right = right
        if not cache or filename not in hdcache:
            hdcache[filename] = HyphDict(filename)
        self.hd = hdcache[filename]

    def positions(self, word):
        """Get a list of positions where the word can be hyphenated.

        :param word: unicode string of the word to hyphenate

        See also ``HyphDict.positions``. The points that are too far to the
        left or right are removed.

        """
        right = len(word) - self.right
        return [i for i in self.hd.positions(word) if self.left <= i <= right]

    def iterate(self, word):
        """Iterate over all hyphenation possibilities, the longest first.

        :param word: unicode string of the word to hyphenate

        """
        for position in reversed(self.positions(word)):
            if position.data:
                # get the nonstandard hyphenation data
                change, index, cut = position.data
                index += position
                if word.isupper():
                    change = change.upper()
                c1, c2 = change.split('=')
                yield word[:index] + c1, c2 + word[index + cut:]
            else:
                yield word[:position], word[position:]

    def wrap(self, word, width, hyphen='-'):
        """Get the longest possible first part and the last part of a word.

        :param word: unicode string of the word to hyphenate
        :param width: maximum length of the first part
        :param hyphen: unicode string used as hyphen character

        The first part has the hyphen already attached.

        Returns ``None`` if there is no hyphenation point before ``width``, or
        if the word could not be hyphenated.

        """
        width -= len(hyphen)
        for w1, w2 in self.iterate(word):
            if len(w1) <= width:
                return w1 + hyphen, w2

    def inserted(self, word, hyphen='-'):
        """Get the word as a string with all the possible hyphens inserted.

        :param word: unicode string of the word to hyphenate
        :param hyphen: unicode string used as hyphen character

        E.g. for the dutch word ``'lettergrepen'``, this method returns the
        unicode string ``'let-ter-gre-pen'``. The hyphen string to use can be
        given as the second parameter, that defaults to ``'-'``.

        """
        word_list = list(word)
        for position in reversed(self.positions(word)):
            if position.data:
                # get the nonstandard hyphenation data
                change, index, cut = position.data
                index += position
                if word.isupper():
                    change = change.upper()
                word_list[index:index + cut] = change.replace('=', hyphen)
            else:
                word_list.insert(position, hyphen)

        return ''.join(word_list)

    __call__ = iterate
