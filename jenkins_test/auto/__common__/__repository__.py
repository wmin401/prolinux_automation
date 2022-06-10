
from __common__.__module__ import *
from __common__.__logger__ import *
from __common__.__print__ import *

## repository 생성하는 함수
class Repository:  ## 하나의 repository 클래스는 하나의 .repo 파일 관리자
    def __init__(self, file):  ## 
        self.file = file

    def addRepo(self, *args):
        output, error = commandExec(execMode, 'ls /etc/yum.repos.d/' + self.file + '.repo')
        
        # if output != [] and output[0] == '/etc/yum.repos.d/' + self.file+'.repo':
        #     print("* Same repository is already exists ...")
        #     print("* Deleting existed repository ...")            
        #     commandExec(execMode, 'rm -rf /etc/yum.repos.d/' + self.file + '.repo')           
        print("* Creating new repository " + self.file + ".repo")
        commandExec(execMode, 'touch /etc/yum.repos.d/' + self.file + '.repo')
        
        print("* Add repository " + str(args[1]) +" in " + self.file + '.repo')
        commandExec(execMode, "echo [" + str(args[0]) + "] >> /etc/yum.repos.d/"+str(self.file)+'.repo')
        commandExec(execMode, "echo name=" + str(args[1]) + " >> /etc/yum.repos.d/"+str(self.file)+'.repo')
        commandExec(execMode, "echo baseurl=" + str(args[2]) + " >> /etc/yum.repos.d/" + str(self.file)+'.repo')
        if args[3] != None:
            commandExec(execMode, "echo gpgkey=" + str(args[3]) + " >> /etc/yum.repos.d/" + str(self.file)+'.repo')
        commandExec(execMode, "echo gpgcheck=" + str(args[4]) + " >> /etc/yum.repos.d/" + str(self.file)+'.repo')
        commandExec(execMode, "echo enabled=" + str(args[5]) + " >> /etc/yum.repos.d/" + str(self.file)+'.repo')
        #commandExec(execMode, "echo ' ' >> /etc/yum.repos.d/" + str(self.file)+'.repo')
        ## header, name, baseurl, gpgkey, gpgcheck, enabled
        
    def removeRepo(self):
        print("* Removing repository " + str(self.file) + '.repo')
        commandExec(execMode, "rm -r /etc/yum.repos.d/"+str(self.file)+'.repo')


    def printRepo(self):
        # 레포지토리 출력
        output, error = commandExec(execMode, "cat /etc/yum.repos.d/"+str(self.file)+'.repo')
        printBeautify(output)


    def disableRepo(self, repoFile):        
        # 레포지토리 비활성화
        output, error = commandExec(execMode, 'grep -r "enabled" /etc/yum.repos.d/' + repoFile + '.repo')                
        if output == []: ## output이 없을 때, 즉 enabled가 없을때
            commandExec(execMode, "sed -i'' -r -e" + ' "/gpgcheck/a\enabled=0"' + " /etc/yum.repos.d/"+repoFile + '.repo')
            print("* Added enabled=0 into /etc/yum.repos.d/" + repoFile + ".repo")  #gpgcheck=1 아래에 enabled=0을 넣는다.
        elif 'enabled=1' in output[0]: ## enabled=1이 있을 경우 0으로 바꿈
            commandExec(execMode, 'find /etc/yum.repos.d/ -name "' + repoFile + '.repo" -exec sed -i "s/enabled=1/enabled=0/g" {} \;')
            print("* enabled=1 to enabled=0 in /etc/yum.repos.d/"+repoFile+".repo")  ##1을 0으로 바꾼다.
        elif 'enabled=0' in output[0]: ## enabled=0인 경우 그대로
            pass
        else:
            print("* What kinds of case is this ??")

    ## addRepo에 포함되지 않은 속성을 추가하고싶을 때 사용
    ## 제일 하단에 추가되기 때문에 위치를 잘 맞춰야한다. 
    ## addRepo 바로 뒤에 사용
    def addProperty(self, property, value):
        line = str(property) + '=' + str(value)
        commandExec(execMode, "echo '" + line + "' >> /etc/yum.repos.d/" + str(self.file)+'.repo')