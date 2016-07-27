#!/bin/bash

build_dir="${SRC_DIR}/../build_dir"

mkdir -p $build_dir
cd $build_dir

cmake $SRC_DIR

make
#sudo ln -s /usr/include/freetype2/freetype /usr/include/freetype
make install

$PYTHON "${RECIPE_DIR}/setup.py" install
