### Package Install Test

from __import__ import *
from __common__.__repository__ import *
import auto_package as ap



def pkgInstall(reinstall=False):
    if reinstall == True:
        command = 'reinstall'
    else:
        command = 'install'
    
    resultList = [['Package', '%s'%command, 'Message']]
    resultList = ap.pkgProcess('%s'%command, PACKAGE_ALL_INSTALL_FILE, resultList, 1)
    resultList = ap.rpmCheck('%s'%command, PACKAGE_ALL_INSTALL_FILE, resultList, 1 ) ## install 하고 rpm 체크

    exportCSV(resultList, PACKAGE_ALL_INSTALL_RESULT_FILE, None)
    # rpm 체크하여 최종결과 저장
    numOfPFS('PACKAGE %s'%command.upper(), getTotalinList(resultList, 1))    
    #[0].append([getTotalinList(resultList, 1).count(PASS), getTotalinList(resultList, 1).count(FAIL), getTotalinList(resultList, 1).count(SKIP)])

def main():

    if PACKAGE_ALL_INSTALL_TEST == 'true':
        printSquare('Package Install Test')
        pkg_start = time.time()

        ## 네트워크 정보 백업
        th = testHelper()
        th.ip_backup()
        if PROCESS_KILLER == 'true':
            ## 백그라운드에서 process killer 실행
            pi1 = threading.Thread(target = th.proc_killer, args=('package',))
            pi1.start() ## cpu saver 실행

        commandExec(execMode, INSTALL_PKG + ' clean all')    

        if PACKAGE_RE_INSTALL == 'true':
            pkgInstall(reinstall=True)
        else:
            pkgInstall(reinstall=False)

        if PROCESS_KILLER == 'true':
            pi1.do_run = False
    
        th.ip_cloudInit()
        sshd_config()

        h, m, s = secToHms(pkg_start, time.time())
        print("* Package Install Running Time : %dh %dm %.2fs"%(h, m, s))

if __name__ == '__main__':

    main()

    if IN_JENKINS == None and execMode != 'shell':
        execMode.close()
        #print("ssh closed")