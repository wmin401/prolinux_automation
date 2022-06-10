#!/bin/bash
file=$1

echo "====================="
while read line; do
        echo $line
        yum install -y $line 2>&1
        echo "====================="
done < $file
