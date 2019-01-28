#!/bin/bash
apt-get update
apt-get install -y build-essential python python-setuptools python-dev zip libgtest-dev
easy_install pip
pip install PyYAML

apt-get install -y cmake
cd /usr/src/gtest
cmake CMakeLists.txt
make
cp *.a /usr/lib
