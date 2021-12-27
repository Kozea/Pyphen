Going Further
=============


Why pyphen?
-----------

pyphen has been created to handle hyphenation in WeasyPrint_.

We wanted to provide a simple Python API and to include hyphenation
dictionaries. So we forked the discontinued python-hyphenator module, written
by Wilbert Berendsen, and released pyphen.

.. _WeasyPrint: https://www.courtbouillon.org/weasyprint

Why Python?
-----------

Python is a really good language to design a small, OS-agnostic parser. As it
is object-oriented, it gives the possibility to follow the specification with
high-level classes and a small amount of very simple code.

And of course, WeasyPrint is written in Python too, giving an obvious reason
for this choice.

Speed is not pyphen’s main goal. Code simplicity, maintainability and
flexibility are more important goals for this library, as they give the ability
to stay really close to the specification and to fix bugs easily.
