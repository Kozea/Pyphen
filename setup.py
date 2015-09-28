import os.path
from setuptools import setup

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
    'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
    'License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.1',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Text Processing',
    'Topic :: Text Processing :: Linguistic',
]

_dict_folder = os.path.join(os.path.dirname(__file__), 'dictionaries')
setup(
    name='Pyphen',
    version='0.9.2',
    py_modules=['pyphen'],
    provides=['pyphen'],
    data_files=[(
        os.path.join('share', 'pyphen', 'dictionaries'), (
            os.path.join(_dict_folder, filename)
            for filename in os.listdir(_dict_folder)
            if filename.endswith('.dic')))],
    author='Guillaume Ayoub',
    author_email='guillaume.ayoub@kozea.fr',
    url='https://github.com/Kozea/Pyphen',
    description='Pure Python module to hyphenate text',
    zip_safe=False,
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README')).read(),
    classifiers=classifiers,
)
