
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ODCanToolkit',
    version='0.1dev',
    description='Python tool to fetch data from Canada\'s open data portal',
    long_description=long_description,

    url='https://github.com/gchamp20/ODCanToolkit',

    author='Guillaume Champagne',
    author_email='guillaume.champagne@polymtl.ca',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='canada open data json mongodb',

    packages=find_packages(exclude=['data', 'results', 'tests']),

    # List run-time dependencies here.
    install_requires=['pymongo'],

    # List additional groups of dependencies here (e.g. development
    # dependencies).
    extras_require={
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'ODCanToolkit=ODCanToolkit:launch',
        ],
    },
)
