import os
import sys
from xml.etree.ElementTree import Element, SubElement #, Comment, tostring
from xml.etree.ElementTree import ElementTree

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from auto.__common__.__parameter__ import FAIL

def if_junit(junitClass, customfield, result):
    try:
        junitClass.build(customfield, result[1], result[2])
    except:
        pass
class junit:
    def __init__(self, folder):      
        self.junitsFolder = folder + '/junit_xml'
        if not os.path.isdir(self.junitsFolder):
            os.makedirs(self.junitsFolder)

    def build(self, *args):
        args = list(args)   
        testSuite = Element('testsuite')
        testCase = SubElement(testSuite, 'testcase')
        testCase.set('classname', args[0])
        testCase.set('name', args[0])
        testCase.set('status',args[1].lower()+'ed')
        if args[1] == FAIL:
            failure = SubElement(testCase, 'failure')
            failure.text = args[2]
        else: ## pass or blocked
            testCase.text = args[2]

        ## block인 경우엔 testNG 파일이 필요한 상태

        tree = ElementTree(testSuite)
        filePath = self.junitsFolder+ '/junit-'+str(args[0])+'.xml'
        try:
            tree.write(filePath,encoding="utf-8", xml_declaration=True)
            print("junit file is successfully created!")
        except:
            print("Failed to create junit file. Check your condition!")
            return
