#!/bin/bash
file=$1
while read line; do
        ls Packages/ | grep $line
done < $file

# find package from directory
