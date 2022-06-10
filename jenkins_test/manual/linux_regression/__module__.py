import os
import sys
import socket
import subprocess as sp
import paramiko

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from auto.__common__.__parameter__ import IN_JENKINS, HOST_ID, HOST_IP, HOST_PORT, HOST_PW

## ssh 연결 함수 paramiko 라이브러리 사용
def ssh_connection(hostIP, hostId, hostPw, hostPort):
    #print(hostIP, hostId, hostPw, hostPort)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostIP, username=hostId, password=hostPw, port=hostPort)
    stdin, stdout, stderr = ssh.exec_command('rpm --query prolinux-release')

    output = stdout.readlines()
    #output[0] = output[0].replace('\n','')
    return ssh
 
def command_exec(*args):
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
        def make_up_msg(msgList):
            ## 입력받은 메시지 리스트에서 \n과 , 삭제
            returnMsg = []
            for i in msgList:
                i = i.replace('\n','')
                #i = i.replace(',', ' ')
                returnMsg.append(i)
            return returnMsg
        output = error = []
        if len(args) > 2:
            stdin, stdout, stderr = args[0].exec_command(args[1], timeout=args[2])
        else:
            stdin, stdout, stderr = args[0].exec_command(args[1])
        try:
            output =  make_up_msg(stdout.readlines())
        except socket.timeout:
            output = ['socket.timeout']
        except UnicodeDecodeError:
            output = ['UnicodeDecodeError']
        except:
            output = ['Another Except']
        try: 
            error = make_up_msg(stderr.readlines())
        except socket.timeout:
            error = ['socket.timeout']
        except UnicodeDecodeError:
            error = ['UnicodeDecodeError']
        except:
            error = ['Another Except']

    return output, error
   
def get_exec_mode():
    ### 젠킨스에서 사용할 떄는 shell 에서 테스트하도록 shell 반환
    ### 로컬에서 할 때는 ssh로 테스트할 수 있게 ssh 반환
    if IN_JENKINS == 'true':
        mode = 'shell'
        print('* INPUT MODE : shell')
    else: ## in_jenkins == None : 
        mode = ssh_connection(HOST_IP, HOST_ID, HOST_PW, int(HOST_PORT))
        print('* INPUT MODE : ssh')

    ## shell로 하고 싶을 경우 아래 shell 주석 해제, ssh로만 하고 싶을 경우 아래 ssh_connection 주석 해제
    #mode = 'shell'
    #mode = ssh_connection(HOST_IP, HOST_ID, HOST_PW, int(HOST_PORT))
    return mode
execMode = get_exec_mode()  ## 테스트 시작시 shell 인지 ssh인지 반환해줌


def makeFolder(dir):
    if os.path.isdir(dir):
        return False
    else:
        os.makedirs(dir)
