# linux_regression
RHEL 기반 Linux 제품 테스트시 여러가지 테스트의 결과를 동일한 방법으로 반환받기 위해 사용

1) 쉘스크립트 코드 실행
2) 파일 내용 확인
3) 명령어 실행

- 윈도우에서 코드 실행시 ssh로 명령어 전달
- 리눅스에서 코드 실행시 popen으로 명령어 직접 쉘에 입력
#### 적용 방법
  - linux_regression과 같은 경로에 존재하는 파일 내부에 ` import linux_regression.__import__ as reg ` 입력시 바로 사용 가능
  
## 사용 가능 함수 
#### 1. ` script_test(testName, shCommand) `
  - 쉘 스크립트 명령어를 입력받아서 실행 후 결과를 반환해주는 함수
  - 인자
    - 0 : 테스트 이름 (모든 테스트 공통, 저장에 필요한 인자)
    - 1 : 쉘 스크립트 명령어 문자열
  - 반환값(리스트)
    - 0 : 테스트 이름 (모든 테스트 공통, 저장에 필요한 인자)
    - 1 : 테스트 결과
      - PASS : 모든 쉘 스크립트의 명령어에 오류가 없을 경우
      - FAIL : 하나의 코드라도 오류가 있을 경우
    - 2 : 테스트 메세지(오류가 있을 경우엔 오류가 발생한 명령어)
  - 사용법
    ```
    import linux_regression.__import__ as reg  # 고정

    # 쉘스크립트 코드 작성 및 변수에 할당
    # 변수할당하지 않고 바로 함수에 인자로 작성도 가능
    shString = '''
        ls -al
        ls |grep test.txt
    '''
    var1 = reg.script_test('ls test', shString)    
    print(var1)
    ```
    ```
    ['ls test', PASS, 'No error']
    ```

#### 2. ` file_test(testName, fileName, need = None, noNeed = None) `
  - 파일 내부에 원하는 문자열이나 원하지 않는 문자열이 있는지 확인하는 함수
  - 인자
    - 0 : 테스트 이름
    - 1 : 파일 이름
    - 2 : 포함되어야 하는 문자열
      - 2가지 방법으로 작성 가능
      - '문자열,문자열,문자열, ...'
      - ['문자열', '문자열', '문자열', ...]
    - 3 : 포함되면 안되는 문자열(입력 안해도 됨)
      - 2가지 방법으로 작성 가능
      - '문자열,문자열,문자열, ...'
      - ['문자열', '문자열', '문자열', ...]
    - 참고사항
      1. 파일이름(idx 1)까지만 인자를 입력시, 파일의 존재 유무를 확인하여 파일이 존재하면 PASS, 존재하지 않을 경우 FAIL를 반환
      2. idx 3은 입력하지 않아도됨
      3. `포함되지 않아야하는 문자열만 확인이 필요할 경우 idx 2 에 None 을 입력`
        * ex. file_test('file test', 'test.txt', None, ['noNeed1', 'noNeed2'])
  - 반환값(리스트)
    - 0 : 테스트 이름
    - 1 : 테스트 결과
      - 파일 이름만 입력시(인덱스1)
        - PASS : 파일 존재
        - FAIL: 파일 미존재
      - 포함되는 문자열까지만 입력
        - PASS : 모든 문자열이 포함되어있을 때
        - FAIL : 하나의 문자열이라도 포함되어있지 않을 때 
      - 포함되면 안되는 문자열만 입력
        - PASS : 모든 문자열이 포함되어있지 않을 때
        - FAIL : 하나의 문자열이라도 포함되어있을 때
    - 2 : 테스트 메세지(오류가 있을 경우엔 어디서 오류가 발생했는지)
  - 사용법
    ```
    import linux_regression.__import__ as reg  # 고정
    '''
    /root/test.txt
    need1
    need2

    noNeed1
    noNeed2
    '''
    ## test.txt 파일이 존재하는지 확인
    var1 = reg.file_test('txtTest', 'test.txt') # 파일이름(인덱스 1)까지만 입력
    ## test.txt 파일 내부에 need1과 need2가 모두 있어야 성공
    var2 = reg.file_test('txtTest', 'test.txt', 'need1,need2') # 포함되어야하는 문자열(인덱스 2)까지만 입력
    # var2 = file_test('txtTest', 'test.txt', ['need1','need2']) # 위와 같은 결과
    ## test.txt 파일 내부에 noNeed1와 noNeed2가 없어야 성공
    var3 = reg.file_test('txtTest', 'test.txt', None, ['noNeed1','noNeed2']) # 포함되면 안되는 문자열(인덱스 3)만 필요할 때 
    ## test.txt 파일 내부에 need1과 need2가 있어야하며, noNeed3이나 noNeed4가 없으면 성공
    var4 = reg.file_test('txtTest', 'test.txt', 'need1,need2', ['noNeed3','noNeed4'])
    print(var1)
    print(var2)
    print(var3)
    print(var4)
    ```
    ```
    ['txtTest', PASS, 'File exists'] # 파일이 존재
    ['txtTest', PASS, 'No error'] # 파일 내부에 need1과 need2가 있어서 성공
    ['txtTest', FAIL, 'noNeed1 exists'] # 파일 내부에 noNeed1이 있어서 실패
    ['txtTest', PASS, 'No error'] # 파일 내부에 need1, need2가 있고 noNeed1, noNeed2가 없어서 성공
    ```

#### 3. ` exec_test(testName, exec, type_='output' ,*args) `
  - 한 줄의 명령어를 실행하고 결과를 확인하는 함수
  - 인자
    - 0 : 테스트 이름
    - 1 : 실행할 명령어
    - 2 : 
      - output : 명령어 실행 결과 문자열을 확인
      - file : 명려어 실행 후 파일 존재 확인
    - 3 :
      - 2가 output : output 에 포함되어야 하는 문자열(여러 문자열 입력가능)
        - ex. exec_test('cat test', 'cat /root/test.txt', 'output', `'need1' ,'need2', '...'`)
      - 2가 file : 확인이 필요한 파일 경로
        - ex. exec_test('touch test', 'touch /root/test.txt', 'file','test.txt')
  - 반환값(리스트)
    - 0 : 테스트 이름
    - 1 : 테스트 결과
      - output : 
        - PASS : 포함되어야하는 문자열이 모두 포함되어있을 경우
        - FAIL : 하나의 문자열이라도 포함되어있지 않을 경우
      - file : 
        - PASS : 파일이 존재
        - FAIL : 파일 미존재
    - 2 : 테스트 메세지(오류가 있을 경우엔 어디서 오류가 발생했는지)
  - 사용법
    ```
    import linux_regression.__import__ as reg # 고정
    '''
    /root/test.txt
    need1
    need2

    noNeed1
    noNeed2
    '''    
    var1 = reg.exec_test('cat test', 'cat /root/test.txt', 'output','need3'))
    var2 = reg.exec_test('cat test', 'cat /root/test.txt', 'output','need1'))
    var3 = reg.exec_test('touch test', 'touch /root/test.txt', 'file','test.txt'))
    var4 = reg.exec_test('touch test', 'touch /root/test.txt', 'file','test1.txt'))
    print(var1)
    print(var2)
    print(var3)
    print(var4)
    ```
    ```
    ['cat test', FAIL, 'need3'] # test.txt 파일 내부에 need3 문자열 없음
    ['cat test', PASS, 'No error'] # test.txt 파일 내부에 need1 문자열 있음
    ['touch test', PASS, 'test.txt is exist'] # test.txt 파일 존재
    ['touch test', FAIL, 'test1.txt doesn't exist'] # test1.txt 파일 미존재
    ```

## 함수명, 변수명 규칙
  - 함수명 : snake_case
  - 젠킨스 변수 : UPPER_SNAKE_CASE
  - 나머지 변수 : lowerCamelCase