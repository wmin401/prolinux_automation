from __common__.__module__ import *
from __common__.__print__ import *
from __common__.__logger__ import *

import time
import threading

class testHelper:
    #def __init__(self) -> None:
        #print("Test Helper can : ")
        #print("1) ip backup and recovery")
        #print("2) cloud init")
        #print("3) process kill")

    def ip_backup(self): ## package, daemon, install
        # ifcfg 파일을 root로 복사(dhcp 일 경우하지 않음)
        output, error = commandExec(execMode, 'cat /etc/sysconfig/network-scripts/ifcfg-e*')         
        for i in output:
            if 'BOOTPROTO=dhcp' in i or 'BOOTPROTO="dhcp"' in i:
                print("* Network was changed already ... ")
                print("* Need to check your network information ...")
                print("* Don't backup ifcfg file ... ")
                printLine()
                return 
        print("* Backup ifcfg file to /root ...")
        commandExec(execMode, '\cp /etc/sysconfig/network-scripts/ifcfg-e* /root/')
        output, error = commandExec(execMode, 'cat /root/ifcfg-e*')
        #print('Before ifcfg file : ')
        #printBeautify(output)
        printLine()

    def ip_recovery(self): ## package, daemon
        ## ifcfg 파일이 dhcp로 변경되면 root에 잇는 파일로 복구
        output, error = commandExec(execMode, 'cat /etc/sysconfig/network-scripts/ifcfg-e*')            
        for i in output:            
            if 'BOOTPROTO=dhcp' in i or 'BOOTPROTO="dhcp"' in i:
                printLine()
                print("* Network information was changed ... ")
                print("* Start to trying recovery using original ifcfg file in /root/... ")
                commandExec(execMode, '\cp /root/ifcfg-e* /etc/sysconfig/network-scripts/')
                commandExec(execMode, 'systemctl restart NetworkManager')
                output, error = commandExec(execMode, 'cat /etc/sysconfig/network-scripts/ifcfg-e*')  
                print("* After ifcfg file : ")
                printBeautify(output)         
                printLine()  
                return
        print("* Don't have to change ip ...")
        
            
    def ip_cloudInit(self): ## package, install
        print("* Cloud init ... ")
        output, error = commandExec(execMode, 'cat /etc/sysconfig/network-scripts/ifcfg-e*')            
        for i in output:            
            if 'BOOTPROTO=dhcp' in i or 'BOOTPROTO="dhcp"' in i:
                commandExec(execMode, '\cp /etc/sysconfig/network-scripts/ifcfg-e* /root/')
        commandExec(execMode, 'touch /etc/cloud/cloud-init.disabled')

        
        output, error = commandExec(execMode, 'cat /etc/dracut.conf |grep omit_dracutmodules')
        if output != []:
            if 'ifcfg network' in output[0]:
                print("* Already exists 'ifcfg network'")
                pass
            else:
                commandExec(execMode, "sed -i 's/"+'#omit_dracutmodules+=""'+'/omit_dracutmodules+="ifcfg network"/g' + "' " + '/etc/dracut.conf')
                print('* Successfully Input omit_dracutmodules="ifcfg network"')
                commandExec(execMode, 'dracut -fv')


    def proc_killer(self, tester=None): ## daemon, cmd        
        global PROCESS_KILLER
        ## 프로세스 강제종료 할 때 로그에 저장
        #logfile = open(tester + '_kill.log', 'wt', encoding='utf-8')
        #logfile.close()
        if tester == 'package': ## cmd 일 경우에 종료하는 프로세스
            procList = ['yum','dnf']
        elif tester == 'daemon': ## 데몬일 경우 종료하는 프로세스
            procList = ['systemd-journald', 'hypervfcopyd', 'rsyslogd']            
        elif tester == 'cmd': ## cmd 일 경우에 종료하는 프로세스
            procList = ['sosreport', 'cp', 'gzip', 'tgz', 'servertool', 'jconsole', 'troff', 'instperf', 'man', 'instperf']
        else:  # None # tester를 지정하지 않을 경우엔 전부다
            procList = ['sosreport', 'cp', 'gzip', 'tgz', 'servertool', 'jconsole', 'troff', 'instperf', 'man', 'systemd-journald', 'hypervfcopyd','fio-genzipf']
        print('Turn on the Process Killer')
        ssh = sshConnection(HOST_IP, HOST_ID, HOST_PW, HOST_PORT)
        ## killer 는 ssh로만 동작하도록
        if PROCESS_KILLER == 'true':
            timeCnt = 0
            timeStack = []
            t = threading.currentThread() ## 현재 쓰레드 정보를 가져옴
            while getattr(t, "do_run", True): ## do_run 이 False가 되면 종료됨
                for proc in procList:
                    if tester == 'package': 
                        output, error = commandExec(ssh, 'ps -C ' + proc + ' -o %mem') ## dnf 던
                        memoryCnt = len(output)-1
                        if memoryCnt >= 5:
                            print("* Too many " + proc)                            
                            commandExec(ssh, 'killall -9 ' + proc)                       
                            print("* Process Killer killed all '" + proc + "' processes")

                    else:
                        output, error = commandExec(ssh, 'ps -C ' + proc + ' -o %cpu')
                        if len(output) > 1: # ex) output = ['%CPU', '1.0', '33.0']
                            for i in range(1, len(output)): ## cpu List
                                cpu = float(output[i])
                                if cpu >= 50: ## 50%이상을 계쏙 유지하면 강제종료
                                    if proc == 'man': ## man 은 예외처리가 필요 100
                                        if timeCnt == 0:
                                            timeStack.append(time.time()) ## 처음 발생한 시간 저장
                                            timeCnt = 1     
                                        if timeCnt == 1:                                   
                                            diff = time.time() - timeStack[0]
                                            if diff >= 5: # man 이 5초이상 100%가 유지되면 종료 
                                                #print(proc + " %.2f 초 점유 강제 종료 실행"%(diff))                                         
                                                commandExec(ssh, 'killall -9 man')
                                                print('* Process Killer killed man')
                                                timeCnt = 0
                                                timeStack = []
                                    else:
                                        commandExec(ssh, 'killall -9 ' + proc)          
                                        print('* Process Killer killed ' + proc)                  
                                    break
        ssh.close()             
        print("* Turn off the Process Killer")