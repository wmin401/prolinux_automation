#!/bin/bash

# 1. 필요 패키지 설치
yum -y install wget
yum -y install tftp tftp-server xinetd
yum -y install vsftpd
yum -y install dhcp
yum -y install syslinux
yum -y install iptables-services

# 2. 보안정책 구성
systemctl restart firewalld
firewall-cmd --permanent --add-service=ftp
firewall-cmd --permanent --add-service=tftp
firewall-cmd --permanent --add-service=dhcp
firewall-cmd --permanent --add-service=proxy-dhcp
firewall-cmd --add-port=69/tcp --permanent
firewall-cmd --add-port=69/udp --permanent
firewall-cmd --add-port=4011/udp --permanent

firewall-cmd --reload

# 3. dhcp 설정
echo "ddns-update-style interim;" >> /etc/dhcp/dhcpd.conf
echo "ignore client-updates;" >> /etc/dhcp/dhcpd.conf
echo "allow booting;" >> /etc/dhcp/dhcpd.conf
echo "allow bootp;" >> /etc/dhcp/dhcpd.conf
echo "allow unknown-clients;" >> /etc/dhcp/dhcpd.conf
echo "authoritative;" >> /etc/dhcp/dhcpd.conf
echo "subnet 192.168.17.0 netmask 255.255.255.0 {" >> /etc/dhcp/dhcpd.conf
echo "      option routers                  192.168.17.1;" >> /etc/dhcp/dhcpd.conf
echo "      option subnet-mask              255.255.255.0;" >> /etc/dhcp/dhcpd.conf
echo "      option domain-name-servers     	168.126.63.1;" >> /etc/dhcp/dhcpd.conf
echo "      default-lease-time              7200;" >> /etc/dhcp/dhcpd.conf
echo "      max-lease-time                  36000;" >> /etc/dhcp/dhcpd.conf
echo "      range           192.168.17.31   192.168.17.160;" >> /etc/dhcp/dhcpd.conf
echo "      next-server                     192.168.17.34;" >> /etc/dhcp/dhcpd.conf
echo '      filename                        "pxelinux.0";' >> /etc/dhcp/dhcpd.conf
echo "}" >> /etc/dhcp/dhcpd.conf


systemctl start dhcpd && systemctl enable dhcpd
systemctl start tftp && systemctl enable tftp
systemctl start xinetd && systemctl enable xinetd
systemctl enable vsftpd && systemctl start vsftpd

# 4. ftp 환경 설정
setsebool -P allow_ftpd_full_access 1

# 5. tftp 환경 설정 # 14번째 줄 yes 에서 no 로 변경(disabled)
sed -i '14s/yes/no/g' /etc/xinetd.d/tftp

# 6. syslinux 파일 복사
cp -v /usr/share/syslinux/pxelinux.0 /var/lib/tftpboot
cp -v /usr/share/syslinux/menu.c32 /var/lib/tftpboot
cp -v /usr/share/syslinux/memdisk /var/lib/tftpboot
cp -v /usr/share/syslinux/mboot.c32 /var/lib/tftpboot
cp -v /usr/share/syslinux/chain.c32 /var/lib/tftpboot

# 7. PXE Menufile 설정
mkdir /var/lib/tftpboot/pxelinux.cfg
touch /var/lib/tftpboot/pxelinux.cfg/default
echo "default menu.c32" >> /var/lib/tftpboot/pxelinux.cfg/default
echo "prompt 0" >> /var/lib/tftpboot/pxelinux.cfg/default
echo "timeout 30" >> /var/lib/tftpboot/pxelinux.cfg/default
echo "MENU TITLE ProLinux PXE Menu" >> /var/lib/tftpboot/pxelinux.cfg/default
echo "LABEL prolinux7_x64" >> /var/lib/tftpboot/pxelinux.cfg/default
echo "MENU LABEL ProLinux7.7" >> /var/lib/tftpboot/pxelinux.cfg/default
echo "KERNEL /networkboot/prolinux/vmlinuz" >> /var/lib/tftpboot/pxelinux.cfg/default
echo "APPEND initrd=/networkboot/prolinux/initrd.img inst.repo=ftp://192.168.17.34/pub/prolinux ks=ftp://192.168.17.34/pub/prolinux/prolinux7_7.cfg" >> /var/lib/tftpboot/pxelinux.cfg/default

# 8. 이미지 로딩
mkdir /media/iso
wget http://pldev-repo.tk/prolinux/7.7/isos/ProLinux-7.7.5.iso
mount /root/ProLinux-7.7.5.iso /media/iso
mkdir /var/ftp/pub
mkdir /var/ftp/pub/prolinux
cp -r /media/iso/* /var/ftp/pub/prolinux/

mkdir /var/lib/tftpboot/networkboot/
mkdir /var/lib/tftpboot/networkboot/prolinux/
cp /var/ftp/pub/prolinux/images/pxeboot/initrd.img /var/lib/tftpboot/networkboot/prolinux/
cp /var/ftp/pub/prolinux/images/pxeboot/vmlinuz /var/lib/tftpboot/networkboot/prolinux/

# 9. kickstart 구성
touch /var/ftp/pub/prolinux/prolinux7_7.cfg
cp /root/anaconda-ks.cfg /var/ftp/pub/prolinux/prolinux7_7.cfg
chmod 755 /var/ftp/pub/prolinux/prolinux7_7.cfg

# 비밀번호 asdf로 설정
PASSWD_ASDF=$(openssl passwd -1 asdf)
echo $PASSWD_ASDF

# cdrom 삭제
sed -i '/cdrom/d' /var/ftp/pub/prolinux/prolinux7_7.cfg  
# 네트워크 기반 설치 경로 설정
sed -i'' -r -e '/CDROM/a\url --url="ftp://192.168.17.34/pub/prolinux/"' /var/ftp/pub/prolinux/prolinux7_7.cfg 
# 기존 비밀번호 삭제
sed -i '/rootpw --iscrypted/d' /var/ftp/pub/prolinux/prolinux7_7.cfg 
# root 비밀번호 설정
sed -i'' -r -e "/Root password/a\rootpw --iscrypted $PASSWD_ASDF" /var/ftp/pub/prolinux/prolinux7_7.cfg 
# 기존 유저 삭제
sed -i '/user --name=/d' /var/ftp/pub/prolinux/prolinux7_7.cfg 
# dongill 유저 생성 및 비밀번호 설정
sed -i'' -r -e "/--isUtc/a\user --name=dongill --password=$PASSWD_ASDF/ --iscrypted --gecos='dongill'" /var/ftp/pub/prolinux/prolinux7_7.cfg 
# java-1.8.0 설치
sed -i'' -r -e "/kexec-tools/a\java-1.8.0-openjdk" /var/ftp/pub/prolinux/prolinux7_7.cfg 
# 볼륨 설정 삭제
sed -i '/part/d' /var/ftp/pub/prolinux/prolinux7_7.cfg
sed -i '/part pv/d' /var/ftp/pub/prolinux/prolinux7_7.cfg
sed -i '/volgroup/d' /var/ftp/pub/prolinux/prolinux7_7.cfg
sed -i '/logvol swap/d' /var/ftp/pub/prolinux/prolinux7_7.cfg
sed -i '/logvol/d' /var/ftp/pub/prolinux/prolinux7_7.cfg
# 볼륨 자동으로 생성되도록 설정
sed -i'' -r -e "/bootloader --append/a\autopart --type=lvm" /var/ftp/pub/prolinux/prolinux7_7.cfg #
sed -i'' -r -e "/# Partition/a\clearpart --none --initlabel" /var/ftp/pub/prolinux/prolinux7_7.cfg #
# 미니멀 패키지 삭제(kickstart에서 minimal 안됨)
sed -i '/@^minimal/d' /var/ftp/pub/prolinux/prolinux7_7.cfg 
# base 패키지로 설치
sed -i'' -r -e "/%packages/a\@ Base" /var/ftp/pub/prolinux/prolinux7_7.cfg 

# dhcp 서버 ip 로 되어있기 때문에 ??로 바꿈
# sed -i "s/--ip=192.168.17.34/--ip=192.168.17.34/g" /var/ftp/pub/prolinux/prolinux7_7.cfg

systemctl restart dhcpd
systemctl restart tftp
systemctl restart xinetd
systemctl reenable vsftpd