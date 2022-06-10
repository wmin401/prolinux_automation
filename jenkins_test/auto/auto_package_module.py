from __import__ import *

PKG_MODULE_TIMEOUT = 60

def modulePkgInstall():

    eachModuleResultList = []
    allModuleResultList = []

    tmpCsvInit(REALTIME_MODULE_RESULT_FILE, 'module' + DELIM + 'package' + DELIM + 'result' + DELIM + 'message')

    MODULE_FILES = [file for file in os.listdir(PACKAGE_MODULE_FILE_PATH) if file.endswith('.txt')]# 전체 파일 리스트

    for file in MODULE_FILES:
        a_time = time.time()
        printLine()        
        print('* FILE : ' + file)
        moduleInfo = getListinFile(PACKAGE_MODULE_FILE_PATH + '/' + file)
        moduleName = moduleInfo[0][moduleInfo[0].find('[')+1: moduleInfo[0].find(']')]        
        print("* MODULE NAME : " + moduleName.split(":")[0])
        if ':' in moduleName:
            print("* MODULE VERSION : " + moduleName.split(":")[1])

        print('1) Module Reset')
        output, error = commandExec(execMode, INSTALL_PKG + ' module reset -y ' + moduleName, PKG_MODULE_TIMEOUT)


        print('2) Module Enable')        
        if 'Conditions=' in moduleInfo[1]:
            print('[* CONDITIONS *]')
            # 특정 조건이 있는 모듈인 경우
            '''
            0 [모듈이름]
            1 Conditions=(e)모듈활성화,(d)모듈비활성화,(i)패키지설치,(r)패키지삭제
            2 패키지1
            3 패키지2
            4 패키지3            
            5 ...
            '''
            # output, error = commandExec(execMode, INSTALL_PKG + ' module enable -y ' + moduleName)  
            conditions = moduleInfo[1][11:].split(',')
            for condition in conditions:
                if '(e)' in condition: # 모듈 활성화
                    print('[ENABLE MODULE] %s'%(condition[3:]))
                    output, error = commandExec(execMode, INSTALL_PKG + ' module enable -y ' + condition[3:], PKG_MODULE_TIMEOUT)
                elif '(d)' in condition: # 모듈 비활성화
                    print('[DISABLE MODULE] %s'%(condition[3:]))
                    output, error = commandExec(execMode, INSTALL_PKG + ' module disable -y ' + condition[3:], PKG_MODULE_TIMEOUT)
                elif '(R)' in condition: # 모듈 리셋
                    print('[RESET MODULE] %s'%(condition[3:]))
                    output, error = commandExec(execMode, INSTALL_PKG + ' module reset -y ' + condition[3:], PKG_MODULE_TIMEOUT)
                elif '(i)' in condition: # 패키지 설치
                    print('[INSTALL PACKAGE] %s'%(condition[3:]))
                    output, error = commandExec(execMode, INSTALL_PKG + ' install -y ' + condition[3:], PKG_MODULE_TIMEOUT)
                elif '(r)' in condition: # 패키지 삭제
                    print('[REMOVE PACKAGE] %s'%(condition[3:]))
                    output, error = commandExec(execMode, INSTALL_PKG + ' remove -y ' + condition[3:], PKG_MODULE_TIMEOUT)
                else: # 조건 외에 다른 것이 있다 -> 리스트가 잘못된 것이지만 테스트는 진행 -> 현재 모듈 활성화
                    pass                
                # output, error = commandExec(execMode, INSTALL_PKG + ' module enable -y ' + moduleName)  
            idx = 2

        else:             
            idx = 1
        for i in range(2):
            output, error = commandExec(execMode, INSTALL_PKG + ' module enable -y ' + moduleName, PKG_MODULE_TIMEOUT)  
            time.sleep(2)
        
        # idx는 패키지리스트의 시작 줄
        print('3) Start Install Package')
        for i in range(idx,len(moduleInfo)):
            printLine()
            eachModuleResultList = []
            print('PACKAGE : ' + moduleInfo[i])
            modResult = FAIL
            modMsg = ''
            moduleInfo[i] = moduleInfo[i].replace('\n','')
            output, error = commandExec(execMode, INSTALL_PKG + ' install -y ' + moduleInfo[i], PKG_MODULE_TIMEOUT)
            
            if output != []:
                for k in output:
                    if 'already installed' in k or 'Complete!' in k: 
                        modResult = PASS
                        modMsg = 'module enable'
                
            if error != []:                
                if 'rpmdb' in error[0]:
                    commandExec(execMode, 'rm -f /var/lib/rpm/_db*')
                    commandExec(execMode, 'rpm -vv --rebuilddb')
                    commandExec(execMode, 'sleep 15')
                    commandExec(execMode, 'systemctl start fapolicyd')
                    print('Start fapolicyd')
                elif 'fapolicyd.fifo' in error[0]:
                    commandExec(execMode, 'systemctl start fapolicyd') ## pipe does not exist error
                    print('Start fapolicyd')
                elif 'unfinished transactions remaining' in error[0]:
                    commandExec(execMode, 'yum-complete-transaction --cleanup-only')
                    print('Transaction cleanup')
                ###########################################################################################################
                modResult = FAIL
                modMsg = mergeMsg(error)

            print("RESULT : " + modResult)
            print("MESSAAGE : " + modMsg)
            eachModuleResultList = saveResult(eachModuleResultList, moduleName, moduleInfo[i], modResult, modMsg)
            saveCSV(eachModuleResultList, REALTIME_MODULE_RESULT_FILE) # 실시간 결과 저장
            allModuleResultList.append(eachModuleResultList)
            printLine()

        ## 하나의 모듈 끝날때마다 RPM 체크 
        print("* Rpm -q check")
        for i in range(idx, len(moduleInfo)):
            cnt = 0
            for each in allModuleResultList: 
                if moduleInfo[i] in each:
                    output, error = commandExec(execMode, 'rpm -q ' + moduleInfo[i], PKG_MODULE_TIMEOUT)
                    if output != [] and 'not installed' in output[0]:
                        if allModuleResultList[cnt][2] == PASS:
                            print(allModuleResultList[cnt])
                            allModuleResultList[cnt][2] = FAIL
                            allModuleResultList[cnt][3] = 'rpm check failed'                    
                            print(allModuleResultList[cnt])
                cnt += 1


        h, m, s = secToHms(a_time, time.time())
        print("* %s Module Package Test Running Time : %dh %dm %.2fs"%(moduleName, h, m, s))
    return allModuleResultList

def main():

    if PACKAGE_MODULE_TEST == 'true':
        printSquare('Package Module Test')
        pkg_mod_start = time.time()

        ## 네트워크 정보 백업
        th = testHelper()
        th.ip_backup()
        if PROCESS_KILLER == 'true':
            ## 백그라운드에서 process killer 실행
            pm1 = threading.Thread(target = th.proc_killer, args=('package',))
            pm1.start() ## cpu saver 실행

        resultList = modulePkgInstall()
    
        if PROCESS_KILLER == 'true':
            pm1.do_run = False

        # 결과 저장
        exportCSV(resultList, PACKAGE_MODULE_RESULT_FILE,'module' + DELIM + 'package' + DELIM + 'result' + DELIM + 'message')

        h, m, s = secToHms(pkg_mod_start, time.time())
        print("* Module Package Test Running Time : %dh %dm %.2fs"%(h, m, s))


if __name__ == '__main__':

    main()

    if IN_JENKINS == None and execMode != 'shell':
        execMode.close()
        #print("ssh closed")
