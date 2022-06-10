#!/bin/bash
file=$1

echo "===================================="
while read line; do
        echo $line
        dnf deplist $line | grep insights-client
        echo "===================================="
done < $file
