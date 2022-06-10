## 테스트 실행  

if [ $MAJOR_VERSION == '7' ]; then
	source /root/.bash_profile > bash_profile.log 2>&1
fi

python --version

SRC_FOLDER=$(find /home/jenkins/workspace/$PROJECT_NAME -name jenkins_test -type d)
cd $SRC_FOLDER/auto

python main.py