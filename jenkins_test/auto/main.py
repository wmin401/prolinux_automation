
import auto_package as ap
import auto_daemon as ad
import auto_daemon_pre_condition as adpc
import auto_cmd as ac
import auto_metadata as am
import auto_package_install as api
import auto_package_module as apm

from __import__ import *
from __common__.__testlink__ import *
from __common__.__local__ import *

## manual 폴더 포함하기 위해
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import manual.main as reg

def main():

    test_start = time.time()

    getOSInfo()

    th = testHelper()

    # dracut
    th.ip_backup()
    th.ip_cloudInit()
    
    # sshd 설정
    sshd_config()
    
    if CLEAN_RESULT == 'true':
        if os.path.isdir(RESULT_PATH):
            shutil.rmtree(RESULT_PATH)

    makeFolder(RESULT_PATH)
    
    # HYPERVM 일 경우 레포 설정
    if HYPERVM_TEST == 'true':          
        ## 로컬일 경우엔 다르게
        if LOCAL_REPOSITORY == 'true':  
            HYPERVMLocalRepo = Repository('HYPERVM_local') ## 레포지토리 클래스 생성
            HYPERVMLocalRepo.addRepo(
                'HYPERVM_local',
                'HYPERVM_local',
                HYPERVM_LOCAL_URL,
                None,
                0,
                1             
            )
            ## 로컬 레포 다운
            am.getRpmFiles(HYPERVM_RPM_FOLDER,HYPERVM_RPM_URL)
        else:
            HYPERVMRepo = Repository('HYPERVM') ## 레포지토리 클래스 생성
            HYPERVMRepo.addRepo(
                'HYPERVM',
                'HYPERVM',
                HYPERVM_RPM_URL,
                None,
                0,
                1             
            )          
        ## ProLinux enabled=0 추가      
        #HYPERVMRepo.disableRepo('ProLinux') 
    # HYPERVM 이 아닐 경우 로컬레포 설정(패키지, 메타데이터일때만 가능)
    else:
        if LOCAL_REPOSITORY == 'true':
            setLocalRepo()  

    TEST_LIST = [
        [PACKAGE_MODULE_TEST, apm],
        [PACKAGE_ALL_INSTALL_TEST, api],
        [DAEMON_TEST, ad],
        [DAEMON_PRE_CONDITION, adpc],
        [CMD_TEST, ac],
        [METADATA_TEST, am],
        [PACKAGE_TEST, ap],
    ]
    # 각 테스트 중 true 인 것만 실행
    for i in range(len(TEST_LIST)):
        #try:
        TEST_LIST[i][1].main() ## 테스트 실행
        #except Exception as e:
            #print("*** Main Exception : %s"%(str(e)))
            #break
    ## block 은 포함하지 않게 변경

    # # 로컬 레포 설정되어있다면 해제
    # if LOCAL_REPOSITORY == 'true':
    #     unsetLocalRepo()

    h, m, s = secToHms(test_start, time.time())
    print("* Total Running Time : %dh %dm %.2fs"%(h, m, s))    

    ## 테스트 종료
    if IN_JENKINS == None and execMode != 'shell':
        execMode.close()
        print("* ssh closed")

    ## manual to auto test
    if MANUAL_TEST == 'true':
        reg_start = time.time()
        reg.main()  
        h, m, s = secToHms(reg_start, time.time())
        print("* Manual Running Time : %dh %dm %.2fs"%(h, m, s))    

if __name__ == '__main__':
    
    main()