import os
import socket
import subprocess as sp
import paramiko
from __common__.__print__ import *
from __common__.__parameter__ import *
from __common__.__exception__ import *
from __common__.__logger__ import *
 


## ssh 연결 함수 paramiko 라이브러리 사용
def sshConnection(HOST_IP, HOST_ID, HOST_PW, HOST_PORT):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOST_IP, username=HOST_ID, password=HOST_PW, port=HOST_PORT)
        print("* Successfully connected to %s !!!"%HOST_IP)
        stdin, stdout, stderr = ssh.exec_command('rpm --query prolinux-release')

        output = stdout.readlines()
        #output[0] = output[0].replace('\n','')
        return ssh
    except Exception as e:
        print("*** SSH Exception : %s"%str(e))
        return None
 
def getOSInfo():
    print("* Get OS information in /etc/*release files")
    output, error = commandExec(execMode, 'ls /root |grep OSInfo.txt')
    try:
        if output != [] and 'OSInfo.txt' in output[0]:
            commandExec(execMode, 'rm -rf /root/OSInfo.txt')
    except Exception as e:
        print("* Get OS Info Exception : %s"%(str(e)))
    commandExec(execMode, 'cat /etc/*release* >> /root/OSInfo.txt')

def sshd_config(): # package ,daemon, cmd , install
    # ssh가 설치되어있지 않을 경우 설치
    output, error = commandExec(execMode, 'rpm -q openssh-server')        

    if output != [] and 'openssh-server' in output[0] and 'not' not in output[0]: ## 설치 되어있을 때 
        pass        
    else: #설치되어있지 않을때               
        warningLog("*************** Warning ***************")     
        warningLog("* sshd.service is deleted !!!")
        warningLog("* Start to install openssh-server right now !!!")
        commandExec(execMode, INSTALL_PKG + ' install openssh-server -y')
        warningLog("* sshd setting is finished")
        warningLog("***************************************")
            
    print("* Changing configuration in /etc/ssh/sshd_config ...")
    def configChange(file_path, config, after_config):
        before_config, error = commandExec(execMode, "cat " + file_path + " |grep -x " + config)
        if before_config != [] and before_config[0] != after_config:
            print("* " + before_config[0], '->' , after_config)
            commandExec(execMode,"sed -i 's%" + before_config[0] + "%" + after_config + "%g' " + file_path)            

    configChange('/etc/ssh/sshd_config', "'#Port 22'", "Port 22")
    configChange('/etc/ssh/sshd_config', "'#MaxSessions 10'", "MaxSessions 300")
    configChange('/etc/ssh/sshd_config', "'#PermitRootLogin yes'", "PermitRootLogin yes")
    configChange('/etc/ssh/sshd_config', "'PasswordAuthentication no'", "PasswordAuthentication yes")
    configChange('/etc/ssh/sshd_config', "'#AllowTcpForwarding yes'", "AllowTcpForwarding yes")
    configChange('/etc/ssh/sshd_config', "'AllowTcpForwarding no'", "AllowTcpForwarding yes")
    configChange('/etc/ssh/sshd_config', "'#ClientAliveInterval 0'", "ClientAliveInterval 3600")
    configChange('/etc/ssh/sshd_config', "'#ClientAliveCountMax 3'", "ClientAliveCountMax 10")

    # PermitOpen any 설정 추가
    output, error = commandExec(execMode, "cat /etc/ssh/sshd_config |grep 'PermitOpen any'")
    if output == []:
        commandExec(execMode, "echo 'PermitOpen any' >> /etc/ssh/sshd_config")
        print("* Added 'PermitOpen any'")     

    commandExec(execMode, "systemctl restart sshd")
    print("* Restarted sshd.service")
        
    
def commandExec(*args):
    if args[0] == 'shell':
        a = sp.Popen(args[1], shell=True, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)        
        try : 
            output, error = a.communicate(timeout=args[2])
        except UnicodeDecodeError:
            a.kill()
            return ['UnicodeDecodeError'], ['UnicodeDecodeError']
        except sp.TimeoutExpired:
            a.kill()
            return ['subprocess.TimeoutExpired'], ['subprocess.TimeoutExpired']
        except:
            output, error = a.communicate()
            #return ['Another Except'], ['Another Except']
        
        if output != []:
            output =  [v for v in output.split('\n') if v]
        else:
            output = []
        if error != []:
            error =  [v for v in error.split('\n') if v]
        else:
            error = []
    else: ##  args[0] == ssh class
        output = error = []
        if len(args) > 2:
            stdin, stdout, stderr = args[0].exec_command(args[1], timeout=args[2])
        else:
            stdin, stdout, stderr = args[0].exec_command(args[1])
        try:
            output =  makeUpMsg(stdout.readlines())
        except socket.timeout:
            output = ['socket.timeout']
        except UnicodeDecodeError:
            output = ['UnicodeDecodeError']
        except:
            output = ['Another Except']
        try: 
            error = makeUpMsg(stderr.readlines())
        except socket.timeout:
            error = ['socket.timeout']
        except UnicodeDecodeError:
            error = ['UnicodeDecodeError']
        except:
            error = ['Another Except']

    error = assertionError(error)

    return output, error
   
def getExecMode():
    ### 젠킨스에서 사용할 떄는 shell 에서 테스트하도록 shell 반환
    ### 로컬에서 할 때는 ssh로 테스트할 수 있게 ssh 반환
    if IN_JENKINS == 'true':
        mode = 'shell'
        print('* INPUT MODE : shell')
    else: ## in_jenkins == None : 
        mode = sshConnection(HOST_IP, HOST_ID, HOST_PW, int(HOST_PORT))
        print('* INPUT MODE : ssh')

    ## shell로 하고 싶을 경우 아래 shell 주석 해제, ssh로만 하고 싶을 경우 아래 sshConnection 주석 해제
    #mode = 'shell'
    #mode = sshConnection(HOST_IP, HOST_ID, HOST_PW, int(HOST_PORT))
    return mode
execMode = getExecMode()  ## 테스트 시작시 shell 인지 ssh인지 반환해줌

## 시작시간과 종료시간을 입력받으면 시, 분, 초로 보여주는 함수
def secToHms(start, end): # 시작시간, 끝나는 시간
    sec = end - start
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    return h,m,s

## 메세지 리스트 처리하는 부분
def mergeMsg(msg):
    ## 에러 최대 두번째 줄까지만 추가
    merge = ''
    if len(msg) < 1:
        merge = ''
    elif len(msg) == 1:
        merge = msg[0]
    else:
        merge = ''
        for i in range(0,2):
            msg[i] = msg[i].replace("\n",' ')
            msg[i] = msg[i].replace(";",'')
            merge += msg[i]
    return merge
def makeUpMsg(msg_list):
    ## 입력받은 메시지 리스트에서 \n과 , 삭제
    returnMsg = []
    for i in msg_list:
        i = i.replace('\n','')
        #i = i.replace(',', ' ')
        returnMsg.append(i)
    return returnMsg

## 해당 경로에있는 파일을 읽어와 리스트로 만듬
## 테스트 진행시 파일에 있는 내용은 테스트를 실행하지 않고 넘어감
def getListinFile(list_path_):
    #No stop daemon    
    _LIST = open(list_path_, 'r', encoding='utf-8').read()
    _LIST = [v for v in _LIST.split('\n') if v]
    return _LIST

## 원하는 경로에 폴더를 생성해줌
## 하위 경로 입력시, 폴더가 존재하지 않으면 같이 생성
def makeFolder(path_):
    if os.path.isdir(path_):
        print("* " + path_ + ' folder is already existed!')
        return
    else:
        print("* " + path_ + ' folder made!')
        os.makedirs(path_)

def existPath(path):## 파일이나 폴더 존재 유무 확인
    file = ''
    output, error = commandExec(execMode, 'find / -wholename ' + path)
    if output != []:
        file = output[0].replace('\n','')
    if path in file:
        print(file + ' exists')
        return True  ## 존재
    else:
        return False ## 없음

def findFile(folder, name):      
    ## 특정 폴더에 특정 내용이 포함된 파일 찾기  
    filenames = os.listdir(folder)
    for file in filenames:
        if name in file:
            return file

## 명령어, 데몬 등 앞에 /를 포함한 경로가 있을 경우 / 앞부분 prefix를 지워줌
def deletePath(path):
    pathName = ''
    cmd = ''
    for i in range(len(path)-1, 0, -1):
        if path[i] != '/':
            pathName += path[i]
        else:
            cmd = pathName
            break
    return cmd[::-1]

# 메타데이터에서 사용중임
# 특정 문자열의 개수를 찾을 때 사용한다.(PASS, )
def getTotalinList(lst, idx):
    total = []
    for i in range(0, len(lst)):
        total.append(lst[i][idx])
    return total

def numOfPFS(name, lst):  #결과만 저장된 리스트를 받아서 pass와 fail stop의 개수를 반환해줌
    p = lst.count(PASS)
    f = lst.count(FAIL)
    s = lst.count(SKIP)
    print()

    try:
        sum_ = p+f+s
        rate = p/sum_ * 100
        print("%s TOTAL : %s%sPASS : %s%sFAIL : %s%sSKIP : %s%sSUCCESS RATE : %.2f %%"%(name, p+f+s,TAP,p,TAP,f,TAP,s,TAP,TAP,rate))
    except:
        pass
    
## RPM 파일에서 패키지의 이름만 추출
def export_rpm_name(rpm):
    hipenIdx = list(filter(lambda x:rpm[x]=='-',range(len(rpm))))
    for idx in hipenIdx:
        if rpm[int(idx)+1].isalpha():
            isNum = False            
        else:
            isNum = True            
        if isNum == True:
            to = idx
            break
    return rpm[:to]

# 경로가 있는 파일명에서 경로 제거(deletePath와 비슷)
def getFileName(filePath):
    a = filePath.split('/')
    b = a[len(a)-1]
    return b
    