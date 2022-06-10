from manual.linux_regression.__module__ import *
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from auto.__common__.__parameter__ import PASS, FAIL

def exist_path(path):## 파일이나 폴더 존재 유무 확인
    output, error = command_exec(execMode, 'ls |grep ' + path)
    #print(output)
    if output != []:
        file = output[0].replace('\n','')
        #print(file)
        if path in file:
            #print("* "+file + ' exists')
            return PASS  ## 존재
        else:
            return FAIL ## 없음
    else:
        return FAIL

def str_to_list(str_):
    if type(str_) == type([]): ## 입력한 매개변수가 문자열인지 리스트인지 비교
        ## 리스트일 경우엔 그대로 반환
        return str_
    else:
        if ',' in str_: ## 문자열 내부에서 콤마로 나뉘어있을 경우엔 split를 이용하여 리스트로 변환
            lst = str_.split(',')
        ## 리스트가 아닐경우엔 리스트[0]에 값 추가하여 리스트로 반환(길이는 1)
        else:
            lst=[str(str_)]
        #str_=str(str_)
        #lst = [str_]    
    return lst

def file_test(testName, fileName, need = None, noNeed = None):# 0 = 파일 이름, 1 = 포함되어야 하는 내용(리스트로 가능), 2 = 포함되면 안되는 내용(리스트로 가능)
    status = FAIL ## 상태 초기화
    msg = 'Success'
    print("--------------------------------------------------------------------------------")
    print("TEST : " + testName)
    if need == None and noNeed == None: ## 파일명만 있을 경우 해당 파일이 있는지 체크
        if exist_path(fileName):
            status = PASS
            msg = 'File exists'
        else:
            status = FAIL
            msg = "File doesn't exist"
    ## 0 1
    else:        
        output, error = command_exec(execMode, 'cat ' + fileName, 30)
        if error == []:
            ## 0 1
            if need != None: ## 포함되어야 하는 문자열이 있을 경우
                need = str_to_list(need)
                for needStr in need: ## 입력받은 문자열 순서대로 검색
                    status = FAIL ## 처음엔 FAIL
                    for line in output:
                        if needStr in line: ## 해당 문자열이 있다
                            status = PASS ## 결과 PASS
                            #msg = 'No error' ## 에러 없어
                ## 해당 문자열이 하나라도 포함되어있지 않으면 실패임
                    if status == FAIL:
                        msg = needStr + " doesn't exist"
                        print("RESULT : " + status)
                        print("MESSAGE : " + msg)
                        return [testName, status, msg]
                    
                if noNeed != None :  # 0 1 2 ## 필요한 문자열과 필요없는 문자열 모두 체크할때    
                    noNeed = str_to_list(noNeed)
                    for noNeedStr in noNeed:
                        status = PASS
                        for line in output:
                            if noNeedStr in line: ## 없어야 하는 문자열이 있을 경우 바로 실패 처리
                                status = FAIL
                                msg = noNeedStr + ' exists'
                                print("RESULT : " + status)
                                print("MESSAGE : " + msg)
                                return [testName, status, msg]
            else: ## need 가 없을 때 , noNeed는무조건 있음(둘다 없다면 제일 위에서 체크)
                noNeed = str_to_list(noNeed)
                for noNeedStr in noNeed:
                    status = PASS
                    for line in output:
                        if noNeedStr in line: ## 없어야 하는 문자열이 있을 경우 바로 실패 처리
                            status = FAIL
                            msg = noNeedStr + ' exists'
                            break
                    if status == FAIL:
                        break
                
        else:
            status = FAIL
            msg = 'File open exception'  
    
    print("RESULT : " + status)
    print("MESSAGE : " + msg)
    print("--------------------------------------------------------------------------------")
    return [testName, status, msg]

if __name__ == "__main__":
    
    print(file_test('txtTest', 'test.txt')) ## PASS
    print(file_test('txtTest', 'test.txt','need1')) ##PASS
    print(file_test('txtTest', 'test.txt',['need1','need3']) )  ##FAIL
    print(file_test('txtTest', 'test.txt',['need1','need2']))   ##PASS
    print(file_test('txtTest', 'test.txt',None, ['need1','need2']) )  ##FAIL
    print(file_test('txtTest', 'test.txt',None, ['need3','need4']) )  ##PASS
    print(file_test('txtTest', 'test.txt',['need3','need4'], ['need3','need4']) )  ##FAIL
    print(file_test('txtTest', 'test.txt',['need1','need2'], ['need3','need4'])  ) ##PASS
