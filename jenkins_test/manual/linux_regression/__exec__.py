from manual.linux_regression.__file__ import exist_path
from manual.linux_regression.__module__ import *

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from auto.__common__.__parameter__ import FAIL, PASS

def exec_test(testName, exec, type_='output' ,*args): ## 명령어,문자열 or 파일 존재 확인
    # type_ : output / file
    # output : 명령어 실행 결과 문자열 확인
    # file : 파일 존재 유무 확인(있으면 True 없으면 False)
    status = FAIL
    msg = 'Success'

    print("--------------------------------------------------------------------------------")
    print("TEST : " + testName)
    output, error = command_exec(execMode, exec, 30)
    args = list(args)

    if type_ == None : 
        type_ = 'output'
    if type_ == 'output':
        if output != []:
            for arg in args:
                status = FAIL
                for line in output:
                    if arg in line:
                        status = PASS
                        break
                if status == FAIL:
                    msg = output[0]
                    break
        elif error != []:
            for arg in args:
                status = FAIL
                for line in error:
                    if 'could not be found' in line:
                        msg = line
                        break
                    if arg in line:
                        status = PASS
                        break
                if status == FAIL:
                    msg = error[0]
                    break
        else: ## output == [] and error == []
            status = FAIL
            msg = 'Nothing messages'
            
    else:# type_ == 'file':## elif type_ == 'file'
        #print("파일 유무 확인")
        if exist_path(args[0]) == PASS:
            status = PASS 
            msg = args[0] + ' exists'
        else:
            status = FAIL
            msg = args[0] + " doesn't exist"
            
    print("RESULT : " + status)
    print("MESSAGE : " + msg)
    print("--------------------------------------------------------------------------------")
    return [testName, status, msg]

if __name__=="__main__":

    print(exec_test('catTest', 'cat /root/test.txt', 'output','need3'))
    print(exec_test('catTest', 'cat /root/test.txt', 'output','need1'))
    print(exec_test('catTest', 'cat /root/test.txt', 'file','test.txt'))
    print(exec_test('catTest', 'cat /root/test.txt', 'file','test1.txt'))