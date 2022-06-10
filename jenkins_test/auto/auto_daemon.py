### Daemon Test

from __import__ import *

DAEMON_TIMEOUT = 60

DAEMON_TOTAL = []

# 데몬 테스트 필요 함수
def getActive(daemon):
    output, error = commandExec(execMode, 'systemctl status ' + daemon, DAEMON_TIMEOUT) ## get status active

    INACTIVE = "Active: inactive"
    ACTIVE = "Active: active"
    ACTIVATING = "Active: activating"
    FAILED = "Active: failed"


    if error != []: #stop 또는 start 할 때 오류가 있을 경우
        return error[0]
    else:
        for line in output:
            if 'since' in line:
                line = line[0:line.find('since')] ## Active 에서 뒤에 since 및 시간은 출력 안함
            if ACTIVE in line or ACTIVATING in line:
                return 'Active'
            elif INACTIVE in line:
                return 'Inactive'
            elif FAILED in line:
                return 'Failed'
            else:
                if line == output[len(output)-1]:
                    return 'No Status'
                continue

def setActive(daemon, func): ## start 또는 stop, 데몬
    output, error = commandExec(execMode, 'systemctl ' + func + ' ' + daemon, DAEMON_TIMEOUT)

    if error != []:
        try :
            return (str(error[0]) + str(error[1]))
        except:
            return error[0]
    else:
        if output != []:
            try :
                return (str(output[0]) + str(output[1]))
            except:
                return output[0]
        else:
            return 'Nothing Message'

def eachTest(daemon, func, curr): # set and get status, and return result
    setMsg, currStatus, isPassed = '', '', ''
    ## setMsg : start 또는 stop을 실행했을 때 error또는 아웃풋이 있을 경우 받아옴
    ## currStatus : start 또는 stop을 실행하고 난 뒤에 active 상태
    ## isPassed : 정상적으로 변경되었는지 확인
    setMsg = setActive(daemon, func)  ## stop 진행
    currStatus = getActive(daemon) # Active, Inactive, Failed, No Status
    if currStatus == curr: ## Active , Inactive
        isPassed = PASS
    else:
        if 'Warning' in setMsg and curr == 'Active':
            isPassed = PASS
        else:
            isPassed = FAIL
    return setMsg, currStatus, isPassed

## 데몬 테스트
def daemonTest(DAEMON_TEST_FILE, RESULT_FILE): ## inactive -> active / active -> inactive

    DAEMON_LIST = getListinFile(DAEMON_TEST_FILE)
    print("TEST FILE : " + DAEMON_TEST_FILE)
    SKIP_DAEMON_LIST = getListinFile(SKIP_DAEMON_FILE) ## start / stop 하면 안되는 데몬리스트

    tmpCsvInit(REALTIME_DAEMON_RESULT_FILE, 'Path' + DELIM + 'Daemon' + DELIM + '1st before' + DELIM + '1st after' + DELIM + '1st Result' + DELIM + '1st Message' + DELIM + '2nd before' + DELIM + '2nd after' + DELIM + '2nd Result' + DELIM + '2nd Message' + DELIM + 'Total')

    num = 0
    a_time = time.time()

    daemonResultTotal = []

    for daemonPath in DAEMON_LIST:
        num += 1
        daemon = deletePath(daemonPath) ## 경로 제거
        daemonResult = []
        daemonResult = saveResult(daemonResult, daemonPath, daemon)
        printLine(num)
        print("DAEMON PATH :", daemonPath)
        print("DAEMON :", daemon)

        ## 종료하면 안되는 데몬은 리스트로 만들어서 비교
        if daemonPath in SKIP_DAEMON_LIST:
            print("RESULT : SKIP")
            print("MESSAGE : Don't test Automatically")
            daemonResult = saveResult(daemonResult, '','',SKIP,'','','',SKIP,'',SKIP)
            saveCSV(daemonResult, REALTIME_DAEMON_RESULT_FILE)
            daemonResultTotal.append(daemonResult)
            #before, after, result, remark, before, after, result, remark, total
            h, m, s = secToHms(a_time, time.time())
            print("TIME : %dh %dm %.2fs"%(h, m, s))
            printLine()
            DAEMON_TOTAL.append(SKIP)
            continue

        for testNum in range(0,2): ## start -> stop -> start 또는 stop -> start -> stop 이렇게만 진행
            if testNum == 0:
                print("TEST : 1st")
            else:
                print("TEST : 2nd")

            ## 이전 상태 불러오기
            prevStatus = getActive(daemon)
            print('PREV STATUS :', prevStatus)

            ## 이전 상태에 따라서 stop 또는 start 실행
            if prevStatus == 'Active': ## 이전 상태가 Active 일 때
                setMsg, currStatus, isPassed = eachTest(daemon, 'stop', 'Inactive')
            elif prevStatus == 'Inactive' or prevStatus == 'Failed':          ## inactive 또는 failed 일때
                setMsg, currStatus, isPassed = eachTest(daemon, 'start', 'Active')
            else : #No Status ## status가 없을 때
                setMsg, currStatus, isPassed = prevStatus, '-', FAIL

            if setMsg != '':
                print("MESSAGE : " + str(setMsg))
            print("CURR STATUS : " + str(currStatus))
            print("RESULT : " + str(isPassed))
            daemonResult = saveResult(daemonResult, prevStatus, currStatus, isPassed, setMsg) # previous # current, result, remark

        ## total 결과
        if daemonResult[4] == PASS and daemonResult[8] == daemonResult[4]:
            if daemonResult[2] == daemonResult[6] and daemonResult[2] == 'Failed':
                print("TOTAL RESULT : " + FAIL)
                daemonResult = saveResult(daemonResult, FAIL)
                DAEMON_TOTAL.append(FAIL)
            else:
                print("TOTAL RESULT : " + PASS)
                daemonResult = saveResult(daemonResult, PASS)
                DAEMON_TOTAL.append(PASS)
        else:
            print("TOTAL RESULT : " + FAIL)
            daemonResult = saveResult(daemonResult, FAIL)
            DAEMON_TOTAL.append(FAIL)

        h, m, s = secToHms(a_time, time.time())
        print("TIME : %dh %dm %.2fs"%(h, m, s))
        printLine()

        ## 결과 저장
        daemonResultTotal.append(daemonResult)
        saveCSV(daemonResult, REALTIME_DAEMON_RESULT_FILE)

    exportCSV(daemonResultTotal, RESULT_FILE, 'Path' + DELIM + 'Daemon' + DELIM + '1st before' + DELIM + '1st after' + DELIM + '1st Result' + DELIM + '1st Message' + DELIM + '2nd before' + DELIM + '2nd after' + DELIM + '2nd Result' + DELIM + '2nd Message' + DELIM + 'Total') ## 모든 결과 저장됨 ## 필요없음

def main():
    global DAEMON_TOTAL
    # 데몬 테스트
    if DAEMON_TEST == 'true':
        printSquare("Daemon Test")
        daemon_start = time.time()


        th = testHelper()
        th.ip_backup()
        if PROCESS_KILLER == 'true':
            ## 백그라운드에서 process killer 실행
            d1 = threading.Thread(target = th.proc_killer, args=('daemon',))
            d1.start() ## cpu saver 실행

        daemonTest(DAEMON_FILE, DAEMON_RESULT_FILE)  ## 프리컨디션 없이 실행
        numOfPFS('DAEMON', DAEMON_TOTAL)
        #ONLY_RESULT[1].append([DAEMON_TOTAL.count(PASS), DAEMON_TOTAL.count(FAIL), DAEMON_TOTAL.count(SKIP)])
        
        if PROCESS_KILLER == 'true':
            d1.do_run = False

        th.ip_recovery() ## 네트워크 설정이 변경되었을 경우 원상복구
        th.ip_cloudInit()
        sshd_config() ## sshd 설정도 변경


        h, m, s = secToHms(daemon_start, time.time())
        print("* Daemon Test Running Time : %dh %dm %.2fs"%(h, m, s))


if __name__ == '__main__':

    main()

    if IN_JENKINS == None and execMode != 'shell':
        execMode.close()
        #print("ssh closed")
