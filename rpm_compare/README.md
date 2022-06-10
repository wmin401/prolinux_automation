# RPMcompare 사용법(windows)

## 기본 설치

1. 기본 라이브러리 설치(BeautifulSoup4, requests, paramiko)
* ` install.bat ` 실행하기 또는 아래 명령어 직접 명령 프롬포트에 입력
```
    > python -m pip install --upgrade pip
```
```
    > python -m pip install bs4 requests paramiko
```
  - BeautifulSoup4(bs4), requests : remote repository parsing 
  - paramiko : ssh connection

2. ` RPMcompare.py ` 실행

3. 파일 및 레포지토리 주소 입력
  - 신규 버전(기준) : 찾기 버튼 클릭하여 iso 파일 선택 또는 iso 파일 경로 직접 입력
  - 이전 버전 + 원격 레포지토리 모두 비교하고 싶을 경우
    - 이전 버전 : 찾기 버튼 클릭하여 iso 파일 선택 또는 iso 파일 경로 직접 입력(이전과 동일)
    - 원격 레포지토리 주소 : 원격 레포지토리의 주소 입력(레포지토리 이름 앞 주소 까지)
      - 마지막에 '/' 가 있어도 되고 없어도됨

4. compare 버튼 클릭

5. 결과 csv 생성
  - 이전 버전 비교는 ` compare_local_월일_시분초.csv ` 로 생성

6. package_changed.txt로 차이가 있는 패키지 저장됨