# coding=UTF-8

import os
from setuptools import setup, find_packages
from codecs import open
from os import path


long_description = 'Raumfeld controlled by python scripts'
here = path.abspath(path.dirname(__file__))
s = path.join(here, 'README.rst')

if os.path.exists(s):
    long_description = open('README.rst', 'r', encoding='utf8').read()
else:
    print("cant open readme.rst")

setup(
    name='hpd20',
    version='0.0.7',
    author='Jürgen Schwietering',
    author_email='scjurgen@yahoo.com',
    description='hpd-20 simple patch editor and librarian',
    long_description=long_description,
    license='MIT',
    keywords=['roland', 'handsonic', 'hpd20', 'hpd-20', 'percussion', 'editor', 'librarian', 'kit', 'pad'],
    url='http://github.com/scjurgen/hpd-20',
    packages=['hpd20', ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Multimedia :: Sound/Audio :: Editors',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 2.7',
    ],
    #py_modules=['hpd20'],
    # https://packaging.python.org/en/latest/requirements.html
    #install_requires=['wx'],
    install_requires=['ConfigParser',],
    #packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    entry_points={
        'console_scripts': [
            'hpd20-ui=hpd20.hpd20wx:run_main',
            'hpd20-cli=hpd20.hpd20:run_main'
        ],
    }
)
