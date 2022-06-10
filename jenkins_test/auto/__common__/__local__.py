
from __common__.__module__ import *
from __common__.__repository__ import *
from __common__.__logger__ import *

class LocalRepository:
    def __init__(self):
        self.repo = Repository('local')
        
        outupt, error = commandExec(execMode, 'rpm -q wget')
        if 'not installed' in outupt[0]:
            print("* Installing wget ...")
            commandExec(execMode, INSTALL_PKG + ' install wget -y')

    def mount(self, filename, folderPath):
        # iso파일을 마운트
        if existPath(folderPath) == True:
            print("* Deleting exist folder ...")
            commandExec(execMode, 'umount -f ' + folderPath)        
            commandExec(execMode, 'rm -rf ' + folderPath)        
            
        print("* mount folder creating ...")
        commandExec(execMode, 'mkdir -p ' + folderPath)        

        print("* ISO file mounting ...")
        output, error = commandExec(execMode, 'mount -o loop /root/' + filename + ' ' + folderPath) 
        if 'already' in error[0] or 'failed' in error[0]:
            print("* Mount failed ...")

    def inputRepo(self, folderPath): ## path, header, name, baseurl, gpgkey, gpgcheck, enabled
        # 레포지토리파일에 레포지토리 추가
        if MAJOR_VERSION == '7':
            repoList = ['Base']   
        elif MAJOR_VERSION == '8':
            repoList = ['BaseOS', 'AppStream']

        for repo in repoList:
            self.repo.addRepo(
                'local_'+repo,
                'local_'+repo,
                'file://' + folderPath + '/' + repo + ' >> /etc/yum.repos.d/local.repo',
                'file:///etc/pki/rpm-gpg/RPM-GPG-KEY-prolinux-' + MAJOR_VERSION + '-release',
                1,
                1            
            )

    def umount(self, folderPath, remove): # umount and remove(if want)
        # 언마운트
        commandExec(execMode, 'umount -f ' + folderPath)
        if remove == True:
            commandExec(execMode, 'rm -rf ' + folderPath)

    def getISO(self, filename, url, path):
        # iso파일 다운로드
        if existPath('/root/' + filename) == False:
            print("* ISO file downloading ...")
            commandExec(execMode, 'wget -q -c --tries=10 '+ url + ' -P ' + path)

    def removeISO(self, filename, path):
        # iso 파일 삭제
        commandExec(execMode, 'rm -rf ' + path + '/' + filename)
  
    def disableRepo(self, repoFile):        
        # 매개변수로 받은 레포지토리파일의 enabled를 0으로 변경
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
            print("What kinds of case is this ??")

    def enableRepo(self, repoFile):
        # 매개변수로 받은 레포지토리파일의 enabled 를 1로 변경
        #print('* find /etc/yum.repos.d -name "' + repoFile + '.repo" -exec sed -i "s/enabled=0/enabled=1/g" {} \;')        ## enable 0 to 1
        commandExec(execMode, 'find /etc/yum.repos.d -name "' + repoFile + '.repo" -exec sed -i "s/enabled=0/enabled=1/g" {} \;')                
        print("* Change enabled=0 to enabled=1 in " + repoFile)

    def removeLocalRepo(self):
        self.repo.removeRepo()


localRepo = LocalRepository()

def setLocalRepo():
    global localRepo

    ## 로컬 레포지토리 설정
    print("* Creating local repository ...")
    ## 1) 파일 다운
    localRepo.getISO(IMG_NAME, IMG_DOWNLOAD_ADDR + '/' + IMG_NAME, '/root')
    ## 2) 마운트 
    localRepo.mount(IMG_NAME, MOUNT_FOLDER_PATH)
    ## 3) 레포 설정     
    localRepo.inputRepo(MOUNT_FOLDER_PATH)
    ## 4) ProLinux disable
    #localRepo.disableRepo('ProLinux-Base-beta')         
    commandExec(execMode, INSTALL_PKG + ' update -y')

def unsetLocalRepo():    
    global localRepo
    ## 레포지토리 원상복구     
    localRepo.enableRepo('ProLinux')
    localRepo.removeLocalRepo()
    localRepo.umount(MOUNT_FOLDER_PATH, True) ## folderpath, remove folder
    #localRepo.removeISO(IMG_NAME, '/root')
    print("* Deleting local repository ...")
