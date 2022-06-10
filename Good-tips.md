# Installation process history inquiry  
dnf history

# Rollback action (removing history)
dnf history rollback {history id of wanting to go back}

# Undo action (registering history)
dnf history undo {history id of wanting to undo}

# Undo last action (without id)
dnf history undo last

# Extract file list only & Extract file name only
ls -l | grep -v ^d  > {file name for saving list}  
cut -c 46- {file name for saving list}

# Backup dnf history
mv /var/lib/dnf/history.sqlite history.sqlite_backup

# Clear dnf history
rm -rf /var/lib/dnf/history.sqlite

# show info of module
dnf module info {mod_name}

# show module list
dnf module list

# enable module
dnf module enable {mod_name}

# download iso file from web (reduce integrity problem)
wget {URL}

# provide list of updateable pacakges
dnf check-update  
ex)  
![image](https://user-images.githubusercontent.com/24868649/89974707-bf42f000-dc9e-11ea-8422-24b48a716fbe.png)

# enabled or disabled repositories and add new repositories
dnf config-manager --enable {repo_name}  
dnf config-manager --disable {repo_name}  
dnf config-manager --add-repo {baseURL_of_repo}

# Print the number of included strings (in vi editor)
:%s/module//n

# Delete line containing string (in vi editor)
:%g/module/d

# Substitute string (in vi editor)
:%s/(finding_pattern)/(changing_pattern)/(option)
ex) :%s/"//g

# Substitute string by line (in vi editor)
:(start_line),(end_line)s/(finding_pattern)/(changing_pattern)/(option)

# trouble shooting: remote: HTTP Basic: Access denied
git config --system --unset credential.helper
git config credential.helper store
git pull
