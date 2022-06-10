'''
 RPMcompare.py 프로그램은
 ProLinux의 iso 파일끼리
 rpm 파일을 비교할 때 사용하는 것이며
 버전이 업데이트된 rpm 파일을 찾아낼 때 사용하면 유용하다.
 현재는 iso 파일끼리의 비교만 가능하다. 
 '''




import os
import time
import paramiko
import subprocess as sp
from tkinter import * 
from tkinter import filedialog
import tkinter.ttk as ttk

# for parsing
import requests
from bs4 import BeautifulSoup

root = Tk()
root.title('Rpm compare')
newVolume = 'E'
oldVolume = 'F'

vIsoFileNEW = StringVar()
vIsoFileOLD = StringVar()
vRepoURL = StringVar()
vRepoName1 = StringVar()
vRepoName2 = StringVar()
vRepoName3 = StringVar()
vCommit_str = StringVar()
vJenkins = IntVar()
vHOST_IP = StringVar()
l_var2 = '' 

cnt = 0
cnt2 = 0
fixed = 0

changedPkg = []
class RPM_COMPARE:
    def __init__(self):
        self.tt = time.localtime()
        if not os.path.isdir('results'):
            os.makedirs('results')
            
    def mount_image(self,filePath):
        time.sleep(5)
        if filePath == '':
            return False
        print("mounting image : " + filePath)
        a1 = "powershell -command Mount-DiskImage -Imagepath '" + filePath + "'"
        print(a1)
        cmd1 = sp.Popen(a1, shell=True, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)    
        time.sleep(1)
        o1, e1 = cmd1.communicate()    
        time.sleep(3)
        print(o1, e1)

        a2 = 'powerShell -command "Get-DiskImage  -ImagePath ' + "'" + filePath + "' |  Get-Volume" + '"'
        print(a2)
        cmd2 = sp.Popen(a2, shell=True, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)    
        time.sleep(1)
        o2, e2 = cmd2.communicate() 
        time.sleep(3)
        print(o2, e2)
        
        # 마운트 디스크 찾기
        last_hipen = ['----','---','--', '-']
        '''
        * 마운트 후 디스크 찾기를 통해 출력하면 아래와 같이 하나의 문자열로 보여짐
        * 따라서 마지막에 나오는 -- 뒤에 나오는 문자열을 디스크 문자로 인식(E,F,H 등)
        * 그런데 마지막에 하이픈이 -, --, ---, ---- 이렇게 총 4가지로 나옴(나오는 기준에 대해선 확인안됨)
        * 따라서 마지막에 나오는 하이픈에 따라서 다른 문자열 위치 때문에, alpha 값으로 하이픈 개수에 따라 다르게
        * 문자열의 index를 찾도록 함
        * 출력문
        DriveLetter FriendlyName               FileSystemType DriveType HealthStatus OperationalStatus Si 
                                                                                                       ze 
                                                                                                       Re 
                                                                                                       ma 
                                                                                                       in 
                                                                                                       in 
                                                                                                       g 
        ----------- ------------               -------------- --------- ------------ ----------------- --  << 여기 부분
        E           ProLinux-8.2 Server.x86_64 Unknown        CD-ROM    Healthy      OK                 B 
        '''
        ti = 0
        alpha = len(last_hipen) + 1
        for i in range(len(last_hipen)):
            if o2.find(last_hipen[i]+'\n') != -1:
                ti = i
                alpha = len(last_hipen) + 1 - i
                break
        volume = o2[o2.find(last_hipen[ti]+'\n')+alpha]
        print('FILE : ' + filePath)
        print('VOLUME : ' + volume)
        return volume
        
    def dismount_image(self, filePath):
        print("dismounting image " + filePath)
        a = "powershell -command Dismount-DiskImage -Imagepath '" + filePath + "'"
        print(a)
        cmd = sp.Popen(a, shell=True, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)    
        o, e = cmd.communicate()   

    def find_rpm_files(self, dirname, rpmFiles):       
        try:
            dirFiles = os.listdir(dirname)
            for filename in dirFiles:
                absFileName = os.path.join(dirname, filename) ## 절대경로로 만들기
                if os.path.isdir(absFileName): ## 해당 경로가 폴더일 때
                    self.find_rpm_files(absFileName, rpmFiles) ## 한 번 더 폴더 속으로
                else: ## 폴더가 아닐때는 현재 위치에서 rpm 파일이 있는지 확인
                    ext = os.path.splitext(absFileName)[-1]
                    if ext == '.rpm':
                        #absFileName_split = absFileName.split('\\')
                        #print(absFileName_split[len(absFileName_split)-1])                    
                        rpmFiles.append(filename)

        except Exception as e:
            print("*** RPM Compare Exception : %s"%(e))
        return rpmFiles

    def export_rpm_name(self, rpm):
        hipenIdx = list(filter(lambda x:rpm[x]=='-',range(len(rpm))))
        for idx in hipenIdx:
            if rpm[int(idx)+1].isalpha():
                isNum = False
            else:
                isNum = True
            if isNum == True:
                to = idx
                break
        return rpm[:to]

    def delete_path(self,path):
        pathName = ''
        cmd = ''
        for i in range(len(path)-1, 0, -1):
            if path[i] != '/':
                pathName += path[i]
            else:
                cmd = pathName
                break
        return cmd[::-1]
    
    # def rpm_from_url(self, url, repoName):
    #     if url == '':
    #         return []
    #     rpmList = []

    #     if repoName == '':
    #         repoFullPath = url + '/Packages'
    #     else:
    #         repoFullPath = url + '/' + repoName + '/Packages'
    #     print('Remote URL : ' + repoFullPath)
    #     page = requests.get(repoFullPath)
    #     soup = BeautifulSoup(page.content, "html.parser")
    #     for i in soup.find_all('a'):
    #         if '.rpm' in i.attrs['href']:
    #             rpmList.append(i.attrs['href'])                           

    #   return rpmList
        
    def compare(self):
        global newVolume, oldVolume, cnt, cnt2, vIsoFileNEW, vIsoFileOLD, vRepoURL, l_var2, changedPkg
        print("start to compare ")
        
        if not os.path.isfile('results/compare_local_%02d%02d_%02d%02d%02d.csv'%(self.tt.tm_mon, self.tt.tm_mday, self.tt.tm_hour, self.tt.tm_min, self.tt.tm_sec)) and oldVolume != False:
            with open('results/compare_local_%02d%02d_%02d%02d%02d.csv'%(self.tt.tm_mon, self.tt.tm_mday, self.tt.tm_hour, self.tt.tm_min, self.tt.tm_sec),'w',encoding='utf-8') as log:
                log.write('No;%s;%s\n'%(self.delete_path(vIsoFileNEW.get())[:-4],self.delete_path(vIsoFileOLD.get())[:-4]))
            
        # if not os.path.isfile('results/compare_remote_%02d%02d_%02d%02d%02d.csv'%(self.tt.tm_mon, self.tt.tm_mday, self.tt.tm_hour, self.tt.tm_min, self.tt.tm_sec)) and vRepoURL.get() != '':
        #     with open('results/compare_remote_%02d%02d_%02d%02d%02d.csv'%(self.tt.tm_mon, self.tt.tm_mday, self.tt.tm_hour, self.tt.tm_min, self.tt.tm_sec),'w',encoding='utf-8') as log2:
        #         log2.write('No;Type;Repository;%s;Remote\n'%(self.delete_path(vIsoFileNEW.get())[:-4]))
            
        #args = list(args)
        #remoteRepo = []

        # remotevRepoURL = vRepoURL.get()
        # if remotevRepoURL != '' :
        #     if remotevRepoURL[len(remotevRepoURL)-1] == '/':
        #         remotevRepoURL =  remotevRepoURL[:-1]
        
        l_var2.set('extract rpm list')    
        newRepo = []
        oldRepo = []   
        newRepo = self.find_rpm_files(newVolume+":/", newRepo)
        #newRepo.append(new_R)
        oldRepo = self.find_rpm_files(oldVolume+":/", oldRepo)
        #oldRepo.append(old_R)
        #remote_R = self.rpm_from_url(remotevRepoURL)
        #remoteRepo.append(remote_R)
        print("rpm 총합(Base) : %d"%(len(newRepo)))
        print("rpm 총합(Compare) : %d"%(len(oldRepo)))
        #print("rpm 총합(Remote) : %d"%(len(remoteRepo[0])))
        
        l_var2.set('compare')
        for new_rpm in newRepo:
            new_name = self.export_rpm_name(new_rpm) ## 이름 추출
            ttt = 0
            #ttt2 = 0
            exists = False
            #exists2 = False
            tmp = ''
            #tmp2 = ''

            ## 1) 이전 레포랑 비교                
            for old_rpm in oldRepo:
                ttt += 1                    
                if new_name in old_rpm:
                    old_name = self.export_rpm_name(old_rpm)
                    if new_name == old_name:
                        tmp = old_rpm
                        #print(old_name, new_name)
                        if new_rpm == old_rpm:
                            exists = True
                            break

                if exists == False and ttt == len(oldRepo) and oldVolume != False:
                    cnt += 1
                    self.log = open('results/compare_local_%02d%02d_%02d%02d%02d.csv'%(self.tt.tm_mon, self.tt.tm_mday, self.tt.tm_hour, self.tt.tm_min, self.tt.tm_sec),'a',encoding='utf-8')
                    if tmp == '':
                        self.log.write("%d;%s;%s\n"%(cnt,new_rpm, '없다'))
                    else:
                        self.log.write("%d;%s;%s\n"%(cnt,new_rpm, tmp))
                    changedPkg.append(new_rpm)
                    self.log.close()

            ## 2) 원격 레포랑 비교
            # for remote_rpm in remoteRepo[i]:
            #     ttt2 += 1                    
            #     if new_name in remote_rpm:
            #         remote_name = self.export_rpm_name(remote_rpm)
            #         if new_name == remote_name:
            #             tmp2 = remote_rpm
            #             #print(remote_name, new_name)
            #         if new_rpm == remote_rpm:
            #             exists = True
            #             break

            #     if exists2 == False and ttt2 == len(remoteRepo[i]) and tmp2 == '' and remotevRepoURL != '':
            #         cnt2 += 1
            #         self.log = open('results/compare_remote_%02d%02d_%02d%02d%02d.csv'%(self.tt.tm_mon, self.tt.tm_mday, self.tt.tm_hour, self.tt.tm_min, self.tt.tm_sec),'a',encoding='utf-8')
            #         self.log.write("%d;Remote;%s;%s;%s\n"%(cnt2,args[i], new_rpm, '없다'))
            #         self.log.close()

            #     elif exists2 == False and ttt2 == len(remoteRepo[i]) and tmp2 != '' and remotevRepoURL != '':
            #         cnt2 += 1
            #         self.log2 = open('results/compare_remote_%02d%02d_%02d%02d%02d.csv'%(self.tt.tm_mon, self.tt.tm_mday, self.tt.tm_hour, self.tt.tm_min, self.tt.tm_sec),'a',encoding='utf-8')
            #         self.log2.write("%d;Remote;%s;%s;%s\n"%(cnt2,args[i], new_rpm, tmp2))
            #         self.log2.close()



def start():
    global vIsoFileNEW, vIsoFileOLD, vRepoName1, vRepoName2, vRepoName3, newVolume, oldVolume, l_var2, changedPkg, vJenkins

    # def popen(cmd):
    #     print(cmd)
    #     a = sp.Popen(cmd,shell=True, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)     
    #     o, e = a.communicate(timeout=30)        


    def updateProgress(prog, var, value):    
        global fixed  

        if int(value) == 0:
            var.set(0)
            prog.update()
    
        for i in range(fixed, int(value)): 
            var.set(i)
            prog.update()
            time.sleep(.001)

        fixed = value

    ## for_jenkins 로 브랜치 변경
    #popen('git checkout for_jenkins')
    #popen('git pull origin master')

    # progressbar
    newWindow = Toplevel(root)
    newWindow.title('compare')
    newWindow.geometry('400x40')
    l_var2 = StringVar()
    p_var2 = DoubleVar()
    label2 = ttk.Label(newWindow, textvariable=l_var2)
    progressbar2 = ttk.Progressbar(newWindow, maximum=100, length=400, variable=p_var2)
    label2.pack()
    progressbar2.pack()
    

    rc = RPM_COMPARE()
    
    # 1 ############################################
    # 이미지 마운트
    status = 0    
    l_var2.set('wait')
    updateProgress(progressbar2, p_var2, status)
    
    # new
    l_var2.set('mount images')
    time.sleep(1)
    newVolume = rc.mount_image(vIsoFileNEW.get())
    
    status += 10
    updateProgress(progressbar2, p_var2, status)
    # old
    time.sleep(1)
    oldVolume = rc.mount_image(vIsoFileOLD.get())
    status += 10
    updateProgress(progressbar2, p_var2, status)
    ################################################
    
    # 2 ############################################
    # 각 레포지토리에서 파일 비교 시작



    l_var2.set('searching repository and start to compare')
    rc.compare()
    status += 30
    updateProgress(progressbar2, p_var2, status)

    # repoList = [vRepoName1.get(), vRepoName2.get(), vRepoName3.get()]

    # changedPkg = []
    # for repo in repoList:
    #     if repo == '':
    #         status += 10
    #         updateProgress(progressbar2, p_var2, status)
    #         continue
    #     l_var2.set('searching repository and start to compare in ' + repo)
    #     rc.compare(repo)
    #     status += 20
    #     updateProgress(progressbar2, p_var2, status)
    # ################################################
    status += 30
    
    # 3 ############################################
    # rpm 파일 팀 서버로 보내서 데몬, 기본기능 확인 후 파일로 만들기
    # l_var2.set('ssh connection to %s'%(vHOST_IP.get()))
    # print('ssh connection to %s'%(vHOST_IP.get()))
    # # ssh 연결 #
    # ssh = paramiko.SSHClient()
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.connect(vHOST_IP.get(), username='root', password='asdf', port=22)   
    # ssh.exec_command('mkdir -p /root/rpms_for_compare') # rpm 저장 폴더 생성

    # 저장할 리스트 초기화 #
    l_var2.set('extract changed package, daemon, cmd list')
    changedPkgList = []
    for i in changedPkg:
        changedPkgList.append(i[:-4] + '\n')
    #changedDaemonList = [] ##.service, .socket, .target, .timer, .mount
    #changedCmdList = [] ## bin, sbin

    # 팀 서버로 rpm 파일 보내서 데몬, 기본 기능 찾기 #
    # print('finding daemon, cmding files')

    ## 해당 파일을 보내려면 파일 경로를 알아야하는데
    ## 경로까지 받아오면 그걸 다시 처리해줘야하는게 골치...흠
    
    # l_var2.set('find daemon, cmd files')
    # for i in range(len(changedPkg)):
    #     if i == 0:
    #         continue
    #     rpmPath = newVolume + ':/' + changedPkg[i][0] + '/Packages/' + changedPkg[i][1]     
    #     # E:/AppStream/Packages/*.rpm
    #     print("send %s to %s"%(changedPkg[i][1],vHOST_IP.get()))
    #     l_var2.set("send %s to %s"%(changedPkg[i][1],vHOST_IP.get()))
    #     a = sp.Popen('echo y | pscp -pw asdf ' + rpmPath + ' root@%s:/root/rpms_for_compare/'%(vHOST_IP.get()),
    #                 shell=True, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)     ## pscp 로 파일 보내기
    #     o, e = a.communicate(timeout=30)        
    #     stdin, stdout, stderr  = ssh.exec_command('rpm -qlp /root/rpms_for_compare/' + changedPkg[i][1])   ## rpm 파일 내부에 있는 파일 검색
    #     output = stdout.readlines()
    #     for line in output:
    #         if ('.service' or '.socket' or '.target' or '.timer' or '.mount') in line:
    #             print('find daemon file : ' + str(line).replace('\n',''))
    #             l_var2.set('find daemon file : ' + str(line).replace('\n',''))
    #             #line = line.replace('\n','')
    #             changedDaemonList.append(line)                
    #         elif ('/bin/' or '/sbin/') in line:
    #             #line = line.replace('\n','')
    #             print('find cmd file : ' + str(line).replace('\n',''))
    #             l_var2.set('find cmd file : ' + str(line).replace('\n',''))
    #             changedCmdList.append(line)

    #     # 1) 팀 서버로 rpm 파일들 보냄
    #     # 2) 폴더 : /root/rpms_for_compare/
    #     ## 데몬 리스트, 기본 기능 리스트 추출
    
    # 전송한 rpm 파일 삭제 #
    # ssh.exec_command('rm -rf /root/rpms_for_compare')
    # ssh.close()
    status += 20
    updateProgress(progressbar2, p_var2, status)

    print('make changed file')
    l_var2.set('make changed file')

    # 패키지, 데몬, 기본기능 파일로 생성 #
    def changedFile(fileName, lst):
        ff = open(fileName, 'w', encoding='utf-8')

        if lst == []:
            ff.write('Nothing')
        else:
            for i in lst:
                ff.write(i)
        ff.close()

    changedFile('results/package_changed.txt', changedPkgList)
    #changedFile('results/daemon_changed.txt', changedDaemonList)
    #changedFile('results/cmd_changed.txt', changedCmdList)
    ################################################


    # 4 ############################################
    # 변경된 내역 git commit 추가
    # 변경된 내역이 Nothing 일 경우 진행하지 않음
    # if vJenkins.get() == 1 :
    #     print(changedPkgList)
    #     if changedPkgList != []:
    #         l_var2.set('git commit changed files')

    #         popen('git add results/package_changed.txt')
    #         popen('git add results/daemon_changed.txt')
    #         popen('git add results/cmd_changed.txt')
    #         popen('git commit -m "%s"'%(vCommit_str.get()))
    #         popen('git pull origin for_jenkins')
    #         popen('git push origin for_jenkins')
    #         popen('git checkout master')
    #         popen('git merge for_jenkins')
    #         popen('git pull origin master')
    #         popen('git push origin master')

    #         ## 여기서 이제 젠킨스 빌드까지 실행 
    #     else:
    #         print("Nothing changed packages")
    #         l_var2.set('Nothing changed packages')
    # else:      
    #     popen('git checkout master')
    status += 10
    updateProgress(progressbar2, p_var2, status)
    ################################################

    # 5 ############################################
    # 이미지 언마운트 
    print("umount images")
    l_var2.set('dis mount')
    rc.dismount_image(vIsoFileNEW.get())
    status += 10
    updateProgress(progressbar2, p_var2, status)

    if oldVolume != False:
        rc.dismount_image(vIsoFileOLD.get())
    status += 10
    updateProgress(progressbar2, p_var2, status)
    ################################################

    root.destroy()

    
label = Label(root, text='비교할 버전명 이름 입력(iso 폴더명)').grid(row=0, column =1)
#----------------------------------------------------------------------------------------#

vIsoFileNEW.set('C:/Users/Lee/Desktop/ProLinux-8.4.11.iso')
def find_new():
    global vIsoFileNEW
    new_file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file", filetypes=(("ISO files", "*.iso"),("all files", "*.*")))
    print('기준 파일 :', new_file_path)
    vIsoFileNEW.set(new_file_path)    
new_label = Label(root, text='신규 버전(기준)').grid(row=1,column=0)
new_iso = Entry(root, width=50, textvariable=vIsoFileNEW).grid(row=1,column=1)
new_btn = Button(text = '찾기', width=10, command = find_new).grid(row=1,column=2)
##########################################################################################

#----------------------------------------------------------------------------------------#
vIsoFileOLD.set('C:/Users/Lee/Desktop/ProLinux-8.4.10.iso')
def find_old():
    global vIsoFileOLD
    old_file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file",filetypes=(("ISO files", "*.iso"),("all files", "*.*")))
    print('비교 파일 :', old_file_path)
    vIsoFileOLD.set(old_file_path)
old_label = Label(root, text='이전 버전').grid(row=2,column=0)
old_iso = Entry(root, width=50, textvariable=vIsoFileOLD).grid(row=2,column=1)
old_btn = Button(text = '찾기', width=10, command = find_old).grid(row=2,column=2)
##########################################################################################



# #----------------------------------------------------------------------------------------#
# vRepoURL.set('http://192.168.2.136/prolinux/8.2/os/x86_64/')
# remote_label = Label(root, text='원격 레포 주소').grid(row=3,column=0)
# # remote_box = ttk.Combobox(root, values=["Release", "GS"])
# # remote_box.grid(row = 3, column = 1)
# # remote_box.current(0)
# # remote_box.bind("<<ComboboxSelected>>", callback_selectbox)
# remote_url = Entry(root, width=50, textvariable=vRepoURL).grid(row=3,column=1)
# ##########################################################################################

#----------------------------------------------------------------------------------------#
# vRepoName1.set('BaseOS')
# #vRepoName2.set('BaseOS')
# repo_label = Label(root, text='비교할 레포명 입력(최대 3개)').grid(row=5, column=1)
# repo_label1 = Label(root, text='레포지토리1').grid(row=6,column=0)
# repo_entry1 = Entry(root, width=50, textvariable=vRepoName1).grid(row=6,column=1)
# repo_label2 = Label(root, text='레포지토리2').grid(row=7,column=0)
# repo_entry2 = Entry(root, width=50, textvariable=vRepoName2).grid(row=7,column=1)
# repo_label3 = Label(root, text='레포지토리3').grid(row=8,column=0)
# repo_entry3 = Entry(root, width=50, textvariable=vRepoName3).grid(row=8,column=1)
# ##########################################################################################

#----------------------------------------------------------------------------------------#
# vCommit_str.set('changed files update')
# commit_label = Label(root, text='Jenkins Build').grid(row=10,column=0)
# commit_checkbutton = Checkbutton(root, text="", variable = vJenkins).grid(row=10, column=1, sticky="w")
# commit_label2 = Label(root, text='Commit Message').grid(row=11,column=0)
# commit_msg = Entry(root, width=50, textvariable=vCommit_str).grid(row=11,column=1, sticky="w")
##########################################################################################

#----------------------------------------------------------------------------------------#
# vHOST_IP.set('192.168.17.162')
# repo_label = Label(root, text='ISO 파일 전송용 IP 입력').grid(row=12, column=0)
# repo_entry1 = Entry(root, width=50, textvariable=vHOST_IP).grid(row=12,column=1)

##########################################################################################
#----------------------------------------------------------------------------------------#
compare_btn = Button(text = 'compare', command = start).grid(row=99,column=1)
##########################################################################################

root.mainloop()


