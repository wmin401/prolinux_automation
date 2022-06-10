if [ $LOCAL_REPOSITORY == true ] || [ $METADATA_TEST == true ] ; then
    # 로컬 레포 삭제 및 기존 레포 활성화
    echo "Start deleting local repository settings"
    {
        rm -rf /etc/yum.repos.d/local.repo
    } || {
        echo "Remove failed. Not exists locael.repo"
    }
    function CHANGE_ENABLED(){        
        {
            find /etc/yum.repos.d -name "$1.repo" -exec sed -i "s/enabled=0/enabled=1/g" {} \;
        } || {
            echo "Not changed $1.repo file"
        }
    }
    if [ $VERSION_DETAIL == 'v7_5' ]; then
        CHANGE_ENABLED 'ProLinux-Base'
    elif [ $VERSION_DETAIL == 'v7_7' ]; then
        #CHANGE_ENABLED 'ProLinux-Base-beta'
        CHANGE_ENABLED 'public-yum-pl7'
    elif [ $VERSION_DETAIL == 'v8_1' ] || [ $VERSION_DETAIL == 'v8_2' ]; then
        CHANGE_ENABLED 'ProLinux'
    else
        echo "This version cannot make local repository"
    fi
    echo "Local repository settings have been deleted"
    {
        echo "Start deleting mount folder and image file"
        rm -f /root/$IMG_NAME
        umount -f $MOUNT_FOLDER_PATH
        rm -rf $MOUNT_FOLDER_PATH
        echo "Mount folder and image file have been deleted"

    } || {
        echo "Failed to deleting mount folder and image file."
    }
    $INSTALL_PKG clean all
fi
