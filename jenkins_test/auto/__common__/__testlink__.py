import os
import shutil
from xml.etree.ElementTree import Element, SubElement #, Comment, tostring
from xml.etree.ElementTree import ElementTree
from __common__.__parameter__ import FAIL, RESULT_PATH, BLOCK, FAIL
from __common__.__print__ import printSquare
from __common__.__logger__ import *


class testlink:
    def __init__(self):      
        print("* Start the connection with the Testlink ! ")
        self.junitsFolder = 'junit_xml'
        if not os.path.isdir(RESULT_PATH + '/'+ self.junitsFolder):
            os.makedirs(RESULT_PATH + '/'+ self.junitsFolder)
        ## __init__
        ## 처음 커스텀필드값을 BLOCK로 초기화
        ## 테스트가 끝나면 해당 값이 PASS나 FAIL로 변경됨
        self.customFields = [['package_install', BLOCK], ['daemon', BLOCK], ['cmd', BLOCK], ['metadata', BLOCK], ['package', BLOCK], ['manual', BLOCK]]

    # junit.xml 파일 생성 코드
    def junitBuilder(self, *args):
        args = list(args)   
        testsuite = Element('testsuite')
        testcase = SubElement(testsuite, 'testcase')
        testcase.set('classname', args[0])
        testcase.set('name', args[0])
        testcase.set('status',args[1].lower()+'ed')
        if args[1] == FAIL:
            failure = SubElement(testcase, 'failure')
            failure.text = args[2]
        else: ## pass or blocked
            testcase.text = args[2]

        ## block인 경우엔 testNG 파일이 필요한 상태

        tree = ElementTree(testsuite)
        filePath = RESULT_PATH + '/' + self.junitsFolder+ '/junit-'+str(args[0])+'.xml'
        try:
            tree.write(filePath,encoding="utf-8", xml_declaration=True)
            print("* junit file is successfully created!")
        except Exception as e:            
            print("*** Junit Build Exception : %s"%(e))
            return