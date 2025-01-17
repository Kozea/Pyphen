First Steps
===========


Installation
------------

The easiest way to use Pyphen is to install it in a Python `virtual
environment`_. When your virtual environment is activated, you can then install
Pyphen with pip_::

    pip install pyphen

.. _virtual environment: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
.. _pip: https://pip.pypa.io/


Short Example
-------------

.. code-block:: python

   >>> dic = pyphen.Pyphen(lang='fr_FR')
   >>> dic.inserted('fromage')
   'fro-mage'


Included Dictionaries
---------------------

The dictionaries included in LibreOffice are distributed with Pyphen:

* Afrikaans
* Albanian
* Assamese
* Basque
* Belarusian
* Bulgarian
* Catalan
* Croatian
* Czech
* Danish
* Dutch
* English (United Kingdom and United States)
* Esperanto
* Estonian
* French
* Galician
* German (Austria, Germany and Switzerland)
* Greek
* Hungarian
* Icelandic
* Indonesian
* Italian
* Kannada
* Lithuanian
* Latvian
* Marathi
* Mongolian
* Norwegian (Bokmål and Nynorsk)
* Oriya
* Polish
* Portuguese (Brazil and Portugal)
* Punjabi
* Romanian
* Russian
* Sanskrit
* Serbian (Cyrillic and Latin)
* Slovak
* Slovenian
* Spanish
* Swedish
* Telugu
* Thai
* Ukrainian
* Zulu
