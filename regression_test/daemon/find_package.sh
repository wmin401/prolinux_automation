#!/bin/sh
file=$1

while read line; do
        install_message=$(yum provides $line | sed -n 2p)
        echo $line";"${install_message%% : *}
done < $file

# 인자로 데몬 리스트 (ex. /usr/lib/systemd/system/dhcrelay.service)가 들어 왔을 때 해당 데몬이 속한 패키지를 출력
