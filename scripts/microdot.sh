#!/bin/bash

if [ -z "$1" ]; then
  PORT="/dev/ttyUSB0"
else
  PORT="$1"
fi

. .venv/bin/activate

rshell --port "${PORT}" --rts 0 --dtr 0 rm -rf /pyboard/lib/microdot/
rshell --port "${PORT}" --rts 0 --dtr 0 mkdir /pyboard/lib
rshell --port "${PORT}" --rts 0 --dtr 0 mkdir /pyboard/lib/microdot
rshell --port "${PORT}" --rts 0 --dtr 0 cp -r .microdot/* /pyboard/lib/microdot

deactivate