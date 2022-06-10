#!/bin/bash

function INSTALL_CHECK()
{   
    INSTALL_LIST=($1)
    NOT_INSTALLED="not installed"
    for PKG in "${INSTALL_LIST[@]}" 
    do
        STATUS_MESSAGE=$(rpm -q $PKG 2>&1)
        if [[ $STATUS_MESSAGE =~ $NOT_INSTALLED ]]; then
            echo $PKG" installing..."
            $INSTALL_PKG install $PKG -y > /dev/null
        else
            echo $PKG" is already installed"
        fi
    done
}


INSTALL_CHECK 'git java-1.8.0-openjdk'

## 폴더가 있다면 pull 만 땡겨오기(현재는 jenkins_test부분만 pull로 댕겨옴 이부분 수정 해야됨)
    
cd ..
if [ -d $PROJECT_NAME/jenkins_test ]; then
	cd $PROJECT_NAME
    echo "$PROJECT_NAME already exists and try to pull"
    git pull http://$GIT_USERNAME:$GIT_PASSWORD@$GIT_REPOSITORY_URL
else
    echo "git init"
    git init
    echo "git clone http://$GIT_USERNAME:$GIT_PASSWORD@$GIT_REPOSITORY_URL/tree/dongill $PROJECT_NAME"
    git clone http://$GIT_USERNAME:$GIT_PASSWORD@$GIT_REPOSITORY_URL $PROJECT_NAME
	cd $PROJECT_NAME
fi
# 파이썬 설치
echo "This Version is $VERSION_DETAIL"
if [ ${VERSION_DETAIL} == 'v8_1' ]; then
    $INSTALL_PKG clean all
	INSTALL_CHECK "python${PYTHON3_VERSION:0:1}${PYTHON3_VERSION:2:1}-$PYTHON3_VERSION python3-pip"    
    if [ ! -f /usr/bin/python ]; then
        cd /usr/bin
        \cp python3 python
    fi
    cd /home/jenkins/workspace/$PROJECT_NAME/jenkins_test
    pip3 install --upgrade pip 
    pip3 --default-timeout=1000 install -r requirements.txt  > pip_install.log 2>&1
    echo "Python library installation is finished. You can see log in pip_install.log"
elif [ ${VERSION_DETAIL} == 'v7_7' ] || [ ${VERSION_DETAIL} == 'v7_8' ]; then
    $INSTALL_PKG clean all
	INSTALL_CHECK "python${PYTHON3_VERSION:0:1}-$PYTHON3_VERSION python3-pip"    
    if [ ! -f /usr/bin/python ]; then
        cd /usr/bin
        \cp python3 python
    fi
    cd /home/jenkins/workspace/$PROJECT_NAME/jenkins_test
    pip3 install --upgrade pip 
    pip3 --default-timeout=1000 install -r requirements.txt  > pip_install.log 2>&1
    echo "Python library installation is finished. You can see log in pip_install.log"
    
    ALIAS_PYTHON3=$(grep -r 'python3' /root/.bash_profile)
    PYTHON3_PATH=$(which python3)
    if [ "$ALIAS_PYTHON3" != "alias python='$PYTHON3_PATH'" ] ; then
        #echo "alias python='$PYTHON3_PATH'" >> /root/.bashrc
        echo "alias python='$PYTHON3_PATH'" >> /root/.bash_profile
        echo "Add alias python in /root/.bash_profile"
    else
        echo "Already exists alias python in /root/.bash_profile"
    fi
    echo "Python installation is finished"
elif [ ${VERSION_DETAIL} == 'v8_2' ]; then
    $INSTALL_PKG clean all
	INSTALL_CHECK "python${PYTHON3_VERSION:0:1}${PYTHON3_VERSION:2:1}-$PYTHON3_VERSION python3-pip"    
    if [ ! -f /usr/bin/python ]; then
        cd /usr/bin
        \cp python3 python
    fi
    cd /home/jenkins/workspace/$PROJECT_NAME/jenkins_test    
    pip3 install --upgrade pip 
    pip3 --default-timeout=1000 install -r requirements.txt  > pip_install.log 2>&1
    echo "Python library installation is finished. You can see log in pip_install.log"
else

    INSTALL_CHECK 'gcc openssl-devel bzip2-devel libffi-devel wget'

    cd /usr/src
    if [ ! -d Python-$PYTHON3_VERSION ] ; then
        ## 기존 폴더가 있다면 다운받지 않음
        echo "downloading python${PYTHON3_VERSION:0:1}${PYTHON3_VERSION:2:1}-$PYTHON3_VERSION..."
        wget -q -c --tries=10 https://www.python.org/ftp/python/$PYTHON3_VERSION/Python-$PYTHON3_VERSION.tgz
        tar -xzf Python-$PYTHON3_VERSION.tgz
        rm Python-$PYTHON3_VERSION.tgz         
        cd Python-$PYTHON3_VERSION
        if [ ! -d logs ]; then
            mkdir logs
        fi
        echo "installing python${PYTHON3_VERSION:0:1}${PYTHON3_VERSION:2:1}-$PYTHON3_VERSION..."
        ./configure > logs/configure.log 2>&1
        echo "./configure finished. You can see log in logs/configure.log"
        make altinstall > logs/altinstall.log 2>&1
        echo "make altinstall finished. You can see log in logs/altinstall.log"
    fi
    
    ALIAS_PYTHON3=$(grep -r 'python3' /root/.bash_profile)
    if [ "$ALIAS_PYTHON3" != "alias python='/usr/local/bin/python${PYTHON3_VERSION:0:3}'" ] ; then
        echo "alias python='/usr/local/bin/python${PYTHON3_VERSION:0:3}'" >> /root/.bash_profile
        echo "Add alias python in /root/.bash_profile"
    else
        echo "Already exists alias python in /root/.bash_profile"
    fi
    echo "Python installation is finished"
    # pip 설치
    if [ ! -f get-pip.py ]; then    
        echo "getting get-pip.py..."
        wget -q -c --tries=10 https://bootstrap.pypa.io/get-pip.py --no-check-certificate
    fi
    echo "installing pip..."
    python${PYTHON3_VERSION:0:3} get-pip.py > get-pip.log 2>&1
    echo "Pip installation is finished. You can see log in get-pip.log"
    cd /home/jenkins/workspace/$PROJECT_NAME/jenkins_test
    {
        echo "installing python library..."
        python${PYTHON3_VERSION:0:3} -m pip install -r requirements.txt > pip_install.log 2>&1
        echo "Python library installation is finished. You can see log in pip_install.log"
    } || {
        echo "failed to install python library"
    }
fi