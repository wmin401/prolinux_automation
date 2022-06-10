from __common__.__module__ import DELIM, makeFolder, RESULT_PATH
from __common__.__logger__ import *


def addDelimit(list_idx): ## add ';'
    ## 결과 리스트에 csv 파일 저장을 위해 delimit 값을 넣어주는 함수
    result = list_idx[0]
    for i in range(1,len(list_idx)):
        result += DELIM + list_idx[i]
    result += DELIM + '\n'
    #print(result)
    return result

def tmpCsvInit(filename, header):
    ## temp 폴더에 실시간 csv 파일을 생성하기 위해
    ## tmp 폴더 생성 및 tmp 결과 파일 생성
    makeFolder(RESULT_PATH + '/tmp')
    with open(filename, "wt", encoding="UTF8") as REALTIME_RESULT_FILE:
        if header != None:
            REALTIME_RESULT_FILE.write(header + ';\n')

## 한줄씩 저장
def saveCSV(result, resultFile): ## 결과 temp 파일(install, remove 따로 저장)
    result = addDelimit(result)
    with open(resultFile, "a", encoding="UTF8") as csvFile:
        csvFile.write(result)

# 리스트 한번에 저장
def exportCSV(lst, resultFile, header):    
    print("* Change list to str for saving to csv file ...")
    save = open(resultFile, "wt", encoding="UTF8")
    if header != None:
        save.write(header+';\n')
    for i in range(0,len(lst)):
        line = addDelimit(lst[i])
        if i == len(lst)-1:
            save.write(line.replace('\n',''))
        else:
            save.write(line)
    save.close()


def saveResult(lst, *args):    
    ## lst : 리스트(lst
    ## args[0] ~ : 삽입할 아이템들
    if len(args) == 0:
        return lst
    elif len(args) == 1:
        lst.append(args[0])
        return lst
    else: #삽입할 인자가2개 이상
        for i in range(0, len(args)):
            lst.append(args[i])
        return lst

