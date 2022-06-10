#!/bin/bash
file=$1

while read line; do
        echo $(repoquery --queryformat '%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}\n' $line)
done < $file
