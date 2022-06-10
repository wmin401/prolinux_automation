#!/bin/bash
file=$1
inactive="Active: inactive"
active="Active: active"

while read line; do
        status_message=$(systemctl status ${line#/usr/lib/systemd/system/})
        if [[ $status_message =~ $inactive ]]; then
                #echo "inactive"
		systemctl start ${line#/usr/lib/systemd/system/}
        	status_message=$(systemctl status ${line#/usr/lib/systemd/system/})
        	if [[ $status_message =~ $inactive ]]; then
			echo ${line#/usr/lib/systemd/system/}",inactive start failed"
        	elif [[ $status_message =~ $active ]]; then
			echo ${line#/usr/lib/systemd/system/}",inactive start success"
		else
			echo ${line#/usr/lib/systemd/system/}" has exception"
		fi
        elif [[ $status_message =~ $active ]]; then
		# echo "active"
		systemctl stop ${line#/usr/lib/systemd/system/}
        	status_message=$(systemctl status ${line#/usr/lib/systemd/system/})
        	if [[ $status_message =~ $inactive ]]; then
			echo ${line#/usr/lib/systemd/system/}",active stop success"
        	elif [[ $status_message =~ $active ]]; then
			echo ${line#/usr/lib/systemd/system/}",active stop failed"
		else
			echo ${line#/usr/lib/systemd/system/}" has exception"
		fi
	else
		echo ${line#/usr/lib/systemd/system/}" has exception"
	fi
done < $file
