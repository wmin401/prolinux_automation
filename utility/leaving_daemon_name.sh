#!/bin/bash
file=$1
while read line; do
        removed_path=${line##*/}
        echo $removed_path
done < $file

# using this script when leaved daemon service name
