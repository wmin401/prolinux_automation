#!/bin/bash

echo "버전 업데이트 (CentOS 7.5, 7.6, 7.8 확인)"
echo "1. 빠른 미러 서버를 사용하기 위해 설치"
yum install -y yum-plugin-fastestmirror

echo "2. 버전 업그레이드에 앞서 전체 환경을 최신 상태로 업데이트 진행"
yum update -y

echo "3. epel 저장소 설치"
yum install -y epel-release

echo "4. 진행 시 필요한 추가 패키지 설치 (epel repository 설치 필요)"
yum install -y yum-utils
yum install -y rpmconf

echo "5. 패키지들의 설정 파일 체크"
yes "" | rpmconf -a

echo "6. 필요하지 않은 모든 패키지 정리"
package-cleanup --leaves
package-cleanup --orphans

echo "7. dnf 패키지 설치(extras에 존재)"
yum install -y dnf

echo "8. 충돌 방지를 위해 Python 관련 패키지 업데이트 및 설치 진행"
yum update -y python*
yum install -y dnf-data dnf-plugins-core libdnf-devel libdnf python2-dnf-plugin-migrate dnf-automatic

echo "9. yum 관련 패키지들 삭제"
dnf remove -y yum yum-metadata-parser

echo "10. dnf 업그레이드 (epel 업그레이드)"
dnf upgrade -y

echo "11. yum 디렉토리 삭제"
rm -Rf /etc/yum

echo "12. 8.x 레포 관련 패키지 설치 (레포 변경)"
dnf install -y http://mirror.centos.org/centos/8/BaseOS/x86_64/os/Packages/centos-repos-8.2-2.2004.0.1.el8.x86_64.rpm http://mirror.centos.org/centos/8/BaseOS/x86_64/os/Packages/centos-release-8.2-2.2004.0.1.el8.x86_64.rpm http://mirror.centos.org/centos/8/BaseOS/x86_64/os/Packages/centos-gpg-keys-8.2-2.2004.0.1.el8.noarch.rpm

echo "13. epel을 최신(8버전)을 바라보도록 dnf 명령어로 업그레이드"
dnf upgrade -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm

echo "14. 임시 파일 정리"
dnf clean all

echo "15. 이전의 7버전 kernel 및 충돌 패키지 제거"
rpm -e `rpm -q kernel`
rpm -e --nodeps sysvinit-tools

echo "16. 충돌되는 패키지들 미리 삭제"
dnf remove -y python36-rpmconf

echo "17. 8 버전 시스템 업그레이드 (8.x 패키지들 설치))"
dnf --releasever=8 --allowerasing --setopt=deltarpm=false -y distro-sync

echo "18. kernel-core 설치"
dnf install -y kernel-core

echo "19. groupupdate 진행"
dnf groupupdate -y "Core" "Minimal Install"
