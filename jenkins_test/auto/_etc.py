## for test

from __import__ import *
import re # epoch 제거 위해 추가

def downRpmMakeList():
    ## unable 리스트 가져오기
    lst = []
    with open('qwe.txt','r',encoding='utf-8') as f:
        for i in f:
            lst.append(i.replace('\n',''))

    # for i in lst:
    #     print(i)

    ## rpm 파일다운받고 리스트로 만들기
    rpmlst = []
    #commandExec(execMode, 'mkdir '+ SUPERVM_RPM_FOLDER)
    #infoLog("Downloading rpm files in " + SUPERVM_RPM_FOLDER + " ...")
    #infoLog("Need to wait for downloading rpm files ...")
    #output, error = commandExec(execMode, 'wget -N -qc -r -np -t --accept=rpm ' + SUPERVM_RPM_URL + ' -P ' + SUPERVM_RPM_FOLDER)
    
    output, error = commandExec(execMode, "find " + HYPERVM_RPM_FOLDER + " -name '*.rpm'")  ## rpm 리스트 가져오기    

    for i in output:
        i = i.replace('\n','')
        i = deletePath(i)
        rpmlst.append(i[:-4])        
        #print(i)
    print("Found "+ str(len(rpmlst)) +' RPMs')

    ## 리스트 비교
    cnt = 0
    for i in lst:
        i_prime = export_rpm_name(i)
        for j in rpmlst:
            j_prime = export_rpm_name(j)
            if i_prime == j_prime:
                #time.sleep(1)
                print(i, j)
                if i == j:
                    print('같다')
                    cnt += 1
                    break

    print(cnt)

def findPkg(fileName):

    ## 기본기능이 어디 패키지에 속해있는지 찾기
    cccc = getListinFile(fileName)

    with open('found_pkg.txt','w',) as fff:
        for i in cccc:
            output, error = commandExec(execMode,'yum provides ' + i)
            #print(output[0])
            t = output[0].split(':')
            print(t[0])
            fff.write(t[0]+'\n')

def findFromAllPkg(filename, *args):
    # 모든 패키지 파일에서 데몬이나 기본기능 찾아낼때 사용(현재는 사용하지 않음) -> findDaemonCmdList로 대체
    #f = 'found_cmd.txt'
    #cc = open(f,'w',encoding='utf-8')

    findList = list(args)

    tmpLst = []

    output, error = commandExec(execMode, 'find ' + MOUNT_FOLDER_PATH + ' -name "*.rpm"')
    with open(filename ,'w',encoding='utf-8') as cc:
        for i in output:            
            output2, error2 = commandExec(execMode, 'rpm -qlp ' + i)
            for j in output2:
                for k in findList:
                    if k in j:
                        if j not in tmpLst:
                            tmpLst.append(j)
                            print(j)
                            cc.write(j + '\n')

def pkgFromCmd():
    # CMD 파일을 읽어와서 해당 CMD가 어디 패키지에 속해잇는지 찾아냄
    aa = open(CMD_FILE, 'r', encoding='utf-8')
    cc = open('cmd_list.csv', 'w',encoding='utf-8')
    cc.close()
    #with open('cmd_list.csv', 'a',encoding='utf-8') as cc:
    for i in aa:
        cc = open('cmd_list.csv', 'a',encoding='utf-8')
        i = i.replace('\n','')
        output,error = commandExec(execMode, 'dnf provides ' + i)
        try:
            output[1] = output[1].replace('\n','')
            z = output[1].split(':')
            cc.write(i+';설치불가:'+z[0]+'\n')
            print(i+' - '+z[0])
        except Exception as e:
            cc.write(i+';Exception\n')
        cc.close()
      
def removeDuplicate(fileName):
    # 파일에서 중복되는 내용 제거
    b = []
    
    a = open(fileName, 'r', encoding='utf-8')
    for i in a:
        if i not in b:
            b.append(i)

    fileName_ = fileName.split('.')

    with open(fileName_[0] + '_dup.txt', 'w', encoding='utf=8') as ab:
        for i in b:
            ab.write(i)

def findDaemonCmdList(fileName, findList):
    # BaseOS와 AppStream의 rpm 파일에서 데몬과 기본기능 리스트 추출
    PACKAGE_ALL_INSTALL_FILE = 'list/'+VERSION_DETAIL+'/' + IMAGE_TYPE + '/package/package_all.txt'
    a = getListinFile(PACKAGE_ALL_INSTALL_FILE)
    with open(fileName, 'w', encoding='utf-8') as b:
        for i in a:
            output, error = commandExec(execMode, 'rpm -qlp /root/mnt/BaseOS/Packages/' + i + '.rpm')
            print('rpm -qlp /root/mnt/AppStream/Packages/' + i + '.rpm')
            for j in output:
                for k in findList:
                    if k in j:
                        print(j)
                        b.write(j+'\n')

        a = getListinFile(PACKAGE_ALL_INSTALL_FILE)
        for i in a:
            output, error = commandExec(execMode, 'rpm -qlp /root/mnt/Appstream/Packages/' + i + '.rpm')
            print('rpm -qlp /root/mnt/BaseOS/Packages/' + i + '.rpm')
            for j in output:
                for k in findList:
                    if k in j:
                        print(j)
                        b.write(j+'\n')

  #  removeDuplicate(fileName)

    # # HYPERVM 
    # a = getListinFile(PACKAGE_ALL_INSTALL_FILE)
    # with open(fileName, 'w', encoding='utf-8') as b:
    #     for i in a:
    #         output, error = commandExec(execMode, 'rpm -qlp /root/HYPERVM_rpms/172.21.7.2/supervm/22.0.0-rc2/prolinux/8/arch/x86_64/Packages/' + i + '.rpm')
    #         #print('rpm -qlp /root/mnt/AppStream/Packages/' + i + '.rpm')
    #         for j in output:
    #             for k in findList:
    #                 if k in j:
    #                     print(j)
    #                     b.write(j+'\n')




def po2csv():
    # po파일을 추출하여 csv 파일로 저장
    a = open('../../../poFiles/anaconda8_4.po', 'r', encoding='utf-8')
    b = ''
    for i in a:
        b += i
    fff = []
    c = b.split('msgid')
    for i in c:
        if len(i) > 1:
            d = i.split('msgstr')
            if len(d) > 1:
                f1 = d[0].replace('\n','')
                f2 = d[1].replace('\n','')
                f = f1[2:len(f1)-1] + ';' + f2[2:len(f2)-1]
                fff.append(f)
                

    aa = open('anaconda.csv','w', encoding='utf-8')
    aa.close()
    for i in fff:
        
        bb = open('anaconda.csv','a', encoding='utf-8')
        bb.write(i+'\n')
        bb.close()

# cmd 에서 테스트에 필요없는 리스트 삭제
def cmdExtract():
    a = getListinFile('found_cmd.txt')

    b = open('found_cmd.txt', 'w', encoding='utf-8')

    for i in a:
        if '.pl' not in i and '.py' not in i and '.js' not in i and '.gz' not in i \
            and '.conf' not in i and '.cmd' not in i and '.sendmail' not in i and '.sh' not in i \
                and '.cups' not in i and '.jar' not in i and '.xml' not in i and '/opt/rh/' not in i \
                    and '/usr/share/' not in i and '.org' not in i:
            b.write(i+'\n')
    b.close()

# dnf module list에서 module 리스트 추출
def moduleListFromDnfModuleInfo():
    folderPath = 'testFolder'
    makeFolder(folderPath)
    module_list, e = commandExec(execMode, 'dnf module list')
    module_list2 = []

    # dnf module list에서 이름과 stream만 추출
    for i in range(3, len(module_list)-2) :
        each = module_list[i].split(' ')
        each2 = []
        for j in each:
            if j is not '':
                each2.append(j)
        # print(each2)
        module_list2.append([each2[0], each2[1]])

    # 추출한 이름으로 dnf module info 를 이용하여 상세정보 확인
    for module in module_list2:
        module_info, e = commandExec(execMode, 'dnf module info %s:%s'%(module[0], module[1]))
        for i in range(len(module_info)):
            # line = module_info[i].split(':')
            requires = []
            # Context 따로 추출
            if 'Context' in module_info[i]:
                line = module_info[i].split(':')
                context = line[1]
                module.append(line[1].replace(' ', ''))
            
            cnt = -1
            ## 조건을 리스트에 추가(Requires에 있는 내용)
            if 'Requires' in module_info[i]:
                while True:
                    cnt += 1
                    if 'Artifacts' in module_info[i+cnt]:
                        break

                    if 'platform' in module_info[i+cnt]:
                        continue

                    # print(module_info[i+cnt])
                    require = module_info[i+cnt].split(':')
                    module.append(['require','%s%s'%(require[1].replace(' ', ''),require[2])])
            
            # 패키지들을 리스트에 추가(Artifacts에 있는 패키지들)
            cnt2 = -1
            p = False
            if 'Artifacts' in module_info[i]:
                p = True
                while True:
                    cnt2 += 1
                    # print(module_info[i+cnt2])
                    if '' == module_info[i+cnt2]:
                        p = False
                        break

                    if '.src' in module_info[i+cnt2] or 'module-build-macros' in module_info[i+cnt2] or 'debugsource' in module_info[i+cnt2] or 'debuginfo' in module_info[i+cnt2]:
                        continue

                    # print(module_info[i+cnt2])
                    try:
                        artifact = module_info[i+cnt2].split(':')
                        '''
                            22.05.19 jeonghyeon_kim
                            epoch 제거 과정 추가
                        '''
                        remove_epoch = re.sub(r'\b[0-9]+\b\Z', '', artifact[1]) # 문자열 끝의 숫자 (epoch) 제거
                        # 리스트에서 ':'이 사라져서 강제로 넣어주기 -> epoch 제거를 통해 필요 없어져 주석 처리
                        # artifact.insert(2,':')
                        module.append(['artifact','%s%s'%(remove_epoch.replace(' ', ''), artifact[2])]) # 인덱스 감소로 인해 수정

                    except:
                        pass
                
        # for cac in module:
        #     print(cac)


        # 각각 파일로 저장
        # 파일 이름 형식은 name_stream_module_list.txt
        aa = open('%s\\%s_%s_module_list.txt'%(folderPath, module[0], module[1]), 'w', encoding='utf-8')
        aa.write('[%s:%s]\n'%(module[0], module[1]))

        con = False
        for c in range(3, len(module)):
            if c == 3 and module[c][0] == 'require':
                aa.write('Conditions=')            
            if module[c][0] == 'require':
                req = module[c][1].split('[')
                if req[1][:-1] == '':
                    aa.write('(R)%s,(e)%s,'%(req[0], req[0]))
                else:
                    aa.write('(R)%s,(e)%s:%s,'%(req[0], req[0], req[1][:-1]))
                con = True

            if module[c][0] == 'artifact':
                if con == True:
                    aa.write('\n')
                    con = False
                aa.write('%s\n'%(module[c][1]))

        aa.close()
    
    ## 조건같은 경우는 직접수정이 필요 
    ## perl- 관련 패키지들은 따로 파일 생성 필요



import urllib.request

def extractModuleList(url):

    # modules.yaml의 내용을 읽어온다.
    ## 현재 사용 불가능

    req = urllib.request.Request(url)

    with urllib.request.urlopen(req) as response:
        the_page = response.read()
        mod_str = the_page.decode('utf-8')
    makeFolder('module_list')

    mod_docs = mod_str.split('...')

    for document in mod_docs:    
        cnt = -1
        document = document.split('\n')
        for i in document:
            cnt += 1
            if 'name:' in i:
                fileName1 = i.split(':')[1]
                fileName2 = document[cnt+1].split(':')[1]
                fileName = '%s_%s'%(fileName1.replace(' ',''),fileName2.replace(' ',''))
                print(fileName)
                if fileName1.replace(' ','') == fileName2.replace(' ',''):
                    break
                file = open('module_list\%s_module_list.txt'%fileName, 'w', encoding='utf-8')
                file.write('[%s:%s]\n'%(fileName1.replace(' ',''),fileName2.replace(' ','')))
                file.close()
            elif 'artifacts' in i:
 
                if 'rpms' in document[cnt+1]:
                
                    for j in range(cnt+2,len(document)):
                       
                        rpm = document[j].replace('- ','')
                        rpm = rpm.replace('    ','')
                        # 읽어온 rpm에 특정 문자열 있을경우 리스트 제외 
                        if '.src' in rpm or 'module-build-macros' in rpm or 'debugsource' in rpm or 'debuginfo' in rpm:
                            continue

                        print(rpm)
                        try:
                            with open('module_list\%s_module_list.txt'%fileName, 'a', encoding='utf-8') as aaa:
                                aaa.write(rpm+'\n')
                        except:
                            pass

def DaemonListMod(filename):
    DAEMON_FILE = 'list/'+VERSION_DETAIL+'/' + IMAGE_TYPE + '/daemon/daemon_all.txt'
    a = getListinFile(DAEMON_FILE)
    with open(filename, 'w', encoding='utf-8') as b:
        for i in a:
            output = ('/usr/lib/systemd/system/'+i)
            # output = print('/usr/lib/systemd/system/'+ i)
            #for a in :

            print(output)
            b.write(output+'\n')


#    removeDuplicate(a)
    

def main():
    # # removeDuplicate()
    # findFromAllPkg('found_cmd.txt', '/bin/','/sbin/')
    # # findFromAllPkg('found_daemon.txt', '.service', '.target', '.timer', '.socket', '.slice', '.path', '.mount', '.automount')
    # # findPkg(CMD_FILE)
    # pkgFromCmd()
    # findDaemonCmdList('found_daemon.txt', ['.service', '.target', '.timer', '.socket', '.slice', '.path', '.mount', '.automount'])
    # DaemonListMod('daemon_path.txt')
    # findDaemonCmdList('found_cmd.txt', ['/usr/bin/','/usr/sbin/'])
    # # po2csv()

    extractModuleList("http://192.168.2.136/prolinux/8.5/os_tmp/x86_64/AppStream/modules.yaml")
    # cmdExtract()


    # o, e = commandExec(execMode, 'dnf -y install vim', 30)
  #  moduleListFromDnfModuleInfo()



if __name__=="__main__":


    main()


## 이 코드는 사실상 사용되지 않음
## 원래 의도는 modules.yaml을 이용하여 모듈 리스트를 만들었을 때
## 해당 리스트에서 .src와 module-build-macros 내용을 삭제하기 위해
## 파이썬 파일을 모듈 리스트 폴더에 생성 후 아래의 코드를 붙여넣기 한후
## 빌드함으로써 파일의 내용을 수정하는 것이었는데
## dnf module list에서는 함수 자체에 해당 기능을 포함 시켰기 때문에
## 사용되지 않음
def removeInclude(name, path):
    # name의 값이 있는 파일은 모두리스트에서 제외

    import os

    path = "./"
    file_list = os.listdir(path)


    for i in file_list:
        if '.txt' in i:
            f = open(i, 'r', encoding='utf-8')
            fl = []
            for j in f:
                if name not in j:
                    fl.append(j.replace('\n', ''))
            f2 = open(i, 'w', encoding='utf-8')
            cnt = 0
            for j in fl:
                cnt += 1
                if cnt == len(fl):
                    f2.write(j)
                else:
                    f2.write(j+'\n')
            f2.close()




# removeInclude('module-build-macros-', )
