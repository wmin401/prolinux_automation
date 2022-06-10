#!/bin/bash
file=$1
while read line; do
	#repository_version=$(repoquery --queryformat %{VERSION} $line)
	repository_version=$(repoquery -a --queryformat %{VERSION} $line) # 7버전용
	installed_version=$(rpm -q --queryformat %{VERSION} $line)

	if [[ $repository_version == $installed_version ]]; then
		echo $line":PASS"
	else
		echo $line":FAIL"
	fi
done < $file

# input : package name list (ex. acl)
# extract only name method : rpm -qa --queryformat '%{NAME}\n' | sort > test_list
