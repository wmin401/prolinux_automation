#!/bin/bash
file=$1
while read line; do
        rpm -q $line
done < $file

