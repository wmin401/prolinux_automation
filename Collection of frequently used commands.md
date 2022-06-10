### 초기 패키지 리스트 생성
    # rpm -qa | sort > initial_package_list.txt

### 로컬/원격 패키지 리스트 확인
    # repoquery -a --queryformat '%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}' | sort > local_package_list.txt
    # repoquery -a --queryformat '%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}' | sort > remote_package_list.txt
7버전에선 -a 옵션 추가 필요

### local repo 영구 설정
    # echo "/root/ProLinux-{version} /root/mnt iso9660 loop 0 0" >> /etc/fstab

### 설치된 패키지 리스트 생성
    # rpm -qa | sort > installed_package_list.txt

### 설치된 패키지 메타 데이터 확인
    # rpm -qa --queryformat '%{BUILDHOST};%{VENDOR};%{PACKAGER};\n' | sort > meta_data_list.txt

### 설치 관련 검증 디렉토리 생성
    # mkdir -p install_check/module_check

### 초기 module 리스트 생성
    # dnf module list | tee initial_module_list

### iso 다운로드
    # curl -o ProLinux-8.1.16.iso http://pldev-repo.tk/prolinux/8.1/isos/ProLinux-8.1.16.iso

### local repo 설정
    # yum install -y vim-enhanced // 7.8 버전
    # mkdir mnt
    # mount -o loop ProLinux-7.8.2.iso mnt
    # vi /etc/yum.repos.d/ProLinux.repo

    #[base]
    #name=ProLinux - $releasever - Base
    #baseurl=http://pldev-repo-21.tk/prolinux/7.8/os/x86_64
    #enabled=1
    #gpgcheck=0
    #gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-prolinux-7-release

    [local-base]
    name=ProLinux - $releasever - Base - local
    baseurl=file:///root/mnt
    enabled=1
    gpgcheck=0
    gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-prolinux-7-release

    # dnf install -y vim-enhanced // 8.1 버전
    # mkdir mnt
    # mount -o loop ProLinux-8.1-minimal.iso mnt
    # vi /etc/yum.repos.d/ProLinux.repo

    #[BaseOS]
    #name=ProLinux-$releasever - BaseOS
    #baseurl=http://pldev-repo.tk/prolinux/8.1/os/BaseOS
    [BaseOS-local]
    name=ProLinux-$releasever - BaseOS - local
    baseurl=file:///root/mnt/BaseOS
    gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-prolinux-$releasever-release
    gpgcheck=1
    #[AppStream]
    #name=ProLinux-$releasever - AppStream
    #baseurl=http://pldev-repo.tk/prolinux/8.1/os/AppStream
    [AppStream-local]
    name=ProLinux-$releasever - AppStream - local
    baseurl=file:///root/mnt/AppStream
    gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-prolinux-$releasever-release
    gpgcheck=1

### 이미지 다운로드
    # curl -o ProLinux-7.7.4.iso http://pldev-repo.tk/prolinux/7.7/isos/ProLinux-7.7.4.iso

### low format (예시)
    # dd if=/dev/zero of=/dev/sdb5

### module package 정리
    # cat module_info_list.txt | grep -e noarch -e x86_64 | grep -v module-build-macros | tr -d ' ' | tee module_package_list

### local rpm 정리
    # ls /root/mnt/BaseOS/Packages /root/mnt/AppStream/Packages | grep -v TRANS.TBL | sort | tee local_rpm_list.txt
8.1 기준 2개 제외해야 함, 8.3.2 기준 (/root/mnt/BaseOS/Packages /root/mnt/AppStream/Packages)

    # ls /root/mnt/BaseOS/Packages | grep -v TRANS.TBL | sort | tee local_rpm_list.txt
8.2 minimal

    # ls /root/hyperVM_rpms/prolinux-repo.tmaxos.com/ovirt/4.4/el8/x86_64/Packages/ /root/hyperVM_rpms/prolinux-repo.tmaxos.com/ovirt/4.4/el8/x86_64/ceph/ | sort | tee diff_local_rpm_list.txt
HyperVM 4.4 기준 2개 제외해야 함 (/root/hyperVM_rpms/prolinux-repo.tmaxos.com/ovirt/4.4/el8/x86_64/ceph/: /root/hyperVM_rpms/prolinux-repo.tmaxos.com/ovirt/4.4/el8/x86_64/Packages/:)

    # ls /root/mnt/Packages | grep -v TRANS.TBL | sort | tee local_rpm_list.txt
7.7, 7.8, 7.9 기준

    # ls /root/mnt/BaseOS/not_found /root/mnt/BaseOS/Packages /root/mnt/BaseOS/pl_only /root/mnt/AppStream/modules/Packages /root/mnt/AppStream/normal /root/mnt/AppStream/normal/Packages /root/mnt/AppStream/pl_only | grep -v TRANS.TBL | grep -v Packages | sort | tee local_rpm_list.txt
8.2.2 기준 6개 제외해야 함 (/root/mnt/AppStream/modules/Packages /root/mnt/AppStream/normal/Packages /root/mnt/AppStream/pl_only /root/mnt/BaseOS/not_found /root/mnt/BaseOS/Packages /root/mnt/BaseOS/pl_only)

### 복사 (TRANS.TBL 삭제)
    # cp -r mnt/BaseOS/Packages/ mnt/AppStream/Packages/ .
8.1 기준

    # cp -r mnt/Packages/ .
7.7, 7.8, 7.9 기준

  # cp -r mnt/BaseOS/Packages/ .
8.2 minimal 기준

### 메타 데이터 확인
    # ./vendor_check.sh ../local_rpm_list | tee ../vendor_check_list.xlsx

### Boot Loader 복구
    # chroot /mnt/sysimage
    # grub2-install /dev/sdb
    # grub2-mkconfig -o /boot/grub2/grub.cfg
    # exit
    # reboot

### VM 구성
    # dnf install -y cockpit cockpit-machines virt-install virt-viewer

### 분할 압축 실행
    # tar -cvf - ProLinux-8.1_4.18.0-147.el8.x86_64.iso | split -b 4096m - ProLinux-8.1_4.18.0-147.el8.x86_64.iso.tar

### 분할 압축 해제
    # cat ProLinux-8.1_4.18.0-147.el8.x86_64.iso.tar* | tar xvf -

### 디버깅 메시지 확인
    # ssh 192.168.122.202 -v

### 쿼터 설정
미리 ext4 파일 시스템이 적용된 장치 준비 ex) /dev/sda4  
마운트할 폴더 생성

    # mkdir /root/ext4_mount

mount 내용 추가  
ex)

    # vi /etc/fstab
    # Created by anaconda on Wed Jan  6 16:55:33 2021
    중략..
    /dev/sda4 /root/ext4_mount ext4 defaults 0 0

실제 mount 실행

    # mount -o loop  /dev/sda4 /root/ext4_mount/

사용자 쿼터 사용 설정

    # mount -o remount,quota,usrjquota=aquota.user,jqfmt=vfsv0 /root/ext4_mount
    # quotacheck -cvu /root/ext4_mount
    quotacheck: Scanning /dev/loop0 [/root/ext4_mount] done
    quotacheck: Cannot stat old user quota file /root/ext4_mount/aquota.user: No such file or directory. Usage will not be subtracted.
    quotacheck: Old group file name could not been determined. Usage will not be subtracted.
    quotacheck: Checked 3 directories and 0 files
    quotacheck: Old file not found.

### 제공 패키지 확인
    # yum provides '*/applydeltarpm'

### EFI 설정으로 인해 ProLinux가 Desktop에서 설치되지 않을 때
- BIOS 진입 - Boot - CSM - Launch CSM 하위 - legacy only로 설정

### rpm db 파일이 깨져 설치가 안될때
    # rm -f /var/lib/rpm/_db*
    # rpm -vv --rebuilddb
    # systemctl start fapolicyd

db_verify로 rpmdb 무결성을 체크
    # db_verify /var/lib/rpm/Packages

1안 만약 실패한다면, 아래처럼 수정

    # cd /var/lib/rpm
    # mv Packages Packages-ORIG
    # db_dump Packages-ORIG | db_load Packages

2안 만약 실패한다면, 아래처럼 수정

    # mv /var/lib/rpm/__db* /tmp
    # cd /var/lib/rpm
    # rm -rf __db*
    # db_verify Packages
    # rm -rf /var/cache/yum
    # rpm --rebuilddb
    # reboot
    # yum update
    # rm -rf /tmp/__db*
