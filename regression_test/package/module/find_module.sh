#!/bin/bash
file=$1
echo "======================"
while read line; do
        echo $line
        repoquery | grep $line
        echo "======================"
done < $file
