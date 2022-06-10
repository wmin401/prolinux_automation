#!/bin/bash
file=$1

echo "!!!!!FIND BINARY!!!!!"
while read line; do
        echo -e "\n====="$line"====="
        rpm -ql $line | grep bin/
        echo "=====END====="
done < $file

echo -e "\n!!!!!FIND DAEMON!!!!!"
while read line; do
        echo -e "\n====="$line"====="
        rpm -ql $line | grep -e .service -e .socket -e .timer -e .target -e .mount -e .automount -e .path -e .slice
        echo "=====END====="
done < $file

# 인자로 package list를 입력으로 받아 binary 파일과 .service, .socket, .timer, .target, .mount, .automount, .path, .slice 파일을 찾는 스크립트
# 포함되는 문자가 있을 경우 무조건 출력하므로 출력되는 결과에 대해 검토 필요
