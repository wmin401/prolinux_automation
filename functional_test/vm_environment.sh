#!/bin/bash

echo "1. cockpit 설치"
dnf install -y cockpit cockpit-machines cockpit-podman
yum install -y cockpit* # 7.7버전, Virtual Machine, Docker  생성 미지원 중

echo "2. cockpit 사용 설정"
systemctl enable --now cockpit.socket
systemctl start cockpit

echo "3. cockpit 상태 확인"
systemctl status cockpit

echo "4. 방화벽 설정" # 7.7, 7.9, 8.3 버전
firewall-cmd --permanent --zone=public --add-service=cockpit
firewall-cmd --reload

echo "5. 접속 확인"
브라우저에서 접속 (ex. https://{host_IP}:9090/)

echo "6. KVM 설치"
dnf module install -y virt # 8.1 버전
dnf install -y virt-install virt-viewer

echo "7. KVM 사용 적합성 확인"
virt-host-validate

# LXC: Checking if device /sys/fs/fuse/connections exists : FAIL (Load the 'fuse' module to enable /proc/ overrides) 발생 시 확인
# yum reinstall fuse -y
# modprobe fuse

# QEMU: Checking if IOMMU is enabled by kernel : WARN 발생 시 확인
# vi /etc/default/grub
# GRUB_CMDLINE_LINUX="... intel_iommu=on" 추가
# grub2-mkconfig -o /boot/grub2/grub.cfg
# reboot
# QEMU: Checking if IOMMU is enabled by kernel : PASS

echo "8. KVM 사용 설정"
systemctl start libvirtd.service
systemctl enable libvirtd.service

echo "9. KVM 상태 확인"
systemctl status libvirtd.service

echo "10. VM 생성 관련 이미지 다운로드"
curl -o CentOS-7-x86_64-Minimal-2009.iso http://mirror.navercorp.com/centos/7.9.2009/isos/x86_64/CentOS-7-x86_64-Minimal-2009.iso
mv CentOS-7-x86_64-Minimal-2009.iso /var/lib/libvirt/images/
