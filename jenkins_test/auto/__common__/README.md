1. `__module__.py` : 공통적으로 사용되는 함수를 모아 놓은 파일
2. `__parameter__.py` : 공통적으로 사용되는 변수를 모아 놓은 파일
3. `__csv__.py` : csv 저장에필요한 함수를 모아놓은 파일
4. `__repository__.py`: 레포지토리 관련 클래스 파일
5. `__helper__.py` : 테스트헬퍼 클래스 파일
6. `__local__.py` : 로컬 레포지토리 설정을 위한 클래스 파일
7. `__print__.py` : 출력을 위한 함수를 모아놓은 파일
8. `__exception__.py`: 예외처리를 위한 함수를 모아놓은 파일(아직 미적용)
9. `__junit__.py`: testlink 연결에 필요한 junit을 생성하는 클래스 파일
10. `code_sample.py`: 테스트에 사용했던 코드를 모아놓은 파일

# Repository 클래스 설명
- Repository를 생성 및 삭제할 수 있는 클래스이다. 
- 클래스 생성시 파일명만 입력하면 파일이 생성된다. (.repo 는 입력하지 않는다.)
- addRepo 함수로 파일 내부에 레포지토리를 추가한다.
  - addRepo 함수의 매개변수는 아래와 같으며, 순서대로 입력해야한다. 
    - 이름 : repository 제일 상단에 보여지는 이름
    - 표시이름 : name
    - 주소 : baseurl
    - 서명키주소 : gpgkey(None을 입력할 경우)
    - 서명키 사용여부 : gpgcheck
    - 활성화 : enabled
- ex)
```
# repository 클래스 선언 및 repository 파일 생성
SUPERVMRepo = repository('SUPERVM') # 레포지토리 클래스 선언시 파일 생성됨
SUPERVMRepo.addRepo(
    'SUPERVM', 
    'SUPERVM',
    'SUPERVM',
    'http://pldev-repo-21.tk/prolinux/ovirt/4.4/el8/x86_64/',
    None,
    0,
    1                      
) ## 레포지토리 추가
```
# 결과 /etc/yum.repos.d/SUPERVM.repo
```
[SUPERVM]
name=SUPERVM
baseurl=http://pldev-repo-21.tk/prolinux/ovirt/4.4/el8/x86_64/
gpgcheck=0
enabled=1
```
# Repository 함수 설명
1. `addRepo` : header, name, baseurl, gpgkey ,gpgcheck, enabled 6개의 인자를 이용하여 레포지토리를 생성한 레포지토리 파일에 추가한다.
2. `removeRepo` : 생성한 레포지토리 파일을 삭제한다.
3. `printRepo` : 생성된 레포지토리를 출력한다. 
4. `appProperty` : 제일 하단에 원하는 속성을 추가한다.(인자로 key, value를 받는다.)

# Repository 클래스 사용 방법
### repository.py import 및 클래스 선언
```
from __common__.repository import *
testRepo = Repositroy('test')
```

### 파일 생성 및 레포지토리 정보 입력
```
testRepo.addRepo(
    'testHeader',
    'testName',
    'http://pldev-repo-21.tk/prolinux/ovirt/4.4/el8/x86_64/',
    None,
    0,
    1            
)
```

### 생성된 파일 출력
```
testRepo.printRepo()
```

### 속성 추가
```
testRepo.addProperty('test',1)
```

### 파일 삭제
```
testRepo.removeRepo()
```