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

echo "1. 수동 시작/종료 금지 등 주석 처리 - 대상: 전체 데몬"
echo "2. [Service] 섹션 찾아서 내용 추가 - 대상: oneshot/forking 데몬"

while read line; do
  sed -i.bak 's/RefuseManualStop=yes/#RefuseManualStop=yes/g' $line
  sed -i.bak 's/RefuseManualStop=true/#RefuseManualStop=true/g' $line
  sed -i.bak 's/RefuseManualStart=yes/#RefuseManualStart=yes/g' $line
  sed -i.bak 's/RefuseManualStart=true/#RefuseManualStart=true/g' $line
  sed -i.bak 's/StopWhenUnneeded=yes/#StopWhenUnneeded=yes/g' $line
  sed -i.bak 's/ConditionPathIsReadWrite=!\//#ConditionPathIsReadWrite=!\//g' $line
  sed -i.bak 's/ConditionNeedsUpdate=\/var/#ConditionNeedsUpdate=\/var/g' $line
  sed -i.bak 's/ConditionPathIsMountPoint=\/etc\/machine-id/#ConditionPathIsMountPoint=\/etc\/machine-id/g' $line
  sed -i.bak 's/ConditionNeedsUpdate=\/etc/#ConditionNeedsUpdate=\/etc/g' $line
  sed -i.bak 's/ConditionNeedsUpdate=|\/etc/#ConditionNeedsUpdate=|\/etc/g' $line
  sed -i.bak 's/ConditionNeedsUpdate=|\/var/#ConditionNeedsUpdate=|\/var/g' $line
  sed -i.bak 's/ConditionSecurity=!selinux/#ConditionSecurity=!selinux/g' $line
  sed -i.bak 's/ConditionPathExists=!\/run\/plymouth\/pid/#ConditionPathExists=!\/run\/plymouth\/pid/g' $line
  sed -i.bak 's/ConditionPathExists=!\/.autorelabel/#ConditionPathExists=!\/.autorelabel/g' $line
  sed -i.bak 's/RemainAfterExit=no/#RemainAfterExit=no/g' $line
  sed -i.bak 's/ConditionVirtualization=no/#ConditionVirtualization=no/g' $line

  type_message=$(grep $oneshot $line 2>&1)
  type_message2=$(grep $forking $line 2>&1)
  if [[ $type_message =~ $oneshot ]] || [[ $type_message2 =~ $forking ]]; then
    option_message=$(grep $remain $line 2>&1)
    if [[ $option_message != *$remain* ]]; then
      sed -i.bak 's/\[Service\]/\[Service\]\nRemainAfterExit=yes/g' $line
    fi
  fi
done < $file

echo "3. 파일 생성"
touch /usr/lib/initrd-release
touch /lib/dracut/need-initqueue
touch /boot/grub2/grubenv.new
touch /run/plymouth/pid
touch /etc/initrd-release
touch /run/user/1
touch /lib/module-load.d
mkdir -p /run/teamd/
\cp /usr/share/doc/teamd-1.27/example_configs/activebackup_arp_ping_1.conf /run/teamd/test.conf
touch /var/log/Xorg.0.log
touch /etc/multipath.conf
touch /etc/ethers
touch /etc/krb5.keytab
touch /etc/openwsman/owsmangencert.sh
touch /etc/quagga/babeld.conf
touch /etc/quagga/bgpd.conf
touch /etc/quagga/isisd.conf
touch /etc/quagga/ospf6d.conf
touch /etc/quagga/ospfd.conf
touch /etc/quagga/ripd.conf
touch /etc/quagga/ripngd.conf
touch /var/lib/mdcheck/MD_UUID_0

echo "4. 폴더 및 하위 파일 존재"
mkdir -p /lib/dracut/hooks/mount
touch /lib/dracut/hooks/mount/test

mkdir -p /lib/dracut/hooks/pre-mount/
touch /lib/dracut/hooks/pre-mount/test

mkdir -p /lib/dracut/hooks/pre-pivot
touch /lib/dracut/hooks/pre-pivot/test

mkdir -p /lib/dracut/hooks/pre-trigger
touch /lib/dracut/hooks/pre-trigger/test

mkdir -p /lib/dracut/hooks/pre-udev
touch /lib/dracut/hooks/pre-udev/test

mkdir -p /etc/sysconfig/modules
touch  /etc/sysconfig/modules/test

mkdir -p /lib/modules-load.d
touch /lib/modules-load.d/test

mkdir -p  /lib/dracut/hooks/cmdline
touch /lib/dracut/hooks/cmdline/test

mkdir -p /var/lib/iscsi/nodes
touch /var/lib/iscsi/nodes/test

mkdir -p /usr/lib/mdadm/
touch /usr/lib/mdadm/mdadm_env.sh

mkdir -p /usr/share/mdadm
touch /usr/share/mdadm/mdcheck

echo "5. 실행 권한 부여"
chmod +x /etc/rc.d/rc.local
chmod +x /usr/share/mdadm/mdcheck
chmod +x /usr/lib/mdadm/mdadm_env.sh

echo "6. 개별 데몬 제어"
systemctl daemon-reload
status_message=$(systemctl status systemd-journald.service 2>&1)
if [[ $status_message =~ $active ]]; then
  systemctl stop systemd-journald.socket
  systemctl stop systemd-journald-dev-log.socket
  systemctl stop systemd-journald.service
fi

status_message=$(systemctl status systemd-timedated.service 2>&1)
if [[ $status_message =~ $masked ]]; then
  systemctl unmask systemd-timedated.service
fi

status_message=$(systemctl status systemd-udevd.service 2>&1)
if [[ $status_message =~ $active ]]; then
  systemctl stop systemd-udevd-kernel.socket
  systemctl stop systemd-udevd-control.socket
  systemctl stop systemd-udevd.service
fi

status_message=$(systemctl status abrtd.service 2>&1)
if [[ $status_message =~ $inactive ]]; then
  systemctl start abrtd.service
fi

status_message=$(systemctl status amanda-udp.socket 2>&1)
if [[ $status_message =~ $inactive ]]; then
  systemctl start amanda-udp.socket
fi

status_message=$(systemctl status named.service 2>&1)
if [[ $status_message =~ $inactive ]]; then
  systemctl start name.service
fi

echo "7. 패키지 설치"
yum install -y quota


echo "8. 파일 내용 생성"
echo '#!/bin/bash' > /usr/lib/mdadm/mdadm_env.sh
echo '#!/bin/bash' > /usr/share/mdadm/mdcheck
