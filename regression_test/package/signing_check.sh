file=$1
while read line; do
  rpm --checksig $line
done < $file

# rpm 파일의 gpgcheck signing 확인용 스크립트 파일
# rpm 파일을 인자로 넣어줘야 함
# cp -r mnt/BaseOS/Packages/ mnt/AppStream/Packages/ .
# cp -r mnt/Packages/ .
# local.repo 설정 후 파일을 복사하여 패키지가 있는 위치에서 rpm 리스트를 인자로 넣어 실행하기
