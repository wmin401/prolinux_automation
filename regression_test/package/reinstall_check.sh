#!/bin/bash
file=$1
protected="protected"
success="Complete"
already="already installed"
nopackage="No Package"
nopackage2="No package"
nopackage3="No Match"

while read line; do
        reinstall_message=$(yum reinstall -y $line 2>&1)
        if [[ $reinstall_message =~ $success ]]; then
                echo "Reinstall,$line,P,$(rpm -qa | wc -l)"
        elif [[ $reinstall_message =~ $protected ]]; then
                echo "Reinstall,$line,Protected Package,$(rpm -qa | wc -l)"
        elif [[ $reinstall_message =~ $already ]]; then
                echo "Reinstall,$line,Already Installed,$(rpm -qa | wc -l)"
        elif [[ $reinstall_message =~ $nopackage ]] || [[ $reinstall_message =~ $nopackage2 ]] || [[ $install_message =~ $nopackage3 ]]; then
                echo "Reinstall,$line,No Package,$(rpm -qa | wc -l)"
        else
                echo "Reinstall,$line,Exception,$(rpm -qa | wc -l)"
        fi
done < $file
