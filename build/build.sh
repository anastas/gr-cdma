#!/bin/bash
echo "i/install for compiling and install"
echo "u/uninstall for uninstall"
read cmd
if [ $cmd == "i" ] || [ $cmd == "install" ]; then
	cmake -DENABLE_DOXYGEN=ON ../
	make
	sudo make install
	sudo ldconfig
elif [ $cmd == "u" ] || [ $cmd == "uninstall" ]; then
	sudo make uninstall
fi
