from __import__ import *
import auto_daemon as ad


class PRE_CONDITIONS:
    def __init__(self):
        self.INACTIVE="Active: inactive"
        self.ACTIVE="Active: active"
        self.FAILED="Active: failed"
        self.MASKED="Loaded: masked"
        self.ONESHOT="Type=oneshot"
        self.FORKING="Type=forking"
        self.DBUS_TYPE ='Type=dbus'

    def checkRemain(self, path):
        output, error = commandExec(execMode, 'cat ' + path + ' |grep RemainAfterExit')
        try:
            remain = output[0]
            if 'RemainAfterExit=yes' in output or 'RemainAfterExit=true' in output :
                return True
            else:
                return False
        except:
            return False

    def remainRecovery(self, filePath):
        print("* Remain recoverying")
        file1 = open(filePath,'rt',encoding='utf-8')
        for daemon in file1:
            daemon = daemon.replace('\n','')
            output, error = commandExec(execMode, "cat " + daemon + " |grep -A 1 '\[Service\]'")
            if output != []:
                if output[0] == '[Service]' and output[1] == 'RemainAfterExit=yes':
                    commandExec(execMode, "sed -i '/" + output[1] + "/d' " + daemon)
                elif output[0] == self.ONESHOT and output[1] == 'RemainAfterExit=yes':
                    commandExec(execMode, "sed -i '/" + output[1] + "/d' " + daemon)


    def Apply(self, LISTFILE):

        apply_start = time.time()
        ## 현재는 7.7이 작성되지 않기 때문에 8.1과 동일한 내용으로 적용 중
        ## 7.7 조건이 완성되면 그때 나눠서 다시 작성
        print("* Pre condition version : " + str(VERSION_DETAIL))

        if HYPERVM_TEST == 'true':
            print("* SUPERVM pre condition")
            if HYPERVM_VERSION == 'v4_4':
                print("1. 파일 내용 변경 및 주석 처리")
                cnt = 0
                file = open(LISTFILE,'rt',encoding="utf-8")
                for line in file:
                    cnt += 1
                    line = line.replace('\n','')
                    ## 주석처리
                    commandExec(execMode, "sed -i.bak 's%ConditionPathExists=/proc/xen/capabilities%#ConditionPathExists=/proc/xen/capabilities%g' " + line) #

                    a = self.checkRemain(line)
                    if a == False: #RemainAfterExit=yes 또는 true 가 없을때,
                        commandExec(execMode, 'sed -i.bak'' -r -e "/\[Service\]/a\RemainAfterExit=yes" ' + line) ## 2
                print("2. Daemon Reload!")
                commandExec(execMode, "systemctl daemon-reload")
                print("3. 시작 조건 실행")
                commandExec(execMode, "vdsm-tool configure --force")
                print("4. 패키지 설치")
                commandExec(execMode, INSTALL_PKG + " install collectd-5.9.2-2.el8.x86_64 -y")

        else:

            if VERSION_DETAIL == 'v8_1':

                print("1. 수동 시작/종료 금지 등 주석 처리 - 대상: 전체 데몬")
                print("1-1. [Service] 섹션 찾아서 내용 추가 - 대상: oneshot/forking 데몬")
                cnt = 0
                file = open(LISTFILE,'rt',encoding="utf-8")
                for line in file:
                    cnt += 1
                    line = line.replace('\n','')
                    #print(str(cnt) + ") APPLY : " + line)

                    commandExec(execMode, "sed -i.bak 's/RefuseManualStop=yes/#RefuseManualStop=yes/g' " + line)
                    commandExec(execMode, "sed -i.bak 's/RefuseManualStart=yes/#RefuseManualStart=yes/g' " + line)
                    commandExec(execMode, "sed -i.bak 's/StopWhenUnneeded=yes/#StopWhenUnneeded=yes/g' " + line)
                    commandExec(execMode, "sed -i.bak 's/ConditionPathIsReadWrite=!\//#ConditionPathIsReadWrite=!\//g' " + line)
                    commandExec(execMode, "sed -i.bak 's/ConditionNeedsUpdate=\/var/#ConditionNeedsUpdate=\/var/g' " + line)
                    commandExec(execMode, "sed -i.bak 's/ConditionPathIsMountPoint=\/etc\/machine-id/#ConditionPathIsMountPoint=\/etc\/machine-id/g' " + line)
                    commandExec(execMode, "sed -i.bak 's/ConditionNeedsUpdate=\/etc/#ConditionNeedsUpdate=\/etc/g' " + line)
                    commandExec(execMode, "sed -i.bak 's/ConditionNeedsUpdate=|\/etc/#ConditionNeedsUpdate=|\/etc/g' " + line)
                    commandExec(execMode, "sed -i.bak 's/ConditionNeedsUpdate=|\/var/#ConditionNeedsUpdate=|\/var/g' " + line)
                    commandExec(execMode, "sed -i.bak 's/ConditionSecurity=!selinux/#ConditionSecurity=!selinux/g' " + line)
                    commandExec(execMode, "sed -i.bak 's/ConditionPathExists=!\/run\/plymouth\/pid/#ConditionPathExists=!\/run\/plymouth\/pid/g' " + line)
                    commandExec(execMode, "sed -i.bak 's/ConditionPathExists=!\/.autorelabel/#ConditionPathExists=!\/.autorelabel/g' " + line)

                    type_message, error = commandExec(execMode, 'grep "' + self.ONESHOT + '" ' + line + ' 2>&1')
                    type_message2, error = commandExec(execMode, 'grep "' + self.FORKING + '" ' + line + ' 2>&1')

                    if (type_message != [] and self.ONESHOT in type_message[0]) or (type_message2 != [] and self.FORKING in type_message2[0]):
                        option_message, error = commandExec(execMode, 'grep "' + self.REMAIN + '" ' + line + ' 2>&1')
                        if option_message != [] and self.REMAIN in option_message[0]:
                            commandExec(execMode, "sed -i.bak 's/\[Service\]/\[Service\]\nRemainAfterExit=yes/g' " + line)
                    #print(i + ' done')
                commandExec(execMode, 'systemctl daemon-reload')

                print("2. 파일 생성")
                commandExec(execMode, "touch /usr/lib/initrd-release")
                commandExec(execMode, "touch /lib/dracut/need-initqueue")
                commandExec(execMode, "touch /boot/grub2/grubenv.new")
                commandExec(execMode, "touch /run/plymouth/pid")
                commandExec(execMode, "touch /etc/initrd-release")
                commandExec(execMode, "touch /run/user/1")
                commandExec(execMode, "touch /lib/module-load.d")
                commandExec(execMode, "mkdir -p /run/teamd/")
                commandExec(execMode, "\cp /usr/share/doc/teamd/example_configs/activebackup_arp_ping_1.conf /run/teamd/test.conf")

                print("3. 폴더 및 하위 파일 존재")

                commandExec(execMode, "mkdir -p /lib/dracut/hooks/mount")
                commandExec(execMode, "touch /lib/dracut/hooks/mount/test")

                commandExec(execMode, "mkdir -p /lib/dracut/hooks/pre-mount/")
                commandExec(execMode, "touch /lib/dracut/hooks/pre-mount/test")

                commandExec(execMode, "mkdir -p /lib/dracut/hooks/pre-pivot")
                commandExec(execMode, "touch /lib/dracut/hooks/pre-pivot/test")

                commandExec(execMode, "mkdir -p /lib/dracut/hooks/pre-trigger")
                commandExec(execMode, "touch /lib/dracut/hooks/pre-trigger/test")

                commandExec(execMode, "mkdir -p /lib/dracut/hooks/pre-udev")
                commandExec(execMode, "touch /lib/dracut/hooks/pre-udev/test")

                commandExec(execMode, "mkdir -p /etc/sysconfig/modules")
                commandExec(execMode, "touch  /etc/sysconfig/modules/test")

                commandExec(execMode, "mkdir -p /lib/modules-load.d")
                commandExec(execMode, "touch /lib/modules-load.d/test")

                print("4. 실행 권한 부여")
                commandExec(execMode, "chmod +x /etc/rc.d/rc.local")

            elif VERSION_DETAIL == 'v7_7' :     ## 현재 테스트 중
                print("1. 수동 시작/종료 금지 등 주석 처리 - 대상: 전체 데몬")
                print("1-1. [Service] 섹션 찾아서 내용 추가 - 대상: 전체 데몬")
                cnt = 0
                file = open(LISTFILE,'rt',encoding="utf-8")
                for line in file:
                    cnt += 1
                    line = line.replace('\n','')
                    #print(str(cnt) + ") APPLY : " + line)
                    #print("sed -i.bak 's/ConditionKernelCommandLine=debug/#ConditionKernelCommandLine=debug/g' " + line)

                    commandExec(execMode, "sed -i.bak 's%RefuseManualStop=yes%#RefuseManualStop=yes%g' " + line)
                    commandExec(execMode, "sed -i.bak 's%RefuseManualStop=true%#RefuseManualStop=true%g' " + line)
                    commandExec(execMode, "sed -i.bak 's%RefuseManualStart=yes%#RefuseManualStart=yes%g' " + line)
                    commandExec(execMode, "sed -i.bak 's%RefuseManualStart=true%#RefuseManualStart=true%g' " + line)
                    commandExec(execMode, "sed -i.bak 's%StopWhenUnneeded=yes%#StopWhenUnneeded=yes%g' " + line)
                    commandExec(execMode, "sed -i.bak 's%ConditionKernelCommandLine=debug%#ConditionKernelCommandLine=debug%g' " + line)
                    commandExec(execMode, "sed -i.bak 's%ConditionPathIsReadWrite=!/%#ConditionPathIsReadWrite=!/%g' " + line)
                    commandExec(execMode, "sed -i.bak 's%ConditionNeedsUpdate=/etc%#ConditionNeedsUpdate=/etc%g' " + line)
                    commandExec(execMode, "sed -i.bak 's%ConditionNeedsUpdate=|/etc%#ConditionNeedsUpdate=|/etc%g' " + line)
                    commandExec(execMode, "sed -i.bak 's%ConditionNeedsUpdate=/var%#ConditionNeedsUpdate=/var%g' " + line)
                    commandExec(execMode, "sed -i.bak 's%ConditionNeedsUpdate=|/var%#ConditionNeedsUpdate=|/var%g' " + line)
                    commandExec(execMode, "sed -i.bak 's%ConditionFileNotEmpty=|!/etc/ssh/ssh_host_rsa_key%#ConditionFileNotEmpty=|!/etc/ssh/ssh_host_rsa_key%g' " + line)
                    commandExec(execMode, "sed -i.bak 's%ConditionFileNotEmpty=|!/etc/ssh/ssh_host_ecdsa_key%#ConditionFileNotEmpty=|!/etc/ssh/ssh_host_ecdsa_key%g' " + line)
                    commandExec(execMode, "sed -i.bak 's%ConditionFileNotEmpty=|!/etc/ssh/ssh_host_ed25519_key%#ConditionFileNotEmpty=|!/etc/ssh/ssh_host_ed25519_key%g' " + line)
                    commandExec(execMode, "sed -i.bak 's%ConditionPathIsMountPoint=/etc/machine-id%#ConditionPathIsMountPoint=/etc/machine-id%g' " + line)
                    commandExec(execMode, "sed -i.bak 's%ConditionSecurity=!selinux%#ConditionSecurity=!selinux%g' " + line)
                    commandExec(execMode, "sed -i.bak 's%ConditionPathExists=!/.autorelabel%#ConditionPathExists=!/.autorelabel%g' " + line)
                    commandExec(execMode, "sed -i.bak 's%ConditionPathExists=!/run/plymouth/pid%#ConditionPathExists=!/run/plymouth/pid%g' " + line)
                    commandExec(execMode, "sed -i.bak 's%RemainAfterExit=no%#RemainAfterExit=no%g' " + line)
                    commandExec(execMode, "sed -i.bak 's%ConditionVirtualization=no%#ConditionVirtualization=no%g' " + line)

                    commandExec(execMode, "sed -i.bak 's%ConditionPathExists=!/etc/initrd-release%#ConditionPathExists=!/etc/initrd-release%g' " + line)

                    output_remain_yes, error = commandExec(execMode, "cat " + line + " | grep RemainAfterExit=yes")
                    output_remain_true, error = commandExec(execMode, "cat " + line + " | grep RemainAfterExit=true")
                    if output_remain_yes == [] and output_remain_true == []:
                        output_remain_true, error = commandExec(execMode, "sed -i.bak 's/\[Service\]/\[Service\]\\nRemainAfterExit=yes/g' " + line)


                commandExec(execMode, "systemctl daemon-reload")

                print("2. 파일 생성 및 이동")

                commandExec(execMode, "touch /usr/lib/initrd-release")
                commandExec(execMode, "touch /lib/dracut/need-initqueue")
                commandExec(execMode, "touch /boot/grub2/grubenv.new")
                commandExec(execMode, "touch /run/plymouth/pid")
                commandExec(execMode, "touch /etc/initrd-release")

                commandExec(execMode, "touch /run/user/1")
                commandExec(execMode, "touch /lib/module-load.d")
                commandExec(execMode, "mkdir -p /run/teamd/")
                commandExec(execMode, "\cp /usr/share/doc/teamd-1.27/example_configs/activebackup_arp_ping_1.conf /run/teamd/test.conf")
                commandExec(execMode, "touch /var/log/Xorg.0.log")
                commandExec(execMode, "touch /etc/multipath.conf")
                commandExec(execMode, "touch /etc/ethers")
                commandExec(execMode, "touch /etc/krb5.keytab")
                commandExec(execMode, "touch /etc/openwsman/owsmangencert.sh")
                commandExec(execMode, "touch /etc/quagga/babeld.conf")
                commandExec(execMode, "touch /etc/quagga/bgpd.conf")
                commandExec(execMode, "touch /etc/quagga/isisd.conf")
                commandExec(execMode, "touch /etc/quagga/ospf6d.conf")
                commandExec(execMode, "touch /etc/quagga/ospfd.conf")
                commandExec(execMode, "touch /etc/quagga/ripd.conf")
                commandExec(execMode, "touch /etc/quagga/ripngd.conf")
                commandExec(execMode, "touch /var/lib/mdcheck/MD_UUID_0")

                commandExec(execMode, "mv /etc/alsa/state-daemon.conf /root/")
                #commandExec(execMode, "mv /etc/cloud/cloud-init.disabled /root/")
                commandExec(execMode, "mv /etc/pki/cyrus-imapd/cyrus-imapd.pem /root/")
                commandExec(execMode, "touch /var/crash/a")
                commandExec(execMode, "touch /run/initramfs/state/temp")
                commandExec(execMode, "touch /dev/capi20")
                commandExec(execMode, "touch /dev/isdn/capi20")
                commandExec(execMode, "touch /.readahead")
                commandExec(execMode, "echo temp message >> /.readahead")

                commandExec(execMode, "touch /run/initramfs/upgrade.conf")

                tangFiles, error = commandExec(execMode, "ls /var/db/tang |grep .jwk")
                for tangfile in tangFiles:
                    output, error = commandExec(execMode, "mv /var/db/tang/"+tangfile+" /root/")

                print ("3. 폴더 및 하위 파일 존재")
                commandExec(execMode, "mkdir -p /lib/dracut/hooks/mount")
                commandExec(execMode, "touch /lib/dracut/hooks/mount/test")

                commandExec(execMode, "mkdir -p /lib/dracut/hooks/pre-mount/")
                commandExec(execMode, "touch /lib/dracut/hooks/pre-mount/test")

                commandExec(execMode, "mkdir -p /lib/dracut/hooks/pre-pivot")
                commandExec(execMode, "touch /lib/dracut/hooks/pre-pivot/test")

                commandExec(execMode, "mkdir -p /lib/dracut/hooks/pre-trigger")
                commandExec(execMode, "touch /lib/dracut/hooks/pre-trigger/test")

                commandExec(execMode, "mkdir -p /lib/dracut/hooks/pre-udev")
                commandExec(execMode, "touch /lib/dracut/hooks/pre-udev/test")

                commandExec(execMode, "mkdir -p /etc/sysconfig/modules")
                commandExec(execMode, "touch  /etc/sysconfig/modules/test")

                commandExec(execMode, "mkdir -p /lib/modules-load.d")
                commandExec(execMode, "touch /lib/modules-load.d/test")

                commandExec(execMode, "mkdir -p  /lib/dracut/hooks/cmdline")
                commandExec(execMode, "touch /lib/dracut/hooks/cmdline/test")

                commandExec(execMode, "mkdir -p /var/lib/iscsi/nodes")
                commandExec(execMode, "touch /var/lib/iscsi/nodes/test")

                commandExec(execMode, "mkdir -p /usr/lib/mdadm/")
                commandExec(execMode, "touch /usr/lib/mdadm/mdadm_env.sh")

                commandExec(execMode, "mkdir -p /usr/share/mdadm")
                commandExec(execMode, "touch /usr/share/mdadm/mdcheck")

                commandExec(execMode, "mkdir /var/svn")
                commandExec(execMode, "mkdir /var/log/journal")

                commandExec(execMode, "mv /etc/unbound/unbound_control.key /root/")
                commandExec(execMode, "mv /etc/dnssec-trigger/dnssec_trigger_control.key /root/")

                commandExec(execMode, "mkdir /etc/sysconfig/modules")
                commandExec(execMode, "touch /etc/sysconfig/modules/temp")


                print ("4. 실행 권한 부여")
                commandExec(execMode, "chmod +x /etc/rc.d/rc.local")
                commandExec(execMode, "chmod +x /usr/share/mdadm/mdcheck")
                commandExec(execMode, "chmod +x /usr/lib/mdadm/mdadm_env.sh")

                print("5. 개별 데몬 제어")
                commandExec(execMode, "systemctl daemon-reload")
                commandExec(execMode, "systemctl stop cups.service")
                commandExec(execMode, "systemctl stop dbus.socket")
                commandExec(execMode, "systemctl stop iscsid.service")
                commandExec(execMode, "systemctl start named-chroot.service")
                commandExec(execMode, "systemctl start amanda-udp.socket")
                commandExec(execMode, "systemctl start dmraid-activation.service")
                commandExec(execMode, "systemctl start systemd-udev-trigger.service")
                commandExec(execMode, "systemctl start dnssec-triggerd-keygen.service")
                commandExec(execMode, "systemctl start ntalk.socket")
                commandExec(execMode, "systemctl start abrtd.service")
                commandExec(execMode, "systemctl start named.service")

            elif VERSION_DETAIL == 'v7_8':
                print("1. 수동 시작/종료 금지 등 주석 처리 - 대상: 전체 데몬")
                print("1-1. [Service] 섹션 찾아서 내용 추가 - 대상: 전체 데몬")
                cnt = 0
                file = open(LISTFILE,'rt',encoding="utf-8")
                for line in file:
                    cnt += 1
                    line = line.replace('\n','')
                    print(str(cnt) + ") APPLY : " + line)
                    #commandExec(execMode, "sed -i.bak 's%IgnoreOnIsolate=1%#IgnoreOnIsolate=1%g' " + line) #
                    #commandExec(execMode, "sed -i.bak 's%ConditionNeedsUpdate=/var%#ConditionNeedsUpdate=/var%g' " + line)#
                    #commandExec(execMode, "sed -i.bak 's%ConditionKernelCommandLine=ostree%#ConditionKernelCommandLine=ostree%g' " + line) #
                    #commandExec(execMode, "sed -i.bak 's%ConditionPathExists=!/.autorelabel%#ConditionPathExists=!/.autorelabel%g' " + line)#

                    commandExec(execMode, "sed -i.bak 's%ConditionKernelCommandLine=debug%#ConditionKernelCommandLine=debug%g' " + line)  # V
                    commandExec(execMode, "sed -i.bak 's%RefuseManualStop=yes%#RefuseManualStop=yes%g' " + line) # V
                    commandExec(execMode, "sed -i.bak 's%ConditionSecurity=!selinux%#ConditionSecurity=!selinux%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%RefuseManualStart=true%#RefuseManualStart=true%g' " + line) # V
                    commandExec(execMode, "sed -i.bak 's%ConditionDirectoryNotEmpty=/sys/class/iscsi_session%#ConditionDirectoryNotEmpty=/sys/class/iscsi_session%g' " + line) # V
                    commandExec(execMode, "sed -i.bak 's%RemainAfterExit=no%#RemainAfterExit=no%g' " + line) # V
                    commandExec(execMode, "sed -i.bak 's%ConditionFileNotEmpty=|!/etc/ssh/ssh_host_rsa_key%#ConditionFileNotEmpty=|!/etc/ssh/ssh_host_rsa_key%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionFileNotEmpty=|!/etc/ssh/ssh_host_ecdsa_key%#ConditionFileNotEmpty=|!/etc/ssh/ssh_host_ecdsa_key%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionFileNotEmpty=|!/etc/ssh/ssh_host_ed25519_key%#ConditionFileNotEmpty=|!/etc/ssh/ssh_host_ed25519_key%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionPathExists=!/run/ostree-booted%#ConditionPathExists=!/run/ostree-booted%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%StopWhenUnneeded=yes%#StopWhenUnneeded=yes%g' " + line) # V
                    commandExec(execMode, "sed -i.bak 's%RefuseManualStop=true%#RefuseManualStop=true%g' " + line) # V
                    commandExec(execMode, "sed -i.bak 's%ConditionPathIsReadWrite=!/%#ConditionPathIsReadWrite=!/%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionNeedsUpdate=|/etc%#ConditionNeedsUpdate=|/etc%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionNeedsUpdate=/etc%#ConditionNeedsUpdate=/etc%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionPathIsMountPoint=/etc/machine-id%#ConditionPathIsMountPoint=/etc/machine-id%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionCapability=CAP_SYS_MODULE%#ConditionCapability=CAP_SYS_MODULE%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionDirectoryNotEmpty=|/lib/modules-load.d%#ConditionDirectoryNotEmpty=|/lib/modules-load.d%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionDirectoryNotEmpty=|/usr/lib/modules-load.d%#ConditionDirectoryNotEmpty=|/usr/lib/modules-load.d%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionDirectoryNotEmpty=|/usr/local/lib/modules-load.d%#ConditionDirectoryNotEmpty=|/usr/local/lib/modules-load.d%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionDirectoryNotEmpty=|/etc/modules-load.d%#ConditionDirectoryNotEmpty=|/etc/modules-load.d%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionDirectoryNotEmpty=|/run/modules-load.d%#ConditionDirectoryNotEmpty=|/run/modules-load.d%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionKernelCommandLine=|modules-load%#ConditionKernelCommandLine=|modules-load%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionKernelCommandLine=|rd.modules-load%#ConditionKernelCommandLine=|rd.modules-load%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionVirtualization=no%#ConditionVirtualization=no%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionNeedsUpdate=|/var%#ConditionNeedsUpdate=|/var%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%RefuseManualStart=yes%#RefuseManualStart=yes%g' " + line) # V

                    # 조건 6 (조건 1, 3 조합)
                    commandExec(execMode, "sed -i.bak 's%ConditionDirectoryNotEmpty=/sys/fs/pstore%#ConditionDirectoryNotEmpty=/sys/fs/pstore%g' " + line) # V

                    a = self.checkRemain(line)
                    if a == False: #RemainAfterExit=yes  true 가 없을때,
                        commandExec(execMode, 'sed -i.bak'' -r -e "/\[Service\]/a\RemainAfterExit=yes" ' + line)# V

                print("* Daemon Reload!")
                commandExec(execMode, "systemctl daemon-reload")

                print("2. 파일 생성, 이동, 권한 부여, 실행")
                #commandExec(execMode, 'touch /var/crash/test')#
                #commandExec(execMode, 'touch /var/lib/fwupd/pending.db')#
                #commandExec(execMode, 'mkdir -p /dev/vmbus')#
                #commandExec(execMode, 'touch /dev/vmbus/hv_fcopy')#
                #commandExec(execMode, "touch /etc/sysconfig/nfs")#
                #commandExec(execMode, "touch /run/ostree-booted")#
                #commandExec(execMode, "\cp /usr/share/doc/stunnel/stunnel.conf-sample /etc/stunnel/stunnel.conf")#
                #commandExec(execMode, 'touch /usr/lib/initrd-release')#
                ############
                #commandExec(execMode, '\mv /etc/cloud/cloud-init.disabled /etc/cloud/cloud-init.disabled.bak')#
                #commandExec(execMode, "\mv /etc/ld.so.cache /etc/ld.so.cache.bak")#
                #commandExec(execMode, "\mv /etc/unbound/unbound_control.key /etc/unbound/unbound_control.key.bak")#
                #commandExec(execMode, "touch /etc/ctdb/nodes")#
                #commandExec(execMode, 'echo "'+ HOST_IP +'" >> /etc/ctdb/nodes')
                #commandExec(execMode, "touch /etc/sysconfig/ctdb")#
                #commandExec(execMode, 'echo CTDB_NODES=/etc/ctdb/nodes >> /etc/sysconfig/ctdb')
                #commandExec(execMode, 'echo CTDB_PUBLIC_ADDRESSES=/etc/ctdb/public_addresses >> /etc/sysconfig/ctdb')
                #commandExec(execMode, 'echo CTDB_RECOVERY_LOCK="/mnt/ctdb/.ctdb.lock" >> /etc/sysconfig/ctdb')
                #commandExec(execMode, 'echo CTDB_MANAGES_SAMBA=yes >> /etc/sysconfig/ctdb')
                #commandExec(execMode, 'echo CTDB_MANAGES_WINBIND=yes >> /etc/sysconfig/ctdb')
                #commandExec(execMode, '\mv /etc/pki/dovecot/certs/dovecot.pem /etc/pki/dovecot/certs/dovecot.pem.bak')#
                #commandExec(execMode, '\mv /etc/pki/dovecot/private/dovecot.pem /etc/pki/dovecot/private/dovecot.pem.bak')#
                #commandExec(execMode, '\mv /etc/pki/tls/certs/localhost.crt /etc/pki/tls/certs/localhost.crt.bak')
                #commandExec(execMode, '\mv /etc/pki/tls/private/localhost.key /etc/pki/tls/private/localhost.key.bak')
                #commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd.pem /etc/pki/cyrus-imapd/cyrus-imapd.pem.bak')
                #commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd-key.pem /etc/pki/cyrus-imapd/cyrus-imapd-key.pem.bak')
                #commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd-ca.pem /etc/pki/cyrus-imapd/cyrus-imapd-ca.pem.bak')
                #commandExec(execMode, '\mv /var/lib/cloud/instance /var/lib/cloud/instance_back') ## cloud-final, cloud-config service 테스트용
                #commandExec(execMode, "\cp /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd.conf.bak")
                ############ pair가 아닌 조건들
                #commandExec(execMode, '\mv /etc/cockpit/ws-certs.d/0-self-signed.cert /etc/cockpit/ws-certs.d/0-self-signed.cert.2') # cockpit.service 시작 실패 시 시작 조건
                #commandExec(execMode, "sh /etc/openwsman/owsmangencert.sh")

                commandExec(execMode, '\mv /etc/alsa/state-daemon.conf /root/')# V
                commandExec(execMode, 'touch /etc/multipath.conf')# V
                commandExec(execMode, "touch /etc/initrd-release")# V
                commandExec(execMode, 'mkdir -p /lib/dracut/hooks/cmdline')# V
                commandExec(execMode, 'touch /lib/dracut/hooks/cmdline/test')# V
                commandExec(execMode, 'mkdir -p /lib/dracut/hooks/mount')# V
                commandExec(execMode, 'touch /lib/dracut/hooks/mount/test')# V
                commandExec(execMode, 'mkdir -p /lib/dracut/hooks/pre-mount')# V
                commandExec(execMode, 'touch /lib/dracut/hooks/pre-mount/test')# V
                commandExec(execMode, 'mkdir -p /lib/dracut/hooks/pre-pivot')# V
                commandExec(execMode, 'touch /lib/dracut/hooks/pre-pivot/test')# V
                commandExec(execMode, 'mkdir -p /lib/dracut/hooks/pre-trigger')# V
                commandExec(execMode, 'touch /lib/dracut/hooks/pre-trigger/test')# V
                commandExec(execMode, 'mkdir -p /lib/dracut/hooks/pre-udev')# V
                commandExec(execMode, 'touch /lib/dracut/hooks/pre-udev/test')# V
                commandExec(execMode, 'mkdir -p /etc/sysconfig/modules')# V
                commandExec(execMode, 'touch /etc/sysconfig/modules/test')# V
                commandExec(execMode, 'touch /etc/rc.modules')# V
                commandExec(execMode, 'chmod 777 /etc/rc.modules')# V
                commandExec(execMode, 'touch /etc/sysconfig/ipvsadm')# V
                commandExec(execMode, 'mkdir -p /var/lib/iscsi/nodes/')# V
                commandExec(execMode, 'touch /var/lib/iscsi/nodes/test')# V
                commandExec(execMode, "touch /etc/ethers")# V
                commandExec(execMode, "touch /etc/krb5.keytab")# V
                commandExec(execMode, "/usr/bin/postgresql-setup initdb")# V, 7.8 버전에선 -- 기호 빼고 실행
                commandExec(execMode, "touch /etc/quagga/babeld.conf")# V
                commandExec(execMode, "touch /etc/quagga/bgpd.conf")# V
                commandExec(execMode, "touch /etc/quagga/isisd.conf")# V
                commandExec(execMode, "touch /etc/quagga/ospfd.conf")# V
                commandExec(execMode, "touch /etc/quagga/ripd.conf")# V
                commandExec(execMode, "touch /etc/quagga/ripngd.conf")# V
                commandExec(execMode, "mkdir /var/svn")# V
                commandExec(execMode, "chmod +x /etc/rc.d/rc.local")# V
                commandExec(execMode, "\mv /etc/unbound/unbound_control.key /etc/unbound/unbound_control.key.bak")# V

                # 조건 5 (조건 1, 2 조합)
                commandExec(execMode, 'mkdir -p /var/lib/mdcheck')#
                commandExec(execMode, 'touch /var/lib/mdcheck/MD_UUID_0')#
                commandExec(execMode, 'mkdir -p /usr/lib/mdadm/')#
                commandExec(execMode, 'touch /usr/lib/mdadm/mdadm_env.sh')#
                commandExec(execMode, 'mkdir -p /usr/share/mdadm')#
                commandExec(execMode, 'touch /usr/share/mdadm/mdcheck')#
                commandExec(execMode, 'chmod +x /usr/share/mdadm/mdcheck')
                commandExec(execMode, 'chmod +x /usr/lib/mdadm/mdadm_env.sh')
                commandExec(execMode, "echo '#!/bin/bash' > /usr/lib/mdadm/mdadm_env.sh")
                commandExec(execMode, "echo '#!/bin/bash' > /usr/share/mdadm/mdcheck")
                commandExec(execMode, "rm -rf /run/systemd/readahead/done")# V
                commandExec(execMode, "rm -rf /run/systemd/readahead/cancel")# V
                commandExec(execMode, "touch /.readahead")
                commandExec(execMode, "rm -rf /var/db/tang/*.jwk")

                # 조건 7 (조건 2, 3 조합)
                commandExec(execMode, "touch /var/log/Xorg.0.log") # V, 누락된 조건 추가

                # 조건 8 (조건 2, 999 조합)
                commandExec(execMode, "chmod +w /sys")

                print("3. 개별 데몬 제어")
                #commandExec(execMode, "systemctl start named.service")
                #commandExec(execMode, "systemctl start cockpit.service")
                #commandExec(execMode, "systemctl stop cups.service")
                #commandExec(execMode, "systemctl stop sysstat-collect.timer")
                #commandExec(execMode, "systemctl start sys-kernel-config.mount")

                commandExec(execMode, "systemctl start amanda-udp.socket")# V
                commandExec(execMode, "systemctl start dbus.service")# V
                commandExec(execMode, "systemctl start polkit.service")# V
                commandExec(execMode, "systemctl start ntalk.socket")# V

                # 조건 6 (조건 1, 3 조합)
                commandExec(execMode, "systemctl start systemd-udev-settle.service")

                # 조건 6 (조건 1, 3 조합), 조건 7 (조건 2, 3 조합)
                commandExec(execMode, "systemctl start abrtd.service")

                print("4. 개별 파일 내용 변경")
                # 맥 주소, 아이피주소 입력
                #output, error = commandExec(execMode, "cat /sys/class/net/e*/address")
                #if output != []:
                #    MAC_ADDR = output[0]
                #    commandExec(execMode, "sed -i.bak 's%# SYSLOGMACADDR=%SYSLOGMACADDR=" + MAC_ADDR + "%g' /etc/sysconfig/netconsole")#
                #    commandExec(execMode, "sed -i 's%# SYSLOGADDR=%SYSLOGADDR=" + HOST_IP + "%g' /etc/sysconfig/netconsole")#
                #else:
                #    print("No Mac address")

                #commandExec(execMode, "command='subnet 192.168.17.0 netmask 255.255.255.0 {\n\toption routers 192.168.17.1;\n\toption subnet-mask 255.255.255.0;\n\trange dynamic-bootp 192.168.17.200 192.168.17.220;\n\tdefault-lease-time 600;\n\tmax-lease-time 7200;\n}'")
                #commandExec(execMode, "echo -e $command >> /etc/dhcp/dhcpd.conf")
                #commandExec(execMode, "firewall-cmd --permanent --add-port=67/udp && firewall-cmd --reload")

                commandExec(execMode, "sed -i.bak 's%" + 'OPENHPI_UNCONFIGURED = "YES"' + "%" + '#OPENHPI_UNCONFIGURED = "YES"' + "%g' /etc/openhpi/openhpi.conf")# V
                commandExec(execMode, "sed -i 's%" + '#OPENHPI_LOG_ON_SEV = "MINOR"' + "%" + 'OPENHPI_LOG_ON_SEV = "MINOR"' + "%g' /etc/openhpi/openhpi.conf")# V
                commandExec(execMode, "systemctl daemon-reload")

            elif VERSION_DETAIL == 'v7_9':

                print("1. 수동 시작/종료 금지 등 주석 처리 - 대상: 전체 데몬")
                print("1-1. [Service] 섹션 찾아서 내용 추가 - 대상: 전체 데몬")
                cnt = 0
                file = open(LISTFILE,'rt',encoding="utf-8")
                for line in file:
                    cnt += 1
                    line = line.replace('\n','')
                    print(str(cnt) + ") APPLY : " + line)
                    #commandExec(execMode, "sed -i.bak 's%IgnoreOnIsolate=1%#IgnoreOnIsolate=1%g' " + line) #
                    #commandExec(execMode, "sed -i.bak 's%ConditionNeedsUpdate=/var%#ConditionNeedsUpdate=/var%g' " + line)#
                    #commandExec(execMode, "sed -i.bak 's%ConditionKernelCommandLine=ostree%#ConditionKernelCommandLine=ostree%g' " + line) #
                    #commandExec(execMode, "sed -i.bak 's%ConditionPathExists=!/.autorelabel%#ConditionPathExists=!/.autorelabel%g' " + line)#

                    commandExec(execMode, "sed -i.bak 's%ConditionKernelCommandLine=debug%#ConditionKernelCommandLine=debug%g' " + line)  # V
                    commandExec(execMode, "sed -i.bak 's%RefuseManualStop=yes%#RefuseManualStop=yes%g' " + line) # V
                    commandExec(execMode, "sed -i.bak 's%ConditionSecurity=!selinux%#ConditionSecurity=!selinux%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%RefuseManualStart=true%#RefuseManualStart=true%g' " + line) # V
                    commandExec(execMode, "sed -i.bak 's%ConditionDirectoryNotEmpty=/sys/class/iscsi_session%#ConditionDirectoryNotEmpty=/sys/class/iscsi_session%g' " + line) # V
                    commandExec(execMode, "sed -i.bak 's%RemainAfterExit=no%#RemainAfterExit=no%g' " + line) # V
                    commandExec(execMode, "sed -i.bak 's%ConditionFileNotEmpty=|!/etc/ssh/ssh_host_rsa_key%#ConditionFileNotEmpty=|!/etc/ssh/ssh_host_rsa_key%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionFileNotEmpty=|!/etc/ssh/ssh_host_ecdsa_key%#ConditionFileNotEmpty=|!/etc/ssh/ssh_host_ecdsa_key%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionFileNotEmpty=|!/etc/ssh/ssh_host_ed25519_key%#ConditionFileNotEmpty=|!/etc/ssh/ssh_host_ed25519_key%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionPathExists=!/run/ostree-booted%#ConditionPathExists=!/run/ostree-booted%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%StopWhenUnneeded=yes%#StopWhenUnneeded=yes%g' " + line) # V
                    commandExec(execMode, "sed -i.bak 's%RefuseManualStop=true%#RefuseManualStop=true%g' " + line) # V
                    commandExec(execMode, "sed -i.bak 's%ConditionPathIsReadWrite=!/%#ConditionPathIsReadWrite=!/%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionNeedsUpdate=|/etc%#ConditionNeedsUpdate=|/etc%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionNeedsUpdate=/etc%#ConditionNeedsUpdate=/etc%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionPathIsMountPoint=/etc/machine-id%#ConditionPathIsMountPoint=/etc/machine-id%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionCapability=CAP_SYS_MODULE%#ConditionCapability=CAP_SYS_MODULE%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionDirectoryNotEmpty=|/lib/modules-load.d%#ConditionDirectoryNotEmpty=|/lib/modules-load.d%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionDirectoryNotEmpty=|/usr/lib/modules-load.d%#ConditionDirectoryNotEmpty=|/usr/lib/modules-load.d%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionDirectoryNotEmpty=|/usr/local/lib/modules-load.d%#ConditionDirectoryNotEmpty=|/usr/local/lib/modules-load.d%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionDirectoryNotEmpty=|/etc/modules-load.d%#ConditionDirectoryNotEmpty=|/etc/modules-load.d%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionDirectoryNotEmpty=|/run/modules-load.d%#ConditionDirectoryNotEmpty=|/run/modules-load.d%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionKernelCommandLine=|modules-load%#ConditionKernelCommandLine=|modules-load%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionKernelCommandLine=|rd.modules-load%#ConditionKernelCommandLine=|rd.modules-load%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionVirtualization=no%#ConditionVirtualization=no%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%ConditionNeedsUpdate=|/var%#ConditionNeedsUpdate=|/var%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%RefuseManualStart=yes%#RefuseManualStart=yes%g' " + line) # V
                    commandExec(execMode, "sed -i.bak 's%ConditionPathIsMountPoint=/system-upgrade-root%#ConditionPathIsMountPoint=/system-upgrade-root%g' " + line) # V

                    # 조건 6 (조건 1, 3 조합)
                    commandExec(execMode, "sed -i.bak 's%ConditionDirectoryNotEmpty=/sys/fs/pstore%#ConditionDirectoryNotEmpty=/sys/fs/pstore%g' " + line) # V

                    a = self.checkRemain(line)
                    if a == False: #RemainAfterExit=yes  true 가 없을때,
                        commandExec(execMode, 'sed -i.bak'' -r -e "/\[Service\]/a\RemainAfterExit=yes" ' + line)# V

                print("* Daemon Reload!")
                commandExec(execMode, "systemctl daemon-reload")

                print("2. 파일 생성, 이동, 권한 부여, 실행")
                #commandExec(execMode, 'touch /var/crash/test')#
                #commandExec(execMode, 'touch /var/lib/fwupd/pending.db')#
                #commandExec(execMode, 'mkdir -p /dev/vmbus')#
                #commandExec(execMode, 'touch /dev/vmbus/hv_fcopy')#
                #commandExec(execMode, "touch /etc/sysconfig/nfs")#
                #commandExec(execMode, "touch /run/ostree-booted")#
                #commandExec(execMode, "\cp /usr/share/doc/stunnel/stunnel.conf-sample /etc/stunnel/stunnel.conf")#
                #commandExec(execMode, 'touch /usr/lib/initrd-release')#
                ############
                #commandExec(execMode, '\mv /etc/cloud/cloud-init.disabled /etc/cloud/cloud-init.disabled.bak')#
                #commandExec(execMode, "\mv /etc/ld.so.cache /etc/ld.so.cache.bak")#
                #commandExec(execMode, "\mv /etc/unbound/unbound_control.key /etc/unbound/unbound_control.key.bak")#
                #commandExec(execMode, "touch /etc/ctdb/nodes")#
                #commandExec(execMode, 'echo "'+ HOST_IP +'" >> /etc/ctdb/nodes')
                #commandExec(execMode, "touch /etc/sysconfig/ctdb")#
                #commandExec(execMode, 'echo CTDB_NODES=/etc/ctdb/nodes >> /etc/sysconfig/ctdb')
                #commandExec(execMode, 'echo CTDB_PUBLIC_ADDRESSES=/etc/ctdb/public_addresses >> /etc/sysconfig/ctdb')
                #commandExec(execMode, 'echo CTDB_RECOVERY_LOCK="/mnt/ctdb/.ctdb.lock" >> /etc/sysconfig/ctdb')
                #commandExec(execMode, 'echo CTDB_MANAGES_SAMBA=yes >> /etc/sysconfig/ctdb')
                #commandExec(execMode, 'echo CTDB_MANAGES_WINBIND=yes >> /etc/sysconfig/ctdb')
                #commandExec(execMode, '\mv /etc/pki/dovecot/certs/dovecot.pem /etc/pki/dovecot/certs/dovecot.pem.bak')#
                #commandExec(execMode, '\mv /etc/pki/dovecot/private/dovecot.pem /etc/pki/dovecot/private/dovecot.pem.bak')#
                #commandExec(execMode, '\mv /etc/pki/tls/certs/localhost.crt /etc/pki/tls/certs/localhost.crt.bak')
                #commandExec(execMode, '\mv /etc/pki/tls/private/localhost.key /etc/pki/tls/private/localhost.key.bak')
                #commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd.pem /etc/pki/cyrus-imapd/cyrus-imapd.pem.bak')
                #commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd-key.pem /etc/pki/cyrus-imapd/cyrus-imapd-key.pem.bak')
                #commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd-ca.pem /etc/pki/cyrus-imapd/cyrus-imapd-ca.pem.bak')
                #commandExec(execMode, '\mv /var/lib/cloud/instance /var/lib/cloud/instance_back') ## cloud-final, cloud-config service 테스트용
                #commandExec(execMode, "\cp /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd.conf.bak")
                ############ pair가 아닌 조건들
                #commandExec(execMode, '\mv /etc/cockpit/ws-certs.d/0-self-signed.cert /etc/cockpit/ws-certs.d/0-self-signed.cert.2') # cockpit.service 시작 실패 시 시작 조건
                #commandExec(execMode, "sh /etc/openwsman/owsmangencert.sh")

                commandExec(execMode, '\mv /etc/alsa/state-daemon.conf /root/')# V
                commandExec(execMode, 'touch /etc/multipath.conf')# V
                commandExec(execMode, "touch /etc/initrd-release")# V
                commandExec(execMode, "touch /lib/dracut/need-initqueue")# V
                commandExec(execMode, 'mkdir -p /lib/dracut/hooks/cmdline')# V
                commandExec(execMode, 'touch /lib/dracut/hooks/cmdline/test')# V
                commandExec(execMode, 'mkdir -p /lib/dracut/hooks/mount')# V
                commandExec(execMode, 'touch /lib/dracut/hooks/mount/test')# V
                commandExec(execMode, 'mkdir -p /lib/dracut/hooks/pre-mount')# V
                commandExec(execMode, 'touch /lib/dracut/hooks/pre-mount/test')# V
                commandExec(execMode, 'mkdir -p /lib/dracut/hooks/pre-pivot')# V
                commandExec(execMode, 'touch /lib/dracut/hooks/pre-pivot/test')# V
                commandExec(execMode, 'mkdir -p /lib/dracut/hooks/pre-trigger')# V
                commandExec(execMode, 'touch /lib/dracut/hooks/pre-trigger/test')# V
                commandExec(execMode, 'mkdir -p /lib/dracut/hooks/pre-udev')# V
                commandExec(execMode, 'touch /lib/dracut/hooks/pre-udev/test')# V
                commandExec(execMode, 'mkdir -p /etc/sysconfig/modules')# V
                commandExec(execMode, 'touch /etc/sysconfig/modules/test')# V
                commandExec(execMode, 'touch /etc/rc.modules')# V
                commandExec(execMode, 'chmod 777 /etc/rc.modules')# V
                commandExec(execMode, 'touch /etc/sysconfig/ipvsadm')# V
                commandExec(execMode, 'mkdir -p /var/lib/iscsi/nodes/')# V
                commandExec(execMode, 'touch /var/lib/iscsi/nodes/test')# V
                commandExec(execMode, 'touch /etc/stinit.def')# V
                commandExec(execMode, "touch /etc/ethers")# V
                commandExec(execMode, "touch /etc/krb5.keytab")# V
                commandExec(execMode, "touch /run/plymouth/pid")# V
                commandExec(execMode, "/usr/bin/postgresql-setup initdb")# V, 7.8 버전에선 -- 기호 빼고 실행
                commandExec(execMode, "touch /etc/quagga/babeld.conf")# V
                commandExec(execMode, "touch /etc/quagga/bgpd.conf")# V
                commandExec(execMode, "touch /etc/quagga/isisd.conf")# V
                commandExec(execMode, "touch /etc/quagga/ospfd.conf")# V
                commandExec(execMode, "touch /etc/quagga/ripd.conf")# V
                commandExec(execMode, "touch /etc/quagga/ripngd.conf")# V
                commandExec(execMode, "touch /run/initramfs/upgrade.conf")# V
                commandExec(execMode, "mkdir /var/svn")# V
                commandExec(execMode, "chmod +x /etc/rc.d/rc.local")# V
                commandExec(execMode, "\mv /etc/unbound/unbound_control.key /etc/unbound/unbound_control.key.bak")# V
                commandExec(execMode, "cp /usr/lib64/sssd/conf/sssd.conf /etc/sssd/")# V
                commandExec(execMode, "chmod 600 /etc/sssd/sssd.conf")# V

                # 조건 5 (조건 1, 2 조합)
                commandExec(execMode, 'touch /usr/share/sounds/freedesktop/stereo/system-bootup.oga')# V
                commandExec(execMode, 'touch /usr/share/sounds/freedesktop/stereo/system-shutdown.oga')# V
                commandExec(execMode, 'mkdir -p /var/lib/mdcheck')#
                commandExec(execMode, 'touch /var/lib/mdcheck/MD_UUID_0')#
                commandExec(execMode, 'mkdir -p /usr/lib/mdadm/')#
                commandExec(execMode, 'touch /usr/lib/mdadm/mdadm_env.sh')#
                commandExec(execMode, 'mkdir -p /usr/share/mdadm')#
                commandExec(execMode, 'touch /usr/share/mdadm/mdcheck')#
                commandExec(execMode, 'chmod +x /usr/share/mdadm/mdcheck')
                commandExec(execMode, 'chmod +x /usr/lib/mdadm/mdadm_env.sh')
                commandExec(execMode, "echo '#!/bin/bash' > /usr/lib/mdadm/mdadm_env.sh")
                commandExec(execMode, "echo '#!/bin/bash' > /usr/share/mdadm/mdcheck")
                commandExec(execMode, "rm -rf /run/systemd/readahead/done")# V
                commandExec(execMode, "rm -rf /run/systemd/readahead/cancel")# V
                commandExec(execMode, "touch /.readahead")
                commandExec(execMode, "rm -rf /var/db/tang/*.jwk")

                # 조건 7 (조건 2, 3 조합)
                commandExec(execMode, "touch /var/log/Xorg.0.log") # V, 누락된 조건 추가

                # 조건 8 (조건 2, 999 조합)
                commandExec(execMode, "chmod +w /sys")

                print("3. 개별 데몬 제어")
                #commandExec(execMode, "systemctl start named.service")
                #commandExec(execMode, "systemctl start cockpit.service")
                #commandExec(execMode, "systemctl stop cups.service")
                #commandExec(execMode, "systemctl stop sysstat-collect.timer")
                #commandExec(execMode, "systemctl start sys-kernel-config.mount")

                commandExec(execMode, "systemctl start amanda-udp.socket")# V
                commandExec(execMode, "systemctl start dbus.service")# V
                commandExec(execMode, "systemctl start polkit.service")# V
                commandExec(execMode, "systemctl start ntalk.socket")# V
                commandExec(execMode, "systemctl stop rsyslog.service")# V

                # 조건 6 (조건 1, 3 조합)
                commandExec(execMode, "systemctl start systemd-udev-settle.service")

                # 조건 6 (조건 1, 3 조합), 조건 7 (조건 2, 3 조합)
                commandExec(execMode, "systemctl start abrtd.service")

                print("4. 개별 파일 내용 변경")
                # 맥 주소, 아이피주소 입력
                #output, error = commandExec(execMode, "cat /sys/class/net/e*/address")
                #if output != []:
                #    MAC_ADDR = output[0]
                #    commandExec(execMode, "sed -i.bak 's%# SYSLOGMACADDR=%SYSLOGMACADDR=" + MAC_ADDR + "%g' /etc/sysconfig/netconsole")#
                #    commandExec(execMode, "sed -i 's%# SYSLOGADDR=%SYSLOGADDR=" + HOST_IP + "%g' /etc/sysconfig/netconsole")#
                #else:
                #    print("No Mac address")

                #commandExec(execMode, "command='subnet 192.168.17.0 netmask 255.255.255.0 {\n\toption routers 192.168.17.1;\n\toption subnet-mask 255.255.255.0;\n\trange dynamic-bootp 192.168.17.200 192.168.17.220;\n\tdefault-lease-time 600;\n\tmax-lease-time 7200;\n}'")
                #commandExec(execMode, "echo -e $command >> /etc/dhcp/dhcpd.conf")
                #commandExec(execMode, "firewall-cmd --permanent --add-port=67/udp && firewall-cmd --reload")

                commandExec(execMode, "sed -i.bak 's%" + 'OPENHPI_UNCONFIGURED = "YES"' + "%" + '#OPENHPI_UNCONFIGURED = "YES"' + "%g' /etc/openhpi/openhpi.conf")# V
                commandExec(execMode, "sed -i 's%" + '#OPENHPI_LOG_ON_SEV = "MINOR"' + "%" + 'OPENHPI_LOG_ON_SEV = "MINOR"' + "%g' /etc/openhpi/openhpi.conf")# V
                commandExec(execMode, "systemctl daemon-reload")

            elif VERSION_DETAIL == 'v8_2':
                print("1. 수동 시작/종료 금지 등 주석 처리 - 대상: 전체 데몬")
                print("1-1. [Service] 섹션 찾아서 내용 추가 - 대상: 전체 데몬")
                cnt = 0
                file = open(LISTFILE,'rt',encoding="utf-8")
                for line in file:
                    cnt += 1
                    line = line.replace('\n','')
                    print(str(cnt) + ") APPLY : " + line)
                    commandExec(execMode, "sed -i.bak 's%RefuseManualStop=yes%#RefuseManualStop=yes%g' " + line) #
                    commandExec(execMode, "sed -i.bak 's%RefuseManualStop=true%#RefuseManualStop=true%g' " + line) #
                    commandExec(execMode, "sed -i.bak 's%RefuseManualStart=yes%#RefuseManualStart=yes%g' " + line) #
                    commandExec(execMode, "sed -i.bak 's%RefuseManualStart=true%#RefuseManualStart=true%g' " + line)  #
                    commandExec(execMode, "sed -i.bak 's%RemainAfterExit=no%#RemainAfterExit=no%g' " + line) #
                    commandExec(execMode, "sed -i.bak 's%ConditionDirectoryNotEmpty=/sys/fs/pstore%#ConditionDirectoryNotEmpty=/sys/fs/pstore%g' " + line) #
                    commandExec(execMode, "sed -i.bak 's%ConditionKernelCommandLine=debug%#ConditionKernelCommandLine=debug%g' " + line)  #
                    commandExec(execMode, "sed -i.bak 's%IgnoreOnIsolate=1%#IgnoreOnIsolate=1%g' " + line) #
                    commandExec(execMode, "sed -i.bak 's%ConditionDirectoryNotEmpty=/sys/class/iscsi_session%#ConditionDirectoryNotEmpty=/sys/class/iscsi_session%g' " + line) #
                    commandExec(execMode, "sed -i.bak 's%StopWhenUnneeded=yes%#StopWhenUnneeded=yes%g' " + line) #
                    commandExec(execMode, "sed -i.bak 's%ConditionKernelCommandLine=ostree%#ConditionKernelCommandLine=ostree%g' " + line) #
                    commandExec(execMode, "sed -i.bak 's%ConditionSecurity=!selinux%#ConditionSecurity=!selinux%g' " + line)#
                    commandExec(execMode, "sed -i.bak 's%ConditionPathExists=!/.autorelabel%#ConditionPathExists=!/.autorelabel%g' " + line)#
                    commandExec(execMode, "sed -i.bak 's%ConditionPathIsReadWrite=!/%#ConditionPathIsReadWrite=!/%g' " + line)#
                    commandExec(execMode, "sed -i.bak 's%ConditionNeedsUpdate=/var%#ConditionNeedsUpdate=/var%g' " + line)#
                    commandExec(execMode, "sed -i.bak 's%ConditionNeedsUpdate=/etc%#ConditionNeedsUpdate=/etc%g' " + line)#
                    commandExec(execMode, "sed -i.bak 's%ConditionNeedsUpdate=|/etc%#ConditionNeedsUpdate=|/etc%g' " + line)#
                    commandExec(execMode, "sed -i.bak 's%ConditionNeedsUpdate=|/var%#ConditionNeedsUpdate=|/var%g' " + line)#
                    commandExec(execMode, "sed -i.bak 's%ConditionPathIsMountPoint=/etc/machine-id%#ConditionPathIsMountPoint=/etc/machine-id%g' " + line)#
                    commandExec(execMode, "sed -i.bak 's%ConditionPathExists=!/run/ostree-booted%#ConditionPathExists=!/run/ostree-booted%g' " + line)

                    a = self.checkRemain(line)
                    if a == False: #RemainAfterExit=yes  true 가 없을때,
                        commandExec(execMode, 'sed -i.bak'' -r -e "/\[Service\]/a\RemainAfterExit=yes" ' + line)

                print("* Daemon Reload!")
                commandExec(execMode, "systemctl daemon-reload")

                print("2. 파일 생성, 이동, 권한 부여, 실행")
                commandExec(execMode, 'touch /var/crash/test')#
                commandExec(execMode, 'touch /etc/multipath.conf')#
                commandExec(execMode, 'touch /usr/lib/initrd-release')#
                commandExec(execMode, 'mkdir -p /lib/dracut/hooks/cmdline')#
                commandExec(execMode, 'touch /lib/dracut/hooks/cmdline/test')#
                commandExec(execMode, 'touch /lib/dracut/need-initqueue')# V
                commandExec(execMode, 'mkdir -p /lib/dracut/hooks/mount')#
                commandExec(execMode, 'touch /lib/dracut/hooks/mount/test')#
                commandExec(execMode, 'mkdir -p /lib/dracut/hooks/pre-mount')#
                commandExec(execMode, 'touch /lib/dracut/hooks/pre-mount/test')#
                commandExec(execMode, 'mkdir -p /lib/dracut/hooks/pre-pivot')#
                commandExec(execMode, 'touch /lib/dracut/hooks/pre-pivot/test')#
                commandExec(execMode, 'mkdir -p /lib/dracut/hooks/pre-trigger')#
                commandExec(execMode, 'touch /lib/dracut/hooks/pre-trigger/test')#
                commandExec(execMode, 'mkdir -p /lib/dracut/hooks/pre-udev')#
                commandExec(execMode, 'touch /lib/dracut/hooks/pre-udev/test')#
                commandExec(execMode, 'mv /run/initramfs/bin/sh /run/initramfs/bin/sh.bak')# V
                commandExec(execMode, 'touch /var/lib/fwupd/pending.db')#
                commandExec(execMode, 'mkdir -p /dev/vmbus')#
                commandExec(execMode, 'touch /dev/vmbus/hv_fcopy')#
                commandExec(execMode, 'mkdir -p /etc/sysconfig/modules')#
                commandExec(execMode, 'touch /etc/sysconfig/modules/test')#
                commandExec(execMode, 'touch /etc/sysconfig/ipvsadm')#
                commandExec(execMode, 'mkdir -p /var/lib/iscsi/nodes/')#
                commandExec(execMode, 'touch /var/lib/iscsi/nodes/test')#
                commandExec(execMode, 'mkdir -p /var/lib/mdcheck')#
                commandExec(execMode, 'touch /var/lib/mdcheck/MD_UUID_0')#
                commandExec(execMode, 'mkdir -p /usr/lib/mdadm/')#
                commandExec(execMode, 'touch /usr/lib/mdadm/mdadm_env.sh')#
                commandExec(execMode, 'mkdir -p /usr/share/mdadm')#
                commandExec(execMode, 'touch /usr/share/mdadm/mdcheck')#
                commandExec(execMode, 'chmod +x /usr/share/mdadm/mdcheck')
                commandExec(execMode, 'chmod +x /usr/lib/mdadm/mdadm_env.sh')
                commandExec(execMode, "echo '#!/bin/bash' > /usr/lib/mdadm/mdadm_env.sh")
                commandExec(execMode, "echo '#!/bin/bash' > /usr/share/mdadm/mdcheck")
                commandExec(execMode, "touch /etc/ethers")#
                commandExec(execMode, "touch /etc/krb5.keytab")#
                commandExec(execMode, "touch /etc/sysconfig/nfs")#
                commandExec(execMode, "touch /run/ostree-booted")#
                commandExec(execMode, "\cp /usr/share/doc/stunnel/stunnel.conf-sample /etc/stunnel/stunnel.conf")#
                commandExec(execMode, "touch /etc/initrd-release")#

                ############

                commandExec(execMode, '\mv /etc/alsa/state-daemon.conf /root/')#
                commandExec(execMode, '\mv /etc/cloud/cloud-init.disabled /etc/cloud/cloud-init.disabled.bak')#

                commandExec(execMode, "\mv /etc/ld.so.cache /etc/ld.so.cache.bak")#
                commandExec(execMode, "chmod +x /etc/rc.d/rc.local")
                commandExec(execMode, "chmod +w /sys")
                commandExec(execMode, "\mv /etc/unbound/unbound_control.key /etc/unbound/unbound_control.key.bak")#

                commandExec(execMode, "touch /etc/ctdb/nodes")#
                commandExec(execMode, 'echo "'+ HOST_IP +'" >> /etc/ctdb/nodes')

                commandExec(execMode, "touch /etc/sysconfig/ctdb")#
                commandExec(execMode, 'echo CTDB_NODES=/etc/ctdb/nodes >> /etc/sysconfig/ctdb')
                commandExec(execMode, 'echo CTDB_PUBLIC_ADDRESSES=/etc/ctdb/public_addresses >> /etc/sysconfig/ctdb')
                commandExec(execMode, 'echo CTDB_RECOVERY_LOCK="/mnt/ctdb/.ctdb.lock" >> /etc/sysconfig/ctdb')
                commandExec(execMode, 'echo CTDB_MANAGES_SAMBA=yes >> /etc/sysconfig/ctdb')
                commandExec(execMode, 'echo CTDB_MANAGES_WINBIND=yes >> /etc/sysconfig/ctdb')


                commandExec(execMode, '\mv /etc/pki/dovecot/certs/dovecot.pem /etc/pki/dovecot/certs/dovecot.pem.bak')#
                commandExec(execMode, '\mv /etc/pki/dovecot/private/dovecot.pem /etc/pki/dovecot/private/dovecot.pem.bak')#

                commandExec(execMode, '\mv /etc/pki/tls/certs/localhost.crt /etc/pki/tls/certs/localhost.crt.bak')
                commandExec(execMode, '\mv /etc/pki/tls/private/localhost.key /etc/pki/tls/private/localhost.key.bak')

                commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd.pem /etc/pki/cyrus-imapd/cyrus-imapd.pem.bak')
                commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd-key.pem /etc/pki/cyrus-imapd/cyrus-imapd-key.pem.bak')
                commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd-ca.pem /etc/pki/cyrus-imapd/cyrus-imapd-ca.pem.bak')

                commandExec(execMode, '\mv /var/lib/cloud/instance /var/lib/cloud/instance_back') ## cloud-final, cloud-config service 테스트용
                commandExec(execMode, "\cp /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd.conf.bak")
                commandExec(execMode, "/usr/bin/postgresql-setup --initdb")

                ############ pair가 아닌 조건들
                commandExec(execMode, '\mv /etc/cockpit/ws-certs.d/0-self-signed.cert /etc/cockpit/ws-certs.d/0-self-signed.cert.2') # cockpit.service 시작 실패 시 시작 조건

                commandExec(execMode, "sh /etc/openwsman/owsmangencert.sh")

                print("3. 개별 데몬 제어")
                commandExec(execMode, "systemctl start abrtd.service")
                commandExec(execMode, "systemctl start amanda-udp.socket")
                commandExec(execMode, "systemctl start named.service")
                commandExec(execMode, "systemctl start cockpit.service")
                commandExec(execMode, "systemctl stop cups.service")
                commandExec(execMode, "systemctl stop sysstat-collect.timer")
                commandExec(execMode, "systemctl start sys-kernel-config.mount")
                commandExec(execMode, "systemctl start dbus.service")
                commandExec(execMode, "systemctl start polkit.service")
                commandExec(execMode, "systemctl stop rsyslog.service")

                print("4. 개별 파일 내용 변경")
                commandExec(execMode, "sed -i.bak 's%" + 'OPENHPI_UNCONFIGURED = "YES"' + "%" + '#OPENHPI_UNCONFIGURED = "YES"' + "%g' /etc/openhpi/openhpi.conf")#
                commandExec(execMode, "sed -i 's%" + '#OPENHPI_LOG_ON_SEV = "MINOR"' + "%" + 'OPENHPI_LOG_ON_SEV = "MINOR"' + "%g' /etc/openhpi/openhpi.conf")#

                # 맥 주소, 아이피주소 입력
                output, error = commandExec(execMode, "cat /sys/class/net/e*/address")
                if output != []:
                    MAC_ADDR = output[0]
                    commandExec(execMode, "sed -i.bak 's%# SYSLOGMACADDR=%SYSLOGMACADDR=" + MAC_ADDR + "%g' /etc/sysconfig/netconsole")#
                    commandExec(execMode, "sed -i 's%# SYSLOGADDR=%SYSLOGADDR=" + HOST_IP + "%g' /etc/sysconfig/netconsole")#
                else:
                    print("* No Mac address")

                commandExec(execMode, "command='subnet 192.168.17.0 netmask 255.255.255.0 {\n\toption routers 192.168.17.1;\n\toption subnet-mask 255.255.255.0;\n\trange dynamic-bootp 192.168.17.200 192.168.17.220;\n\tdefault-lease-time 600;\n\tmax-lease-time 7200;\n}'")
                commandExec(execMode, "echo -e $command >> /etc/dhcp/dhcpd.conf")
                commandExec(execMode, "firewall-cmd --permanent --add-port=67/udp && firewall-cmd --reload")

                commandExec(execMode, "systemctl daemon-reload")

            elif VERSION_DETAIL == 'v8_3' or VERSION_DETAIL == 'v8_4':
                    print("1. 수동 시작/종료 금지 등 주석 처리 - 대상: 전체 데몬")
                    print("1-1. [Service] 섹션 찾아서 내용 추가 - 대상: 전체 데몬")
                    cnt = 0
                    file = open(LISTFILE,'rt',encoding="utf-8")
                    for line in file:
                        cnt += 1
                        line = line.replace('\n','')
                        print(str(cnt) + ") APPLY : " + line)
                        commandExec(execMode, "sed -i.bak 's%RefuseManualStop=yes%#RefuseManualStop=yes%g' " + line) #
                        commandExec(execMode, "sed -i.bak 's%RefuseManualStop=true%#RefuseManualStop=true%g' " + line) #
                        commandExec(execMode, "sed -i.bak 's%RefuseManualStart=yes%#RefuseManualStart=yes%g' " + line) #
                        commandExec(execMode, "sed -i.bak 's%RefuseManualStart=true%#RefuseManualStart=true%g' " + line)  #
                        commandExec(execMode, "sed -i.bak 's%RemainAfterExit=no%#RemainAfterExit=no%g' " + line) #
                        commandExec(execMode, "sed -i.bak 's%ConditionDirectoryNotEmpty=/sys/fs/pstore%#ConditionDirectoryNotEmpty=/sys/fs/pstore%g' " + line) #
                        commandExec(execMode, "sed -i.bak 's%ConditionKernelCommandLine=debug%#ConditionKernelCommandLine=debug%g' " + line)  #
                        commandExec(execMode, "sed -i.bak 's%IgnoreOnIsolate=1%#IgnoreOnIsolate=1%g' " + line) #
                        commandExec(execMode, "sed -i.bak 's%ConditionDirectoryNotEmpty=/sys/class/iscsi_session%#ConditionDirectoryNotEmpty=/sys/class/iscsi_session%g' " + line) #
                        commandExec(execMode, "sed -i.bak 's%StopWhenUnneeded=yes%#StopWhenUnneeded=yes%g' " + line) #
                        commandExec(execMode, "sed -i.bak 's%ConditionKernelCommandLine=ostree%#ConditionKernelCommandLine=ostree%g' " + line) #
                        commandExec(execMode, "sed -i.bak 's%ConditionSecurity=!selinux%#ConditionSecurity=!selinux%g' " + line)#
                        commandExec(execMode, "sed -i.bak 's%ConditionPathExists=!/.autorelabel%#ConditionPathExists=!/.autorelabel%g' " + line)#
                        commandExec(execMode, "sed -i.bak 's%ConditionPathIsReadWrite=!/%#ConditionPathIsReadWrite=!/%g' " + line)#
                        commandExec(execMode, "sed -i.bak 's%ConditionNeedsUpdate=/var%#ConditionNeedsUpdate=/var%g' " + line)#
                        commandExec(execMode, "sed -i.bak 's%ConditionNeedsUpdate=/etc%#ConditionNeedsUpdate=/etc%g' " + line)#
                        commandExec(execMode, "sed -i.bak 's%ConditionNeedsUpdate=|/etc%#ConditionNeedsUpdate=|/etc%g' " + line)#
                        commandExec(execMode, "sed -i.bak 's%ConditionNeedsUpdate=|/var%#ConditionNeedsUpdate=|/var%g' " + line)#
                        commandExec(execMode, "sed -i.bak 's%ConditionPathIsMountPoint=/etc/machine-id%#ConditionPathIsMountPoint=/etc/machine-id%g' " + line)#
                        commandExec(execMode, "sed -i.bak 's%ConditionPathExists=!/run/ostree-booted%#ConditionPathExists=!/run/ostree-booted%g' " + line)

                        a = self.checkRemain(line)
                        if a == False: #RemainAfterExit=yes  true 가 없을때,
                            commandExec(execMode, 'sed -i.bak'' -r -e "/\[Service\]/a\RemainAfterExit=yes" ' + line)

                    print("* Daemon Reload!")
                    commandExec(execMode, "systemctl daemon-reload")

                    print("2. 파일 생성, 이동, 권한 부여, 실행")
                    commandExec(execMode, 'touch /var/crash/test')#
                    commandExec(execMode, 'touch /etc/multipath.conf')#
                    commandExec(execMode, 'touch /usr/lib/initrd-release')#
                    commandExec(execMode, 'mkdir -p /lib/dracut/hooks/cmdline')#
                    commandExec(execMode, 'touch /lib/dracut/hooks/cmdline/test')#
                    commandExec(execMode, 'touch /lib/dracut/need-initqueue')# V
                    commandExec(execMode, 'mkdir -p /lib/dracut/hooks/mount')#
                    commandExec(execMode, 'touch /lib/dracut/hooks/mount/test')#
                    commandExec(execMode, 'mkdir -p /lib/dracut/hooks/pre-mount')#
                    commandExec(execMode, 'touch /lib/dracut/hooks/pre-mount/test')#
                    commandExec(execMode, 'mkdir -p /lib/dracut/hooks/pre-pivot')#
                    commandExec(execMode, 'touch /lib/dracut/hooks/pre-pivot/test')#
                    commandExec(execMode, 'mkdir -p /lib/dracut/hooks/pre-trigger')#
                    commandExec(execMode, 'touch /lib/dracut/hooks/pre-trigger/test')#
                    commandExec(execMode, 'mkdir -p /lib/dracut/hooks/pre-udev')#
                    commandExec(execMode, 'touch /lib/dracut/hooks/pre-udev/test')#
                    commandExec(execMode, 'mv /run/initramfs/bin/sh /run/initramfs/bin/sh.bak')# V
                    commandExec(execMode, 'touch /var/lib/fwupd/pending.db')#
                    commandExec(execMode, 'mkdir -p /dev/vmbus')#
                    commandExec(execMode, 'touch /dev/vmbus/hv_fcopy')#
                    commandExec(execMode, 'mkdir -p /etc/sysconfig/modules')#
                    commandExec(execMode, 'touch /etc/sysconfig/modules/test')#
                    commandExec(execMode, 'touch /etc/sysconfig/ipvsadm')#
                    commandExec(execMode, 'mkdir -p /var/lib/iscsi/nodes/')#
                    commandExec(execMode, 'touch /var/lib/iscsi/nodes/test')#
                    commandExec(execMode, 'mkdir -p /var/lib/mdcheck')#
                    commandExec(execMode, 'touch /var/lib/mdcheck/MD_UUID_0')#
                    commandExec(execMode, 'mkdir -p /usr/lib/mdadm/')#
                    commandExec(execMode, 'touch /usr/lib/mdadm/mdadm_env.sh')#
                    commandExec(execMode, 'mkdir -p /usr/share/mdadm')#
                    commandExec(execMode, 'touch /usr/share/mdadm/mdcheck')#
                    commandExec(execMode, 'chmod +x /usr/share/mdadm/mdcheck')
                    commandExec(execMode, 'chmod +x /usr/lib/mdadm/mdadm_env.sh')
                    commandExec(execMode, "echo '#!/bin/bash' > /usr/lib/mdadm/mdadm_env.sh")
                    commandExec(execMode, "echo '#!/bin/bash' > /usr/share/mdadm/mdcheck")
                    commandExec(execMode, "touch /etc/ethers")#
                    commandExec(execMode, "touch /etc/krb5.keytab")#
                    commandExec(execMode, "touch /etc/sysconfig/nfs")#
                    commandExec(execMode, "touch /run/ostree-booted")#
                    commandExec(execMode, "\cp /usr/share/doc/stunnel/stunnel.conf-sample /etc/stunnel/stunnel.conf")#
                    commandExec(execMode, "touch /etc/initrd-release")#

                    ############

                    commandExec(execMode, '\mv /etc/alsa/state-daemon.conf /root/')#
                    commandExec(execMode, '\mv /etc/cloud/cloud-init.disabled /etc/cloud/cloud-init.disabled.bak')#

                    commandExec(execMode, "\mv /etc/ld.so.cache /etc/ld.so.cache.bak")#
                    commandExec(execMode, "chmod +x /etc/rc.d/rc.local")
                    commandExec(execMode, "chmod +w /sys")
                    commandExec(execMode, "\mv /etc/unbound/unbound_control.key /etc/unbound/unbound_control.key.bak")#

                    commandExec(execMode, "touch /etc/ctdb/nodes")#
                    commandExec(execMode, 'echo "'+ HOST_IP +'" >> /etc/ctdb/nodes')

                    commandExec(execMode, "touch /etc/sysconfig/ctdb")#
                    commandExec(execMode, 'echo CTDB_NODES=/etc/ctdb/nodes >> /etc/sysconfig/ctdb')
                    commandExec(execMode, 'echo CTDB_PUBLIC_ADDRESSES=/etc/ctdb/public_addresses >> /etc/sysconfig/ctdb')
                    commandExec(execMode, 'echo CTDB_RECOVERY_LOCK="/mnt/ctdb/.ctdb.lock" >> /etc/sysconfig/ctdb')
                    commandExec(execMode, 'echo CTDB_MANAGES_SAMBA=yes >> /etc/sysconfig/ctdb')
                    commandExec(execMode, 'echo CTDB_MANAGES_WINBIND=yes >> /etc/sysconfig/ctdb')


                    commandExec(execMode, '\mv /etc/pki/dovecot/certs/dovecot.pem /etc/pki/dovecot/certs/dovecot.pem.bak')#
                    commandExec(execMode, '\mv /etc/pki/dovecot/private/dovecot.pem /etc/pki/dovecot/private/dovecot.pem.bak')#

                    commandExec(execMode, '\mv /etc/pki/tls/certs/localhost.crt /etc/pki/tls/certs/localhost.crt.bak')
                    commandExec(execMode, '\mv /etc/pki/tls/private/localhost.key /etc/pki/tls/private/localhost.key.bak')

                    commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd.pem /etc/pki/cyrus-imapd/cyrus-imapd.pem.bak')
                    commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd-key.pem /etc/pki/cyrus-imapd/cyrus-imapd-key.pem.bak')
                    commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd-ca.pem /etc/pki/cyrus-imapd/cyrus-imapd-ca.pem.bak')

                    commandExec(execMode, '\mv /var/lib/cloud/instance /var/lib/cloud/instance_back') ## cloud-final, cloud-config service 테스트용
                    commandExec(execMode, "\cp /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd.conf.bak")
                    commandExec(execMode, "/usr/bin/postgresql-setup --initdb")

                    ############ pair가 아닌 조건들
                    commandExec(execMode, '\mv /etc/cockpit/ws-certs.d/0-self-signed.cert /etc/cockpit/ws-certs.d/0-self-signed.cert.2') # cockpit.service 시작 실패 시 시작 조건

                    commandExec(execMode, "sh /etc/openwsman/owsmangencert.sh")

                    print("3. 개별 데몬 제어")
                    commandExec(execMode, "systemctl start abrtd.service")
                    commandExec(execMode, "systemctl start amanda-udp.socket")
                    commandExec(execMode, "systemctl start named.service")
                    commandExec(execMode, "systemctl start cockpit.service")
                    commandExec(execMode, "systemctl stop cups.service")
                    commandExec(execMode, "systemctl stop sysstat-collect.timer")
                    commandExec(execMode, "systemctl start sys-kernel-config.mount")
                    commandExec(execMode, "systemctl start dbus.service")
                    commandExec(execMode, "systemctl start polkit.service")
                    commandExec(execMode, "systemctl stop rsyslog.service")

                    print("4. 개별 파일 내용 변경")
                    commandExec(execMode, "sed -i.bak 's%" + 'OPENHPI_UNCONFIGURED = "YES"' + "%" + '#OPENHPI_UNCONFIGURED = "YES"' + "%g' /etc/openhpi/openhpi.conf")#
                    commandExec(execMode, "sed -i 's%" + '#OPENHPI_LOG_ON_SEV = "MINOR"' + "%" + 'OPENHPI_LOG_ON_SEV = "MINOR"' + "%g' /etc/openhpi/openhpi.conf")#

                    # 맥 주소, 아이피주소 입력
                    output, error = commandExec(execMode, "cat /sys/class/net/e*/address")
                    if output != []:
                        MAC_ADDR = output[0]
                        commandExec(execMode, "sed -i.bak 's%# SYSLOGMACADDR=%SYSLOGMACADDR=" + MAC_ADDR + "%g' /etc/sysconfig/netconsole")#
                        commandExec(execMode, "sed -i 's%# SYSLOGADDR=%SYSLOGADDR=" + HOST_IP + "%g' /etc/sysconfig/netconsole")#
                    else:
                        print("* No Mac address")

                    commandExec(execMode, "command='subnet 192.168.17.0 netmask 255.255.255.0 {\n\toption routers 192.168.17.1;\n\toption subnet-mask 255.255.255.0;\n\trange dynamic-bootp 192.168.17.200 192.168.17.220;\n\tdefault-lease-time 600;\n\tmax-lease-time 7200;\n}'")
                    commandExec(execMode, "echo -e $command >> /etc/dhcp/dhcpd.conf")
                    commandExec(execMode, "firewall-cmd --permanent --add-port=67/udp && firewall-cmd --reload")

                    commandExec(execMode, "systemctl daemon-reload")
                    
            elif VERSION_DETAIL == 'v8_5':
                print("1. 수동 시작/종료 금지 등 주석 처리 - 대상: 전체 데몬")
                print("1-1. [Service] 섹션 찾아서 내용 추가 - 대상: 전체 데몬")
                cnt = 0
                file = open(LISTFILE,'rt',encoding="utf-8")
                for line in file:
                    cnt += 1
                    line = line.replace('\n','')
                    print(str(cnt) + ") APPLY : " + line)
                    commandExec(execMode, "sed -i.bak 's%RefuseManualStop=yes%#RefuseManualStop=yes%g' " + line) #
                    commandExec(execMode, "sed -i.bak 's%RefuseManualStop=true%#RefuseManualStop=true%g' " + line) #
                    commandExec(execMode, "sed -i.bak 's%RefuseManualStart=yes%#RefuseManualStart=yes%g' " + line) #
                    commandExec(execMode, "sed -i.bak 's%RefuseManualStart=true%#RefuseManualStart=true%g' " + line)  #
                    commandExec(execMode, "sed -i.bak 's%RemainAfterExit=no%#RemainAfterExit=no%g' " + line) #
                    commandExec(execMode, "sed -i.bak 's%ConditionDirectoryNotEmpty=/sys/fs/pstore%#ConditionDirectoryNotEmpty=/sys/fs/pstore%g' " + line) #
                    commandExec(execMode, "sed -i.bak 's%ConditionKernelCommandLine=debug%#ConditionKernelCommandLine=debug%g' " + line)  #
                    commandExec(execMode, "sed -i.bak 's%IgnoreOnIsolate=1%#IgnoreOnIsolate=1%g' " + line) #
                    commandExec(execMode, "sed -i.bak 's%ConditionDirectoryNotEmpty=/sys/class/iscsi_session%#ConditionDirectoryNotEmpty=/sys/class/iscsi_session%g' " + line) #
                    commandExec(execMode, "sed -i.bak 's%StopWhenUnneeded=yes%#StopWhenUnneeded=yes%g' " + line) #
                    commandExec(execMode, "sed -i.bak 's%ConditionKernelCommandLine=ostree%#ConditionKernelCommandLine=ostree%g' " + line) #
                    commandExec(execMode, "sed -i.bak 's%ConditionSecurity=!selinux%#ConditionSecurity=!selinux%g' " + line)#
                    commandExec(execMode, "sed -i.bak 's%ConditionPathExists=!/.autorelabel%#ConditionPathExists=!/.autorelabel%g' " + line)#
                    commandExec(execMode, "sed -i.bak 's%ConditionPathIsReadWrite=!/%#ConditionPathIsReadWrite=!/%g' " + line)#
                    commandExec(execMode, "sed -i.bak 's%ConditionNeedsUpdate=/var%#ConditionNeedsUpdate=/var%g' " + line)#
                    commandExec(execMode, "sed -i.bak 's%ConditionNeedsUpdate=/etc%#ConditionNeedsUpdate=/etc%g' " + line)#
                    commandExec(execMode, "sed -i.bak 's%ConditionNeedsUpdate=|/etc%#ConditionNeedsUpdate=|/etc%g' " + line)#
                    commandExec(execMode, "sed -i.bak 's%ConditionNeedsUpdate=|/var%#ConditionNeedsUpdate=|/var%g' " + line)#
                    commandExec(execMode, "sed -i.bak 's%ConditionPathIsMountPoint=/etc/machine-id%#ConditionPathIsMountPoint=/etc/machine-id%g' " + line)#
                    commandExec(execMode, "sed -i.bak 's%ConditionPathExists=!/run/ostree-booted%#ConditionPathExists=!/run/ostree-booted%g' " + line)

                    a = self.checkRemain(line)
                    if a == False: #RemainAfterExit=yes  true 가 없을때,
                        commandExec(execMode, 'sed -i.bak'' -r -e "/\[Service\]/a\RemainAfterExit=yes" ' + line)

                print("* Daemon Reload!")
                commandExec(execMode, "systemctl daemon-reload")

                print("2. 파일 생성, 이동, 권한 부여, 실행")
                commandExec(execMode, 'touch /var/crash/test')#
                commandExec(execMode, 'touch /etc/multipath.conf')#
                commandExec(execMode, 'touch /usr/lib/initrd-release')#
                commandExec(execMode, 'mkdir -p /lib/dracut/hooks/cmdline')#
                commandExec(execMode, 'touch /lib/dracut/hooks/cmdline/test')#
                commandExec(execMode, 'touch /lib/dracut/need-initqueue')# V
                commandExec(execMode, 'mkdir -p /lib/dracut/hooks/mount')#
                commandExec(execMode, 'touch /lib/dracut/hooks/mount/test')#
                commandExec(execMode, 'mkdir -p /lib/dracut/hooks/pre-mount')#
                commandExec(execMode, 'touch /lib/dracut/hooks/pre-mount/test')#
                commandExec(execMode, 'mkdir -p /lib/dracut/hooks/pre-pivot')#
                commandExec(execMode, 'touch /lib/dracut/hooks/pre-pivot/test')#
                commandExec(execMode, 'mkdir -p /lib/dracut/hooks/pre-trigger')#
                commandExec(execMode, 'touch /lib/dracut/hooks/pre-trigger/test')#
                commandExec(execMode, 'mkdir -p /lib/dracut/hooks/pre-udev')#
                commandExec(execMode, 'touch /lib/dracut/hooks/pre-udev/test')#
                commandExec(execMode, 'mv /run/initramfs/bin/sh /run/initramfs/bin/sh.bak')# V
                commandExec(execMode, 'touch /var/lib/fwupd/pending.db')#
                commandExec(execMode, 'mkdir -p /dev/vmbus')#
                commandExec(execMode, 'touch /dev/vmbus/hv_fcopy')#
                commandExec(execMode, 'mkdir -p /etc/sysconfig/modules')#
                commandExec(execMode, 'touch /etc/sysconfig/modules/test')#
                commandExec(execMode, 'touch /etc/sysconfig/ipvsadm')#
                commandExec(execMode, 'mkdir -p /var/lib/iscsi/nodes/')#
                commandExec(execMode, 'touch /var/lib/iscsi/nodes/test')#
                commandExec(execMode, 'mkdir -p /var/lib/mdcheck')#
                commandExec(execMode, 'touch /var/lib/mdcheck/MD_UUID_0')#
                commandExec(execMode, 'mkdir -p /usr/lib/mdadm/')#
                commandExec(execMode, 'touch /usr/lib/mdadm/mdadm_env.sh')#
                commandExec(execMode, 'mkdir -p /usr/share/mdadm')#
                commandExec(execMode, 'touch /usr/share/mdadm/mdcheck')#
                commandExec(execMode, 'chmod +x /usr/share/mdadm/mdcheck')
                commandExec(execMode, 'chmod +x /usr/lib/mdadm/mdadm_env.sh')
                commandExec(execMode, "echo '#!/bin/bash' > /usr/lib/mdadm/mdadm_env.sh")
                commandExec(execMode, "echo '#!/bin/bash' > /usr/share/mdadm/mdcheck")
                commandExec(execMode, "touch /etc/ethers")#
                commandExec(execMode, "touch /etc/krb5.keytab")#
                commandExec(execMode, "touch /etc/sysconfig/nfs")#
                commandExec(execMode, "touch /run/ostree-booted")#
                commandExec(execMode, "\cp /usr/share/doc/stunnel/stunnel.conf-sample /etc/stunnel/stunnel.conf")#
                commandExec(execMode, "touch /etc/initrd-release")#

                ############

                commandExec(execMode, '\mv /etc/alsa/state-daemon.conf /root/')#
                commandExec(execMode, '\mv /etc/cloud/cloud-init.disabled /etc/cloud/cloud-init.disabled.bak')#

                commandExec(execMode, "\mv /etc/ld.so.cache /etc/ld.so.cache.bak")#
                commandExec(execMode, "chmod +x /etc/rc.d/rc.local")
                commandExec(execMode, "chmod +w /sys")
                commandExec(execMode, "\mv /etc/unbound/unbound_control.key /etc/unbound/unbound_control.key.bak")#

                commandExec(execMode, "touch /etc/ctdb/nodes")#
                commandExec(execMode, 'echo "'+ HOST_IP +'" >> /etc/ctdb/nodes')

                commandExec(execMode, "touch /etc/sysconfig/ctdb")#
                commandExec(execMode, 'echo CTDB_NODES=/etc/ctdb/nodes >> /etc/sysconfig/ctdb')
                commandExec(execMode, 'echo CTDB_PUBLIC_ADDRESSES=/etc/ctdb/public_addresses >> /etc/sysconfig/ctdb')
                commandExec(execMode, 'echo CTDB_RECOVERY_LOCK="/mnt/ctdb/.ctdb.lock" >> /etc/sysconfig/ctdb')
                commandExec(execMode, 'echo CTDB_MANAGES_SAMBA=yes >> /etc/sysconfig/ctdb')
                commandExec(execMode, 'echo CTDB_MANAGES_WINBIND=yes >> /etc/sysconfig/ctdb')


                commandExec(execMode, '\mv /etc/pki/dovecot/certs/dovecot.pem /etc/pki/dovecot/certs/dovecot.pem.bak')#
                commandExec(execMode, '\mv /etc/pki/dovecot/private/dovecot.pem /etc/pki/dovecot/private/dovecot.pem.bak')#

                commandExec(execMode, '\mv /etc/pki/tls/certs/localhost.crt /etc/pki/tls/certs/localhost.crt.bak')
                commandExec(execMode, '\mv /etc/pki/tls/private/localhost.key /etc/pki/tls/private/localhost.key.bak')

                commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd.pem /etc/pki/cyrus-imapd/cyrus-imapd.pem.bak')
                commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd-key.pem /etc/pki/cyrus-imapd/cyrus-imapd-key.pem.bak')
                commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd-ca.pem /etc/pki/cyrus-imapd/cyrus-imapd-ca.pem.bak')

                commandExec(execMode, '\mv /var/lib/cloud/instance /var/lib/cloud/instance_back') ## cloud-final, cloud-config service 테스트용
                commandExec(execMode, "\cp /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd.conf.bak")
                commandExec(execMode, "/usr/bin/postgresql-setup --initdb")

                ############ pair가 아닌 조건들
                commandExec(execMode, '\mv /etc/cockpit/ws-certs.d/0-self-signed.cert /etc/cockpit/ws-certs.d/0-self-signed.cert.2') # cockpit.service 시작 실패 시 시작 조건

                commandExec(execMode, "sh /etc/openwsman/owsmangencert.sh")

                print("3. 개별 데몬 제어")
                commandExec(execMode, "systemctl start abrtd.service")
                commandExec(execMode, "systemctl start amanda-udp.socket")
                commandExec(execMode, "systemctl start named.service")
                commandExec(execMode, "systemctl start cockpit.service")
                commandExec(execMode, "systemctl stop cups.service")
                commandExec(execMode, "systemctl stop sysstat-collect.timer")
                commandExec(execMode, "systemctl start sys-kernel-config.mount")
                commandExec(execMode, "systemctl start dbus.service")
                commandExec(execMode, "systemctl start polkit.service")
                commandExec(execMode, "systemctl stop rsyslog.service")

                print("4. 개별 파일 내용 변경")
                commandExec(execMode, "sed -i.bak 's%" + 'OPENHPI_UNCONFIGURED = "YES"' + "%" + '#OPENHPI_UNCONFIGURED = "YES"' + "%g' /etc/openhpi/openhpi.conf")#
                commandExec(execMode, "sed -i 's%" + '#OPENHPI_LOG_ON_SEV = "MINOR"' + "%" + 'OPENHPI_LOG_ON_SEV = "MINOR"' + "%g' /etc/openhpi/openhpi.conf")#

                # 맥 주소, 아이피주소 입력
                output, error = commandExec(execMode, "cat /sys/class/net/e*/address")
                if output != []:
                    MAC_ADDR = output[0]
                    commandExec(execMode, "sed -i.bak 's%# SYSLOGMACADDR=%SYSLOGMACADDR=" + MAC_ADDR + "%g' /etc/sysconfig/netconsole")#
                    commandExec(execMode, "sed -i 's%# SYSLOGADDR=%SYSLOGADDR=" + HOST_IP + "%g' /etc/sysconfig/netconsole")#
                else:
                    print("* No Mac address")

                commandExec(execMode, "command='subnet 192.168.17.0 netmask 255.255.255.0 {\n\toption routers 192.168.17.1;\n\toption subnet-mask 255.255.255.0;\n\trange dynamic-bootp 192.168.17.200 192.168.17.220;\n\tdefault-lease-time 600;\n\tmax-lease-time 7200;\n}'")
                commandExec(execMode, "echo -e $command >> /etc/dhcp/dhcpd.conf")
                commandExec(execMode, "firewall-cmd --permanent --add-port=67/udp && firewall-cmd --reload")

                commandExec(execMode, "systemctl daemon-reload")
                        

                print("999. 버전 공통 ")
                ## 모든 버전 공통
                status_message, error = commandExec(execMode, "systemctl status systemd-journald.service 2>&1")
                for line in status_message:
                    if self.ACTIVE in line:
                        commandExec(execMode, "systemctl stop systemd-journald.socket")
                        commandExec(execMode, "systemctl stop systemd-journald-dev-log.socket")
                        commandExec(execMode, "systemctl stop systemd-journald.service")
                        break

                status_message, error = commandExec(execMode, "systemctl status systemd-timedated.service 2>&1")
                for line in status_message:
                    if self.MASKED in line:
                        commandExec(execMode, "systemctl unmask systemd-timedated.service")
                        break

                status_message, error = commandExec(execMode, "systemctl status systemd-udevd.service 2>&1")
                for line in status_message:
                    if self.ACTIVE in line:
                        commandExec(execMode, "systemctl stop systemd-udevd-kernel.socket")
                        commandExec(execMode, "systemctl stop systemd-udevd-control.socket")
                        commandExec(execMode, "systemctl stop systemd-udevd.service")
                        break

                commandExec(execMode, INSTALL_PKG +" install -y quota")
                commandExec(execMode, INSTALL_PKG +" install -y rsyslog")

            h, m, s = secToHms(apply_start, time.time())
            print("* Pre condition Apply Running Time : %dh %dm %.2fs"%(h, m, s))

    def Restore(self, LISTFILE):


        ## 현재는 7.7이 작성되지 않기 때문에 8.1과 동일한 내용으로 적용 중
        ## 7.7 조건이 완성되면 그때 나눠서 다시 작성

        restore_start = time.time()

        if HYPERVM_TEST == 'true':
            print("* SUPERVM pre condition restore")
            if HYPERVM_VERSION == 'v4_4':
                file = open(LISTFILE,'rt',encoding="utf-8")
                cnt = 0
                print("1. .bak 파일 복구로 RemainAfterExit=yes 추가한 데몬 원상 복구")
                print("2. 주석처리한 속성 주석 해제")
                for line in file:
                    commandExec(execMode, '\mv -f ' + line + '.bak ' + line)
                    commandExec(execMode, "sed -i 's%#ConditionPathExists=/proc/xen/capabilities%ConditionPathExists=/proc/xen/capabilities%g' " + line) #

        else:
            if VERSION_DETAIL == 'v8_1':
                file = open(LISTFILE,'rt',encoding="utf-8")
                cnt = 0
                print("1. .bak 파일 복구로 Service 섹션에 추가한 내용 제거 - 대상: oneshot/forking 데몬")
                print("1-1. 수동 시작/종료 금지 등 주석 제거 - 대상: 전체 데몬")

                for line in file:
                    cnt += 1
                    line = line.replace('\n','')

                    commandExec(execMode, '\mv -f ' + line + '.bak ' + line)
                    commandExec(execMode, "sed -i 's/#RefuseManualStop=yes/RefuseManualStop=yes/g' " + line)
                    commandExec(execMode, "sed -i 's/#RefuseManualStart=yes/RefuseManualStart=yes/g' " + line)
                    commandExec(execMode, "sed -i 's/#StopWhenUnneeded=yes/StopWhenUnneeded=yes/g' " + line)
                    commandExec(execMode, "sed -i 's/#ConditionPathIsReadWrite=!\//ConditionPathIsReadWrite=!\//g' " + line)
                    commandExec(execMode, "sed -i 's/#ConditionNeedsUpdate=\/var/ConditionNeedsUpdate=\/var/g' " + line)
                    commandExec(execMode, "sed -i 's/#ConditionPathIsMountPoint=\/etc\/machine-id/ConditionPathIsMountPoint=\/etc\/machine-id/g' " + line)
                    commandExec(execMode, "sed -i 's/#ConditionNeedsUpdate=\/etc/ConditionNeedsUpdate=\/etc/g' " + line)
                    commandExec(execMode, "sed -i 's/#ConditionNeedsUpdate=|\/etc/ConditionNeedsUpdate=|\/etc/g' " + line)
                    commandExec(execMode, "sed -i 's/#ConditionNeedsUpdate=|\/var/ConditionNeedsUpdate=|\/var/g' " + line)
                    commandExec(execMode, "sed -i 's/#ConditionSecurity=!selinux/ConditionSecurity=!selinux/g' " + line)
                    commandExec(execMode, "sed -i 's/#ConditionPathExists=!\/run\/plymouth\/pid/ConditionPathExists=!\/run\/plymouth\/pid/g' " + line)
                    commandExec(execMode, "sed -i 's/#ConditionPathExists=!\/.autorelabel/ConditionPathExists=!\/.autorelabel/g' " + line)


                commandExec(execMode, "systemctl daemon-reload")

                print("2. 파일 제거")
                commandExec(execMode, "rm -rf /usr/lib/initrd-release")
                commandExec(execMode, "rm -rf /lib/dracut/need-initqueue")
                commandExec(execMode, "rm -rf /boot/grub2/grubenv.new") #지우지 않아도 되긴 함
                commandExec(execMode, "rm -rf /run/plymouth/pid")
                commandExec(execMode, "rm -rf /etc/initrd-release")
                commandExec(execMode, "rm -rf /run/user/1")

                print("3. 폴더 및 하위 파일 제거")

                commandExec(execMode, "rm -rf /lib/dracut/hooks/mount")
                commandExec(execMode, "rm -rf /lib/dracut/hooks/pre-mount/")
                commandExec(execMode, "rm -rf /lib/dracut/hooks/pre-pivot")
                commandExec(execMode, "rm -rf /lib/dracut/hooks/pre-trigger")
                commandExec(execMode, "rm -rf /lib/dracut/hooks/pre-udev")
                commandExec(execMode, "rm -rf /etc/sysconfig/modules")
                commandExec(execMode, "rm -rf /lib/module-load.d")

                print("4. 기본 권한 복구")
                commandExec(execMode, "chmod 644 /etc/rc.d/rc.local")



                commandExec(execMode, 'systemctl disable selinux-autorelabel-mark.service')
                commandExec(execMode, 'rm -rf /.autorelabel')

            elif VERSION_DETAIL == 'v7_7':

                file = open(LISTFILE,'rt',encoding="utf-8")
                cnt = 0


                print("1. .bak 파일 복구로 Service 섹션에 추가한 내용 제거 - 대상: 전체 데몬")
                print("1-1. 수동 시작/종료 금지 등 주석 제거 - 대상: 전체 데몬")

                for line in file:
                    cnt += 1
                    line = line.replace('\n','')

                    commandExec(execMode, '\mv -f ' + line + '.bak ' + line)

                    commandExec(execMode, "sed -i 's%#RefuseManualStop=yes%RefuseManualStop=yes%g' " + line)
                    commandExec(execMode, "sed -i 's%#RefuseManualStop=true%RefuseManualStop=true%g' " + line)
                    commandExec(execMode, "sed -i 's%#RefuseManualStart=yes%RefuseManualStart=yes%g' " + line)
                    commandExec(execMode, "sed -i 's%#RefuseManualStart=true%RefuseManualStart=true%g' " + line)
                    commandExec(execMode, "sed -i 's%#StopWhenUnneeded=yes%StopWhenUnneeded=yes%g' " + line)
                    commandExec(execMode, "sed -i 's%#ConditionKernelCommandLine=debug%ConditionKernelCommandLine=debug%g' " + line)
                    commandExec(execMode, "sed -i 's%#ConditionPathIsReadWrite=!/%ConditionPathIsReadWrite=!/%g' " + line)
                    commandExec(execMode, "sed -i 's%#ConditionNeedsUpdate=/etc%ConditionNeedsUpdate=/etc%g' " + line)
                    commandExec(execMode, "sed -i 's%#ConditionNeedsUpdate=|/etc%ConditionNeedsUpdate=|/etc%g' " + line)
                    commandExec(execMode, "sed -i 's%#ConditionNeedsUpdate=/var%ConditionNeedsUpdate=/var%g' " + line)
                    commandExec(execMode, "sed -i 's%#ConditionNeedsUpdate=|/var%ConditionNeedsUpdate=|/var%g' " + line)
                    commandExec(execMode, "sed -i 's%#ConditionFileNotEmpty=|!/etc/ssh/ssh_host_rsa_key%ConditionFileNotEmpty=|!/etc/ssh/ssh_host_rsa_key%g' " + line)
                    commandExec(execMode, "sed -i 's%#ConditionFileNotEmpty=|!/etc/ssh/ssh_host_ecdsa_key%ConditionFileNotEmpty=|!/etc/ssh/ssh_host_ecdsa_key%g' " + line)
                    commandExec(execMode, "sed -i 's%#ConditionFileNotEmpty=|!/etc/ssh/ssh_host_ed25519_key%ConditionFileNotEmpty=|!/etc/ssh/ssh_host_ed25519_key%g' " + line)
                    commandExec(execMode, "sed -i 's%#ConditionPathIsMountPoint=/etc/machine-id%ConditionPathIsMountPoint=/etc/machine-id%g' " + line)
                    commandExec(execMode, "sed -i 's%#ConditionSecurity=!selinux%ConditionSecurity=!selinux%g' " + line)
                    commandExec(execMode, "sed -i 's%#ConditionPathExists=!/run/plymouth/pid%ConditionPathExists=!/run/plymouth/pid%g' " + line)
                    commandExec(execMode, "sed -i 's%#ConditionPathExists=!/.autorelabel%ConditionPathExists=!/.autorelabel%g' " + line)
                    commandExec(execMode, "sed -i 's%#RemainAfterExit=no%RemainAfterExit=no%g' " + line)
                    commandExec(execMode, "sed -i 's%#ConditionVirtualization=no%ConditionVirtualization=no%g' " + line)

                    commandExec(execMode, "sed -i 's%#ConditionPathExists=!/etc/initrd-release%ConditionPathExists=!/etc/initrd-release%g' " + line)

                commandExec(execMode, "systemctl daemon-reload")
                print("2. 파일 제거 및 원위치")
                commandExec(execMode, "rm -rf /usr/lib/initrd-release")
                commandExec(execMode, "rm -rf /lib/dracut/need-initqueue")
                commandExec(execMode, "rm -rf /boot/grub2/grubenv.new") #지우지 않아도 되긴 함
                commandExec(execMode, "rm -rf /run/plymouth/pid")
                commandExec(execMode, "rm -rf /etc/initrd-release")
                commandExec(execMode, "rm -rf /run/user/1")
                #commandExec(execMode, "rm -rf /run/teamd/test.conf")
                commandExec(execMode, "rm -rf /var/log/Xorg.0.log")
                commandExec(execMode, "rm -rf /etc/multipath.conf")
                commandExec(execMode, "rm -rf /etc/ethers")
                commandExec(execMode, "rm -rf /etc/krb5.keytab")
                commandExec(execMode, "rm -rf /etc/openwsman/owsmangencert.sh")
                commandExec(execMode, "rm -rf /etc/quagga/babeld.conf")
                commandExec(execMode, "rm -rf etc/quagga/bgpd.conf")
                commandExec(execMode, "rm -rf /etc/quagga/isisd.conf")
                commandExec(execMode, "rm -rf /etc/quagga/ospf6d.conf")
                commandExec(execMode, "rm -rf /etc/quagga/ospfd.conf")
                commandExec(execMode, "rm -rf /etc/quagga/ripd.conf")
                commandExec(execMode, "rm -rf /etc/quagga/ripngd.conf")
                commandExec(execMode, "rm -rf /var/lib/mdcheck/MD_UUID_0")

                commandExec(execMode, "mv /root/cyrus-imapd.pem /etc/pki/cyrus-imapd/")
                commandExec(execMode, "mv /root/state-daemon.conf /etc/alsa/")
                commandExec(execMode, "mv /root/unbound_control.key /etc/unbound/")


                tangFiles, error = commandExec(execMode, "ls /root/ |grep .jwk")
                for tangfile in tangFiles:
                    output, error = commandExec(execMode, "rm -rf /root/"+tangfile)

                print("3. 폴더 및 하위 파일 제거")
                commandExec(execMode, "rm -rf /lib/dracut/hooks/mount")
                commandExec(execMode, "rm -rf /lib/dracut/hooks/pre-mount/")
                commandExec(execMode, "rm -rf /lib/dracut/hooks/pre-pivot")
                commandExec(execMode, "rm -rf /lib/dracut/hooks/pre-trigger")
                commandExec(execMode, "rm -rf /lib/dracut/hooks/pre-udev")
                commandExec(execMode, "rm -rf /etc/sysconfig/modules")
                commandExec(execMode, "rm -rf /lib/module-load.d")
                commandExec(execMode, "rm -rf /lib/dracut/hooks/cmdline")
                commandExec(execMode, "rm -rf /var/lib/iscsi/nodes")
                commandExec(execMode, "rm -rf /usr/lib/mdadm/")
                commandExec(execMode, "rm -rf /usr/share/mdadm")

                commandExec(execMode, "rm -rf /var/crash/a")
                commandExec(execMode, "rm -rf /run/initramfs/state/temp")
                commandExec(execMode, "rm -rf /dev/capi20")
                commandExec(execMode, "rm -rf /dev/isdn/capi20")
                commandExec(execMode, "rm -rf .readahead")
                commandExec(execMode, "rm -rf /root/initrd-release")
                commandExec(execMode, "rm -rf /root/dnssec_trigger_control.key")
                commandExec(execMode, "rm -rf /etc/sysconfig/modules/temp")


                print("4. 기본 권한 복구")
                commandExec(execMode, "chmod 644 /etc/rc.d/rc.local")

            elif VERSION_DETAIL == 'v7_8':
                file = open(LISTFILE,'rt',encoding="utf-8")
                cnt = 0

                print("1. .bak 파일 복구로 Service 섹션에 추가한 내용 제거 - 대상: 전체 데몬")
                print("1-1. 수동 시작/종료 금지 등 주석 제거 - 대상: 전체 데몬")

                for line in file:
                    cnt += 1
                    line = line.replace('\n','')
                    print(str(cnt) + ") RESTORE : " + line)
                    #commandExec(execMode, "sed -i 's%#IgnoreOnIsolate=1%IgnoreOnIsolate=1%g' " + line)#
                    #commandExec(execMode, "sed -i 's%#ConditionKernelCommandLine=ostree%ConditionKernelCommandLine=ostree%g' " + line)#
                    #commandExec(execMode, "sed -i 's%#ConditionPathExists=!/.autorelabel%ConditionPathExists=!/.autorelabel%g' " + line)#
                    #commandExec(execMode, "sed -i 's%#ConditionNeedsUpdate=/var%ConditionNeedsUpdate=/var%g' " + line)

                    commandExec(execMode, '\mv -f ' + line + '.bak ' + line) # V
                    commandExec(execMode, "sed -i 's%#ConditionKernelCommandLine=debug%ConditionKernelCommandLine=debug%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#RefuseManualStop=yes%RefuseManualStop=yes%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionSecurity=!selinux%ConditionSecurity=!selinux%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#RefuseManualStart=true%RefuseManualStart=true%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionDirectoryNotEmpty=/sys/class/iscsi_session%ConditionDirectoryNotEmpty=/sys/class/iscsi_session%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#RemainAfterExit=no%RemainAfterExit=no%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionFileNotEmpty=|!/etc/ssh/ssh_host_rsa_key%ConditionFileNotEmpty=|!/etc/ssh/ssh_host_rsa_key%g' " + line)
                    commandExec(execMode, "sed -i 's%#ConditionFileNotEmpty=|!/etc/ssh/ssh_host_ecdsa_key%ConditionFileNotEmpty=|!/etc/ssh/ssh_host_ecdsa_key%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionFileNotEmpty=|!/etc/ssh/ssh_host_ed25519_key%ConditionFileNotEmpty=|!/etc/ssh/ssh_host_ed25519_key%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionPathExists=!/run/ostree-booted%ConditionPathExists=!/run/ostree-booted%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#StopWhenUnneeded=yes%StopWhenUnneeded=yes%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#RefuseManualStop=true%RefuseManualStop=true%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionPathIsReadWrite=!/%ConditionPathIsReadWrite=!/%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionNeedsUpdate=|/etc%ConditionNeedsUpdate=|/etc%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionNeedsUpdate=/etc%ConditionNeedsUpdate=/etc%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionPathIsMountPoint=/etc/machine-id%ConditionPathIsMountPoint=/etc/machine-id%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionCapability=CAP_SYS_MODULE%ConditionCapability=CAP_SYS_MODULE%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionDirectoryNotEmpty=|/lib/modules-load.d%ConditionDirectoryNotEmpty=|/lib/modules-load.d%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionDirectoryNotEmpty=|/usr/lib/modules-load.d%ConditionDirectoryNotEmpty=|/usr/lib/modules-load.d%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionDirectoryNotEmpty=|/usr/local/lib/modules-load.d%ConditionDirectoryNotEmpty=|/usr/local/lib/modules-load.d%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionDirectoryNotEmpty=|/etc/modules-load.d%ConditionDirectoryNotEmpty=|/etc/modules-load.d%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionDirectoryNotEmpty=|/run/modules-load.d%ConditionDirectoryNotEmpty=|/run/modules-load.d%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionKernelCommandLine=|modules-load%ConditionKernelCommandLine=|modules-load%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionKernelCommandLine=|rd.modules-load%ConditionKernelCommandLine=|rd.modules-load%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionVirtualization=no%ConditionVirtualization=no%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionNeedsUpdate=|/var%ConditionNeedsUpdate=|/var%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#RefuseManualStart=yes%RefuseManualStart=yes%g' " + line)# V

                    # 조건 6 (조건 1, 3 조합)
                    commandExec(execMode, "sed -i 's%#ConditionDirectoryNotEmpty=/sys/fs/pstore%ConditionDirectoryNotEmpty=/sys/fs/pstore%g' " + line)# ㅍ

                commandExec(execMode, "systemctl daemon-reload")

                print("2. 파일 제거 및 원위치, 권한 복구")
                ############
                #commandExec(execMode, 'rm -rf /var/crash/test')#
                #commandExec(execMode, 'rm -rf /var/lib/fwupd/pending.db')#
                #commandExec(execMode, 'rm -rf /dev/vmbus')#
                #commandExec(execMode, "rm -rf /etc/sysconfig/nfs")#
                #commandExec(execMode, "rm -rf /run/ostree-booted")#
                #commandExec(execMode, "rm -rf /etc/stunnel/stunnel.conf")#
                ############
                #commandExec(execMode, '\mv /etc/cloud/cloud-init.disabled.bak /etc/cloud/cloud-init.disabled')#
                #commandExec(execMode, "\mv /etc/ld.so.cache.bak /etc/ld.so.cache")#
                #commandExec(execMode, "rm -rf /etc/sysconfig/ctdb")#
                #commandExec(execMode, '\mv /etc/pki/dovecot/certs/dovecot.pem.bak /etc/pki/dovecot/certs/dovecot.pem')#
                #commandExec(execMode, '\mv /etc/pki/dovecot/private/dovecot.pem.bak /etc/pki/dovecot/private/dovecot.pem')#
                #commandExec(execMode, '\mv /etc/pki/tls/certs/localhost.crt.bak /etc/pki/tls/certs/localhost.crt')
                #commandExec(execMode, '\mv /etc/pki/tls/private/localhost.key.bak /etc/pki/tls/private/localhost.key')
                #commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd.pem.bak /etc/pki/cyrus-imapd/cyrus-imapd.pem')
                #commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd-key.pem.bak /etc/pki/cyrus-imapd/cyrus-imapd-key.pem')
                #commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd-ca.pem.bak /etc/pki/cyrus-imapd/cyrus-imapd-ca.pem')
                #commandExec(execMode, '\mv /var/lib/cloud/instance_back /var/lib/cloud/instance') ## cloud-final, cloud-config service 테스트용
                #commandExec(execMode, "\mv /etc/dhcp/dhcpd.conf.bak /etc/dhcp/dhcpd.conf")

                commandExec(execMode, '\mv /root/state-daemon.conf /etc/alsa/')# V
                commandExec(execMode, 'rm -rf /etc/multipath.conf')# V
                commandExec(execMode, "rm -rf /etc/initrd-release")# V
                commandExec(execMode, 'rm -rf /usr/lib/initrd-release')# V
                commandExec(execMode, 'rm -rf /lib/dracut/hooks/cmdline')# V
                commandExec(execMode, 'rm -rf /lib/dracut/hooks/mount')# V
                commandExec(execMode, 'rm -rf /lib/dracut/hooks/pre-mount')# V
                commandExec(execMode, 'rm -rf /lib/dracut/hooks/pre-pivot')# V
                commandExec(execMode, 'rm -rf /lib/dracut/hooks/pre-trigger')# V
                commandExec(execMode, 'rm -rf /lib/dracut/hooks/pre-udev')# V
                commandExec(execMode, 'rm -rf /etc/sysconfig/modules')# V
                commandExec(execMode, 'rm -rf /etc/rc.modules')# V
                commandExec(execMode, 'rm -rf /etc/sysconfig/ipvsadm')# V
                commandExec(execMode, 'rm -rf /var/lib/iscsi/nodes/')# V
                commandExec(execMode, "rm -rf /etc/ctdb/nodes")# V
                commandExec(execMode, "rm -rf /etc/ethers")# V
                commandExec(execMode, "rm -rf /etc/krb5.keytab")# V
                commandExec(execMode, "rm -rf /var/lib/pgsql/data/*")# V
                commandExec(execMode, "rm -rf /etc/quagga/babeld.conf")# V
                commandExec(execMode, "rm -rf /etc/quagga/bgpd.conf")# V
                commandExec(execMode, "rm -rf /etc/quagga/isisd.conf")# V
                commandExec(execMode, "rm -rf /etc/quagga/ospfd.conf")# V
                commandExec(execMode, "rm -rf /etc/quagga/ripd.conf")# V
                commandExec(execMode, "rm -rf /etc/quagga/ripngd.conf")# V
                commandExec(execMode, "rm -rf /var/svn")# V
                commandExec(execMode, "chmod 644 /etc/rc.d/rc.local")# V
                commandExec(execMode, "\mv /etc/unbound/unbound_control.key.bak /etc/unbound/unbound_control.key")# V

                # 조건 5 (조건 1, 2 조합)
                commandExec(execMode, 'rm -rf /var/lib/mdcheck')# V
                commandExec(execMode, 'rm -rf /usr/lib/mdadm/')# V
                commandExec(execMode, 'rm -rf /usr/share/mdadm')# V
                commandExec(execMode, "rm -rf /.readahead")# V

                # 조건 7 (조건 2, 3 조합)
                commandExec(execMode, "rm -rf /var/log/Xorg.0.log") # V

                # 조건 8 (조건 2, 999 조합)
                commandExec(execMode, "chmod -w /sys")

                ############pair가 아닌 조건들
                commandExec(execMode, "rm -rf /.autorelabel")

                print("3. 개별 데몬 제어")
                #commandExec(execMode, "systemctl stop dbus.service") # 종료하지 않아도 될 것으로 판단중
                #commandExec(execMode, "systemctl stop polkit.service") # 종료하지 않아도 될 것으로 판단중
                #commandExec(execMode, "systemctl stop named.service")
                #commandExec(execMode, "systemctl stop cockpit.service")
                #commandExec(execMode, "systemctl start cups.service")
                #commandExec(execMode, "systemctl start sysstat-collect.timer")
                #commandExec(execMode, "systemctl start sys-kernel-config.mount")

                commandExec(execMode, "systemctl stop amanda-udp.socket")

                # 조건 6 (조건 1, 3 조합), 조건 7 (조건 2, 3 조합)
                commandExec(execMode, "systemctl stop abrtd.service")

                ############pair가 아닌 조건들
                commandExec(execMode, "systemctl disable selinux-autorelabel-mark.service")

                print("4. 개별 파일 내용 복구")
                commandExec(execMode, "\mv /etc/openhpi/openhpi.conf.bak /etc/openhpi/openhpi.conf")  #
                commandExec(execMode, "\mv /etc/sysconfig/netconsole.bak /etc/sysconfig/netconsole") #

            elif VERSION_DETAIL == 'v7_9':
                file = open(LISTFILE,'rt',encoding="utf-8")
                cnt = 0

                print("1. .bak 파일 복구로 Service 섹션에 추가한 내용 제거 - 대상: 전체 데몬")
                print("1-1. 수동 시작/종료 금지 등 주석 제거 - 대상: 전체 데몬")

                for line in file:
                    cnt += 1
                    line = line.replace('\n','')
                    print(str(cnt) + ") RESTORE : " + line)
                    #commandExec(execMode, "sed -i 's%#IgnoreOnIsolate=1%IgnoreOnIsolate=1%g' " + line)#
                    #commandExec(execMode, "sed -i 's%#ConditionKernelCommandLine=ostree%ConditionKernelCommandLine=ostree%g' " + line)#
                    #commandExec(execMode, "sed -i 's%#ConditionPathExists=!/.autorelabel%ConditionPathExists=!/.autorelabel%g' " + line)#
                    #commandExec(execMode, "sed -i 's%#ConditionNeedsUpdate=/var%ConditionNeedsUpdate=/var%g' " + line)

                    commandExec(execMode, '\mv -f ' + line + '.bak ' + line) # V
                    commandExec(execMode, "sed -i 's%#ConditionKernelCommandLine=debug%ConditionKernelCommandLine=debug%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#RefuseManualStop=yes%RefuseManualStop=yes%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionSecurity=!selinux%ConditionSecurity=!selinux%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#RefuseManualStart=true%RefuseManualStart=true%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionDirectoryNotEmpty=/sys/class/iscsi_session%ConditionDirectoryNotEmpty=/sys/class/iscsi_session%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#RemainAfterExit=no%RemainAfterExit=no%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionFileNotEmpty=|!/etc/ssh/ssh_host_rsa_key%ConditionFileNotEmpty=|!/etc/ssh/ssh_host_rsa_key%g' " + line)
                    commandExec(execMode, "sed -i 's%#ConditionFileNotEmpty=|!/etc/ssh/ssh_host_ecdsa_key%ConditionFileNotEmpty=|!/etc/ssh/ssh_host_ecdsa_key%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionFileNotEmpty=|!/etc/ssh/ssh_host_ed25519_key%ConditionFileNotEmpty=|!/etc/ssh/ssh_host_ed25519_key%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionPathExists=!/run/ostree-booted%ConditionPathExists=!/run/ostree-booted%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#StopWhenUnneeded=yes%StopWhenUnneeded=yes%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#RefuseManualStop=true%RefuseManualStop=true%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionPathIsReadWrite=!/%ConditionPathIsReadWrite=!/%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionNeedsUpdate=|/etc%ConditionNeedsUpdate=|/etc%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionNeedsUpdate=/etc%ConditionNeedsUpdate=/etc%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionPathIsMountPoint=/etc/machine-id%ConditionPathIsMountPoint=/etc/machine-id%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionCapability=CAP_SYS_MODULE%ConditionCapability=CAP_SYS_MODULE%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionDirectoryNotEmpty=|/lib/modules-load.d%ConditionDirectoryNotEmpty=|/lib/modules-load.d%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionDirectoryNotEmpty=|/usr/lib/modules-load.d%ConditionDirectoryNotEmpty=|/usr/lib/modules-load.d%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionDirectoryNotEmpty=|/usr/local/lib/modules-load.d%ConditionDirectoryNotEmpty=|/usr/local/lib/modules-load.d%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionDirectoryNotEmpty=|/etc/modules-load.d%ConditionDirectoryNotEmpty=|/etc/modules-load.d%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionDirectoryNotEmpty=|/run/modules-load.d%ConditionDirectoryNotEmpty=|/run/modules-load.d%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionKernelCommandLine=|modules-load%ConditionKernelCommandLine=|modules-load%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionKernelCommandLine=|rd.modules-load%ConditionKernelCommandLine=|rd.modules-load%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionVirtualization=no%ConditionVirtualization=no%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#ConditionNeedsUpdate=|/var%ConditionNeedsUpdate=|/var%g' " + line)# V
                    commandExec(execMode, "sed -i 's%#RefuseManualStart=yes%RefuseManualStart=yes%g' " + line)# V
                    commandExec(execMode, "sed -i.bak 's%#ConditionPathIsMountPoint=/system-upgrade-root%ConditionPathIsMountPoint=/system-upgrade-root%g' " + line) # V

                    # 조건 6 (조건 1, 3 조합)
                    commandExec(execMode, "sed -i 's%#ConditionDirectoryNotEmpty=/sys/fs/pstore%ConditionDirectoryNotEmpty=/sys/fs/pstore%g' " + line)# V

                commandExec(execMode, "systemctl daemon-reload")

                print("2. 파일 제거 및 원위치, 권한 복구")
                ############
                #commandExec(execMode, 'rm -rf /var/crash/test')#
                #commandExec(execMode, 'rm -rf /var/lib/fwupd/pending.db')#
                #commandExec(execMode, 'rm -rf /dev/vmbus')#
                #commandExec(execMode, "rm -rf /etc/sysconfig/nfs")#
                #commandExec(execMode, "rm -rf /run/ostree-booted")#
                #commandExec(execMode, "rm -rf /etc/stunnel/stunnel.conf")#
                ############
                #commandExec(execMode, '\mv /etc/cloud/cloud-init.disabled.bak /etc/cloud/cloud-init.disabled')#
                #commandExec(execMode, "\mv /etc/ld.so.cache.bak /etc/ld.so.cache")#
                #commandExec(execMode, "rm -rf /etc/sysconfig/ctdb")#
                #commandExec(execMode, '\mv /etc/pki/dovecot/certs/dovecot.pem.bak /etc/pki/dovecot/certs/dovecot.pem')#
                #commandExec(execMode, '\mv /etc/pki/dovecot/private/dovecot.pem.bak /etc/pki/dovecot/private/dovecot.pem')#
                #commandExec(execMode, '\mv /etc/pki/tls/certs/localhost.crt.bak /etc/pki/tls/certs/localhost.crt')
                #commandExec(execMode, '\mv /etc/pki/tls/private/localhost.key.bak /etc/pki/tls/private/localhost.key')
                #commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd.pem.bak /etc/pki/cyrus-imapd/cyrus-imapd.pem')
                #commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd-key.pem.bak /etc/pki/cyrus-imapd/cyrus-imapd-key.pem')
                #commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd-ca.pem.bak /etc/pki/cyrus-imapd/cyrus-imapd-ca.pem')
                #commandExec(execMode, '\mv /var/lib/cloud/instance_back /var/lib/cloud/instance') ## cloud-final, cloud-config service 테스트용
                #commandExec(execMode, "\mv /etc/dhcp/dhcpd.conf.bak /etc/dhcp/dhcpd.conf")

                commandExec(execMode, '\mv /root/state-daemon.conf /etc/alsa/')# V
                commandExec(execMode, 'rm -rf /etc/multipath.conf')# V
                commandExec(execMode, "rm -rf /etc/initrd-release")# V
                commandExec(execMode, "rm -rf /lib/dracut/need-initqueue")# V
                commandExec(execMode, 'rm -rf /usr/lib/initrd-release')# V
                commandExec(execMode, 'rm -rf /lib/dracut/hooks/cmdline')# V
                commandExec(execMode, 'rm -rf /lib/dracut/hooks/mount')# V
                commandExec(execMode, 'rm -rf /lib/dracut/hooks/pre-mount')# V
                commandExec(execMode, 'rm -rf /lib/dracut/hooks/pre-pivot')# V
                commandExec(execMode, 'rm -rf /lib/dracut/hooks/pre-trigger')# V
                commandExec(execMode, 'rm -rf /lib/dracut/hooks/pre-udev')# V
                commandExec(execMode, 'rm -rf /etc/sysconfig/modules')# V
                commandExec(execMode, 'rm -rf /etc/rc.modules')# V
                commandExec(execMode, 'rm -rf /etc/sysconfig/ipvsadm')# V
                commandExec(execMode, 'rm -rf /var/lib/iscsi/nodes/')# V
                commandExec(execMode, 'rm -rf /etc/stinit.def')# V
                commandExec(execMode, "rm -rf /etc/ctdb/nodes")# V
                commandExec(execMode, "rm -rf /etc/ethers")# V
                commandExec(execMode, "rm -rf /etc/krb5.keytab")# V
                commandExec(execMode, "rm -rf /run/plymouth/pid")# V
                commandExec(execMode, "rm -rf /var/lib/pgsql/data/*")# V
                commandExec(execMode, "rm -rf /etc/quagga/babeld.conf")# V
                commandExec(execMode, "rm -rf /etc/quagga/bgpd.conf")# V
                commandExec(execMode, "rm -rf /etc/quagga/isisd.conf")# V
                commandExec(execMode, "rm -rf /etc/quagga/ospfd.conf")# V
                commandExec(execMode, "rm -rf /etc/quagga/ripd.conf")# V
                commandExec(execMode, "rm -rf /etc/quagga/ripngd.conf")# V
                commandExec(execMode, "rm -rf /run/initramfs/upgrade.conf")# V
                commandExec(execMode, "rm -rf /var/svn")# V
                commandExec(execMode, "chmod 644 /etc/rc.d/rc.local")# V
                commandExec(execMode, "\mv /etc/unbound/unbound_control.key.bak /etc/unbound/unbound_control.key")# V
                commandExec(execMode, "rm -rf /etc/sssd/sssd.conf")# V
                commandExec(execMode, "chmod 644 /etc/sssd/sssd.conf")# V

                # 조건 5 (조건 1, 2 조합)
                commandExec(execMode, 'rm -rf /usr/share/sounds/freedesktop/stereo/system-bootup.oga')# V
                commandExec(execMode, 'rm -rf /usr/share/sounds/freedesktop/stereo/system-shutdown.oga')# V
                commandExec(execMode, 'rm -rf /var/lib/mdcheck')# V
                commandExec(execMode, 'rm -rf /usr/lib/mdadm/')# V
                commandExec(execMode, 'rm -rf /usr/share/mdadm')# V
                commandExec(execMode, "rm -rf /.readahead")# V

                # 조건 7 (조건 2, 3 조합)
                commandExec(execMode, "rm -rf /var/log/Xorg.0.log") # V

                # 조건 8 (조건 2, 999 조합)
                commandExec(execMode, "chmod -w /sys")

                ############pair가 아닌 조건들
                commandExec(execMode, "rm -rf /.autorelabel")

                print("3. 개별 데몬 제어")
                #commandExec(execMode, "systemctl stop dbus.service") # 종료하지 않아도 될 것으로 판단중
                #commandExec(execMode, "systemctl stop polkit.service") # 종료하지 않아도 될 것으로 판단중
                #commandExec(execMode, "systemctl stop named.service")
                #commandExec(execMode, "systemctl stop cockpit.service")
                #commandExec(execMode, "systemctl start cups.service")
                #commandExec(execMode, "systemctl start sysstat-collect.timer")
                #commandExec(execMode, "systemctl start sys-kernel-config.mount")

                commandExec(execMode, "systemctl stop amanda-udp.socket")

                # 조건 6 (조건 1, 3 조합), 조건 7 (조건 2, 3 조합)
                commandExec(execMode, "systemctl stop abrtd.service")

                ############pair가 아닌 조건들
                commandExec(execMode, "systemctl disable rhel-autorelabel.service")

                print("4. 개별 파일 내용 복구")
                commandExec(execMode, "\mv /etc/openhpi/openhpi.conf.bak /etc/openhpi/openhpi.conf")  #
                commandExec(execMode, "\mv /etc/sysconfig/netconsole.bak /etc/sysconfig/netconsole") #

            elif VERSION_DETAIL == 'v8_2':
                file = open(LISTFILE,'rt',encoding="utf-8")
                cnt = 0

                print("1. .bak 파일 복구로 Service 섹션에 추가한 내용 제거 - 대상: 전체 데몬")
                print("1-1. 수동 시작/종료 금지 등 주석 제거 - 대상: 전체 데몬")

                for line in file:
                    cnt += 1
                    line = line.replace('\n','')
                    print(str(cnt) + ") RESTORE : " + line)
                    commandExec(execMode, '\mv -f ' + line + '.bak ' + line)

                    commandExec(execMode, "sed -i 's%#RefuseManualStop=yes%RefuseManualStop=yes%g' " + line)#
                    commandExec(execMode, "sed -i 's%#RefuseManualStop=true%RefuseManualStop=true%g' " + line)#
                    commandExec(execMode, "sed -i 's%#RefuseManualStart=yes%RefuseManualStart=yes%g' " + line)#
                    commandExec(execMode, "sed -i 's%#RefuseManualStart=true%RefuseManualStart=true%g' " + line)   #
                    commandExec(execMode, "sed -i 's%#RemainAfterExit=no%RemainAfterExit=no%g' " + line) #
                    commandExec(execMode, "sed -i 's%#ConditionDirectoryNotEmpty=/sys/fs/pstore%ConditionDirectoryNotEmpty=/sys/fs/pstore%g' " + line)#
                    commandExec(execMode, "sed -i 's%#ConditionKernelCommandLine=debug%ConditionKernelCommandLine=debug%g' " + line) #
                    commandExec(execMode, "sed -i 's%#IgnoreOnIsolate=1%IgnoreOnIsolate=1%g' " + line)#
                    commandExec(execMode, "sed -i 's%#ConditionDirectoryNotEmpty=/sys/class/iscsi_session%ConditionDirectoryNotEmpty=/sys/class/iscsi_session%g' " + line) #
                    commandExec(execMode, "sed -i 's%#StopWhenUnneeded=yes%StopWhenUnneeded=yes%g' " + line) #
                    commandExec(execMode, "sed -i 's%#ConditionKernelCommandLine=ostree%ConditionKernelCommandLine=ostree%g' " + line)#
                    commandExec(execMode, "sed -i 's%#ConditionSecurity=!selinux%ConditionSecurity=!selinux%g' " + line)#
                    commandExec(execMode, "sed -i 's%#ConditionPathExists=!/.autorelabel%ConditionPathExists=!/.autorelabel%g' " + line)#
                    commandExec(execMode, "sed -i 's%#ConditionPathIsReadWrite=!/%ConditionPathIsReadWrite=!/%g' " + line)#
                    commandExec(execMode, "sed -i 's%#ConditionNeedsUpdate=/var%ConditionNeedsUpdate=/var%g' " + line)#
                    commandExec(execMode, "sed -i 's%#ConditionNeedsUpdate=/etc%ConditionNeedsUpdate=/etc%g' " + line)#
                    commandExec(execMode, "sed -i 's%#ConditionNeedsUpdate=|/etc%ConditionNeedsUpdate=|/etc%g' " + line)#
                    commandExec(execMode, "sed -i 's%#ConditionNeedsUpdate=|/var%ConditionNeedsUpdate=|/var%g' " + line)#
                    commandExec(execMode, "sed -i 's%#ConditionPathIsMountPoint=/etc/machine-id%ConditionPathIsMountPoint=/etc/machine-id%g' " + line)#
                    commandExec(execMode, "sed -i 's%#ConditionPathExists=!/run/ostree-booted%ConditionPathExists=!/run/ostree-booted%g' " + line)#


                commandExec(execMode, "systemctl daemon-reload")

                print("2. 파일 제거 및 원위치, 권한 복구")

                ############
                commandExec(execMode, 'rm -rf /var/crash/test')#
                commandExec(execMode, 'rm -rf /etc/multipath.conf')#
                commandExec(execMode, 'rm -rf /usr/lib/initrd-release')#
                commandExec(execMode, 'rm -rf /lib/dracut/hooks/cmdline')
                commandExec(execMode, 'rm -rf /lib/dracut/need-initqueue') # V
                commandExec(execMode, 'rm -rf /lib/dracut/hooks/mount')#
                commandExec(execMode, 'rm -rf /lib/dracut/hooks/pre-mount')#
                commandExec(execMode, 'rm -rf /lib/dracut/hooks/pre-pivot')#
                commandExec(execMode, 'rm -rf /lib/dracut/hooks/pre-trigger')#
                commandExec(execMode, 'rm -rf /lib/dracut/hooks/pre-udev')#
                commandExec(execMode, 'mv /run/initramfs/bin/sh.bak /run/initramfs/bin/sh')# V
                commandExec(execMode, 'rm -rf /var/lib/fwupd/pending.db')#
                commandExec(execMode, 'rm -rf /dev/vmbus')#
                commandExec(execMode, 'rm -rf /etc/sysconfig/modules')#
                commandExec(execMode, 'rm -rf /etc/sysconfig/ipvsadm')#
                commandExec(execMode, 'rm -rf /var/lib/iscsi/nodes/')#
                commandExec(execMode, 'rm -rf /var/lib/mdcheck')#
                commandExec(execMode, 'rm -rf /usr/lib/mdadm/')#
                commandExec(execMode, 'rm -rf /usr/share/mdadm')  #
                commandExec(execMode, "rm -rf /etc/ethers")#
                commandExec(execMode, "rm -rf /etc/krb5.keytab")#
                commandExec(execMode, "rm -rf /etc/sysconfig/nfs")#
                commandExec(execMode, "rm -rf /run/ostree-booted")#
                commandExec(execMode, "rm -rf /etc/stunnel/stunnel.conf")#
                commandExec(execMode, "rm -rf /etc/initrd-release")#

                ############

                commandExec(execMode, '\mv /root/state-daemon.conf /etc/alsa/')#
                commandExec(execMode, '\mv /etc/cloud/cloud-init.disabled.bak /etc/cloud/cloud-init.disabled')#

                commandExec(execMode, "\mv /etc/ld.so.cache.bak /etc/ld.so.cache")#
                commandExec(execMode, "chmod 644 /etc/rc.d/rc.local")
                commandExec(execMode, "chmod -w /sys")
                commandExec(execMode, "\mv /etc/unbound/unbound_control.key.bak /etc/unbound/unbound_control.key")#

                commandExec(execMode, "rm -rf /etc/ctdb/nodes")#

                commandExec(execMode, "rm -rf /etc/sysconfig/ctdb")#

                commandExec(execMode, '\mv /etc/pki/dovecot/certs/dovecot.pem.bak /etc/pki/dovecot/certs/dovecot.pem')#
                commandExec(execMode, '\mv /etc/pki/dovecot/private/dovecot.pem.bak /etc/pki/dovecot/private/dovecot.pem')#

                commandExec(execMode, '\mv /etc/pki/tls/certs/localhost.crt.bak /etc/pki/tls/certs/localhost.crt')
                commandExec(execMode, '\mv /etc/pki/tls/private/localhost.key.bak /etc/pki/tls/private/localhost.key')

                commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd.pem.bak /etc/pki/cyrus-imapd/cyrus-imapd.pem')
                commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd-key.pem.bak /etc/pki/cyrus-imapd/cyrus-imapd-key.pem')
                commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd-ca.pem.bak /etc/pki/cyrus-imapd/cyrus-imapd-ca.pem')

                commandExec(execMode, '\mv /var/lib/cloud/instance_back /var/lib/cloud/instance') ## cloud-final, cloud-config service 테스트용
                commandExec(execMode, "\mv /etc/dhcp/dhcpd.conf.bak /etc/dhcp/dhcpd.conf")
                commandExec(execMode, "rm -rf /var/lib/pgsql/data/*")

                ############pair가 아닌 조건들
                commandExec(execMode, "rm -rf /.autorelabel")

                print("3. 개별 데몬 제어")
                commandExec(execMode, "systemctl stop abrtd.service")
                commandExec(execMode, "systemctl stop amanda-udp.socket")
                commandExec(execMode, "systemctl stop named.service")
                commandExec(execMode, "systemctl stop cockpit.service")
                commandExec(execMode, "systemctl start cups.service")
                commandExec(execMode, "systemctl start sysstat-collect.timer")
                commandExec(execMode, "systemctl start sys-kernel-config.mount")
                commandExec(execMode, "systemctl stop dbus.service")
                commandExec(execMode, "systemctl stop polkit.service")

                ############pair가 아닌 조건들
                commandExec(execMode, "systemctl disable selinux-autorelabel-mark.service")

                print("4. 개별 파일 내용 복구")
                commandExec(execMode, "\mv /etc/openhpi/openhpi.conf.bak /etc/openhpi/openhpi.conf")  #
                commandExec(execMode, "\mv /etc/sysconfig/netconsole.bak /etc/sysconfig/netconsole") #

            elif VERSION_DETAIL == 'v8_3' or VERSION_DETAIL == 'v8_4':
                    file = open(LISTFILE,'rt',encoding="utf-8")
                    cnt = 0

                    print("1. .bak 파일 복구로 Service 섹션에 추가한 내용 제거 - 대상: 전체 데몬")
                    print("1-1. 수동 시작/종료 금지 등 주석 제거 - 대상: 전체 데몬")

                    for line in file:
                        cnt += 1
                        line = line.replace('\n','')
                        print(str(cnt) + ") RESTORE : " + line)
                        commandExec(execMode, '\mv -f ' + line + '.bak ' + line)

                        commandExec(execMode, "sed -i 's%#RefuseManualStop=yes%RefuseManualStop=yes%g' " + line)#
                        commandExec(execMode, "sed -i 's%#RefuseManualStop=true%RefuseManualStop=true%g' " + line)#
                        commandExec(execMode, "sed -i 's%#RefuseManualStart=yes%RefuseManualStart=yes%g' " + line)#
                        commandExec(execMode, "sed -i 's%#RefuseManualStart=true%RefuseManualStart=true%g' " + line)   #
                        commandExec(execMode, "sed -i 's%#RemainAfterExit=no%RemainAfterExit=no%g' " + line) #
                        commandExec(execMode, "sed -i 's%#ConditionDirectoryNotEmpty=/sys/fs/pstore%ConditionDirectoryNotEmpty=/sys/fs/pstore%g' " + line)#
                        commandExec(execMode, "sed -i 's%#ConditionKernelCommandLine=debug%ConditionKernelCommandLine=debug%g' " + line) #
                        commandExec(execMode, "sed -i 's%#IgnoreOnIsolate=1%IgnoreOnIsolate=1%g' " + line)#
                        commandExec(execMode, "sed -i 's%#ConditionDirectoryNotEmpty=/sys/class/iscsi_session%ConditionDirectoryNotEmpty=/sys/class/iscsi_session%g' " + line) #
                        commandExec(execMode, "sed -i 's%#StopWhenUnneeded=yes%StopWhenUnneeded=yes%g' " + line) #
                        commandExec(execMode, "sed -i 's%#ConditionKernelCommandLine=ostree%ConditionKernelCommandLine=ostree%g' " + line)#
                        commandExec(execMode, "sed -i 's%#ConditionSecurity=!selinux%ConditionSecurity=!selinux%g' " + line)#
                        commandExec(execMode, "sed -i 's%#ConditionPathExists=!/.autorelabel%ConditionPathExists=!/.autorelabel%g' " + line)#
                        commandExec(execMode, "sed -i 's%#ConditionPathIsReadWrite=!/%ConditionPathIsReadWrite=!/%g' " + line)#
                        commandExec(execMode, "sed -i 's%#ConditionNeedsUpdate=/var%ConditionNeedsUpdate=/var%g' " + line)#
                        commandExec(execMode, "sed -i 's%#ConditionNeedsUpdate=/etc%ConditionNeedsUpdate=/etc%g' " + line)#
                        commandExec(execMode, "sed -i 's%#ConditionNeedsUpdate=|/etc%ConditionNeedsUpdate=|/etc%g' " + line)#
                        commandExec(execMode, "sed -i 's%#ConditionNeedsUpdate=|/var%ConditionNeedsUpdate=|/var%g' " + line)#
                        commandExec(execMode, "sed -i 's%#ConditionPathIsMountPoint=/etc/machine-id%ConditionPathIsMountPoint=/etc/machine-id%g' " + line)#
                        commandExec(execMode, "sed -i 's%#ConditionPathExists=!/run/ostree-booted%ConditionPathExists=!/run/ostree-booted%g' " + line)#


                    commandExec(execMode, "systemctl daemon-reload")

                    print("2. 파일 제거 및 원위치, 권한 복구")

                    ############
                    commandExec(execMode, 'rm -rf /var/crash/test')#
                    commandExec(execMode, 'rm -rf /etc/multipath.conf')#
                    commandExec(execMode, 'rm -rf /usr/lib/initrd-release')#
                    commandExec(execMode, 'rm -rf /lib/dracut/hooks/cmdline')
                    commandExec(execMode, 'rm -rf /lib/dracut/need-initqueue') # V
                    commandExec(execMode, 'rm -rf /lib/dracut/hooks/mount')#
                    commandExec(execMode, 'rm -rf /lib/dracut/hooks/pre-mount')#
                    commandExec(execMode, 'rm -rf /lib/dracut/hooks/pre-pivot')#
                    commandExec(execMode, 'rm -rf /lib/dracut/hooks/pre-trigger')#
                    commandExec(execMode, 'rm -rf /lib/dracut/hooks/pre-udev')#
                    commandExec(execMode, 'mv /run/initramfs/bin/sh.bak /run/initramfs/bin/sh')# V
                    commandExec(execMode, 'rm -rf /var/lib/fwupd/pending.db')#
                    commandExec(execMode, 'rm -rf /dev/vmbus')#
                    commandExec(execMode, 'rm -rf /etc/sysconfig/modules')#
                    commandExec(execMode, 'rm -rf /etc/sysconfig/ipvsadm')#
                    commandExec(execMode, 'rm -rf /var/lib/iscsi/nodes/')#
                    commandExec(execMode, 'rm -rf /var/lib/mdcheck')#
                    commandExec(execMode, 'rm -rf /usr/lib/mdadm/')#
                    commandExec(execMode, 'rm -rf /usr/share/mdadm')  #
                    commandExec(execMode, "rm -rf /etc/ethers")#
                    commandExec(execMode, "rm -rf /etc/krb5.keytab")#
                    commandExec(execMode, "rm -rf /etc/sysconfig/nfs")#
                    commandExec(execMode, "rm -rf /run/ostree-booted")#
                    commandExec(execMode, "rm -rf /etc/stunnel/stunnel.conf")#
                    commandExec(execMode, "rm -rf /etc/initrd-release")#

                    ############

                    commandExec(execMode, '\mv /root/state-daemon.conf /etc/alsa/')#
                    commandExec(execMode, '\mv /etc/cloud/cloud-init.disabled.bak /etc/cloud/cloud-init.disabled')#

                    commandExec(execMode, "\mv /etc/ld.so.cache.bak /etc/ld.so.cache")#
                    commandExec(execMode, "chmod 644 /etc/rc.d/rc.local")
                    commandExec(execMode, "chmod -w /sys")
                    commandExec(execMode, "\mv /etc/unbound/unbound_control.key.bak /etc/unbound/unbound_control.key")#

                    commandExec(execMode, "rm -rf /etc/ctdb/nodes")#

                    commandExec(execMode, "rm -rf /etc/sysconfig/ctdb")#

                    commandExec(execMode, '\mv /etc/pki/dovecot/certs/dovecot.pem.bak /etc/pki/dovecot/certs/dovecot.pem')#
                    commandExec(execMode, '\mv /etc/pki/dovecot/private/dovecot.pem.bak /etc/pki/dovecot/private/dovecot.pem')#

                    commandExec(execMode, '\mv /etc/pki/tls/certs/localhost.crt.bak /etc/pki/tls/certs/localhost.crt')
                    commandExec(execMode, '\mv /etc/pki/tls/private/localhost.key.bak /etc/pki/tls/private/localhost.key')

                    commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd.pem.bak /etc/pki/cyrus-imapd/cyrus-imapd.pem')
                    commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd-key.pem.bak /etc/pki/cyrus-imapd/cyrus-imapd-key.pem')
                    commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd-ca.pem.bak /etc/pki/cyrus-imapd/cyrus-imapd-ca.pem')

                    commandExec(execMode, '\mv /var/lib/cloud/instance_back /var/lib/cloud/instance') ## cloud-final, cloud-config service 테스트용
                    commandExec(execMode, "\mv /etc/dhcp/dhcpd.conf.bak /etc/dhcp/dhcpd.conf")
                    commandExec(execMode, "rm -rf /var/lib/pgsql/data/*")

                    ############pair가 아닌 조건들
                    commandExec(execMode, "rm -rf /.autorelabel")

                    print("3. 개별 데몬 제어")
                    commandExec(execMode, "systemctl stop abrtd.service")
                    commandExec(execMode, "systemctl stop amanda-udp.socket")
                    commandExec(execMode, "systemctl stop named.service")
                    commandExec(execMode, "systemctl stop cockpit.service")
                    commandExec(execMode, "systemctl start cups.service")
                    commandExec(execMode, "systemctl start sysstat-collect.timer")
                    commandExec(execMode, "systemctl start sys-kernel-config.mount")
                    commandExec(execMode, "systemctl stop dbus.service")
                    commandExec(execMode, "systemctl stop polkit.service")

                    ############pair가 아닌 조건들
                    commandExec(execMode, "systemctl disable selinux-autorelabel-mark.service")

                    print("4. 개별 파일 내용 복구")
                    commandExec(execMode, "\mv /etc/openhpi/openhpi.conf.bak /etc/openhpi/openhpi.conf")  #
                    commandExec(execMode, "\mv /etc/sysconfig/netconsole.bak /etc/sysconfig/netconsole") #
        
            elif VERSION_DETAIL == 'v8_5':
                    file = open(LISTFILE,'rt',encoding="utf-8")
                    cnt = 0

                    print("1. .bak 파일 복구로 Service 섹션에 추가한 내용 제거 - 대상: 전체 데몬")
                    print("1-1. 수동 시작/종료 금지 등 주석 제거 - 대상: 전체 데몬")

                    for line in file:
                        cnt += 1
                        line = line.replace('\n','')
                        print(str(cnt) + ") RESTORE : " + line)
                        commandExec(execMode, '\mv -f ' + line + '.bak ' + line)

                        commandExec(execMode, "sed -i 's%#RefuseManualStop=yes%RefuseManualStop=yes%g' " + line)#
                        commandExec(execMode, "sed -i 's%#RefuseManualStop=true%RefuseManualStop=true%g' " + line)#
                        commandExec(execMode, "sed -i 's%#RefuseManualStart=yes%RefuseManualStart=yes%g' " + line)#
                        commandExec(execMode, "sed -i 's%#RefuseManualStart=true%RefuseManualStart=true%g' " + line)   #
                        commandExec(execMode, "sed -i 's%#RemainAfterExit=no%RemainAfterExit=no%g' " + line) #
                        commandExec(execMode, "sed -i 's%#ConditionDirectoryNotEmpty=/sys/fs/pstore%ConditionDirectoryNotEmpty=/sys/fs/pstore%g' " + line)#
                        commandExec(execMode, "sed -i 's%#ConditionKernelCommandLine=debug%ConditionKernelCommandLine=debug%g' " + line) #
                        commandExec(execMode, "sed -i 's%#IgnoreOnIsolate=1%IgnoreOnIsolate=1%g' " + line)#
                        commandExec(execMode, "sed -i 's%#ConditionDirectoryNotEmpty=/sys/class/iscsi_session%ConditionDirectoryNotEmpty=/sys/class/iscsi_session%g' " + line) #
                        commandExec(execMode, "sed -i 's%#StopWhenUnneeded=yes%StopWhenUnneeded=yes%g' " + line) #
                        commandExec(execMode, "sed -i 's%#ConditionKernelCommandLine=ostree%ConditionKernelCommandLine=ostree%g' " + line)#
                        commandExec(execMode, "sed -i 's%#ConditionSecurity=!selinux%ConditionSecurity=!selinux%g' " + line)#
                        commandExec(execMode, "sed -i 's%#ConditionPathExists=!/.autorelabel%ConditionPathExists=!/.autorelabel%g' " + line)#
                        commandExec(execMode, "sed -i 's%#ConditionPathIsReadWrite=!/%ConditionPathIsReadWrite=!/%g' " + line)#
                        commandExec(execMode, "sed -i 's%#ConditionNeedsUpdate=/var%ConditionNeedsUpdate=/var%g' " + line)#
                        commandExec(execMode, "sed -i 's%#ConditionNeedsUpdate=/etc%ConditionNeedsUpdate=/etc%g' " + line)#
                        commandExec(execMode, "sed -i 's%#ConditionNeedsUpdate=|/etc%ConditionNeedsUpdate=|/etc%g' " + line)#
                        commandExec(execMode, "sed -i 's%#ConditionNeedsUpdate=|/var%ConditionNeedsUpdate=|/var%g' " + line)#
                        commandExec(execMode, "sed -i 's%#ConditionPathIsMountPoint=/etc/machine-id%ConditionPathIsMountPoint=/etc/machine-id%g' " + line)#
                        commandExec(execMode, "sed -i 's%#ConditionPathExists=!/run/ostree-booted%ConditionPathExists=!/run/ostree-booted%g' " + line)#


                    commandExec(execMode, "systemctl daemon-reload")

                    print("2. 파일 제거 및 원위치, 권한 복구")

                    ############
                    commandExec(execMode, 'rm -rf /var/crash/test')#
                    commandExec(execMode, 'rm -rf /etc/multipath.conf')#
                    commandExec(execMode, 'rm -rf /usr/lib/initrd-release')#
                    commandExec(execMode, 'rm -rf /lib/dracut/hooks/cmdline')
                    commandExec(execMode, 'rm -rf /lib/dracut/need-initqueue') # V
                    commandExec(execMode, 'rm -rf /lib/dracut/hooks/mount')#
                    commandExec(execMode, 'rm -rf /lib/dracut/hooks/pre-mount')#
                    commandExec(execMode, 'rm -rf /lib/dracut/hooks/pre-pivot')#
                    commandExec(execMode, 'rm -rf /lib/dracut/hooks/pre-trigger')#
                    commandExec(execMode, 'rm -rf /lib/dracut/hooks/pre-udev')#
                    commandExec(execMode, 'mv /run/initramfs/bin/sh.bak /run/initramfs/bin/sh')# V
                    commandExec(execMode, 'rm -rf /var/lib/fwupd/pending.db')#
                    commandExec(execMode, 'rm -rf /dev/vmbus')#
                    commandExec(execMode, 'rm -rf /etc/sysconfig/modules')#
                    commandExec(execMode, 'rm -rf /etc/sysconfig/ipvsadm')#
                    commandExec(execMode, 'rm -rf /var/lib/iscsi/nodes/')#
                    commandExec(execMode, 'rm -rf /var/lib/mdcheck')#
                    commandExec(execMode, 'rm -rf /usr/lib/mdadm/')#
                    commandExec(execMode, 'rm -rf /usr/share/mdadm')  #
                    commandExec(execMode, "rm -rf /etc/ethers")#
                    commandExec(execMode, "rm -rf /etc/krb5.keytab")#
                    commandExec(execMode, "rm -rf /etc/sysconfig/nfs")#
                    commandExec(execMode, "rm -rf /run/ostree-booted")#
                    commandExec(execMode, "rm -rf /etc/stunnel/stunnel.conf")#
                    commandExec(execMode, "rm -rf /etc/initrd-release")#

                    ############

                    commandExec(execMode, '\mv /root/state-daemon.conf /etc/alsa/')#
                    commandExec(execMode, '\mv /etc/cloud/cloud-init.disabled.bak /etc/cloud/cloud-init.disabled')#

                    commandExec(execMode, "\mv /etc/ld.so.cache.bak /etc/ld.so.cache")#
                    commandExec(execMode, "chmod 644 /etc/rc.d/rc.local")
                    commandExec(execMode, "chmod -w /sys")
                    commandExec(execMode, "\mv /etc/unbound/unbound_control.key.bak /etc/unbound/unbound_control.key")#

                    commandExec(execMode, "rm -rf /etc/ctdb/nodes")#

                    commandExec(execMode, "rm -rf /etc/sysconfig/ctdb")#

                    commandExec(execMode, '\mv /etc/pki/dovecot/certs/dovecot.pem.bak /etc/pki/dovecot/certs/dovecot.pem')#
                    commandExec(execMode, '\mv /etc/pki/dovecot/private/dovecot.pem.bak /etc/pki/dovecot/private/dovecot.pem')#

                    commandExec(execMode, '\mv /etc/pki/tls/certs/localhost.crt.bak /etc/pki/tls/certs/localhost.crt')
                    commandExec(execMode, '\mv /etc/pki/tls/private/localhost.key.bak /etc/pki/tls/private/localhost.key')

                    commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd.pem.bak /etc/pki/cyrus-imapd/cyrus-imapd.pem')
                    commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd-key.pem.bak /etc/pki/cyrus-imapd/cyrus-imapd-key.pem')
                    commandExec(execMode, '\mv /etc/pki/cyrus-imapd/cyrus-imapd-ca.pem.bak /etc/pki/cyrus-imapd/cyrus-imapd-ca.pem')

                    commandExec(execMode, '\mv /var/lib/cloud/instance_back /var/lib/cloud/instance') ## cloud-final, cloud-config service 테스트용
                    commandExec(execMode, "\mv /etc/dhcp/dhcpd.conf.bak /etc/dhcp/dhcpd.conf")
                    commandExec(execMode, "rm -rf /var/lib/pgsql/data/*")

                    ############pair가 아닌 조건들
                    commandExec(execMode, "rm -rf /.autorelabel")

                    print("3. 개별 데몬 제어")
                    commandExec(execMode, "systemctl stop abrtd.service")
                    commandExec(execMode, "systemctl stop amanda-udp.socket")
                    commandExec(execMode, "systemctl stop named.service")
                    commandExec(execMode, "systemctl stop cockpit.service")
                    commandExec(execMode, "systemctl start cups.service")
                    commandExec(execMode, "systemctl start sysstat-collect.timer")
                    commandExec(execMode, "systemctl start sys-kernel-config.mount")
                    commandExec(execMode, "systemctl stop dbus.service")
                    commandExec(execMode, "systemctl stop polkit.service")

                    ############pair가 아닌 조건들
                    commandExec(execMode, "systemctl disable selinux-autorelabel-mark.service")

                    print("4. 개별 파일 내용 복구")
                    commandExec(execMode, "\mv /etc/openhpi/openhpi.conf.bak /etc/openhpi/openhpi.conf")  #
                    commandExec(execMode, "\mv /etc/sysconfig/netconsole.bak /etc/sysconfig/netconsole") #

            print("999. 버전 공통 ")
            ## 모든 버전 공통
            commandExec(execMode, "systemctl start systemd-journald.socket")
            commandExec(execMode, "systemctl start systemd-journald-dev-log.socket")
            commandExec(execMode, "systemctl start systemd-journald.service")
            commandExec(execMode, "systemctl mask systemd-timedated.service")
            commandExec(execMode, "systemctl start systemd-udevd.service")
            commandExec(execMode, "systemctl start systemd-udevd-kernel.socket")
            commandExec(execMode, "systemctl start systemd-udevd-control.socket")
            #commandExec(execMode, INSTALL_PKG +" remove -y quota") # dependency 패키지를 삭제하는 문제로 주석 처리

        self.remainRecovery(LISTFILE)
        h, m, s = secToHms(restore_start, time.time())
        print("* Pre condition Restore Running Time : %dh %dm %.2fs"%(h, m, s))

def main():

    if DAEMON_PRE_CONDITION == 'true':  ## 단독실행 가능
        print("* Daemon Pre Condition Test")

        pre_condition_start = time.time()

        th = testHelper()

        if PROCESS_KILLER == 'true':
            ## 백그라운드에서 process killer 실행
            d1 = threading.Thread(target = th.proc_killer, args=('daemon',))
            d1.start() ## cpu saver 실행

        pc = PRE_CONDITIONS() ## pre condition 클래스 생성
        print("* Pre condition applying ...")
        ## 아직 pre_condition 세분화를 하지 않은 버전을 위해 분기를 나눔
        if VERSION_DETAIL == 'v8_4' or \
           VERSION_DETAIL == 'v8_3' or \
           VERSION_DETAIL == 'v8_2' or \
           VERSION_DETAIL == 'v7_8' or \
           VERSION_DETAIL == 'v7_9' or \
           VERSION_DETAIL == 'v8_5':
            ## 프리컨디션이 필요한 조건 총 4개를 각 파일별로 테스트하고, 각 파일별로 저장되도록 적용
            ## 999는 아직 미적용
            #DAEMON_TEST_PRE_CONDITION_FILE = PRE_CONDITION_PATH + '/daemon_for_pre_condition_999.txt' ## 999는 상황봐야함
            #pc.Apply(DAEMON_TEST_PRE_CONDITION_FILE, 999)
            if HYPERVM_TEST == 'true':
                print("* SUPERVM condition applying ...")
                pc.Apply(PRE_CONDITION_FILE_DAEMON_FILE)
                ad.daemonTest(DAEMON_FILE, DAEMON_RESULT_FILE)
                pc.Restore(PRE_CONDITION_FILE_DAEMON_FILE)
            else:
                for i in range(1,9):
                    DAEMON_TOTAL = []
                    DAEMON_TEST_PRE_CONDITION_FILE = PRE_CONDITION_PATH + '/daemon_for_pre_condition_%s.txt'%(i)
                    print("* Test File : " + DAEMON_TEST_PRE_CONDITION_FILE)
                    DAEMON_RESULT_FILE_PRE = RESULT_PATH + '/auto_%s_daemon_result_pre_%s.csv'%(VERSION_DETAIL,i)
                    try:
                        pc.Apply(DAEMON_TEST_PRE_CONDITION_FILE)  ## 테스트할 파일과 pre condition 중 어떤 부분을 테스트할지 입력받음(1,2,3,4)
                        ad.daemonTest(DAEMON_TEST_PRE_CONDITION_FILE, DAEMON_RESULT_FILE_PRE) ## 테스트할 파일과 저장 경로를 입력받음
                        pc.Restore(DAEMON_TEST_PRE_CONDITION_FILE) ## 테스트할 파일과 저장 경로를 입력받음
                    except Exception as e:
                        print("*** Daemon Pre Condition Exception : %s"%(e))
                        pass
                    numOfPFS('DAEMON PRE_%s'%(i), DAEMON_TOTAL)


        else: ## 7.6 / 7.7 / 8.1
            pc.Apply(PRE_CONDITION_FILE_DAEMON_FILE)
            ad.daemonTest(DAEMON_FILE, DAEMON_RESULT_FILE)
            pc.Restore(PRE_CONDITION_FILE_DAEMON_FILE)
        h, m, s = secToHms(pre_condition_start, time.time())


        if PROCESS_KILLER == 'true':
            d1.do_run = False

        sshd_config() ## sshd 설정도 변경

        h, m, s = secToHms(pre_condition_start, time.time())
        print("* Pre Condition Test Running Time : %dh %dm %.2fs"%(h, m, s))




if __name__ == '__main__':

    main()

    if IN_JENKINS == None and execMode != 'shell':
        execMode.close()
        #print("ssh closed")
