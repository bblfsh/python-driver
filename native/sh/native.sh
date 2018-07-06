#!/bin/sh
if [ -x "$HOME/build/.local/bin/python_driver" ]
then
    python3 $HOME/build/.local/bin/python_driver
elif [ -x "../../build/.local/bin/python_driver" ]
then
    export PYTHONPATH=../../build/.local/lib/python3.6/site-packages:$PYTHONPATH
    python3 ../../build/.local/bin/python_driver
else
    python3 python_driver
fi
