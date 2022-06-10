## 메타데이터를 로컬 레포에서 가져옴

from __import__ import *

METADATA_TOTAL = []

def getMetaTotal(meta, idx):    
    ## buildHosts
    eachTotal = [meta, 'Not installed', 0]
    if METADATA_TOTAL != []:
        
        each = [[METADATA_TOTAL[0][idx], 0]]
        #printBeautify(METADATA_TOTAL)
        for i in range(len(METADATA_TOTAL)):
            for j in range(len(each)):
                if METADATA_TOTAL[i][idx] == each[j][0]:
                    each[j][1] = each[j][1] + 1
                    break
                else:
                    if j == len(each)-1:
                        each.append([METADATA_TOTAL[i][idx],1])
        eachResult = ''
        eachTotalNum = 0
        for i in range(len(each)):
            eachResult = eachResult + "%s : %s%s"%(each[i][0],each[i][1], TAP)
            eachTotalNum += each[i][1]
        printSquare("%s%sTotal : %s%s%s"%(meta,TAP, eachTotalNum,TAP, eachResult))

        eachTotal = [meta, eachResult, eachTotalNum]
    return eachTotal
def getRpmFiles(rpm_folder, url): 
    ## rpm 파일만 입력된 링크에서 다운받아온다.
    down_start = time.time()
    downloaded_rpmList = []
    
    commandExec(execMode, 'mkdir '+ rpm_folder)
    print("* Downloading rpm files in " + rpm_folder + " ...")
    print("* Need to wait for downloading rpm files ...")
    output, error = commandExec(execMode, 'wget -N -qc -r -np ' + url + ' -P ' + rpm_folder) ## 7버전일 경우 wget -N -qc -r -np 까지만 하면됨
    ## -qc : 출력 없고, 다운받던 파일이 있으면 이어서 
    ## -r : 폴더 다운
    ## -np : 상위 폴더 다운받지않음
    ## -P : 저장경로 지정
    ## -accpet=rpm : rpm 파일만 받음
    ## -t : 무제한 재시도
    ## -N : 같은 파일이면 받지 않음
    #
    h, m, s = secToHms(down_start, time.time())
    print("* Download Time : %dh %dm %.2fs"%(h, m, s))

def getRpmList():
    RPM_LIST = []

    if LOCAL_REPOSITORY == 'true':
        output, error = commandExec(execMode, '%s -y install findutils'%INSTALL_PKG)
        if HYPERVM_TEST == 'true': # 로컬에 rpm 파일을 다운받아서 리스트를 추출 # SUPERVM + local 일때만 가능
            getRpmFiles(HYPERVM_RPM_FOLDER, HYPERVM_RPM_URL)
            output, error = commandExec(execMode, "find " + HYPERVM_RPM_FOLDER + " -name '*.rpm'")  ## rpm 리스트 가져오기    
        else:
            output, error = commandExec(execMode, 'find ' + MOUNT_FOLDER_PATH + " -name '*.rpm'")  ## rpm 리스트 가져오기    
        cnt = 1
        for i in output:
            i = i.replace('\n','')
            RPM_LIST.append(i)
        print("* Found "+ str(len(RPM_LIST)) +' RPMs')
    else:        
        RPM_LIST = getListinFile(METADATA_FILE)        
        print("TEST FILE : " + METADATA_FILE)

    return RPM_LIST

def metaDataTest():

    if LOCAL_REPOSITORY == 'true':
        csvHeader = 'PATH' + DELIM + 'RPM' + DELIM + 'Build Host' + DELIM + 'Vendor' + DELIM + 'Packager' + DELIM + 'Version'
        # csvHeader = 'PATH' + DELIM + 'RPM' + DELIM + 'Build Host' + DELIM + 'Vendor' + DELIM + 'Packager' + DELIM + 'Build Date' + DELIM + 'Version'
    else:
        csvHeader = 'RPM' + DELIM + 'Build Host' + DELIM + 'Vendor' + DELIM + 'Packager' + DELIM + 'Version'
        # csvHeader = 'RPM' + DELIM + 'Build Host' + DELIM + 'Vendor' + DELIM + 'Packager' + DELIM + 'Build Date' + DELIM + 'Version'
    tmpCsvInit(REALTIME_METADATA_RESULT_FILE, csvHeader)
    num = 0

    RPM_LIST = getRpmList()

    metadataTotalResult = []

    for rpm in RPM_LIST:
        num += 1
        printLine(num)
        metaResult = []
        if LOCAL_REPOSITORY=='true':
            execCmd =  "rpm -qp --qf '%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH};%{BUILDHOST};%{VENDOR};%{PACKAGER}' " + rpm
            #Build Date 필요할 경우 쿼리 방법 (코드도 함께 수정되어야함)
            # execCmd =  "rpm -qp --qf '%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH};%{BUILDHOST};%{VENDOR};%{PACKAGER};%{BUILDTIME:date}' " + rpm
            print("PATH : " + rpm)
        else:
            execCmd = "rpm -q --qf '%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH};%{BUILDHOST};%{VENDOR};%{PACKAGER}' " + rpm
            # execCmd =  "rpm -q --qf '%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH};%{BUILDHOST};%{VENDOR};%{PACKAGER};%{BUILDTIME:date}' " + rpm
            print("RPM : " + rpm)
            
        output, error = commandExec(execMode, execCmd)

        if error != []:
            if 'rpmdb' in error[0]:    
                commandExec(execMode, 'rm -f /var/lib/rpm/_db*')
                commandExec(execMode, 'rpm -vv --rebuilddb')
                commandExec(execMode, 'sleep 15')
                commandExec(execMode, 'systemctl start fapolicyd')
                printSquare('Start fapolicyd') 
           
        if (output != [] and 'not installed'  in output[0]) or (output == [] and error):
            metaResult = saveResult(metaResult, rpm, 'Not installed', 'Not installed', 'Not installed')
            print("MESSAGE : Not installed")       

        else:
            result = output[0].split(';')

            ## 설치된 버전과 rpm 파일의 버전이 같은 버전인지 확인
            if LOCAL_REPOSITORY == 'false':
                if rpm != result[0]:
                    check = 'NOT SAME'
                else:
                    check = 'SAME'
            else:
                print(deletePath(rpm.replace('.rpm','')), result[0])
                if deletePath(rpm.replace('.rpm','')) != result[0]:
                    check = 'NOT SAME'
                else:
                    check = 'SAME'
            ##

            if LOCAL_REPOSITORY == 'true':
                #metaResult = saveResult(metaResult, rpm, result[0], result[1], result[2], result[3], result[4], check)
                metaResult = saveResult(metaResult, rpm, result[0], result[1], result[2], result[3], check)
                ## path, rpm, build host, vendor ,packager
                print("RPM : " + result[0])
            else:
                metaResult = saveResult(metaResult, result[0], result[1], result[2], result[3], check)
                # metaResult = saveResult(metaResult, result[0], result[1], result[2], result[3], result[4], check)
            print("BUILD HOST : " + result[1]) 
            print("VENDOR : " + result[2]) 
            print("PACKAGER : " + result[3]) 
            print("VERSION : " + check)
            # print("BUILD DATE : " + result[4]) 
            # METADATA_TOTAL.append([result[1],result[2],result[3],result[4]])     
            METADATA_TOTAL.append([result[1],result[2],result[3]])     
        saveCSV(metaResult,REALTIME_METADATA_RESULT_FILE)    
        metadataTotalResult.append(metaResult) 
        printLine()
    exportCSV(metadataTotalResult, METADATA_RESULT_FILE, csvHeader)

def main():
    if METADATA_TEST == 'true':
        printSquare('Metadata Test')
        meta_start = time.time()

        metaDataTest()

        bh = getMetaTotal('BUILD HOST', 0)
        vd = getMetaTotal('VENDOR', 1)
        pkgr = getMetaTotal('PACKAGER', 2)
       # bd = getMetaTotal('BUILD DATE' , 3)

        ## junit xml 에 적용하기 위한 결과 저장용 
        #ONLY_RESULT[3].append(bh)
        #ONLY_RESULT[3].append(vd)
        #ONLY_RESULT[3].append(pkgr)
        
        # tmp = ONLY_RESULT[3]
        # t = []
        # for i in tmp:
        #     tmp2 = ''
        #     for j in i:
        #         tmp2 += "%s%s"%(str(j),TAP)
        #     tmp2 = tmp2.split(TAP)
        #     tmp2 = [v for v in tmp2 if v != '']
        #     t.append(tmp2)
        #ONLY_RESULT[3] = t


        '''
        ### ONLY_RESULT[3]
        [
            ['BUILD HOST', 'pl-8-builder-1.tk : 7    pl-8-builder-10.tk : 3    ', 10], 
            ['VENDOR', 'Tmax A&C Co., Ltd. : 10    ', 10], 
            ['PACKAGER', 'Tmax A&C Co., Ltd. <https://technet.tmaxsoft.com/> : 10    ', 10]
        ]
        '''
        h, m, s = secToHms(meta_start, time.time())
        print("* Metadata Test Running Time : %dh %dm %.2fs"%(h, m, s))

if __name__ == '__main__':    
    
    main()
    
    if IN_JENKINS == None and execMode != 'shell':
        execMode.close()
        #print("ssh closed")
