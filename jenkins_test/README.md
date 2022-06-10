#### 젠킨스에서 자동화 테스트를 진행하기 위한 소스코드입니다.

-----------------------------------
##### 내용 설명
  * auto : 패키지, 데몬, 기본기능, 메타데이터를 자동으로 테스트하기 위한 소스코드를 모아놓은 폴더 
  * manual : auto를 통해 실패했던 결과를 성공시키기 위한 수동으로 테스트하기 위한 소스코드를 모아놓은 폴더
  * Python_Grammar.md : 자동화 소스코드에서 자주 사용하는 문법들에 대한 설명
  * requirements.txt : 자동화를 위해 필요한 파이썬 라이브러리를 저장하는 파일
  * .gitignore : git 에 commit 하지 않는 파일들

#### 로컬 테스트(윈도우 기준)

-----------------------------------
##### 1. python3 버전 설치(jenkins python 버전은 3.6.8) 
  * https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe (인터넷에 붙여넣기시 자동 다운로드)
  * 설치시 Add to Path 추가 필수
##### 2. cmd 창에 (pip가 안될 경우 pip3)
```
    ## path 에 추가가 되어있어야함
    python -m pip install --upgrade pip 
    python -m pip install paramiko 
```
##### 3. 원하는 위치에서 cmd 창에 (직접 GitLab에서 다운받아도 됨)
```
    git clone http://192.168.105.140/cloudqa/prolinux-automation.git
```
##### 4. ` prolinux-automation/jenkins_test/auto ` 폴더로 들어가기

##### 5. ` auto/__common__/__parameter__.py ` 에서 IN_JENKINS else 부분 상수값 변경
```
ex)
    ...
    HOST_IP = '192.168.17.34' ## -> 본인 테스트용 IP로 변경
    ...
```
##### 6. 파이썬 편집도구를 이용하여 각 파일 테스트(로컬, 젠킨스 모두 같은 코드로 빌드 가능)
 - 커맨드라인에서 python 파일명.py 입력시 테스트 실행
 - 소스코드 위치 : jenkins_test/auto
   - auto
     - ` main.py ` : 전체 코드 실행용 파일
   - auto/tests
     - ` auto_package.py ` : 패키지 테스트용 코드(전체 제거 -> 전체 설치 순서로 진행)
     - ` auto_daemon.py ` : 데몬 테스트용 코드(하나의 데몬 start 또는 stop -> stop 또는 start -> 다른 데몬 순서로 진행)
     - ` auto_cmd.py ` : 기본 기능 테스트용 코드
     - ` auto_metadata.py ` : 메타데이터 체크하는 파일(Vendor, Packager, Build host)
     - ` auto_package_install.py ` : 패키지 설치만을 위한 코드

##### 7. 로컬 레포지토리는 ` __parameter__.py ` 에서 LOCAL_REPOSITORY 를 true로 설정하면 됨

-----------------------------------
### 테스트 도구
  * IDLE 사용시 파일명.py 우클릭 Edit with IDLE 클릭 후 편집화면에서 F5키 입력 시 빌드 시작
  * VSCode 사용시 Extensions에서 python 설치 후 F5키 입력 후 Python 클릭 시 빌드 시작
  * Atom 사용시 script 설치 후 ctrl + shift + b 입력 시 빌드 시작
