#!/bin/bash
file=$1
inactive="Active: inactive"
active="Active: active"
failed="Active: failed"
masked="Loaded: masked"
oneshot="Type=oneshot"
forking="Type=forking"
remain="RemainAfterExit=yes"

# 원본 데몬 파일 경로를 쓰도록 함

echo "1. .bak 파일 복구로 Service 섹션에 추가한 내용 제거 - 대상: oneshot/forking 데몬"
echo "2. 수동 시작/종료 금지 등 주석 제거 - 대상: 전체 데몬"

while read line; do
  \mv -f $line".bak" $line
  sed -i 's/#RefuseManualStop=yes/RefuseManualStop=yes/g' $line
  sed -i 's/#RefuseManualStop=true/RefuseManualStop=true/g' $line
  sed -i 's/#RefuseManualStart=yes/RefuseManualStart=yes/g' $line
  sed -i 's/#RefuseManualStart=true/RefuseManualStart=true/g' $line
  sed -i 's/#StopWhenUnneeded=yes/StopWhenUnneeded=yes/g' $line
  sed -i 's/#ConditionPathIsReadWrite=!\//ConditionPathIsReadWrite=!\//g' $line
  sed -i 's/#ConditionNeedsUpdate=\/var/ConditionNeedsUpdate=\/var/g' $line
  sed -i 's/#ConditionPathIsMountPoint=\/etc\/machine-id/ConditionPathIsMountPoint=\/etc\/machine-id/g' $line
  sed -i 's/#ConditionNeedsUpdate=\/etc/ConditionNeedsUpdate=\/etc/g' $line
  sed -i 's/#ConditionNeedsUpdate=|\/etc/ConditionNeedsUpdate=|\/etc/g' $line
  sed -i 's/#ConditionNeedsUpdate=|\/var/ConditionNeedsUpdate=|\/var/g' $line
  sed -i 's/#ConditionSecurity=!selinux/ConditionSecurity=!selinux/g' $line
  sed -i 's/#ConditionPathExists=!\/run\/plymouth\/pid/ConditionPathExists=!\/run\/plymouth\/pid/g' $line
  sed -i 's/#ConditionPathExists=!\/.autorelabel/ConditionPathExists=!\/.autorelabel/g' $line
  sed -i 's/#RemainAfterExit=no/RemainAfterExit=no/g' $line
  sed -i 's/#ConditionVirtualization=no/ConditionVirtualization=no/g' $line
done < $file
systemctl daemon-reload

echo "3. 파일 제거"
rm -rf /usr/lib/initrd-release
rm -rf /lib/dracut/need-initqueue
rm -rf /boot/grub2/grubenv.new #지우지 않아도 되긴 함
rm -rf /run/plymouth/pid
rm -rf /etc/initrd-release
rm -rf /run/user/1
#rm -rf /run/teamd/test.conf
rm -rf /var/log/Xorg.0.log
rm -rf /etc/multipath.conf
rm -rf /etc/ethers
rm -rf /etc/krb5.keytab
rm -rf /etc/openwsman/owsmangencert.sh
rm -rf /etc/quagga/babeld.conf
rm -rf etc/quagga/bgpd.conf
rm -rf /etc/quagga/isisd.conf
rm -rf /etc/quagga/ospf6d.conf
rm -rf /etc/quagga/ospfd.conf
rm -rf /etc/quagga/ripd.conf
rm -rf /etc/quagga/ripngd.conf
rm -rf /var/lib/mdcheck/MD_UUID_0

echo "4. 폴더 및 하위 파일 제거"
rm -rf /lib/dracut/hooks/mount
rm -rf /lib/dracut/hooks/pre-mount/
rm -rf /lib/dracut/hooks/pre-pivot
rm -rf /lib/dracut/hooks/pre-trigger
rm -rf /lib/dracut/hooks/pre-udev
rm -rf /etc/sysconfig/modules
rm -rf /lib/module-load.d
rm -rf /lib/dracut/hooks/cmdline
rm -rf /var/lib/iscsi/nodes
rm -rf /usr/lib/mdadm/
rm -rf /usr/share/mdadm

echo "5. 기본 권한 복구"
chmod 644 /etc/rc.d/rc.local

echo "6. 패키지 제거"
# yum remove -y quota
