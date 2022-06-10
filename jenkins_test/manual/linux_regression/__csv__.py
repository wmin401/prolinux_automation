
def add_delimit(listIdx): ## add ';'
    result = listIdx[0]
    for i in range(1,len(listIdx)):    
        if listIdx[i] == True:
            listIdx[i] = 'PASS'
        elif listIdx[i] == False:
            listIdx[i] = 'FAIL'
        result += ';' + listIdx[i]
    result += ';' + '\n'
    #print(result)
    return result

def tmp_csv_init(fileName, header):
    REALTIME_RESULT_FILE = open(fileName, "wt", encoding="UTF8")
    if header != None:
        REALTIME_RESULT_FILE.write(header + ';\n')
    REALTIME_RESULT_FILE.close()

## 한줄씩 저장
def save_csv(result, resultFile): ## 결과 temp 파일(install, remove 따로 저장)
    result = add_delimit(result)
    csvFile = open(resultFile, "a", encoding="UTF8")
    csvFile.write(result)
    csvFile.close()

# 리스트 한번에 저장
def export_csv(lst, resultFile, header):    

    ## 결과 출력 하도록 추가
    passCnt = 0
    failCnt = 0
    for i in lst:
        if i[1] == 'PASS':
            passCnt += 1
        elif i[1] == 'FAIL':
            failCnt += 1

    print("--- PASS : %d ---"%passCnt)
    print("--- FAIL : %d ---"%failCnt)
    print("* Changing list to str for saving to csv file ...")

    save = open(resultFile, "wt", encoding="UTF8")
    if header != None:
        save.write(header+';\n')
    for i in range(0,len(lst)):
        line = add_delimit(lst[i])
        if i == len(lst)-1:
            save.write(line.replace('\n',''))
        else:
            save.write(line)
    save.close()

def save_result(lst, *args):    
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

