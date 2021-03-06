

def getP(daemon, line, prop):
    output, error = commandExec(execMode, "cat " + daemon + " |grep -A " + str(line) + " '" + prop + "'")
    #print("cat " + daemon + " |grep '" + prop + "'")
    #printBeautify(output)
    if output !=[]:
        if line == 0:
            print(daemon, ',', prop)
        elif line == 1:            
            if output[0] == '[Service]' and output[1] == 'RemainAfterExit=yes':
                printBeautify(output)
            elif output[0] == 'Type=oneshot' and output[1] == 'RemainAfterExit=yes':
                printBeautify(output)
 
def getProperties():
    file1 = open('list/v8_2/release/daemon/pre_condition/daemon_for_pre_condition_1.txt','rt',encoding='utf-8')
    cnt = 1
    for i in file1:
        i = i.replace('\n','')
        print(cnt, i)
        getP(i, 1, '\[Service\]')
        #getP(ssh, i, 1, 'Type=oneshot')
        '''
        getP(ssh, i, 0, '#RemainAfterExit=yes')
        getP(ssh, i, 0, '#RefuseManualStop=yes')
        getP(ssh, i, 0, '#RefuseManualStart=yes')
        getP(ssh, i, 0, '#RefuseManualStart=true')
        getP(ssh, i, 0, '#RemainAfterExit=no')
        getP(ssh, i, 0, '#ConditionDirectoryNotEmpty=/sys/fs/pstore')
        getP(ssh, i, 0, '#ConditionKernelCommandLine=debug')
        getP(ssh, i, 0, '#IgnoreOnIsolate=1')
        getP(ssh, i, 0, '#StopWhenUnneeded=yes')
        getP(ssh, i, 0, '#ConditionKernelCommandLine=ostree')
        getP(ssh, i, 0, '#ConditionSecurity=!selinux')
        getP(ssh, i, 0, '#ConditionPathExists=!/.autorelabel')
        getP(ssh, i, 0, 'RemainAfterExit=yes')
        getP(ssh, i, 0, '#ConditionPathIsReadWrite=!/')
        getP(ssh, i, 0, '#ConditionNeedsUpdate=/var')
        getP(ssh, i, 0, '#ConditionNeedsUpdate=/etc')
        getP(ssh, i, 0, '#ConditionNeedsUpdate=|/etc')
        getP(ssh, i, 0, '#ConditionNeedsUpdate=|/var')
        getP(ssh, i, 0, '#ConditionPathIsMountPoint=/etc/machine-id')

        '''
        cnt += 1
    file1.close()
def velocityTest():

    pkgLst = [ 'aajohan-comfortaa-fonts-3.001-2.el8.noarch',
                'abattis-cantarell-fonts-0.0.25-4.el8.noarch',
                'abrt-2.10.9-11.0.2.el8.x86_64',
                'abrt-addon-ccpp-2.10.9-11.0.2.el8.x86_64',
                'abrt-addon-coredump-helper-2.10.9-11.0.2.el8.x86_64',
                'abrt-addon-kerneloops-2.10.9-11.0.2.el8.x86_64',
                'abrt-addon-pstoreoops-2.10.9-11.0.2.el8.x86_64',
                'abrt-addon-vmcore-2.10.9-11.0.2.el8.x86_64',
                'abrt-addon-xorg-2.10.9-11.0.2.el8.x86_64',
                'abrt-cli-2.10.9-11.0.2.el8.x86_64']
                
    start1 = time.time()
    for i in pkgLst:
        output, error = commandExec('shell', "dnf remove " + i + " -y")
        output, error = commandExec('shell', "dnf install " + i + " -y")
    end1 = time.time()
    print ("Popen : %.8f"%(end1 - start1))


    ssh = sshConnection('192.168.17.151','root','asdf',22)
    start2 = time.time()
    for i in pkgLst:
        output, error = commandExec(ssh, "dnf remove " + i + " -y")
        output, error = commandExec(ssh, "dnf install " + i + " -y")
    end2 = time.time()
    print ("ssh   : %.8f"%(end2 - start2))


def failCompareWithPreList():
    ## fail case??? predconditon ???????????? ????????????
    # precondition??? ???????????? ???????????? ????????? ????????????
    file1 = open('failcase.txt', 'rt',encoding='utf-8')    

    for i in file1:
        i = i.replace('\n','')
        #print(i)
        file2 = open('list/v7_7/release/daemon/daemon_for_pre_condition.txt', 'rt',encoding='utf-8')    
        for j in file2:
            j = j.replace('\n','')
            #print(j)
            if i == j:
                print(j)
                break        

## gzip ?????? cpu 100% ????????? ??????????????? ??????
def overCPU():
    th = testHelper()
    d1 = threading.Thread(target = th.proc_killer, args=('cmd',)) 
    d1.start() ## cpu saver ??????
    for i in range(10):
        print("10????????? gzip ????????? ??????")
        commandExec(execMode, 'dd if=/dev/urandom | gzip --best >> /dev/null &') ## gzip cpu 100% ?????? ?????? ??????
        time.sleep(10)
          
    d1.do_run = False
class trouble_maker:
    def __init__(self, type_):
        self.type_ = type_
        f = open("trouble_maker_" + self.type_ + ".txt", 'wt', encoding='utf-8')
        f.close()
    
    def report(self, maker):
        f = open("trouble_maker_" + self.type_ + ".txt", 'a', encoding='utf-8')
        ## ip??? ssh ?????? ???????????? ?????? ???????????? ?????? ?????????        
        if self.type_ == 'ip':
            output, error = commandExec(execMode, 'cat /etc/sysconfig/network-scripts/ifcfg-e* |grep BOOTPROTO')
            if 'dhcp' in output[0]:
                print('ip changed')
                f.write(maker + '\n')
        elif self.type_ == 'ssh':
            output, error = commandExec(execMode, 'cat /etc/ssh/sshd_config |grep "PasswordAuthentication no"')
            for i in output:
                if 'PasswordAuthentication no'in i:
                    print('ssh changed')
                    f.write(maker + '\n')        
        f.close()


def getDaemonStatus(folderName, IP):
    ssh1 = sshConnection(IP, HOST_ID, HOST_PW, HOST_PORT)
    execMode = ssh1
    
    output, error = commandExec(execMode, 'touch /root/success')
    DAEMON_LIST = open('list/'+VERSION_DETAIL+'/release/daemon/test_di.txt', 'r', encoding='utf-8')

    for daemonPath in DAEMON_LIST:
        daemonPath = daemonPath.replace('\n','')
        eachResult = [] ## ?????? ????????? ?????? ????????? ??????
        print("DAEMON PATH :", daemonPath)
        eachResult.append(daemonPath) ## ???????????? ?????? ?????? ??????
        daemon = deletePath(daemonPath) ## ?????? ??????
        eachResult.append(daemon) ## ???????????? ???????????? ??????
        print("DAEMON :", daemon)
        commandExec(execMode, 'mkdir /root/res')
        commandExec(execMode, 'rm -rf /root/res/'+daemon+'.log')
        commandExec(execMode, 'touch /root/res/'+daemon+'.log')
        commandExec(execMode, 'systemctl start ' +  daemon, 10)
        commandExec(execMode, 'echo "start" >> /root/res/'+daemon+'.log')
        output, error = commandExec(execMode, 'systemctl status ' +  daemon)
        for i in output:
            commandExec(execMode, 'echo "' + i + '" >> /root/res/'+daemon+'.log')
        
        
        commandExec(execMode, 'echo "stop" >> /root/res/'+daemon+'.log')
        commandExec(execMode, 'systemctl stop ' +  daemon, 10)
        output, error = commandExec(execMode, 'systemctl status ' +  daemon)
        for i in output:
            commandExec(execMode, 'echo "' + i + '" >> /root/res/'+daemon+'.log')
    