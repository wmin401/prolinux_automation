#!/bin/bash
file=$1
while read line; do
        echo ${line%.*}
done < $file

# 모든 것을 떼어내므로 TRANS.TBL 등 확인 필요