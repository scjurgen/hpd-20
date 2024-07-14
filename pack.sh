#!/usr/bin/env bash

versionsetup=`grep "version=" setup.py | sed "s/^.*version=['\"]\([0-9ab.]*\)['\"].*$/\\1/g"`
versionhpd20=`grep "version =" hpd20/hpd20.py | sed "s/^.*version = ['\"]\([0-9ab.]*\)['\"].*$/\\1/g" `

echo hpd20: ${versionhpd20}
echo setup.py ${versionsetup}

if [ "$versionhpd20" != "$versionsetup" ]
then
	echo "The versions are different, please update them before packing"
        sleep 2 
        vi hpd20/hpd20.py +19
        vi setup.py +20
	exit -1
fi

sudo rm -rf hpd20.egg-info
sudo rm -rf dist
sudo rm -rf build
python setup.py build
python setup.py dist 
python setup.py sdist
#python setup.py bdist_wheel
twine upload dist/*

