#!/bin/bash
file=$1
number=0

while read line; do
    number=$((number+1))
    echo $number,Included File,$line,$(rpm -ql $line)
done < $file