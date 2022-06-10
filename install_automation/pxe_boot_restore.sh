#!/bin/bash

# 1. dhcp 삭제 후 다시 생성(초기 상태로)
rm -rf /etc/dhcp/dhcpd.conf
touch /etc/dhcp/dhcpd.conf
echo "#" >> /etc/dhcp/dhcpd.conf
echo "# DHCP Server Configuration file." >> /etc/dhcp/dhcpd.conf
echo "#   see /usr/share/doc/dhcp*/dhcpd.conf.example" >> /etc/dhcp/dhcpd.conf
echo "#   see dhcpd.conf(5) man page" >> /etc/dhcp/dhcpd.conf
echo "#" >> /etc/dhcp/dhcpd.conf

# tftp 파일 yes -> no
sed -i '14s/no/yes/g' /etc/xinetd.d/tftp

# ftp 서버  파일 삭제
cd /var/lib/tftpboot/
rm -rf *
cd /var/ftp
rm -rf *

# 언마운트 및 삭제
umount -l /media/iso
rm -rf /media/iso
cd /root
rm -rf ProLinux-7.7.5.iso