rm -rf ./build/launcher/*
cd ./build/launcher
cmake ../.. -DCMAKE_INSTALL_PREFIX=../../testdist
make
make install