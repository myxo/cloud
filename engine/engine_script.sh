#!/bin/bash

unzip -o  $1.zip -d$1
cd $1
chmod +x run.sh
./run.sh &
python ../check_is_done.py $! $1 $2