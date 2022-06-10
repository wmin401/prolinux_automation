from manual.linux_regression.__module__ import *
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from auto.__common__.__parameter__ import PASS, FAIL

## 스크립트 실행이 정상적으로 완료되면 PASS
## 스크립트 실행 중 오류가 한번이라도 발생하면 FAIL

def script_test(testName, shCommand): ## 쉘스크립트 명령어를 입력받을 경우 결과 전달
    ## 파일인 경우엔 exec로 대체 가능
    print("--------------------------------------------------------------------------------")
    print("TEST : " + testName)
    msg = 'Success'
    shCommand = shCommand.split('\n')
    shCommand = [v for v in shCommand if v != '']
    #print(shCommand)
    for i in shCommand:
        i = i.replace('\n','')
        status = FAIL
        if i == '\n' or i == ' ' or i == '': ## 빈칸은 넘어가기
            continue
    
        output, error = command_exec(execMode, i, 30)

        if error != []:
            status = FAIL
            msg = i
            break
        else:
            status = PASS

    print("RESULT : " + status)
    print("MESSAGE : " + msg)
    print("--------------------------------------------------------------------------------")
    return [testName, status, msg]