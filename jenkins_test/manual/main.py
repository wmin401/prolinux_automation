#-*- coding: utf-8 -*-
import os, sys
## manual 폴더 포함하기 위해
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from auto.__common__.__parameter__ import RESULT_PATH, VERSION_DETAIL

from manual.linux_regression.__module__ import makeFolder
import manual.linux_regression.__import__ as reg

import manual.manual_daemon_1 as md1
import manual.manual_daemon_2 as md2

import manual.manual_test as mt

def main():

    print("* Manual Test Main")
    # 초기화 부분
    testResult = []
    makeFolder(RESULT_PATH) # 결과저장 폴더 만들기
    ############################################

    # testResult = mt.main() ## 아직 미적용

    # 테스트 케이스를 다 csv에 저장하는 방식으로 변경할 경우 위의 코드를 주석해제 하고
    # 아래의 4줄을 주석처리하면 된다.

    testMain = [md1, md2] ## import 추가
    for each in testMain:
        for i in each.main():
            testResult.append(i)


    print("*** TOTAL ***")
    reg.export_csv(testResult, RESULT_PATH + '/manual_'+VERSION_DETAIL+'_total_result.csv', 'name;result;msg')
    ## 파일 결과, 파일명, 헤더

if __name__=="__main__":
    main()
