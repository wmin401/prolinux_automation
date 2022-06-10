#!/bin/bash
file=$1
protected="protected"
success="Complete"
already="already installed"
nopackage="No Package"
nopackage2="No package"
obsolete="obsoleted"
nomatch="No match"
noavailable="No available"
conflict="conflicting requests"

while read line; do
        install_message=$(yum install -y $line 2>&1)
        # install_message=$(yum install -y --allowerasing $line 2>&1)
        if [[ $install_message =~ $already ]]; then
                if [[ $install_message =~ $obsolete ]]; then
                        echo "Install,$line,Obsoleted,$(rpm -qa | wc -l)"
                else
                        echo "Install,$line,Already Installed,$(rpm -qa | wc -l)"
                fi
        elif [[ $install_message =~ $nopackage ]] || [[ $install_message =~ $nopackage2 ]] || [[ $install_message =~ $nomatch ]]; then
                echo "Install,$line,No Package(No Match),$(rpm -qa | wc -l)"
        elif [[ $install_message =~ $noavailable ]]; then
                echo "Install,$line,No Available,$(rpm -qa | wc -l)"
        elif [[ $install_message =~ $conflict ]]; then
                echo "Install,$line,Conflicting Requests,$(rpm -qa | wc -l)"
        elif [[ $install_message =~ $protected ]]; then
                echo "Install,$line,Protected Package,$(rpm -qa | wc -l)"
        elif [[ $install_message =~ $success ]]; then
                echo "Install,$line,P,$(rpm -qa | wc -l)"
        else
                echo "Install,$line,Exception,$(rpm -qa | wc -l)"
        fi
        # yum history undo last -y >> install_log.txt
        # echo "==============================================" >> install_log.txt
done < $file
