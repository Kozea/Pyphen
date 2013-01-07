import os.path
from distutils.core import setup

classifiers = [
    'Development Status :: 4 - Beta',
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
    name='Pyphen',
    version='0.6',
    packages=['pyphen'],
    provides=['pyphen'],
    package_data={'pyphen': ['dictionaries/*.dic']},
    author='Guillaume Ayoub',
    author_email='guillaume.ayoub@kozea.fr',
    url='https://github.com/Kozea/Pyphen',
    description='Pure Python module to hyphenate text',
    zip_safe=False,
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README')).read(),
    classifiers=classifiers,
)
