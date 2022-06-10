from auto.__common__.__print__ import printSquare
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from auto.__common__.__parameter__ import RESULT_PATH, VERSION_DETAIL

from manual.linux_regression.__module__ import command_exec, execMode
import manual.linux_regression.__import__ as reg

def main():
    print("Manual Daemon Test Case")
    ## 초기화 부분 ##############################
    testResult = []
    
    # 8.3 버전
    command_exec(execMode, 'systemctl start bacula-dir.service')
    command_exec(execMode, 'systemctl stop bacula-dir.service')
    test1 = reg.exec_test('bacula-dir.service', 'journalctl -b -u bacula-dir.service', 'output', 'code=exited, status=15')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start named-pkcs11.service')
    test1 = reg.exec_test('named-pkcs11.service', 'journalctl -b -u named-pkcs11.service', 'output', 'initializing DST: no PKCS#11 provider')
    testResult.append(test1)
    test1 = reg.exec_test('named-pkcs11.service', 'journalctl -b -u named-pkcs11.service', 'output', 'exiting (due to fatal error)')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start blivet.service')
    test1 = reg.exec_test('blivet.service', 'journalctl -b -u blivet.service', 'output', 'dbus.exceptions.DBusException: org.freedesktop.DBus.Error.AccessDenied: Connection ":')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start dhcrelay.service')
    test1 = reg.exec_test('dhcrelay.service', 'journalctl -b -u dhcrelay.service', 'output', 'No servers specified.')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start dhcpd6.service')
    test1 = reg.exec_test('dhcpd6.service', 'journalctl -b -u dhcpd6.service', 'output', 'ldap_gssapi_principal is not set,GSSAPI Authentication for LDAP will not be used')
    testResult.append(test1)
    test1 = reg.exec_test('dhcpd6.service', 'journalctl -b -u dhcpd6.service', 'output', 'No subnet6 declaration for')
    testResult.append(test1)
    test1 = reg.exec_test('dhcpd6.service', 'journalctl -b -u dhcpd6.service', 'output', 'Not configured to listen on any interfaces!')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start exchange-bmc-os-info.service')
    test1 = reg.exec_test('exchange-bmc-os-info.service', 'journalctl -b -u exchange-bmc-os-info.service', 'output', 'start failed with result \'dependency\'')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start ipmidetectd.service')
    test1 = reg.exec_test('ipmidetectd.service', 'journalctl -b -u ipmidetectd.service', 'output', 'ipmidetectd: No nodes configured')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start garbd.servicee')
    test1 = reg.exec_test('garbd.service', 'journalctl -b -u garbd.service', 'output', 'List of GALERA_NODES is not configured')
    testResult.append(test1)

    command_exec(execMode, 'mkdir -p /dev/vmbus/')
    command_exec(execMode, 'touch /dev/vmbus/hv_kvp')
    command_exec(execMode, 'systemctl start hypervkvpd.service')
    command_exec(execMode, 'sleep 1')
    test1 = reg.exec_test('hypervkvpd.service', 'journalctl -xe', 'output', '13 Permission denied')
    command_exec(execMode, 'rm -rf /dev/vmbus/')
    testResult.append(test1)

    command_exec(execMode, 'mkdir -p /dev/vmbus/')
    command_exec(execMode, 'touch /dev/vmbus/hv_vss')
    command_exec(execMode, 'systemctl start hypervvssd.service')
    command_exec(execMode, 'sleep 1')
    test1 = reg.exec_test('hypervvssd.service', 'journalctl -xe', 'output', '13 Permission denied')
    command_exec(execMode, 'rm -rf /dev/vmbus/')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start ibacm.service')
    test1 = reg.exec_test('ibacm.service', 'journalctl -b -u ibacm.service', 'output', 'code=exited, status=255')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start kadmin.service')
    test1 = reg.exec_test('kadmin.service', 'journalctl -b -u kadmin.service', 'output', 'Configuration file does not specify default realm while initializing, aborting')
    testResult.append(test1)

    command_exec(execMode, 'touch /var/kerberos/krb5kdc/kpropd.acl')
    command_exec(execMode, 'systemctl start kprop.service')
    command_exec(execMode, 'sleep 1')
    test1 = reg.exec_test('kprop.service', 'journalctl -xe', 'output', 'Configuration file does not specify default realm Unable to get default realm')
    command_exec(execMode, 'rm -rf /var/kerberos/krb5kdc/kpropd.acl')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start krb5kdc.service')
    test1 = reg.exec_test('krb5kdc.service', 'journalctl -b -u krb5kdc.service', 'output', 'Configuration file does not specify default realm, attempting to retrieve default realm')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start phc2sys.service')
    test1 = reg.exec_test('phc2sys.service', 'journalctl -b -u phc2sys.service', 'output', 'uds: sendto failed: No such file or directory')
    testResult.append(test1)
    command_exec(execMode, 'systemctl stop phc2sys.service')
    test1 = reg.exec_test('phc2sys.service', 'journalctl -b -u phc2sys.service', 'output', 'poll failed')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start ptp4l.service')
    test1 = reg.exec_test('ptp4l.service', 'journalctl -b -u ptp4l.service', 'output', 'failed to create a clock')
    testResult.append(test1)
    test1 = reg.exec_test('ptp4l.service', 'journalctl -xe', 'output', 'ioctl SIOCETHTOOL failed: No such device')
    testResult.append(test1)
    test1 = reg.exec_test('ptp4l.service', 'journalctl -b -u ptp4l.service', 'output', 'PTP device not specified and automatic determination is not supported. Please specify PTP device.')
    testResult.append(test1)

    command_exec(execMode, 'echo "test" > /etc/fancontrol')
    command_exec(execMode, 'systemctl start fancontrol.service')
    command_exec(execMode, 'sleep 1')
    test1 = reg.exec_test('fancontrol.service', 'journalctl -xe', 'output', 'Some mandatory settings missing, please check your config file!')
    command_exec(execMode, 'rm -rf /etc/fancontrol')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start lvmlocks.service')
    command_exec(execMode, 'systemctl stop lvmlocks.service')
    test1 = reg.exec_test('lvmlocks.service', 'journalctl -xe', 'output', ' /run/lvm/lvmlockd.socket: connect failed: No such file or directory')
    testResult.append(test1)
    test1 = reg.exec_test('lvmlocks.service', 'journalctl -xe', 'output', ' Cannot connect to lvmlockd.')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start mdmonitor-oneshot.service')
    test1 = reg.exec_test('mdmonitor-oneshot.service', 'journalctl -xe', 'output', 'No mail address or alert command - not monitoring.')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start mailman.service')
    test1 = reg.exec_test('mailman.service', 'journalctl -xe', 'output', 'Site list is missing: mailman')
    testResult.append(test1)

    command_exec(execMode, 'touch /etc/mdadm.conf')
    command_exec(execMode, 'systemctl start mdmonitor.service')
    command_exec(execMode, 'sleep 1')
    test1 = reg.exec_test('mdmonitor.service', 'journalctl -b -u mdmonitor.service', 'output', 'No mail address or alert command - not monitoring')
    command_exec(execMode, 'rm -rf /etc/mdadm.conf')
    testResult.append(test1)

    command_exec(execMode, 'touch /etc/munge/munge.key')
    command_exec(execMode, 'systemctl start munge.service')
    command_exec(execMode, 'sleep 1')
    command_exec(execMode, 'systemctl stop munge.service')
    test1 = reg.exec_test('munge.service', 'journalctl -xe', 'output', 'Keyfile is insecure: "/etc/munge/munge.key" should be owned by UID')
    command_exec(execMode, 'rm -rf /etc/munge/munge.key')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start nfs-blkmap.service')
    command_exec(execMode, 'systemctl stop nfs-blkmap.service')
    test1 = reg.exec_test('nfs-blkmap.service', 'journalctl -b -u nfs-blkmap.service', 'output', 'open pipe file /var/lib/nfs/rpc_pipefs/nfs/blocklayout failed: No such file or directory')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start nvmet.service')
    test1 = reg.exec_test('nvmet.service', 'journalctl -xe', 'output', '/sys/kernel/config/nvmet does not exist.  Giving up.')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start opafm.service')
    test1 = reg.exec_test('opafm.service', 'journalctl -b -u opafm.service', 'output', 'Invalid config detected! Coundn\'t find device for instance 0!.')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start ipmi.service')
    test1 = reg.exec_test('ipmi.service', 'journalctl -b -u ipmi.service', 'output', 'Startup failed.')
    testResult.append(test1)

    command_exec(execMode, 'touch /run/ostree-booted')
    command_exec(execMode, 'mkdir /sysroot')
    command_exec(execMode, 'systemctl start ostree-finalize-staged.service')
    command_exec(execMode, 'sleep 1')
    command_exec(execMode, 'systemctl stop ostree-finalize-staged.service')
    test1 = reg.exec_test('ostree-finalize-staged.service', 'journalctl -b -u ostree-finalize-staged.service', 'output', 'error: opendir(ostree/repo): No such file or directory')
    command_exec(execMode, 'rm -rf /run/ostree-booted /sysroot')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start pcscd.service')
    command_exec(execMode, 'systemctl stop pcscd.service')
    test1 = reg.exec_test('pcscd.service', 'journalctl -b -u pcscd.service', 'output', 'code=exited, status=1/FAILURE')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start qemu-guest-agent.service')
    test1 = reg.exec_test('qemu-guest-agent.service', 'journalctl -b -u qemu-guest-agent.service', 'output', 'start failed with result \'dependency\'')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start ras-mc-ctl.service')
    test1 = reg.exec_test('ras-mc-ctl.service', 'journalctl -b -u ras-mc-ctl.service', 'output', 'code=exited, status=1/FAILURE')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start redfish-finder.service')
    test1 = reg.exec_test('redfish-finder.service', 'journalctl -b -u redfish-finder.service', 'output', 'AttributeError: \'NoneType\' object has no attribute \'getifcname\'')
    testResult.append(test1)

    command_exec(execMode, 'touch /run/ostree-booted')
    command_exec(execMode, 'systemctl start rpm-ostree-bootstatus.service')
    command_exec(execMode, 'sleep 1')
    test1 = reg.exec_test('rpm-ostree-bootstatus.service', 'journalctl -b -u rpm-ostree-bootstatus.service', 'output', 'error: Failed to activate service \'org.projectatomic.rpmostree1\': timed out (service_start_timeout=25000ms)')
    command_exec(execMode, 'rm -rf /run/ostree-booted')
    testResult.append(test1)

    command_exec(execMode, 'mkdir /ostree')
    command_exec(execMode, 'systemctl start rpm-ostreed.service')
    command_exec(execMode, 'sleep 1')
    test1 = reg.exec_test('rpm-ostreed.service', 'journalctl -b -u rpm-ostreed.service', 'output', 'error: Couldn\'t start daemon: Error setting up sysroot: opendir(ostree/repo): No such file or directory')
    command_exec(execMode, 'rm -rf /ostree')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start rrdcached.socket')
    test1 = reg.exec_test('rrdcached.socket', 'journalctl -xe', 'output', 'Failed to create listening socket: Permission denied')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start rrdcached.socket')
    test1 = reg.exec_test('rrdcached.socket', 'journalctl -b -u rrdcached.socket', 'output', 'Failed to listen on sockets: Permission denied')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start rrdcached.socket')
    test1 = reg.exec_test('rrdcached.socket', 'journalctl -b -u rrdcached.socket', 'output', 'Failed with result \'resources\'.')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start speech-dispatcherd.service')
    test1 = reg.exec_test('speech-dispatcherd.service', 'journalctl -b -u speech-dispatcherd.service', 'output', 'Can\'t create pid file in /root/.cache/speech-dispatcher/pid/speech-dispatcher.pid, wrong permissions?')
    testResult.append(test1)

    command_exec(execMode, 'mkdir /var/lib/machines.raw')
    command_exec(execMode, 'systemctl start var-lib-machines.mount')
    command_exec(execMode, 'sleep 1')
    test1 = reg.exec_test('var-lib-machines.mount', 'journalctl -b -u var-lib-machines.mount', 'output', 'mount: /var/lib/machines: failed to setup loop device for /var/lib/machines.raw.')
    command_exec(execMode, 'rm -rf /var/lib/machines.raw')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start varnishncsa.service')
    command_exec(execMode, 'sleep 7')
    test1 = reg.exec_test('varnishncsa.service', 'journalctl -xe', 'output', 'Could not get hold of varnishd')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start ypbind.service')
    command_exec(execMode, 'sleep 3')
    test1 = reg.exec_test('ypbind.service', 'journalctl -xe', 'output', 'domain not found')
    testResult.append(test1)

    command_exec(execMode, 'systemctl start yppasswdd.service')
    test1 = reg.exec_test('yppasswdd.service', 'journalctl -xe', 'output', 'domain not found')
    testResult.append(test1)

    # 8.2 버전
    # command_exec(execMode, 'systemctl start bacula-dir.service')
    # command_exec(execMode, 'systemctl stop bacula-dir.service')
    # test1 = reg.exec_test('bacula-dir.service', 'journalctl -b -u bacula-dir.service', 'output', 'code=exited, status=15')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start named-pkcs11.service')
    # test1 = reg.exec_test('named-pkcs11.service', 'journalctl -b -u named-pkcs11.service', 'output', 'initializing DST: no PKCS#11 provider')
    # testResult.append(test1)
    # test1 = reg.exec_test('named-pkcs11.service', 'journalctl -b -u named-pkcs11.service', 'output', 'exiting (due to fatal error)')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start blivet.service')
    # test1 = reg.exec_test('blivet.service', 'journalctl -b -u blivet.service', 'output', 'dbus.exceptions.DBusException: org.freedesktop.DBus.Error.AccessDenied: Connection ":')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start dhcrelay.service')
    # test1 = reg.exec_test('dhcrelay.service', 'journalctl -b -u dhcrelay.service', 'output', 'No servers specified.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start dhcpd6.service')
    # test1 = reg.exec_test('dhcpd6.service', 'journalctl -b -u dhcpd6.service', 'output', 'ldap_gssapi_principal is not set,GSSAPI Authentication for LDAP will not be used')
    # testResult.append(test1)
    # test1 = reg.exec_test('dhcpd6.service', 'journalctl -b -u dhcpd6.service', 'output', 'No subnet6 declaration for')
    # testResult.append(test1)
    # test1 = reg.exec_test('dhcpd6.service', 'journalctl -b -u dhcpd6.service', 'output', 'Not configured to listen on any interfaces!')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start exchange-bmc-os-info.service')
    # test1 = reg.exec_test('exchange-bmc-os-info.service', 'journalctl -b -u exchange-bmc-os-info.service', 'output', 'start failed with result \'dependency\'')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start ipmidetectd.service')
    # test1 = reg.exec_test('ipmidetectd.service', 'journalctl -b -u ipmidetectd.service', 'output', 'ipmidetectd: No nodes configured')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start garbd.servicee')
    # test1 = reg.exec_test('garbd.service', 'journalctl -b -u garbd.service', 'output', 'List of GALERA_NODES is not configured')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'mkdir -p /dev/vmbus/')
    # command_exec(execMode, 'touch /dev/vmbus/hv_kvp')
    # command_exec(execMode, 'systemctl start hypervkvpd.service')
    # command_exec(execMode, 'sleep 1')
    # test1 = reg.exec_test('hypervkvpd.service', 'journalctl -xe', 'output', '13 Permission denied')
    # command_exec(execMode, 'rm -rf /dev/vmbus/')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'mkdir -p /dev/vmbus/')
    # command_exec(execMode, 'touch /dev/vmbus/hv_vss')
    # command_exec(execMode, 'systemctl start hypervvssd.service')
    # command_exec(execMode, 'sleep 1')
    # test1 = reg.exec_test('hypervvssd.service', 'journalctl -xe', 'output', '13 Permission denied')
    # command_exec(execMode, 'rm -rf /dev/vmbus/')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start ibacm.service')
    # test1 = reg.exec_test('ibacm.service', 'journalctl -b -u ibacm.service', 'output', 'code=exited, status=255')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start kadmin.service')
    # test1 = reg.exec_test('kadmin.service', 'journalctl -b -u kadmin.service', 'output', 'Configuration file does not specify default realm while initializing, aborting')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'touch /var/kerberos/krb5kdc/kpropd.acl')
    # command_exec(execMode, 'systemctl start kprop.service')
    # command_exec(execMode, 'sleep 1')
    # test1 = reg.exec_test('kprop.service', 'journalctl -xe', 'output', 'Configuration file does not specify default realm Unable to get default realm')
    # command_exec(execMode, 'rm -rf /var/kerberos/krb5kdc/kpropd.acl')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start krb5kdc.service')
    # test1 = reg.exec_test('krb5kdc.service', 'journalctl -b -u krb5kdc.service', 'output', 'Configuration file does not specify default realm, attempting to retrieve default realm')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start phc2sys.service')
    # test1 = reg.exec_test('phc2sys.service', 'journalctl -b -u phc2sys.service', 'output', 'uds: sendto failed: No such file or directory')
    # testResult.append(test1)
    # command_exec(execMode, 'systemctl stop phc2sys.service')
    # test1 = reg.exec_test('phc2sys.service', 'journalctl -b -u phc2sys.service', 'output', 'poll failed')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start ptp4l.service')
    # test1 = reg.exec_test('ptp4l.service', 'journalctl -b -u ptp4l.service', 'output', 'failed to create a clock')
    # testResult.append(test1)
    # test1 = reg.exec_test('ptp4l.service', 'journalctl -xe', 'output', 'ioctl SIOCETHTOOL failed: No such device')
    # testResult.append(test1)
    # test1 = reg.exec_test('ptp4l.service', 'journalctl -b -u ptp4l.service', 'output', 'PTP device not specified and automatic determination is not supported. Please specify PTP device.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'echo "test" > /etc/fancontrol')
    # command_exec(execMode, 'systemctl start fancontrol.service')
    # command_exec(execMode, 'sleep 1')
    # test1 = reg.exec_test('fancontrol.service', 'journalctl -xe', 'output', 'Some mandatory settings missing, please check your config file!')
    # command_exec(execMode, 'rm -rf /etc/fancontrol')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start lvmlocks.service')
    # command_exec(execMode, 'systemctl stop lvmlocks.service')
    # test1 = reg.exec_test('lvmlocks.service', 'journalctl -xe', 'output', ' /run/lvm/lvmlockd.socket: connect failed: No such file or directory')
    # testResult.append(test1)
    # test1 = reg.exec_test('lvmlocks.service', 'journalctl -xe', 'output', ' Cannot connect to lvmlockd.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start mdmonitor-oneshot.service')
    # test1 = reg.exec_test('mdmonitor-oneshot.service', 'journalctl -xe', 'output', 'No mail address or alert command - not monitoring.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start mailman.service')
    # test1 = reg.exec_test('mailman.service', 'journalctl -xe', 'output', 'Site list is missing: mailman')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'touch /etc/mdadm.conf')
    # command_exec(execMode, 'systemctl start mdmonitor.service')
    # command_exec(execMode, 'sleep 1')
    # test1 = reg.exec_test('mdmonitor.service', 'journalctl -b -u mdmonitor.service', 'output', 'No mail address or alert command - not monitoring')
    # command_exec(execMode, 'rm -rf /etc/mdadm.conf')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'touch /etc/munge/munge.key')
    # command_exec(execMode, 'systemctl start munge.service')
    # command_exec(execMode, 'sleep 1')
    # command_exec(execMode, 'systemctl stop munge.service')
    # test1 = reg.exec_test('munge.service', 'journalctl -xe', 'output', 'Keyfile is insecure: "/etc/munge/munge.key" should be owned by UID')
    # command_exec(execMode, 'rm -rf /etc/munge/munge.key')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start nfs-blkmap.service')
    # command_exec(execMode, 'systemctl stop nfs-blkmap.service')
    # test1 = reg.exec_test('nfs-blkmap.service', 'journalctl -b -u nfs-blkmap.service', 'output', 'open pipe file /var/lib/nfs/rpc_pipefs/nfs/blocklayout failed: No such file or directory')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start nvmet.service')
    # test1 = reg.exec_test('nvmet.service', 'journalctl -xe', 'output', '/sys/kernel/config/nvmet does not exist.  Giving up.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start opafm.service')
    # test1 = reg.exec_test('opafm.service', 'journalctl -b -u opafm.service', 'output', 'Invalid config detected! Coundn\'t find device for instance 0!.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start ipmi.service')
    # test1 = reg.exec_test('ipmi.service', 'journalctl -b -u ipmi.service', 'output', 'Startup failed.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'touch /run/ostree-booted')
    # command_exec(execMode, 'mkdir /sysroot')
    # command_exec(execMode, 'systemctl start ostree-finalize-staged.service')
    # command_exec(execMode, 'sleep 1')
    # command_exec(execMode, 'systemctl stop ostree-finalize-staged.service')
    # test1 = reg.exec_test('ostree-finalize-staged.service', 'journalctl -b -u ostree-finalize-staged.service', 'output', 'error: opendir(ostree/repo): No such file or directory')
    # command_exec(execMode, 'rm -rf /run/ostree-booted /sysroot')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start pcscd.service')
    # command_exec(execMode, 'systemctl stop pcscd.service')
    # test1 = reg.exec_test('pcscd.service', 'journalctl -b -u pcscd.service', 'output', 'code=exited, status=1/FAILURE')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start qemu-guest-agent.service')
    # test1 = reg.exec_test('qemu-guest-agent.service', 'journalctl -b -u qemu-guest-agent.service', 'output', 'start failed with result \'dependency\'')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start ras-mc-ctl.service')
    # test1 = reg.exec_test('ras-mc-ctl.service', 'journalctl -b -u ras-mc-ctl.service', 'output', 'code=exited, status=1/FAILURE')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start redfish-finder.service')
    # test1 = reg.exec_test('redfish-finder.service', 'journalctl -b -u redfish-finder.service', 'output', 'AttributeError: \'NoneType\' object has no attribute \'getifcname\'')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'touch /run/ostree-booted')
    # command_exec(execMode, 'systemctl start rpm-ostree-bootstatus.service')
    # command_exec(execMode, 'sleep 1')
    # test1 = reg.exec_test('rpm-ostree-bootstatus.service', 'journalctl -b -u rpm-ostree-bootstatus.service', 'output', 'error: Failed to activate service \'org.projectatomic.rpmostree1\': timed out (service_start_timeout=25000ms)')
    # command_exec(execMode, 'rm -rf /run/ostree-booted')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'mkdir /ostree')
    # command_exec(execMode, 'systemctl start rpm-ostreed.service')
    # command_exec(execMode, 'sleep 1')
    # test1 = reg.exec_test('rpm-ostreed.service', 'journalctl -b -u rpm-ostreed.service', 'output', 'error: Couldn\'t start daemon: Error setting up sysroot: opendir(ostree/repo): No such file or directory')
    # command_exec(execMode, 'rm -rf /ostree')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start rrdcached.socket')
    # test1 = reg.exec_test('rrdcached.socket', 'journalctl -xe', 'output', 'Failed to create listening socket: Permission denied')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start rrdcached.socket')
    # test1 = reg.exec_test('rrdcached.socket', 'journalctl -b -u rrdcached.socket', 'output', 'Failed to listen on sockets: Permission denied')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start rrdcached.socket')
    # test1 = reg.exec_test('rrdcached.socket', 'journalctl -b -u rrdcached.socket', 'output', 'Failed with result \'resources\'.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start speech-dispatcherd.service')
    # test1 = reg.exec_test('speech-dispatcherd.service', 'journalctl -b -u speech-dispatcherd.service', 'output', 'Can\'t create pid file in /root/.cache/speech-dispatcher/pid/speech-dispatcher.pid, wrong permissions?')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'mkdir /var/lib/machines.raw')
    # command_exec(execMode, 'systemctl start var-lib-machines.mount')
    # command_exec(execMode, 'sleep 1')
    # test1 = reg.exec_test('var-lib-machines.mount', 'journalctl -b -u var-lib-machines.mount', 'output', 'mount: /var/lib/machines: failed to setup loop device for /var/lib/machines.raw.')
    # command_exec(execMode, 'rm -rf /var/lib/machines.raw')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start varnishncsa.service')
    # command_exec(execMode, 'sleep 7')
    # test1 = reg.exec_test('varnishncsa.service', 'journalctl -xe', 'output', 'Could not get hold of varnishd')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start ypbind.service')
    # command_exec(execMode, 'sleep 3')
    # test1 = reg.exec_test('ypbind.service', 'journalctl -xe', 'output', 'domain not found')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start yppasswdd.service')
    # test1 = reg.exec_test('yppasswdd.service', 'journalctl -xe', 'output', 'domain not found')
    # testResult.append(test1)

    ##############################################################################################################################################

    # 7.8 버전
    # command_exec(execMode, 'systemctl start bacula-fd.service')
    # command_exec(execMode, 'systemctl stop bacula-fd.service')
    # test1 = reg.exec_test('bacula-fd.service', 'journalctl -xe', 'output', 'code=exited, status=15/n/a')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start named-pkcs11.service')
    # test1 = reg.exec_test('named-pkcs11.service', 'journalctl -xe', 'output', 'initializing DST: PKCS#11 initialization failed') # initializing DST: PKCS#11 initialization failed, RHEL과 비교 필요
    # testResult.append(test1)
    # test1 = reg.exec_test('named-pkcs11.service', 'journalctl -xe', 'output', 'exiting (due to fatal error)')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start blivet.service')
    # test1 = reg.exec_test('blivet.service', 'journalctl -b -u blivet.service', 'output', 'dbus.exceptions.DBusException: org.freedesktop.DBus.Error.AccessDenied: Connection ":')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start rbdmap.service')
    # test1 = reg.exec_test('rbdmap.service', 'journalctl -b -u rbdmap.service', 'output', 'Failed to start Map RBD devices.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start conman.service')
    # test1 = reg.exec_test('conman.service', 'journalctl -b -u conman.service', 'output', 'code=exited status=1')
    # testResult.append(test1)
    # test1 = reg.exec_test('conman.service', 'journalctl -b -u conman.service', 'output', 'Configuration "/etc/conman.conf" has no consoles defined')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start dhcpd6.service')
    # test1 = reg.exec_test('dhcpd6.service', 'journalctl -b -u dhcpd6.service', 'output', 'Not searching LDAP since ldap-server, ldap-port and ldap-base-dn were not specified in the config file') # Not searching LDAP since ldap-server, ldap-port and ldap-base-dn were not specified in the config file, RHEL과 비교 필요
    # testResult.append(test1)
    # test1 = reg.exec_test('dhcpd6.service', 'journalctl -b -u dhcpd6.service', 'output', 'No subnet6 declaration for')
    # testResult.append(test1)
    # test1 = reg.exec_test('dhcpd6.service', 'journalctl -xe', 'output', 'Not configured to listen on any interfaces!')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start dhcrelay.service')
    # test1 = reg.exec_test('dhcrelay.service', 'journalctl -b -u dhcrelay.service', 'output', 'No servers specified.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start edac.service')
    # test1 = reg.exec_test('edac.service', 'journalctl -b -u edac.service', 'output', 'No dimm labels for')
    # testResult.append(test1)
    # command_exec(execMode, 'systemctl stop edac.service')
    # test1 = reg.exec_test('edac.service', 'journalctl -b -u edac.service', 'output', 'code=exited status=1')
    # testResult.append(test1)
    # test1 = reg.exec_test('edac.service', 'journalctl -b -u edac.service', 'output', 'Unknown option: unload')
    # testResult.append(test1)

    # command_exec(execMode, 'systemctl start bmc-watchdog.service')
    # command_exec(execMode, 'systemctl stop bmc-watchdog.service')
    # test1 = reg.exec_test('bmc-watchdog.service', 'journalctl -xe', 'output', 'Get Watchdog Timer: driver timeout')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start ipmidetectd.service')
    # test1 = reg.exec_test('ipmidetectd.service', 'journalctl -b -u ipmidetectd.service', 'output', 'ipmidetectd: No nodes configured')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start hwloc-dump-hwdata.service')
    # test1 = reg.exec_test('hwloc-dump-hwdata.service', 'journalctl -xe', 'output', "Couldn't find any KNL information.")
    # testResult.append(test1)
    #
    # command_exec(execMode, 'mkdir -p /dev/vmbus/')
    # command_exec(execMode, 'touch /dev/vmbus/hv_kvp')
    # command_exec(execMode, 'systemctl start hypervkvpd.service')
    # command_exec(execMode, 'sleep 1')
    # test1 = reg.exec_test('hypervkvpd.service', 'journalctl -xe', 'output', '13 Permission denied')
    # command_exec(execMode, 'rm -rf /dev/vmbus/')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'mkdir -p /dev/vmbus/')
    # command_exec(execMode, 'touch /dev/vmbus/hv_vss')
    # command_exec(execMode, 'systemctl start hypervvssd.service')
    # command_exec(execMode, 'sleep 1')
    # test1 = reg.exec_test('hypervvssd.service', 'journalctl -xe', 'output', '13 Permission denied')
    # command_exec(execMode, 'rm -rf /dev/vmbus/')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start ibacm.service')
    # test1 = reg.exec_test('ibacm.service', 'journalctl -b -u ibacm.service', 'output', 'code=exited, status=255')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start ipa.service')
    # test1 = reg.exec_test('ipa.service', 'journalctl -b -u ipa.service', 'output', 'code=exited, status=6')
    # testResult.append(test1)
    # test1 = reg.exec_test('ipa.service', 'journalctl -b -u ipa.service', 'output', 'IPA is not configured')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'touch /dev/ipmi0')
    # command_exec(execMode, 'systemctl start ipmievd.service')
    # test1 = reg.exec_test('ipmievd.service', 'journalctl -xe', 'output', 'Could not open device at /dev/ipmi0 or /dev/ipmi/0 or /dev/ipmidev/0: No such file or directory')
    # testResult.append(test1)
    # command_exec(execMode, 'rm -rf /dev/ipmi0')
    #
    # command_exec(execMode, 'systemctl start capi.service')
    # test1 = reg.exec_test('capi.service', 'journalctl -b -u capi.service', 'output', 'cannot open /dev/capi20 nor /dev/isdn/capi20 - No such file or directory (2)')
    # testResult.append(test1)
    #
    # test1 = reg.exec_test('isdn.service', 'systemctl start isdn.service', 'output', 'Failed to start isdn.service: Unit not found.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start isnsd.service')
    # test1 = reg.exec_test('isnsd.service', 'journalctl -b -u isnsd.service', 'output', 'code=exited, status=1/FAILURE')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start kadmin.service')
    # test1 = reg.exec_test('kadmin.service', 'journalctl -b -u kadmin.service', 'output', 'Configuration file does not specify default realm while initializing, aborting')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'touch /var/kerberos/krb5kdc/kpropd.acl')
    # command_exec(execMode, 'systemctl start kprop.service')
    # command_exec(execMode, 'sleep 1')
    # test1 = reg.exec_test('kprop.service', 'journalctl -xe', 'output', 'Configuration file does not specify default realm Unable to get default realm')
    # command_exec(execMode, 'rm -rf /var/kerberos/krb5kdc/kpropd.acl')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start krb5kdc.service')
    # test1 = reg.exec_test('krb5kdc.service', 'journalctl -b -u krb5kdc.service', 'output', 'Configuration file does not specify default realm, attempting to retrieve default realm')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start phc2sys.service')
    # test1 = reg.exec_test('phc2sys.service', 'journalctl -b -u phc2sys.service', 'output', 'uds: sendto failed: No such file or directory')
    # testResult.append(test1)
    # command_exec(execMode, 'systemctl stop phc2sys.service')
    # test1 = reg.exec_test('phc2sys.service', 'journalctl -xe', 'output', 'poll failed')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start ptp4l.service')
    # test1 = reg.exec_test('ptp4l.service', 'journalctl -b -u ptp4l.service', 'output', 'failed to create a clock')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'echo "test" > /etc/fancontrol')
    # command_exec(execMode, 'systemctl start fancontrol.service')
    # command_exec(execMode, 'sleep 1')
    # test1 = reg.exec_test('fancontrol.service', 'journalctl -xe', 'output', 'Some mandatory settings missing, please check your config file!')
    # command_exec(execMode, 'rm -rf /etc/fancontrol')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start mailman.service')
    # test1 = reg.exec_test('mailman.service', 'journalctl -xe', 'output', 'Site list is missing: mailman')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start mdcheck_start.timer')
    # test1 = reg.exec_test('mdcheck_start.timer', 'journalctl -xe', 'output', 'Failed to parse calendar specification, ignoring: Sun *-*-1..7 1:00:00')
    # testResult.append(test1)
    # test1 = reg.exec_test('mdcheck_start.timer', 'journalctl -xe', 'output', 'mdcheck_start.timer lacks value setting. Refusing.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start mdmonitor-oneshot.service')
    # test1 = reg.exec_test('mdmonitor-oneshot.service', 'journalctl -xe', 'output', 'No mail address or alert command - not monitoring.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'touch /etc/mdadm.conf')
    # command_exec(execMode, 'systemctl start mdmonitor.service')
    # command_exec(execMode, 'sleep 1')
    # test1 = reg.exec_test('mdmonitor.service', 'journalctl -b -u mdmonitor.service', 'output', 'No mail address or alert command - not monitoring')
    # command_exec(execMode, 'rm -rf /etc/mdadm.conf')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start ndctl-monitor.service')
    # test1 = reg.exec_test('ndctl-monitor.service', 'journalctl -xe', 'output', 'code=exited, status=250')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start nfs-blkmap.service')
    # command_exec(execMode, 'systemctl stop nfs-blkmap.service')
    # test1 = reg.exec_test('nfs-blkmap.service', 'journalctl -b -u nfs-blkmap.service', 'output', 'open pipe file /var/lib/nfs/rpc_pipefs/nfs/blocklayout failed: No such file or directory')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start nvmet.service')
    # test1 = reg.exec_test('nvmet.service', 'journalctl -xe', 'output', '/sys/kernel/config/nvmet does not exist.  Giving up.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start opafm.service')
    # test1 = reg.exec_test('opafm.service', 'journalctl -b -u opafm.service', 'output', 'Invalid config detected! Coundn\'t find device for instance 0!.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start ods-enforcerd.service')
    # test1 = reg.exec_test('ods-enforcerd.service', 'journalctl -b -u ods-enforcerd.service', 'output', 'Can\'t open PID file /var/run/opendnssec/enforcerd.pid (yet?) after start: No such file or directory')
    # testResult.append(test1)
    # test1 = reg.exec_test('ods-enforcerd.service', 'journalctl -b -u ods-enforcerd.service', 'output', 'could not find token with the name OpenDNSSEC') # could not find token with the name OpenDNSSEC, RHEL과 비교 필요
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start openwsmand.service')
    # test1 = reg.exec_test('openwsmand.service', 'journalctl -b -u openwsmand.service', 'output', 'There is no ssl server key available for openwsman server to use.')
    # testResult.append(test1)
    # test1 = reg.exec_test('openwsmand.service', 'journalctl -b -u openwsmand.service', 'output', 'Please generate one with the following script and start the openwsman service again:')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start pcscd.service')
    # command_exec(execMode, 'systemctl stop pcscd.service')
    # test1 = reg.exec_test('pcscd.service', 'journalctl -b -u pcscd.service', 'output', 'code=exited, status=1/FAILURE')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start qemu-guest-agent.service')
    # test1 = reg.exec_test('qemu-guest-agent.service', 'journalctl -b -u qemu-guest-agent.service', 'output', 'start failed with result \'dependency\'')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'touch /etc/quagga/ospf6d.conf')
    # command_exec(execMode, 'systemctl start ospf6d.service')
    # command_exec(execMode, 'systemctl stop ospf6d.service')
    # test1 = reg.exec_test('ospf6d.service', 'journalctl -b -u ospf6d.service', 'output', 'code=killed, status=6/ABRT')
    # testResult.append(test1)
    # test1 = reg.exec_test('ospf6d.service', 'journalctl -b -u ospf6d.service', 'output', 'Unit ospf6d.service entered failed state.')
    # testResult.append(test1)
    # command_exec(execMode, 'rm -rf /etc/quagga/ospf6d.conf')
    #
    # command_exec(execMode, 'systemctl start ras-mc-ctl.service')
    # test1 = reg.exec_test('ras-mc-ctl.service', 'journalctl -b -u ras-mc-ctl.service', 'output', 'code=killed, status=11/SEGV')
    # testResult.append(test1)
    # test1 = reg.exec_test('ras-mc-ctl.service', 'journalctl -b -u ras-mc-ctl.service', 'output', 'Unit ras-mc-ctl.service entered failed state.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start redfish-finder.service')
    # test1 = reg.exec_test('redfish-finder.service', 'journalctl -b -u redfish-finder.service', 'output', 'AttributeError: dmiobject instance has no attribute \'device\'') # AttributeError: dmiobject instance has no attribute 'device', RHEL과 비교 필요
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start pppoe-server.service')
    # test1 = reg.exec_test('pppoe-server.service', 'journalctl -b -u pppoe-server.service', 'output', 'pppoe: ioctl(SIOCGIFHWADDR): No such device')
    # testResult.append(test1)
    # test1 = reg.exec_test('pppoe-server.service', 'journalctl -b -u pppoe-server.service', 'output', 'ioctl(SIOCGIFHWADDR): No such device')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start speech-dispatcherd.service')
    # test1 = reg.exec_test('speech-dispatcherd.service', 'journalctl -xe', 'output', 'Can\'t create pid file in /root/.speech-dispatcher/pid/speech-dispatcher.pid, wrong permissions?')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start sssd-autofs.socket')
    # test1 = reg.exec_test('sssd-autofs.socket', 'journalctl -b -u sssd-autofs.socket', 'output', 'failed with result \'dependency\'.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start sssd-pac.socket')
    # test1 = reg.exec_test('sssd-pac.socket', 'journalctl -b -u sssd-pac.socket', 'output', 'failed with result \'dependency\'.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start sssd-pam-priv.socket')
    # test1 = reg.exec_test('sssd-pam-priv.socket', 'journalctl -b -u sssd-pam-priv.socket', 'output', 'failed with result \'dependency\'.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start sssd-pam.socket')
    # test1 = reg.exec_test('sssd-pam.socket', 'journalctl -b -u sssd-pam.socket', 'output', 'failed with result \'dependency\'.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start sssd-ssh.socket')
    # test1 = reg.exec_test('sssd-ssh.socket', 'journalctl -b -u sssd-ssh.socket', 'output', 'failed with result \'dependency\'.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start sssd-sudo.socket')
    # test1 = reg.exec_test('sssd-sudo.socket', 'journalctl -b -u sssd-sudo.socket', 'output', 'failed with result \'dependency\'.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start sssd.service')
    # test1 = reg.exec_test('sssd.service', 'journalctl -b -u sssd.service', 'output', 'code=exited, status=4/NOPERMISSION')
    # testResult.append(test1)
    # test1 = reg.exec_test('sssd.service', 'journalctl -b -u sssd.service', 'output', 'SSSD couldn\'t load the configuration database [2]: No such file or directory.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start sssd-ifp.service')
    # test1 = reg.exec_test('sssd-ifp.service', 'journalctl -b -u sssd-ifp.service', 'output', 'failed with result \'dependency\'.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'touch /.readahead')
    # command_exec(execMode, 'systemctl start systemd-readahead-replay.service')
    # test1 = reg.exec_test('systemd-readahead-replay.service', 'journalctl -b -u systemd-readahead-replay.service', 'output', 'code=exited, status=1/FAILURE')
    # testResult.append(test1)
    # test1 = reg.exec_test('systemd-readahead-replay.service', 'journalctl -xe', 'output', ' Premature end of pack file.')
    # testResult.append(test1)
    # command_exec(execMode, 'rm -rf /.readahead')
    #
    # command_exec(execMode, 'systemctl start ypbind.service')
    # command_exec(execMode, 'sleep 3')
    # test1 = reg.exec_test('ypbind.service', 'journalctl -xe', 'output', 'domain not found')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start yppasswdd.service')
    # test1 = reg.exec_test('yppasswdd.service', 'journalctl -xe', 'output', 'domain not found')
    # testResult.append(test1)
    ##############################################################################################################################################

    # 7.9 버전
    # command_exec(execMode, 'systemctl start bacula-fd.service')
    # command_exec(execMode, 'systemctl stop bacula-fd.service')
    # test1 = reg.exec_test('bacula-fd.service', 'journalctl -xe', 'output', 'code=exited, status=15/n/a')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start named-pkcs11.service')
    # test1 = reg.exec_test('named-pkcs11.service', 'journalctl -xe', 'output', 'initializing DST: PKCS#11 initialization failed') # initializing DST: PKCS#11 initialization failed, RHEL과 비교 필요
    # testResult.append(test1)
    # test1 = reg.exec_test('named-pkcs11.service', 'journalctl -xe', 'output', 'exiting (due to fatal error)')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start blivet.service')
    # test1 = reg.exec_test('blivet.service', 'journalctl -b -u blivet.service', 'output', 'dbus.exceptions.DBusException: org.freedesktop.DBus.Error.AccessDenied: Connection ":')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start rbdmap.service')
    # test1 = reg.exec_test('rbdmap.service', 'journalctl -b -u rbdmap.service', 'output', 'Failed to start Map RBD devices.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start conman.service')
    # test1 = reg.exec_test('conman.service', 'journalctl -b -u conman.service', 'output', 'code=exited status=1')
    # testResult.append(test1)
    # test1 = reg.exec_test('conman.service', 'journalctl -b -u conman.service', 'output', 'Configuration "/etc/conman.conf" has no consoles defined')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start dhcpd6.service')
    # test1 = reg.exec_test('dhcpd6.service', 'journalctl -b -u dhcpd6.service', 'output', 'Not searching LDAP since ldap-server, ldap-port and ldap-base-dn were not specified in the config file') # Not searching LDAP since ldap-server, ldap-port and ldap-base-dn were not specified in the config file, RHEL과 비교 필요
    # testResult.append(test1)
    # test1 = reg.exec_test('dhcpd6.service', 'journalctl -b -u dhcpd6.service', 'output', 'No subnet6 declaration for')
    # testResult.append(test1)
    # test1 = reg.exec_test('dhcpd6.service', 'journalctl -xe', 'output', 'Not configured to listen on any interfaces!')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start dhcrelay.service')
    # test1 = reg.exec_test('dhcrelay.service', 'journalctl -b -u dhcrelay.service', 'output', 'No servers specified.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start edac.service')
    # test1 = reg.exec_test('edac.service', 'journalctl -b -u edac.service', 'output', 'No dimm labels for')
    # testResult.append(test1)
    # command_exec(execMode, 'systemctl stop edac.service')
    # test1 = reg.exec_test('edac.service', 'journalctl -b -u edac.service', 'output', 'code=exited status=1')
    # testResult.append(test1)
    # test1 = reg.exec_test('edac.service', 'journalctl -b -u edac.service', 'output', 'Unknown option: unload')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start firstboot-graphical.service')
    # test1 = reg.exec_test('firstboot-graphical.service', 'journalctl -b -u firstboot-graphical.service', 'output', 'Support for option SysVStartPriority= has been removed and it is ignored')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start bmc-watchdog.service')
    # command_exec(execMode, 'systemctl stop bmc-watchdog.service')
    # test1 = reg.exec_test('bmc-watchdog.service', 'journalctl -xe', 'output', 'Get Watchdog Timer: driver timeout')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start ipmidetectd.service')
    # test1 = reg.exec_test('ipmidetectd.service', 'journalctl -b -u ipmidetectd.service', 'output', 'ipmidetectd: No nodes configured')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'mkdir -p /dev/vmbus/')
    # command_exec(execMode, 'touch /dev/vmbus/hv_kvp')
    # command_exec(execMode, 'systemctl start hypervkvpd.service')
    # command_exec(execMode, 'sleep 1')
    # test1 = reg.exec_test('hypervkvpd.service', 'journalctl -xe', 'output', '13 Permission denied')
    # command_exec(execMode, 'rm -rf /dev/vmbus/')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'mkdir -p /dev/vmbus/')
    # command_exec(execMode, 'touch /dev/vmbus/hv_vss')
    # command_exec(execMode, 'systemctl start hypervvssd.service')
    # command_exec(execMode, 'sleep 1')
    # test1 = reg.exec_test('hypervvssd.service', 'journalctl -xe', 'output', '13 Permission denied')
    # command_exec(execMode, 'rm -rf /dev/vmbus/')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start ibacm.service')
    # test1 = reg.exec_test('ibacm.service', 'journalctl -b -u ibacm.service', 'output', 'code=exited, status=255')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start ipa.service')
    # test1 = reg.exec_test('ipa.service', 'journalctl -b -u ipa.service', 'output', 'code=exited, status=6')
    # testResult.append(test1)
    # test1 = reg.exec_test('ipa.service', 'journalctl -b -u ipa.service', 'output', 'IPA is not configured')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'touch /dev/ipmi0')
    # command_exec(execMode, 'systemctl start ipmievd.service')
    # test1 = reg.exec_test('ipmievd.service', 'journalctl -xe', 'output', 'Could not open device at /dev/ipmi0 or /dev/ipmi/0 or /dev/ipmidev/0: No such file or directory')
    # testResult.append(test1)
    # command_exec(execMode, 'rm -rf /dev/ipmi0')
    #
    # command_exec(execMode, 'systemctl start rdisc.service')
    # test1 = reg.exec_test('rdisc.service', 'journalctl -b -u rdisc.service', 'output', 'code=exited status=5')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start capi.service')
    # test1 = reg.exec_test('capi.service', 'journalctl -b -u capi.service', 'output', 'cannot open /dev/capi20 nor /dev/isdn/capi20 - No such file or directory (2)')
    # testResult.append(test1)
    #
    # test1 = reg.exec_test('isdn.service', 'systemctl start isdn.service', 'output', 'Failed to start isdn.service: Unit not found.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start isnsd.service')
    # test1 = reg.exec_test('isnsd.service', 'journalctl -b -u isnsd.service', 'output', 'code=exited, status=1/FAILURE')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start kadmin.service')
    # test1 = reg.exec_test('kadmin.service', 'journalctl -b -u kadmin.service', 'output', 'Configuration file does not specify default realm while initializing, aborting')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'touch /var/kerberos/krb5kdc/kpropd.acl')
    # command_exec(execMode, 'systemctl start kprop.service')
    # command_exec(execMode, 'sleep 1')
    # test1 = reg.exec_test('kprop.service', 'journalctl -xe', 'output', 'Configuration file does not specify default realm Unable to get default realm')
    # command_exec(execMode, 'rm -rf /var/kerberos/krb5kdc/kpropd.acl')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start krb5kdc.service')
    # test1 = reg.exec_test('krb5kdc.service', 'journalctl -b -u krb5kdc.service', 'output', 'Configuration file does not specify default realm, attempting to retrieve default realm')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start phc2sys.service')
    # test1 = reg.exec_test('phc2sys.service', 'journalctl -b -u phc2sys.service', 'output', 'uds: sendto failed: No such file or directory')
    # testResult.append(test1)
    # command_exec(execMode, 'systemctl stop phc2sys.service')
    # test1 = reg.exec_test('phc2sys.service', 'journalctl -xe', 'output', 'poll failed')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start ptp4l.service')
    # test1 = reg.exec_test('ptp4l.service', 'journalctl -b -u ptp4l.service', 'output', 'failed to create a clock')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'echo "test" > /etc/fancontrol')
    # command_exec(execMode, 'systemctl start fancontrol.service')
    # command_exec(execMode, 'sleep 1')
    # test1 = reg.exec_test('fancontrol.service', 'journalctl -xe', 'output', 'Some mandatory settings missing, please check your config file!')
    # command_exec(execMode, 'rm -rf /etc/fancontrol')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start mailman.service')
    # test1 = reg.exec_test('mailman.service', 'journalctl -xe', 'output', 'Site list is missing: mailman')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start mdcheck_start.timer')
    # test1 = reg.exec_test('mdcheck_start.timer', 'journalctl -xe', 'output', 'Failed to parse calendar specification, ignoring: Sun *-*-1..7 1:00:00')
    # testResult.append(test1)
    # test1 = reg.exec_test('mdcheck_start.timer', 'journalctl -xe', 'output', 'mdcheck_start.timer lacks value setting. Refusing.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start mdmonitor-oneshot.service')
    # test1 = reg.exec_test('mdmonitor-oneshot.service', 'journalctl -xe', 'output', 'No mail address or alert command - not monitoring.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'touch /etc/mdadm.conf')
    # command_exec(execMode, 'systemctl start mdmonitor.service')
    # command_exec(execMode, 'sleep 1')
    # test1 = reg.exec_test('mdmonitor.service', 'journalctl -b -u mdmonitor.service', 'output', 'No mail address or alert command - not monitoring')
    # command_exec(execMode, 'rm -rf /etc/mdadm.conf')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start ndctl-monitor.service')
    # test1 = reg.exec_test('ndctl-monitor.service', 'journalctl -xe', 'output', 'code=exited, status=250')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start nfs-blkmap.service')
    # command_exec(execMode, 'systemctl stop nfs-blkmap.service')
    # test1 = reg.exec_test('nfs-blkmap.service', 'journalctl -b -u nfs-blkmap.service', 'output', 'open pipe file /var/lib/nfs/rpc_pipefs/nfs/blocklayout failed: No such file or directory')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start nvmet.service')
    # test1 = reg.exec_test('nvmet.service', 'journalctl -xe', 'output', '/sys/kernel/config/nvmet does not exist.  Giving up.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start opafm.service')
    # test1 = reg.exec_test('opafm.service', 'journalctl -b -u opafm.service', 'output', 'Invalid config detected! Coundn\'t find device for instance 0!.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start ods-enforcerd.service')
    # test1 = reg.exec_test('ods-enforcerd.service', 'journalctl -b -u ods-enforcerd.service', 'output', 'Can\'t open PID file /var/run/opendnssec/enforcerd.pid (yet?) after start: No such file or directory')
    # testResult.append(test1)
    # test1 = reg.exec_test('ods-enforcerd.service', 'journalctl -b -u ods-enforcerd.service', 'output', 'could not find token with the name OpenDNSSEC') # could not find token with the name OpenDNSSEC, RHEL과 비교 필요
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start openwsmand.service')
    # test1 = reg.exec_test('openwsmand.service', 'journalctl -b -u openwsmand.service', 'output', 'There is no ssl server key available for openwsman server to use.')
    # testResult.append(test1)
    # test1 = reg.exec_test('openwsmand.service', 'journalctl -b -u openwsmand.service', 'output', 'Please generate one with the following script and start the openwsman service again:')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start pcscd.service')
    # command_exec(execMode, 'systemctl stop pcscd.service')
    # test1 = reg.exec_test('pcscd.service', 'journalctl -b -u pcscd.service', 'output', 'code=exited, status=1/FAILURE')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start qemu-guest-agent.service')
    # test1 = reg.exec_test('qemu-guest-agent.service', 'journalctl -b -u qemu-guest-agent.service', 'output', 'start failed with result \'dependency\'')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'touch /etc/quagga/ospf6d.conf')
    # command_exec(execMode, 'systemctl start ospf6d.service')
    # command_exec(execMode, 'systemctl stop ospf6d.service')
    # test1 = reg.exec_test('ospf6d.service', 'journalctl -b -u ospf6d.service', 'output', 'code=killed, status=6/ABRT')
    # testResult.append(test1)
    # test1 = reg.exec_test('ospf6d.service', 'journalctl -b -u ospf6d.service', 'output', 'Unit ospf6d.service entered failed state.')
    # testResult.append(test1)
    # command_exec(execMode, 'rm -rf /etc/quagga/ospf6d.conf')
    #
    # command_exec(execMode, 'systemctl start ras-mc-ctl.service')
    # test1 = reg.exec_test('ras-mc-ctl.service', 'journalctl -b -u ras-mc-ctl.service', 'output', 'code=killed, status=11/SEGV')
    # testResult.append(test1)
    # test1 = reg.exec_test('ras-mc-ctl.service', 'journalctl -b -u ras-mc-ctl.service', 'output', 'Unit ras-mc-ctl.service entered failed state.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start redfish-finder.service')
    # test1 = reg.exec_test('redfish-finder.service', 'journalctl -b -u redfish-finder.service', 'output', 'AttributeError: dmiobject instance has no attribute \'device\'') # AttributeError: dmiobject instance has no attribute 'device', RHEL과 비교 필요
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start pppoe-server.service')
    # test1 = reg.exec_test('pppoe-server.service', 'journalctl -b -u pppoe-server.service', 'output', 'pppoe: ioctl(SIOCGIFHWADDR): No such device')
    # testResult.append(test1)
    # test1 = reg.exec_test('pppoe-server.service', 'journalctl -b -u pppoe-server.service', 'output', 'ioctl(SIOCGIFHWADDR): No such device')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start speech-dispatcherd.service')
    # test1 = reg.exec_test('speech-dispatcherd.service', 'journalctl -xe', 'output', 'Can\'t create pid file in /root/.speech-dispatcher/pid/speech-dispatcher.pid, wrong permissions?')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start sssd-autofs.socket')
    # test1 = reg.exec_test('sssd-autofs.socket', 'journalctl -b -u sssd-autofs.socket', 'output', 'failed with result \'dependency\'.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start sssd-nss.socket')
    # test1 = reg.exec_test('sssd-nss.socket', 'journalctl -b -u sssd-nss.socket', 'output', 'failed with result \'dependency\'.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start sssd-pac.socket')
    # test1 = reg.exec_test('sssd-pac.socket', 'journalctl -b -u sssd-pac.socket', 'output', 'failed with result \'dependency\'.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start sssd-pam-priv.socket')
    # test1 = reg.exec_test('sssd-pam-priv.socket', 'journalctl -b -u sssd-pam-priv.socket', 'output', 'failed with result \'dependency\'.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start sssd-pam.socket')
    # test1 = reg.exec_test('sssd-pam.socket', 'journalctl -b -u sssd-pam.socket', 'output', 'failed with result \'dependency\'.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start sssd-ssh.socket')
    # test1 = reg.exec_test('sssd-ssh.socket', 'journalctl -b -u sssd-ssh.socket', 'output', 'failed with result \'dependency\'.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start sssd-sudo.socket')
    # test1 = reg.exec_test('sssd-sudo.socket', 'journalctl -b -u sssd-sudo.socket', 'output', 'failed with result \'dependency\'.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start sssd.service')
    # test1 = reg.exec_test('sssd.service', 'journalctl -b -u sssd.service', 'output', 'code=exited, status=4/NOPERMISSION')
    # testResult.append(test1)
    # test1 = reg.exec_test('sssd.service', 'journalctl -b -u sssd.service', 'output', 'SSSD couldn\'t load the configuration database [2]: No such file or directory.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start sssd-ifp.service')
    # test1 = reg.exec_test('sssd-ifp.service', 'journalctl -b -u sssd-ifp.service', 'output', 'failed with result \'dependency\'.')
    # testResult.append(test1)
    #
    # test1 = reg.exec_test('-.slice', 'systemctl start -.slice', 'output', "systemctl: invalid option -- \'.\'")
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start syslog.socket')
    # test1 = reg.exec_test('syslog.socket', 'journalctl -b -u syslog.socket', 'output', 'Socket service syslog.service not loaded, refusing.')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'touch /.readahead')
    # command_exec(execMode, 'systemctl start systemd-readahead-replay.service')
    # test1 = reg.exec_test('systemd-readahead-replay.service', 'journalctl -b -u systemd-readahead-replay.service', 'output', 'code=exited, status=1/FAILURE')
    # testResult.append(test1)
    # test1 = reg.exec_test('systemd-readahead-replay.service', 'journalctl -xe', 'output', ' Premature end of pack file.')
    # testResult.append(test1)
    # command_exec(execMode, 'rm -rf /.readahead')
    #
    # command_exec(execMode, 'systemctl start tcsd.service')
    # command_exec(execMode, 'sleep 3')
    # test1 = reg.exec_test('tcsd.service', 'journalctl -xe', 'output', 'TrouSerS ERROR: Could not find a device to open!')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start ypbind.service')
    # command_exec(execMode, 'sleep 3')
    # test1 = reg.exec_test('ypbind.service', 'journalctl -xe', 'output', 'domain not found')
    # testResult.append(test1)
    #
    # command_exec(execMode, 'systemctl start yppasswdd.service')
    # test1 = reg.exec_test('yppasswdd.service', 'journalctl -xe', 'output', 'domain not found')
    # testResult.append(test1)

    ##############################################################################################################################################

    # save result to csv
    reg.export_csv(testResult, RESULT_PATH + '/manual_'+VERSION_DETAIL+'_daemon1_result.csv', 'name;result;msg')

    return testResult

if __name__=="__main__":

    reg.makeFolder(RESULT_PATH) # 결과저장 폴더 만들기

    main()
