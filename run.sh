#!/bin/bash

# Michelle Yang copyright 2019
# script that generates necessary files

SCRIPT=data_analysis/script_data.json

if [ ! 1 -eq $# ]; then
   echo "Usage: ./run <*.json>"
   exit 1
fi

if [ ! -r $1 ]; then
    echo "File does not exist or read permission not granted."
    exit 1
fi

echo "datum = " > $SCRIPT
cat $1 >> $SCRIPT
echo ";" >> $SCRIPT
