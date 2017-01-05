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
    version='0.0.1',
    author='Jürgen Schwietering',
    author_email='scjurgen@yahoo.com',
    description='HPD-20 simple patch editor and librarian',
    long_description=long_description,
    license='MIT',
    keywords=['roland', 'handsonic', 'hpd-20', 'percussion', 'editor', 'librarian', 'kit', 'pad'],
    url='http://github.com/scjurgen/hpd20',
    packages=['hpd20', ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Other Environment',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Multimedia :: Sound/Audio :: Editors',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 2.7',
    ],
    #py_modules=['hpd20','DirBrowse'],
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['wx'],
    #packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    entry_points={
        'console_scripts': [
            'hpd20=hpd20.hpd20wx:run_main',
            'hpd20ui=hpd20.hpd20:run_main'
        ],
    }
)