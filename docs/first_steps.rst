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
