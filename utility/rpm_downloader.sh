#!/bin/bash
file=$1

yum -y install yum-utils

while read line; do
	yumdownloader $line
done < $file

# Using package name list for $line
# This scripts can download rpm file from remote server
