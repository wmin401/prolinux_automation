#!/bin/sh

## 로컬 레포지토리 사용을 원할 경우
## LOCAL_REPO_SET 를 체크하거나
## METADATA_TEST 를 체크하면 실행됨

## workspace와 ssh 서버가 같을 경우에만 사용 가능

if [ $LOCAL_REPOSITORY == true ] || [ $METADATA_TEST == true ] ; then
    echo "Start setting up Local repository."
    $INSTALL_PKG -y install wget > /dev/null
    cd /root
    if [ -f /root/${IMG_NAME} ]; then
        echo "Image file is already exists in /root"
    else
        echo "Downloading image file ..."
        wget -q -c --tries=10 $IMG_DOWNLOAD_ADDR/$IMG_NAME
        echo "image file is downloaded"
    fi
    mkdir "$MOUNT_FOLDER_PATH"
    mount -o loop "/root/$IMG_NAME" "$MOUNT_FOLDER_PATH"

    rm -rf /etc/yum.repos.d/local.repo
    ## 존재할 경우 삭제

    ## local.repo 생성
    if [ -f /etc/yum.repos.d/local.repo ]; then
        rm -f /etc/yum.repos.d/local.repo
    fi
    touch /etc/yum.repos.d/local.repo

    count=0
    for var in $*
    do
        tmp=`expr $count % 2`
        if [ $tmp -eq 0 ]
        then
            echo "[local_"$var"]" >> /etc/yum.repos.d/local.repo
            echo "name=local-"$var  >> /etc/yum.repos.d/local.repo
        else
            echo "baseurl=file://"$MOUNT_FOLDER_PATH""$var >> /etc/yum.repos.d/local.repo
            echo "gpgcheck=1"  >> /etc/yum.repos.d/local.repo
            #echo "gpgcheck=0"  >> /etc/yum.repos.d/local.repo
            echo "enabled=1"  >> /etc/yum.repos.d/local.repo
            if [ $MAJOR_VERSION == '7' ]; then
                echo "gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-prolinux-7-release" >> /etc/yum.repos.d/local.repo
            elif [ $MAJOR_VERSION == '8' ]; then
                echo "gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-prolinux-8-release" >> /etc/yum.repos.d/local.repo
            fi
            echo "" >> /etc/yum.repos.d/local.repo
        fi
        count=$(($count+1))
    done

    ## ProLinux.repo 내용 변경


    #prolinux.repo 내부 enable 체크 함수
    ## 1) /etc/yum.repos.d/local.repo 안에 enabled=1이 있으면 enabled=0으로 변경
    ## 2) /etc/yum.repos.d/local.repo 안에 enabled이 없으면 enabled=0추가(각 gpgcheck=1밑에)
    function ENABLE_CHECK(){
        ENABLED_1_EXISTS=$(grep -r "enabled=1" /etc/yum.repos.d/$1.repo)
        if [ "$ENABLED_1_EXISTS" != "" ];  then  ## enabled=1이라는 값이 있을 때
            echo "enabled=1 to enabled=0 in /etc/yum.repos.d/$1.repo"  ##1을 0으로 바꾼다.
            find /etc/yum.repos.d/ -name "$1.repo" -exec sed -i "s/enabled=1/enabled=0/g" {} \;
        elif [ "$ENABLED_1_EXISTS" == "" ];  then  ## enabeld=1이라는 값이 없을 때
            echo "Added enabled=0 into /etc/yum.repos.d/$1.repo"  #gpgcheck=1 아래에 enabled=0을 넣는다.
            sed -i'' -r -e "/gpgcheck/a\enabled=0" /etc/yum.repos.d/$1.repo
        fi
    }

    ## 7버전
    if [ $VERSION_DETAIL == 'v7_5' ]; then
        ENABLE_CHECK 'ProLinux-Base'
    elif [ $VERSION_DETAIL == 'v7_7' ]; then
        #ENABLE_CHECK 'ProLinux-Base-Beta'
        ENABLE_CHECK 'public-yum-pl7'
    elif [ $VERSION_DETAIL == 'v8_1' ] || [ $VERSION_DETAIL == 'v8_2' ]; then
        ENABLE_CHECK 'ProLinux'
    fi
    ##########################
    $INSTALL_PKG clean all
    sleep 3
    $INSTALL_PKG repolist

    echo "Local repository setup is completed."

else ## 레포나 메타데이터에 체크되지 않았을 경우, 로컬 레포를 설정하지 않음, 설정되어있다면 해당 레포삭제
{
    rm -rf /etc/yum.repos.d/local.repo
} || {
    echo "rm faied. Not exists local.repo"
}
fi
