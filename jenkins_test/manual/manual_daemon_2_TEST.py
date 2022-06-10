
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from auto.__common__.__parameter__ import  RESULT_PATH, VERSION_DETAIL

from manual.linux_regression.__module__ import command_exec, execMode, makeFolder
import manual.linux_regression.__import__ as reg


def main():
    print("* Manual Daemon 2 Test Case")
    ## 초기화 부분 ##############################
    testResult = []

    currPath = os.path.dirname(os.path.realpath(__file__))
    print(currPath)

    try:
        daemonTestFile = open(currPath + '/manual_daemon_2_TC.csv', 'r', encoding='utf-8')
    except Exception as e:        
        print("*** Manual Daemon 2 Exception : %s"%(e))
        return
    daemonList = []
    for line in daemonTestFile:
        daemonList.append(line.replace('\n',''))

    dVer = [
        ['vAll', 0],
        ['v7', 0],
        ['v7_8', 0],
        ['v7_9', 0],
        ['v8', 0],
        ['v8_2', 0],
        ['v8_3', 0]
    ]



    for i in range(1, len(daemonList)):
        if daemonList[i] == '\n':
            continue
        #print(i, end=' ')
        daemon=daemonList[i].split(';')

        ## all은 모든 버전에서 돌리고
        ## all이 아닌 버전은 해당 버전일 때만 돌리도록
        if daemon[0] == 'vAll':        ## 모든 버전에서 동일한 결과를 보여줌
            daemon[2] = daemon[2].replace("'","")
            test1 = reg.exec_test(daemon[1],daemon[2],'output',daemon[3])
            testResult.append(test1)
            dVer[0][1] += 1

        for ver in dVer:
            if daemon[0] == VERSION_DETAIL == ver[0]:
                test = reg.exec_test(daemon[1],daemon[2],'output',daemon[3])
                testResult.append(test)
                ver[1] += 1


    verSum = 0
    for ver in dVer :
        if ver[1] is not 0:
            print("Manual Test Daemon %s Count : %d"%(ver[0], ver[1]))
            verSum += ver[1]

    print("Manual Test Daemon Total Count : %d"%(verSum))

    # save result to csv
    reg.export_csv(testResult, RESULT_PATH + '/manual_'+VERSION_DETAIL+'_dtTEST_result.csv', 'name;result;msg')

    return testResult

if __name__=="__main__":

    makeFolder(RESULT_PATH) # 결과저장 폴더 만들기

    main()
