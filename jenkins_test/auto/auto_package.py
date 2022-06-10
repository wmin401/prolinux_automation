from __import__ import *
from __common__.__repository__ import *

PKG_TIMEOUT = int(PACKAGE_TIMEOUT)

PKG_TOTAL = []

def checkError(msg):
    ## FAIL 중 에러 메세지 내부에 아래와 같은 출력물이 있을 PASS로 간주
    result = False
    errorList = ['protected', 'No packages', 'No Match for argument', 'Skipping']

    for err in errorList:
        if err in msg:
            result = True
            break
    return result

## rpm check 코드 다시 짜기
def rpmCheck(proc, testFile, resultList, order): ## 설치 검증
    print("* " + proc.capitalize() + " Rpm -q checking ...")
    PKG_LIST = getListinFile(testFile)
    num = 0
    for pkg in PKG_LIST:
        num += 1
        output, error = commandExec(execMode, 'rpm -q ' + pkg, PKG_TIMEOUT)

        if order == 1:
            idx = 1
        else:
            idx = 3
        if output != [] and resultList[num][idx] != SKIP:
            if proc == 'install' or proc == 'reinstall':
                if output[0] == pkg:
                    resultList[num][idx] = PASS
                else:
                    if checkError(resultList[num][idx+1]):
                        resultList[num][idx] = PASS
                    else:
                        resultList[num][idx] = FAIL
        elif output != [] and proc == 'remove' and resultList[num][idx] != SKIP:
            if output[0] == pkg:
                if checkError(resultList[num][idx+1]):
                    resultList[num][1] = PASS
                else:
                    resultList[num][1] = FAIL
            else:
                resultList[num][1] = PASS        
        ## get total ## remove와 install의 결과가 같으면 total도 같다.

        if order == 2:
            if resultList[num][1] == resultList[num][3]:
                resultList[num].append(resultList[num][1])
                ## fail + fail = fail ## pass + pass = pass ## skip + skip = skip
            else: ## remove 와 install의 결과가 다르면 fail
                if (resultList[num][1] == SKIP or resultList[num][3] == SKIP) and \
                   (resultList[num][3] == PASS or resultList[num][1] == PASS): ## skip + pass = pass / pass + skip = pass
                    resultList[num].append(PASS)
                else:  ## fail + pass = pass + fail = fail = fail + skip = skip + fail = fail
                    resultList[num].append(FAIL)
    print("* Successfully results updated ...")
    return resultList

def pkgProcess(proc, testFile, resultList, order): ## install or remove, 결과 저장 리스트, 순서

    if proc == 'install' or proc == 'reinstall':
        SKIP_LIST = getListinFile(SKIP_PACKAGE_INSTALL_FILE)
        REALTIME_RESULT = REALTIME_INSTALL_RESULT_FILE
    else :
        SKIP_LIST = getListinFile(SKIP_PACKAGE_REMOVE_FILE)
        REALTIME_RESULT = REALTIME_REMOVE_RESULT_FILE

    ## 각자 결과 파일 생성
    tmpCsvInit(REALTIME_RESULT, None)

    saveCSV(['Package', proc.capitalize(), 'Message'], REALTIME_RESULT)

    PKG_LIST = getListinFile(testFile)
    num = 0
    a_time = time.time()

    startNumber = 0 ## 중간부터 시작하기 위한 숫자
    
    for pkg in PKG_LIST:
        num += 1
        if num < startNumber:
            continue
        printLine(num)# printLine(num)
        print('PACKAGE : ' + pkg)
        if order == 1: ## 처음 테스트인 경우
            procList = [pkg]
        else: ## 두번째 테스트인 경우
            procList = resultList[num]
            ## procList에 resultList[num]이 연결됨
        eachList = [] ## 각 테스트 결과 저장을 위한 리스트(install, remove 각자 저장을 위함)
        eachList = saveResult(eachList, pkg)
        if pkg in SKIP_LIST:
            print("RESULT : SKIP")
            #print("MESSAGE : " + proc.capitalize() + " skip")
            procList = saveResult(procList, SKIP, '-')
            eachList = saveResult(eachList, SKIP, '-')
            if order == 1:
                resultList.append(procList)
            saveCSV(eachList, REALTIME_RESULT)
            h, m, s = secToHms(a_time, time.time())
            print(proc.upper() + " TIME : %dh %dm %.2fs"%(h, m, s))
            printLine()
            PKG_TOTAL.append(SKIP)
            continue
        else:
            command = INSTALL_PKG + ' ' + proc + ' ' + pkg + ' -y'
            output, error = commandExec(execMode, command, PKG_TIMEOUT)

            if error != []: ## rpm 으로 할거기 때문에 error 메세지만 추출
                ### 예외처리 ###
                if 'rpmdb' in error[0]:
                    commandExec(execMode, 'rm -f /var/lib/rpm/_db*')
                    commandExec(execMode, 'rpm -vv --rebuilddb')
                    commandExec(execMode, 'sleep 15')
                    commandExec(execMode, 'systemctl start fapolicyd')
                    print('Start fapolicyd')
                    output, error = commandExec(execMode, command, PKG_TIMEOUT) ## 오류 발생할 경우 기존 명령어 재실행
                ## fapolicyd - file access policyd daemon 파일에 접근하기 위한 정책을 관리하는 데몬
                elif 'fapolicyd.fifo' in error[0]:
                    commandExec(execMode, 'systemctl start fapolicyd') ## pipe does not exist error
                    print('Start fapolicyd')
                    output, error = commandExec(execMode, command, PKG_TIMEOUT) ## 오류 발생할 경우 기존 명령어 재실행
                elif 'unfinished transactions remaining' in error[0]:
                    commandExec(execMode, 'yum-complete-transaction --cleanup-only')
                    print('Transaction cleanup')
                    output, error = commandExec(execMode, command, PKG_TIMEOUT) ## 오류 발생할 경우 기존 명령어 재실행
                ###########################################################################################################
                if error != []:
                    errMsg = mergeMsg(error)
                    if checkError(errMsg): ## True 일경우는 pass처리
                        procResult = PASS
                    else:
                        procResult = FAIL
                    print("MESSAGE : " + errMsg)
                else:
                    errMsg = ''
                    procResult = PASS
                procList = saveResult(procList, procResult, errMsg) ## idx 2 ## 결과위치이지만 rpm 을 기다리기 때문에 wait으로 입력
                eachList = saveResult(eachList, procResult, errMsg)

                print("RESULT : " + procResult)
            else: ## 에러메세지가 없을 경우 output으로 확인
                procList = saveResult(procList, 'PASS','') ## idx 2 ## 결과위치이지만 rpm 을 기다리기 때문에 wait으로 입력
                eachList = saveResult(eachList, 'PASS','') ## idx 2 ## 결과위치이지만 rpm 을 기다리기 때문에 wait으로 입력
                print("RESULT : PASS")

        if order == 1:
            resultList.append(procList)

        saveCSV(eachList, REALTIME_RESULT)
        h, m, s = secToHms(a_time, time.time())
        print(proc.upper() + " TIME : %dh %dm %.2fs"%(h, m, s))
        printLine()
    return resultList

## 패키지 설치 제거 실행용 함수
def pkgTest(remove, install):

    RESULT_CSV = open(PACKAGE_RESULT_FILE, "wt", encoding="UTF8")
    RESULT_CSV.close()

    ## 3가지 경우의 수 (순서는 무조건 remove -> install)
    # 1) remove only
    # 2) install only
    # 3) remove + install

    resultList = []

    if remove == True:
        if install == True: ## 3)
            resultList.append(['Package', 'Remove', 'Message', 'Install', 'Message', 'Total'])
            resultList = pkgProcess('remove', PACKAGE_FILE, resultList, 1)
            resultList = rpmCheck('remove', PACKAGE_FILE, resultList, 1 ) ## remove 하고 rpm 체크
            resultList = pkgProcess('install', PACKAGE_FILE, resultList, 2)
            resultList = rpmCheck('install', PACKAGE_FILE, resultList, 2 ) ## install 하고 rpm 체크
            numOfPFS('PACKAGE', getTotalinList(resultList, 5))

        else : ## 1) # 젠킨스 자동화에서는 코드 수정해야해서 사용하지 않음
            resultList.append(['Package', 'Remove', 'Message'])
            resultList = pkgProcess('remove', PACKAGE_FILE, resultList, 1)
            resultList = rpmCheck('remove', PACKAGE_FILE, resultList, 1 ) ## remove 하고 rpm 체크
            numOfPFS('PACKAGE REMOVE', getTotalinList(resultList, 1))

    else: ## remove == False
        if install == True:  ## 2)
            resultList.append(['Package', 'Install', 'Message'])
            resultList = pkgProcess('install', PACKAGE_FILE, resultList, 1)
            resultList = rpmCheck('install', PACKAGE_FILE, resultList, 1 ) ## install 하고 rpm 체크
            ## install 하고 rpm 체크
            numOfPFS('PACKAGE INSTALL', getTotalinList(resultList, 1))

    #ONLY_RESULT[4].append([getTotalinList(resultList, 1).count(PASS), getTotalinList(resultList, 1).count(FAIL), getTotalinList(resultList, 1).count(SKIP)])
    exportCSV(resultList, PACKAGE_RESULT_FILE, None)


def main():

    if PACKAGE_TEST == 'true':
        printSquare('Package Test')
        pkg_start = time.time()

        ## 네트워크 정보 백업
        th = testHelper()
        th.ip_backup()
        
        if PROCESS_KILLER == 'true':
            # 백그라운드에서 process killer 실행
            p1 = threading.Thread(target = th.proc_killer, args=('package',))
            p1.start() ## cpu saver 실행

        commandExec(execMode, INSTALL_PKG + ' clean all')

        pkgTest(True, True) ## RemoveTest, InstallTest

        if PROCESS_KILLER == 'true':
            p1.do_run = False

        th.ip_recovery() ## 네트워크 설정이 변경되었을 경우 원상복구
        th.ip_cloudInit()

        sshd_config()

        commandExec(execMode, INSTALL_PKG + ' install git java-1.8.0-openjdk -y')

        h, m, s = secToHms(pkg_start, time.time())
        print("* Package Test Running Time : %dh %dm %.2fs"%(h, m, s))


if __name__ == '__main__':

    main()

    if IN_JENKINS == None and execMode != 'shell':
        execMode.close()
        #print("ssh closed")
