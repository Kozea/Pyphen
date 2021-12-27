First Steps
===========


Installation
------------

The easiest way to use pyphen is to install it in a Python `virtual
environment`_. When your virtual environment is activated, you can then install
pyphen with pip_::

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
* Belarusian
* Bulgarian
* Catalan
* Croatian
* Czech
* Danish
* Dutch
* English (Great-Britain and United-States)
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
* Lithuanian
* Latvian
* Mongolian
* Norwegian (Bokmål and Nynorsk)
* Polish
* Portuguese (Brazil and Portugal)
* Romanian
* Russian
* Serbian (cyrillic and latin)
* Slovak
* Slovenian
* Spanish
* Swedish
* Telugu
* Ukrainian
* Zulu
