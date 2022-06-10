
from __common__.__module__ import *
from __common__.__print__ import * 


# assertionError 예외처리(한번 사용)
def assertionError(err):
    try:
        if err != [] and 'Traceback' in err[0] :
            if 'AssertionError' in err[21]:
            #print(msg[0])
                err  = err[22:]
        return err
    except:
        return err
