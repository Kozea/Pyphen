import os.path
from distutils.core import setup

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: '
    'GNU Library or Lesser General Public License (LGPL)',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.1',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Text Processing',
    'Topic :: Text Processing :: Linguistic',
]

setup(
    name='hyphenator',
    version='0.5.1',
    py_modules=['hyphenator'],
    author='Wilbert Berendsen',
    author_email='wbsoft@xs4all.nl',
    url='http://python-hyphenator.googlecode.com/',
    description=(
        'Pure Python module to hyphenate text '
        'using existing dictionaries'),
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README')).read(),
    classifiers=classifiers,
)
