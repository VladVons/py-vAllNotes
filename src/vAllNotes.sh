#!/bin/bash

py=python3
Dir=~/virt/python3
Src=$Dir/bin/activate
echo "env: $Src"
source $Src

python3 -B vAllNotes.py --conf Dev
