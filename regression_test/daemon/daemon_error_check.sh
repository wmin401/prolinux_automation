#!/bin/bash
file=$1
inactive="Active: inactive"
active="Active: active"
failed="Active: failed"

echo "====================="
while read line; do
	echo "daemon name: "$line
	status_message=$(systemctl status $line 2>&1)
	if [[ $status_message =~ $inactive ]] || [[ $status_message =~ $failed ]]; then
		systemctl start $line
		journalctl -b -u $line
	elif [[ $status_message =~ $active ]]; then
		systemctl stop $line
		journalctl -b -u $line
	fi
	echo "====================="
done < $file
