#!/bin/bash
file=$1
while read line; do
        echo ${line%-*}
done < $file

# using this script when removing src, rpm, el*, etc.
