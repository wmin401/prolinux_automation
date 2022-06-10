### Cmd Test

from __import__ import *

CMD_TIMEOUT = 3

CMD_TOTAL = []

#a = open('cmd.log', 'w',encoding='utf-8')
## cmd 테스트 후 생성되는 파일들 삭제를 위한 함수
def deleteFiles():
    print("* Deleting result files from cmd test")
    ## 입력받은 이름으로 시작되는 파일들 모두 삭제
    def find_and_delete(path, file):
        output, error = commandExec(execMode, 'ls ' + path + '/ |grep ' + file)
        
        for i in output:
            commandExec(execMode, 'rm -rf /root/' + i)

    deleteList = ['.kde','.config', '.java', 'orb.db', '.cache', '.hplip', '.gnome2', '-h', '--h', '-help', 
                  '--help', '.bltk', 'results','.gnupg', 'perl5', 'festival_server.log', 'last_results', 'last_cmd', 
                  '.bashrc.old','.bash_profile.old', '.cshrc.old', 'last_cmd', 'last_results', '.bzr.log', 'IMB_out', 
                  'IMB_out_0', '-h.tgz', '--h.tgz', '-help.tgz', '--help.tgz', '.speech-dispatcher', 'results.001', 
                  'rpmbuild','.qt','texput.log', '-help-dir', '--help-dir', '-h-dir', '--h-dir','.dbus',
                  'Public', 'Documents', 'Templates', 'Videos', 'Music', 'Pictures', 'Desktop']

    for i in deleteList:
        commandExec(execMode, 'rm -rf /root/' + i)

    find_and_delete('/root', 'festival')
    find_and_delete('/root', 'fabtests')   
    find_and_delete('/root', 'mpi')   

def checkOutput(output):
    exist = False
    for line in output:
        line = line.replace('\n','')
        line = line.lower()
        if 'usage' in line or 'options' in line or 'synopsis' in line or \
           '[name]' in line or 'description' in line or 'use:' in line:
            exist = True
            break
        else:
            exist = False
    return exist

def cmdEXE(cmd):
    
    output, error = commandExec(execMode, cmd, CMD_TIMEOUT)
    
    msg = ''
    if output != [] and error != []:
        isPassed = checkOutput(output)    
        if isPassed == True:
            CMD_TOTAL.append(PASS)
            return [PASS, 'exe']
        else:    
            isPassed = checkOutput(error)
            msg = error        
    elif output != [] and error == []:        
        isPassed = checkOutput(output)
        msg = output
    elif output == [] and error != []:     
        isPassed = checkOutput(error)
        msg = error        

    else:# output == [] and error == []:        
        CMD_TOTAL.append(FAIL)
        print('MESSAGE : exe FAIL - Nothing')
        return [FAIL, 'exe FAIL - Nothing']

    if isPassed == True:
        CMD_TOTAL.append(PASS)
        return [PASS, 'exe']
    else:                             
        try: 
            msg = list(filter(('\n').__ne__, msg))           
            print('MESSAGE : exe FAIL - ' + msg[0])      
            CMD_TOTAL.append(FAIL)
            return [FAIL, msg[0]] 
        except:
            msg = 'Nothing'
            print('MESSAGE : exe FAIL - ' + msg)     
            CMD_TOTAL.append(FAIL) 
            return [FAIL, 'exe FAIL - Nothing'] 

def cmdHelp(cmd): ## man으로 걸러내지 못하는 테스트 걸러내기 위해 help 로 테스트
    helpList = ['--help', '-help', '-h', '--h']
    # 순서대로 help 입력 후 출력 잘 되는지 확인
    helpCount = 0
    for help in helpList:
        msg = ''
        helpCount += 1

        output, error = commandExec(execMode, cmd + ' ' + help, CMD_TIMEOUT)

        if output != [] and error != []:
            isPassed = checkOutput(output)
            if isPassed == True:
                return [PASS, help]
            else:
                isPassed = checkOutput(error)
                msg = error
        elif output != [] and error == []:
            isPassed = checkOutput(output)
            msg = output
        elif output == [] and error != []:
            isPassed = checkOutput(error)    
            msg = error

        else:# output == [] and error == []: 
            ## ouptut 이나 error에 내용이 있을 땐      
            if helpCount > 3: 
                return [FAIL, 'help FAIL - Nothing']
            else:
                continue
        
        try:
            msg = list(filter(('\n').__ne__, msg))
        except:
            msg = 'Nothing'
        if isPassed == True:
            return [PASS, help]
        else:
            if helpCount > 3: 
                return [FAIL, 'help FAIL - ' + msg[0]]
            continue

def help_and_exe(cmd, cmdResult):
    helpResult = cmdHelp(cmd)            
    if helpResult[0] == FAIL:
        print("MESSAGE : " + helpResult[1])        
        exeResult = cmdEXE(cmd)         
        if 'weather' in cmd:
            exeResult[1] = ''
        print("RESULT : " + exeResult[0])
        print("MESSAGE : " + exeResult[1])
        cmdResult = saveResult(cmdResult, exeResult[0], exeResult[1])
        
    else: ## helpResult pass ?
        CMD_TOTAL.append(PASS)
        print("RESULT : " + helpResult[0])
        print("MESSAGE : " + helpResult[1])
        cmdResult = saveResult(cmdResult, helpResult[0], helpResult[1])
    saveCSV(cmdResult, REALTIME_CMD_RESULT_FILE)
    return cmdResult

def cmdMan():

    commandExec(execMode, INSTALL_PKG + ' install man-db -y')

    CMD_LIST = getListinFile(CMD_FILE)
    print("TEST FILE : " + CMD_FILE)
    SKIP_CMD_LIST = getListinFile(SKIP_CMD_FILE)

    tmpCsvInit(REALTIME_CMD_RESULT_FILE, 'Command' + DELIM + 'Result' + DELIM + 'Messages')
    
    cmdResult = []
    cmdResultTotal = []

    a_time = time.time()
    num = 0
    for cmd in CMD_LIST:
        num += 1
        printLine(num)
        print("CMD :", cmd)
        cmdResult = [cmd]                
        # 제외 리스트
        if cmd in SKIP_CMD_LIST:
            print("RESULT : SKIP")
            cmdResult = saveResult(cmdResult,SKIP,'')
            saveCSV(cmdResult, REALTIME_CMD_RESULT_FILE)
            cmdResultTotal.append(cmdResult)
            h, m, s = secToHms(a_time, time.time())
            print("TIME : %dh %dm %.2fs"%(h, m, s))
            printLine()
            CMD_TOTAL.append(SKIP)
            continue

        # man + 명령어 입력
        output, error = commandExec(execMode, 'man ' + cmd, CMD_TIMEOUT)
                

        msg = ''
        # man 입력값이 정상적으로 출력된지 확인
        if output != [] and error == []:
            isPassed = checkOutput(output)
            msg = output
        elif output == [] and error != []:
            isPassed = checkOutput(error)
            msg = error
        elif output != [] and error != []:            
            isPassed = checkOutput(output)
            if isPassed == False:          
                isPassed = checkOutput(error)  
                msg = error
        else:
            isPassed = False

        if isPassed == True: # 정상 출력은 pass로 하고 다음 명령어로 넘어감
            print("RESULT : " + PASS)
            CMD_TOTAL.append(PASS)
            cmdResult = saveResult(cmdResult,PASS,'')
            saveCSV(cmdResult, REALTIME_CMD_RESULT_FILE)
        else:
            try:
                msg = list(filter(('\n').__ne__, msg)) ## 줄내림 삭제
                print("MESSAGE : man FAIL - " + msg[0])
            except :
                print("MESSAGE : man FAIL - Nothing")

            cmdResult = help_and_exe(cmd, cmdResult)                                
                

        cmdResultTotal.append(cmdResult)
        h, m, s = secToHms(a_time, time.time())
        print("TIME : %dh %dm %.2fs"%(h, m, s))
        printLine()
       




    exportCSV(cmdResultTotal, CMD_RESULT_FILE, 'Command' + DELIM + 'Result' + DELIM + 'Messages')

def main():
    if CMD_TEST == 'true':        
        printSquare("Cmd Test")
        cmd_start = time.time()
  
        th = testHelper()
        if PROCESS_KILLER == 'true':      
            ## 백그라운드에서 process killer 실행
            c1 = threading.Thread(target = th.proc_killer, args=('cmd',)) 
            c1.start() ## cpu saver 실행      
            
        ## 테스트
        cmdMan()
        #deleteFiles()
        ##

        if PROCESS_KILLER == 'true':  
            c1.do_run = False

        sshd_config()
        
        numOfPFS('CMD', CMD_TOTAL)
        #ONLY_RESULT[2].append([CMD_TOTAL.count(PASS), CMD_TOTAL.count(FAIL), CMD_TOTAL.count(SKIP)])
        h, m, s = secToHms(cmd_start, time.time())
        print("* Cmd Test Running Time : %dh %dm %.2fs"%(h, m, s))

            
if __name__ == '__main__':
    #3. cmd 테스트
    #print("writing print in output.txt")
    #sys.stdout = open('cmd_output.txt','w')

    main()
    
    if IN_JENKINS == None and execMode != 'shell':
        execMode.close()
        #infoLog("ssh closed")

