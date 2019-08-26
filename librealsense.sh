#!/bin/bash

kernel_version=`uname -r`

echo 
echo Kernel version = $kernel_version 

echo 
echo If kernel version is 4.4.X, 4.8.X or 4.10.X press c to continue...
echo If not press any other key...

read -rsn1 input
if [ "$input" = "c" ]; then

    sudo apt-get update && sudo apt-get -y upgrade
    sudo apt-get install -y git cmake
    sudo apt-get install -y libudev-dev pkg-config libgtk-3-dev
    sudo apt-get install -y libglfw3-dev
    sudo apt-get install -y libssl-dev
    sudo apt-get install -y libusb-1.0-0-dev libusb-1.0-doc
    sudo apt-get install -y python3 python3-dev

    cd ~
    git clone https://github.com/IntelRealSense/librealsense.git
    cd librealsense
    mkdir -p build && cd build
    cmake ../ -DBUILD_EXAMPLES=true -DBUILD_PYTHON_BINDINGS=bool:true
    cores=`nproc`
    sudo make uninstall && make clean && make -j$cores && sudo make install

    cd ..
    sudo cp config/99-realsense-libusb.rules /etc/udev/rules.d/
    sudo udevadm control --reload-rules && udevadm trigger

    sudo ./scripts/patch-realsense-ubuntu-xenial.sh
  
  if grep -Fxq 'export PYTHONPATH=$PYTHONPATH:/usr/local/lib' ~/.bashrc
    then
        echo PYTHONPATH already in .bashrc file
    else
        echo 'export PYTHONPATH=$PYTHONPATH:/usr/local/lib' >> ~/.bashrc 
        echo PYTONPATH added to ~/.bashrc. Pyhon wrapper is now available using import pyrealsense2
    fi

fi
