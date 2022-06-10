#!/bin/bash
file=$1

while read line; do
        echo $(dnf module install -y $line)
done < $file

# 패키지 셋으로 설치가 안되는 모듈8개
# 389-ds, container-tools, golang-ecosystem, libselinux-python, mod_auth_openidc, parfait, pki-core, pki-deps
# mysql 와 mariadb는 conflict
