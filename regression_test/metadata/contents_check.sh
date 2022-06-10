#!/bin/bash
file=$1
while read line; do
	#grep -rn "Warning : Intel Processor" $line
	grep -irn -E "Red Hat|RedHat|RHEL" $line
done < $file

# Can be used to search RHEL phrases

## This is script for searching words in directory group
## input file example ##

# example.txt
# /bin
# /boot
# /dev
# /etc
# /home
# /lib
# /lib64
# /media
# /mnt
# /opt
# /root
# /run
# /sbin
# /srv
# /tmp
# /usr
# /var

# trouble_shooting_example.txt
# /bin
# /boot
# /dev
# /etc
# /firmware
# /home
# /lib
# /lib64
# /lost+found
# /mnt
# /modules
# /root
# /run
# /sbin
# /srv
# /tmp
# /usr
# /var
