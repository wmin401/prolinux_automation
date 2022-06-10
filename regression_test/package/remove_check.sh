#!/bin/bash
file=$1
protected="protected"
success="Complete"
already="already installed"
nopackage="No Package"
nopackage2="No package"

while read line; do
        remove_message=$(yum remove -y $line 2>&1)
        if [[ $remove_message =~ $protected ]]; then
                echo "Remove,$line,Protected Package,$(rpm -qa | wc -l)"
        elif [[ $remove_message =~ $nopackage ]] || [[ $remove_message =~ $nopackage2 ]]; then
                echo "Remove,$line,No Package,$(rpm -qa | wc -l)"
        elif [[ $remove_message =~ $success ]]; then
                echo "Remove,$line,P,$(rpm -qa | wc -l)"
        else
                echo "Remove,$line,Exception,$(rpm -qa | wc -l)"
        fi
        # yum history undo last -y >> remove_log.txt
        # echo "==============================================" >> install_log.txt
done < $file
