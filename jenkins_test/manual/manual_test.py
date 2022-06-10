import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from auto.__common__.__parameter__ import RESULT_PATH, VERSION_DETAIL, MAJOR_VERSION

from manual.linux_regression.__module__ import makeFolder
import manual.linux_regression.__import__ as reg

def test_main(testFileName, totalTestResult):
    print("Manual "+ testFileName[7:-7].upper() + " Test Case")
    ## 초기화 부분 ##############################
    testResult = []
    
    currPath = os.path.dirname(os.path.realpath(__file__))
    print("Current Path : %s"%currPath)
    try:
        testFile = open(currPath + '\\testcase\\' + testFileName, 'r', encoding='utf-8')
    except Exception as e:
        print("*** Manual Test Exception in test_main : %s"%(e))
        return
    testList = []
    for line in testFile:
        testList.append(line.replace('\n',''))

    allVer = [
        ['vAll', 0],
        ['v7', 0],
        ['v7_8', 0],
        ['v7_9', 0],
        ['v8', 0],
        ['v8_2', 0],
        ['v8_3', 0],
    ]

    for i in range(1, len(testList)):
        if testList[i] == '\n':
            continue
        test=testList[i].split(';')

        ## all은 모든 버전에서 돌리고
        ## all이 아닌 버전은 해당 버전일 때만 돌리도록
        if test[0] == 'vAll':        ## 모든 버전에서 동일한 결과를 보여줌      
            test = reg.exec_test(test[1],test[2],'output',test[3])
            totalTestResult.append(test)           
            testResult.append(test)
            allVer[0][1] += 1
        
        for ver in allVer:
            if test[0] == VERSION_DETAIL == ver[0] or test[0] == ver[0] == 'v' + MAJOR_VERSION:
                test = reg.exec_test(test[1],test[2],'output',test[3])
                totalTestResult.append(test)    
                testResult.append(test)
                ver[1] += 1

    verSum = 0
    for ver in allVer :
        if ver[1] is not 0:
            print("Manual Test " + testFileName[7:-7] + " %s Count : %d"%(ver[0], ver[1]))
            verSum += ver[1]

    print("Manual Test "+testFileName[7:-7]+" Total Count : %d"%(verSum))            

    

    # save result to csv
    reg.export_csv(testResult, RESULT_PATH + '/manual_'+VERSION_DETAIL+'_' + testFileName[7:-7] + '_result.csv', 'name;result;msg')

    return totalTestResult

def main():

    makeFolder(RESULT_PATH) # 결과저장 폴더 만들기

    totalTestResult = []
    tcFiles = []

    try:
        currPath = os.path.dirname(os.path.realpath(__file__))
        print('Current Path : %s'%currPath)    
        allFiles = os.listdir(currPath + '\\testcase')
    except Exception as e:
        print("*** Manual Test Exception in main: %s"%str(e))

    print("Test Case File : ")
    j = 0
    for i in range(0,len(allFiles)):
        if 'TC.csv' not in allFiles[i]: ## 파일의 마지막이 TC.csv가 아니면 테스트파일이 아님
            continue
        else:
            j += 1
            tcFiles.append(allFiles[i])
            print('%d) %s'%(j,allFiles[i]))

    for TCFile in tcFiles:
        totalTestResult = test_main(TCFile, totalTestResult)

    return totalTestResult

if __name__=="__main__":

    main()

    ### 파일내에 있는 csv 파일 읽어와서 파일명 넣기

    #test_main('cmd')
    #test_main('daemon_2')
