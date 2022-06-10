#!/bin/bash
file=$1
while read line; do
        echo $line
        dnf module info $line | grep apache-commons
done < $file