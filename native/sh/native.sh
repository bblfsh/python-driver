#!/bin/sh
if [ -x "$HOME/.local/bin/python_driver" ]
then
    exec $HOME/.local/bin/python_driver
else
    exec python_driver
fi
