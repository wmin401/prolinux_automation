from __common__.__parameter__ import TAP

printLength = 80

def printLine(*args):
    ## 인자가 있을 경우 라인 안에 글자를 삽입
    length = printLength
    if len(args) != 0:
        args = str(args[0])
        tmp = length-len(args)
        for i in range(0, int(tmp/2) - 1):
            print('-',end='')
        print(' '+ args+' ',end='')
        if (len(args)) % 2 == 0:
            half = int(tmp/2) - 1
        else:
            half = int(tmp/2)
        for i in range(0, half):
            print('-',end='')
        print()
    else:
        for i in range(length):
            print('-',end='')
        print()

## 네모 칸 안에 출력 해주는 코드
def printSquare(msg):
    hiphen = printLength - 2
    ## 글자가 길 경우 아래로 내림
    if len(msg) >= printLength:
        msgList = msg.split(TAP)
    print('|',end ='')
    for i in range(hiphen):
        print('-',end='')
    print('|')

    # name
    if len(msg) >= printLength:
        for i in range(len(msgList)-1):
            print(TAP+str(msgList[i]))
    else:
        print(TAP+str(msg))
    
    print('|',end ='')
    for i in range(hiphen):
        print('-',end='')
    print('|')


#리스트로 받아오는 output을 한줄씩 출력해줌
def printBeautify(*args):    
    args = list(args)
    for msg in args:
        if str(type(msg)) != "<class 'list'>":
            print(msg)
            printLine()
        else:
            for i in msg:
                i = str(i)
                if '\n' in i:
                    i = i.replace('\n','')
                print(i)
            printLine()

