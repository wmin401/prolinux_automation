#!/bin/bash
file=$1
while read line; do
        removed_release=${line%-*}
        echo ${removed_release%-*}
done < $file

# using this script when leaved package name
