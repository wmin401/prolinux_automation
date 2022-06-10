# local repo에서 얻는 방법
#!/bin/bash
file=$1
while read line; do
  rpm -qp --qf '%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH};%{BUILDHOST};%{VENDOR};%{PACKAGER};\n' $line
done < $file
# 설치되지 않은 패키지에 대해 정보 얻기, 이때의 $line은 local에 마운트된 디렉토리를 list화해서 넣고 rpm 파일들을 복사한 후 그 폴더에서 진행하기

# 개별 패키지에 대해서 정보 얻는 방법
# echo $(rpm -qa --queryformat '%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH};%{BUILDHOST};%{VENDOR};%{GROUP};%{SUMMARY}\n' $line)
# echo $(rpm -qa --queryformat '%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH};%{BUILDHOST};%{VENDOR};%{PACKAGER}\n' $line)
# 이 때의 $line은 순수한 패키지 이름만 넣어주기(ex. acl(O), acl-2.2.51-14.el7.x86_64(X))
# 이름만 추출하기 : rpm -qa --queryformat '%{NAME}\n' | sort > test_list
# vendor_check.csv와 같은 파일로 만들고 구분자를 ;(세미콜론)으로 하기

# 설치된 모든 패키지에 대한 정보는 간단한 명령어를 통해 얻을 수 있음
# 예시
# rpm -qa --queryformat '%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH};%{BUILDHOST};%{VENDOR};%{PACKAGER}\n' | sort | tee vendor_check_list.xlsx

# 설치된 개별 패키지에 대해 정보 얻기, 이때의 $line은 local에 마운트된 디렉토리를 list화해서 넣고 rpm 파일들을 복사한 후 그 폴더에서 진행하기
# 예시)
# rpm -q --qf '%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH};%{BUILDHOST};%{VENDOR};%{PACKAGER};\n' $line
