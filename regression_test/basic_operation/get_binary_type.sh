#!/bin/sh
file=$1

echo "===================================="
while read line; do
        echo $line
        sed -n 1p < $line
        echo "===================================="
done < $file

# 인자로 binary list를 입력으로 받아 파일의 첫 줄을 출력하는 스크립트
# ELF, python 코드, Shell Scripts 코드, Ruby Code 코드 등 확인하여 분류
