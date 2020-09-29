#!/bin/bash
FILES=../docs/scripting_examples/*.py
for f in $FILES
do 
  python $f > $f.out
done
