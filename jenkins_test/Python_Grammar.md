자동화에 사용된 Python 기본 문법 정리

0. 아래 사용된 문법들은 가장 기초만을 나타내는 것이며, 더 심화적인 방법도 있다는 것을 참고하기 바랍니다.
- https://wikidocs.net/book/1 자세한 내용은 사이트 참조
1. 변수
- 변수 선언 자체가 없다.
- 변수 선언과 동시에 값 할당
- boolean 값은 True와 False로 사용한다.
ex)
```
    a = 1
    b = 'abc'
    ab = [1,2,3]
    save = True
    funcCount = 0    
    RESULT_FILE = open('JenkinsTest/results/package_result.csv', "wt", encoding="UTF8")
```
- 전역 변수(global) : 전역 변수 생성 후 원하는 함수 내부 상단에 ` global 변수 `를 입력한다.
```
    funcCount = 1
    def packageTest(ssh, remove, install):
        global funcCount
        funcCount = 0
```

2. 연산
```
    'a' + 'b' -> 'ab' # 문자 + 문자(가능)
    'a' * 3 -> 'aaa' # 문자 * 숫자(가능)
    'a' + 3 -> X # 문자 + 숫자(불가능)
```


3. 입출력
```
    a = input('여기에 텍스트 입력 가능') # 입력 : 입력한 문자를 문자열로 읽어옴
    b = int(input('텍스트 입력 가능')) # 숫자를 입력받기 위해서는 int(input()) 으로 하면된다.
    print('여기에 텍스트 입력') # 출력
```
-  출력시 변수를 사용하고 싶을 때
```
    print(a + ' text ' + b)  # a와 b는 변수이며 문자열만 가능하다.(a와 b가 숫자일경우엔 str(a) 함수 사용)
    print("%d text %d"%(a,b)) # %d와 같은 포맷 스트링을 사용하고 싶을 때는 ""뒤에 %()를 사용한다.
    print("Package Test Running Time : %dh %dm %.2fs"%(h, m, s))
```
- print문에는 항상 \n가 포함되어있어서, 하나의 print문이 끝나면 줄내림이 된다. 줄내림을 원치 않을 경우엔 ` end ` 매개변수를 사용한다.
```
    ## print문의 end 매개변수는 기본값으로 \n을 갖고 있다. 따라서 end의 \n을 직접 다른 값으로 바꿔주면된다.
    print(1)
    print(2)
    ## 출력시
    1
    2
    
    print(1, end = '!!')
    print(2)
    ## 출력시
    1!!2
```

4. 들여쓰기
- 파이썬 에서는 {} 대신 들여쓰기로 범위를 나타낸다. 보통 입력시 Tab 키를 많이 이용하며, 편집도구에 따라 차이가 있지만 2칸 또는 4칸을 많이 사용한다.
```
    a = 1  #범위 1
    b = 2  #범위 1
    ····c = 3  #범위 2
    ····d = 3  #범위 2
    if a == 1 :
    ····print('a는 1이다') # if 안에 포함된 내용
    else :
    ····print('a는 이 아니다') # else 안에 포함된 내용
    print(a) # if또는 else에 포함되지 않는다.
```

5. 분기문
- 분기문은 if else를 사용한다. 문법은  ` if (조건식) : ` 이다.
- 입력시 ` :(콜론) ` 이 입력되지 않으면 오류가 발생한다. 파이썬 에서는 : 로 조건을 구분한다.
- 들여쓰기로 범위를 표현한다.
- ` if `
  - 조건식의 값이 참일 경우엔 if 문 내부로 들어가서 명령어를 실행한다.
  - 아래는 조건식에서 사용 가능한 비교 연산자의 예시이다.
```
    if a > 1 :
    if b <= 1 :
    if c >= 1 :
    if d == 1 :
    if e != 1 : 또는 if not e == 1 :
```
```
    a = 1
    if a == 1:
        print('a는 1')  ## 실행시 a는 1이 출력된다.
```
- ` if else `
  - if 의 조건식의 값이 참이 아닐때, else가 있다면 else 내부로 들어가게 된다.
  - if와 else 사이에는 다른 명령이 있으면 안된다.
```
    a = 2
    if a == 1:
        print('a는 1')
    else:
        print('a는 1이 아니다.') ## 실행시 a는 1이 아니다가 출력된다.
```
- ` if elif (+ else) `
  - if와 else사이에 elif 가 있을 경우 else를 가기전 elif의 조건식을 먼저 따져본다.
  - if의 조건식이 거짓이고, elif의 조건식이 참일 경우 elif의 내부 명령어를 실행한다.
```
    a = 2
    if a == 1:
        print('a는 1')
    elif a == 2:
        print('a는 2') ## 실행시 a는 2가 출력된다.
    else:
        print('a는 1이나 2가 아니다.') ## else문은 있는 것이 좋지만, 없어도 실행하는 것에는 문제가 없다.
```
- ` try except `
  - 원하는 조건 자체가 성립되지 않을 때 사용(리스트의 경우 길이가 달라질때가 있으므로, 항상 고정으로 인덱스를 사용하기 원할 때 자주 사용)
  - try 내부의 명령어가 실패했을 때 except가 실행된다.
  - except는 다양한 오류를 포함할 수 있다.
```
    a = [1,2,3]  ## 길이가 3인 리스트
    try :
        if a[3] == 4 : # a는 길이가 3이기 때문에 최대 인덱스는 2이다. 따라서 해당 조건은 성립되지 않음(파이썬 자체에서 오류를 내버림)
            print("a[3]은 4다")
    except:
        print("a[3]은 4가 아니다.")
    
    try:
        error = stderr.readlines()
    except socket.timeout as e:  # as e는 오류를 e라는 변수에 저장하여 사용한다는 뜻이다. e를 출력할 경우 오류 문구가 출력된다.
        print("RESULT : " + FAIL)
        print("MESSAGE : socket timeout 30s")
        result.append(FAIL)
        result.append('socket timeout 30s')
        return result
    
    # try except는 위와같은 상황에서만 쓰이는 것이 아님
    # 위는 하나의 예시이며, 자동화 코드에서는 저렇게 사용 중
```

- 논리연산자 : ` and , or , not ` 으로 사용한다.
  - 원하는 조건의 반대값을 원할 경우 not을 앞에 붙여서 사용한다.
```
    if a >= 1 and b <= 1:
        print(a,b)
    
    if c == True or d == True:
        print(c,d)
    
    if not a == 1:
        print('a는 1이 아니다')
```
- ` in `
  - in 은 뒤에 나오는 리스트 또는 문자열 내부를 검색할 수 있는 기능이다.
```
    string = 'This is text'
    if 'text' in string:  # string 변수의 할당되어있는 문자열 안에 'text'가 있는지 확인한다.
        print(True)
    else:
        print(False)
```
6. 반복문
- ` while `
  - ` while (조건식) : ` 에서 조건식이 참일 경우 반복문을 수행한다.
  - 조건식이 True 일 경우엔 무한 반복
  - 분기문과 마찬가지로 들여쓰기로 범위를 표현한다.
```
    a = 1
    while a < 5 :
        print(a)
        a = a + 1
```    
- ` for `
  - 범위를 정해서 사용하는 반복문이다.
  - 가장 기본적인 사용 방법은 ` for 변수 in 리스트 : ` 이다.
  - ` range() ` : 최대 3개의 매개변수를 이용하여 숫자로된 리스트를 반환한다.
    - range(1,10,2) : 1이상 10미만의 숫자로 리스트를 생성하되, 1에서 2씩 증가한다. -> [1,3,5,7,9] 를 반환한다.
    - ` 기본 시작값은 0 `이고, `기본 증강값은 1 `이다. ex) ` range(5) == range(0,5,1) ` , ` range(0,4) == range(0,4,1) `
  - ` 변수 ` 는 리스트의 0번째부터 마지막까지 인덱스의 값을 할당받는다.
```
    lst = [1,'a',True]
    for i in lst:
        print(i)
    ## 출력
    1
    a
    True
    
    for j in range(0,5):
        print(j)  
    ## 출력
    1
    2
    3
    4
    5
```
- ` break, continue `
  - ` break ` 와 ` continue ` 는 반복문에서만 사용 가능한 명령어이다.
  - ` break ` 는 명령어가 사용될 경우 포함된 반복문을 벗어나게 해주는 명령어이다.
  - ` continue ` 는 명령어가 사용될 경우 포함된 반복문에서 continue 외부에 있는 모든 명령어는 무시하고, 반복문의 제일 상단 명령어로 돌아간다.
```
    for i in range(0,5):
        if i <2 :  ## i가 2보다 작을 때
            print(i)
        else:
            break  ## i가 2보다 크거나 같을 때(i가 2가 됐을 때, break 명령어를 만나서 해당 반복문인 for문을 벗어난다.)
    ## 출력
    0
    1

    for i in range(0,5):
        if i == 2 :  ## i가 2와 같을 때, continue를 만났기 때문에 나머지 명령어는 무시하고, 가장 위로 올라간다.
            continue
        else :
            print(i)  

    ## 출력
    0
    1
    3
    4
```
7. 함수
- 함수는 크게 4개의 함수로 볼 수 있다.
- ` 매개변수 X, 반환값 X `
```
    def printFunc():
        print("-----")
        print("print")
        print("-----")
```
- ` 매개변수 X, 반환값 O `
```
    def printFunc():
        a = 1
        b = 2
        c = a + b
        return c
```
- ` 매개변수 O, 반환값 X `
```
    def printFunc(num):
        b = 2
        c = num + b
        print(c)
```
- ` 매개변수 O, 반환값 O `
```
    def printFunc(num):
        b = 2
        c = num + b
        return c
```

8. 자주 사용되는 함수 및 메소드
- ` str() `
  - 괄호 안에 포함된 변수 또는 문자가 아닌 상수를 문자열로 변환해준다.(단순히 해당 상수에 ''를 씌워준다고 생각하면 된다.)
```
    a = 123     ## 출력시 123, type은 int
    b = str(a)  ## 출력시 123, type은 str
```
- ` int() `
  - 괄호 안에 포함된 변수 또는 문자를 정수로 변환해준다. (숫자 문자열만 가능)
  - 숫자가 아닌 문자열을 입력했을 경우 오류 발생 ` ValueError: invalid literal for int() with base 10 `
```
    a = '123'     ## 출력시 123, type은 str
    b = int(a)    ## 출력시 123, type은 int
```
- ` len() `
  - 괄호 안에 포함된 리스트의 길이를 반환해준다.
```
    a = [1,2,3,4]
    b = len(a)    ## 출력시 4
```
- ` find() `
  - string 에서 특정 문자열의 가장 앞 인덱스를 반환해준다.
```
    a = 'Python is good'  
    # 문자열 |P|y|t|h|o|n| |i|s| |g |o |o |d |
    # 인덱스 |0|1|2|3|4|5|6|7|8|9|10|11|12|13|
    b = a.find('is')  # 출력시 7 (i의 인덱스가 7)
```
- ` replace() `
  - 2개의 매개변수를 입력받으며, 첫번째 매개변수를 찾아서 두번째 매개변수로 변경해준다.
  - 변경된 값을 저장하기 위해서는 변수에 값을 할당해야한다.
```
    a = 'Python is good'
    b = a.replace('Python','Dongill')  # 출력시 Dongill is good
```

9. 파일 입출력
- ` open() `
  - 매개변수 : 파일경로, 모드, 인코딩(더 있으나 여기선 3개만 사용)
  - 파일 입출력에 대한 자세한 설명은 https://wikidocs.net/16077 참고
- ` write() `
  - 열려있는 파일에 값을 입력한다.
- ` close() `
  - 파일을 닫는다.
  - 파일을 열고, 작성 후 닫지 않으면, 값이 파일에 입력되지 않는다.
  - 파일을 열었을 경우엔 항상 닫아줘야한다.
```
    packageList = open('JenkinsTest/results/test.csv', 'r',encoding="utf-8")
    packageList.write('패키지, 결과, 비고\n')  ## 줄내림을 입력하지 않으면 한줄로 입력된다.
    packageList.close()
```
10. ` import `
- 자주 사용하는 라이브러리
```
    import os
    import sys
    import time
    import paramiko
```
- 직접 만든 코드 import
```
    from 폴더경로 import 파일명
```
- as
  - as는 라이브러리 명이 길때나 본인이 원하는 이름을 사용하기 월할 때 해당 라이브러리 뒤에 ` as 이름 ` 으로 붙여서 사용한다.
```
    from auto import __common__ as com
```

11. 편집 도구
- IDLE
- ` VSCODE(추천) `
- ` Atom(추천) `
- Shell
- Sublimetext
- notepad 등 ...
