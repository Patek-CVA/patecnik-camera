#!/bin/bash

if [ -z "$1" ]; then
  PORT="/dev/ttyUSB0"
else
  PORT="$1"
fi

. .venv/bin/activate

rshell --port "${PORT}" --rts 0 --dtr 0

deactivate