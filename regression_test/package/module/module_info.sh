#!/bin/bash
file=$1

echo "===================================="
while read line; do
        echo $line
        dnf module info $line
        echo "===================================="
done < $file
