#!/bin/sh
if [ -x "$HOME/build/.local/bin/python_driver" ]
then
    exec $HOME/build/.local/bin/python_driver
else
    exec python_driver
fi
