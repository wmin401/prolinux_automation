#!/bin/bash
file=$1
# 상태를 나타내는 비교 string
inactive="Active: inactive"
active="Active: active"
failed="Active: failed"
# 두번의 테스트를 진행하여 테스트 전의 상태로 복귀
pass_num=2

systemctl daemon-reload
while read line; do
	success_count=0
	fail_count=0
	exception_count=0
	status_message=$(systemctl status ${line#/usr/lib/systemd/system/} 2>&1)
	# 정규식을 통해 상태 메시지에 문구 포함 여부 확인
	if [[ $status_message =~ $inactive ]] || [[ $status_message =~ $failed ]]; then
		#echo "inactive -> active"
		systemctl start ${line#/usr/lib/systemd/system/}
		sleep 1
		status_message=$(systemctl status ${line#/usr/lib/systemd/system/} 2>&1)
		if [[ $status_message =~ $inactive ]]; then
			#echo $line",start failed"
			fail_count=$((fail_count+1))
		elif [[ $status_message =~ $active ]]; then
			#echo $line",start success"
			success_count=$((success_count+1))
			systemctl stop ${line#/usr/lib/systemd/system/}
			sleep 1
			status_message=$(systemctl status ${line#/usr/lib/systemd/system/} 2>&1)
			if [[ $status_message =~ $inactive ]]; then
				#echo "$line,stop success"
				success_count=$((success_count+1))
			elif [[ $status_message =~ $active ]]; then
				#echo $line",stop failed"
				fail_count=$((fail_count+1))
			else
				#echo $line",Exception"
				exception_count=$((exception_count+1))
			fi
		else
			#echo $line",Exception"
			exception_count=$((exception_count+1))
		fi
	elif [[ $status_message =~ $active ]]; then
		#echo "active -> inactive"
		systemctl stop ${line#/usr/lib/systemd/system/}
		status_message=$(systemctl status ${line#/usr/lib/systemd/system/} 2>&1)
		if [[ $status_message =~ $inactive ]]; then
			#echo "$line,stop success"
			success_count=$((success_count+1))
			systemctl start ${line#/usr/lib/systemd/system/}
			sleep 1
			status_message=$(systemctl status ${line#/usr/lib/systemd/system/} 2>&1)
			if [[ $status_message =~ $inactive ]]; then
				#echo $line",start failed"
				fail_count=$((fail_count+1))
			elif [[ $status_message =~ $active ]]; then
				#echo $line",start success"
				success_count=$((success_count+1))
			else
				#echo $line",Exception"
				exception_count=$((exception_count+1))
			fi
		elif [[ $status_message =~ $active ]]; then
			#echo $line",stop failed"
			fail_count=$((fail_count+1))
		else
			#echo $line",Exception"
			exception_count=$((exception_count+1))
		fi
	else
		#echo $line",Exception"
		exception_count=$((exception_count+1))
	fi
	# 2번의 테스트를 통해 모두 통과하면 PASS, 아니면 FAIL
	if [ $success_count -eq $pass_num ]; then
		echo $line",PASS"
	else
		echo $line",FAIL"
	fi
done < $file
