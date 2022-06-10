#!/bin/bash
file=$1

while read line; do
  rpm -ql $line | grep -e .service -e .socket -e .timer -e .target -e .mount -e .automount -e .path -e .slice
done < $file

# 인자로 package list를 입력으로 받아 binary 파일을 찾는 스크립트
# 포함되는 문자가 있을 경우 무조건 출력하므로 출력되는 결과에 대해 검토 필요
