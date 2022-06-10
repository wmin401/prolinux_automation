#!/bin/bash
file=$1
options_arr=("options" "Options" "OPTIONS")
usage_arr=("usage" "Usage" "USAGE")
help_arr=("-h" "--help")
pass_num=0

while read line; do
  status_message=$(man $line 2>&1)
  pass_count=0
  for o_arr in "${options_arr[@]}"; do
    for u_arr in "${usage_arr[@]}"; do
      if [[ $status_message =~ $o_arr ]] || [[ $status_message =~ $u_arr ]]; then
        pass_count=$((pass_count+1))
        break
      fi
    done
    if [ $pass_count -gt $pass_num ]; then
      break
    fi
  done
  if [ $pass_count -gt $pass_num ]; then
    echo $line",PASS"
    continue
  else
    for o_arr in "${options_arr[@]}"; do
      for u_arr in "${usage_arr[@]}"; do
        for h_arr in "${help_arr[@]}"; do
          status_message=$($line $h_arr 2>&1)
          if [[ $status_message =~ $o_arr ]] || [[ $status_message =~ $u_arr ]]; then
            pass_count=$((pass_count+1))
            break
          fi
        done
        if [ $pass_count -gt $pass_num ]; then
          break
        fi
      done
      if [ $pass_count -gt $pass_num ]; then
        break
      fi
    done
    if [ $pass_count -gt $pass_num ]; then
      echo $line",PASS"
    else
      echo $line",FAIL"
    fi
  fi
done < $file
