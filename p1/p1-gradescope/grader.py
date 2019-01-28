#!/usr/bin/python
from xml.dom import minidom
import subprocess
import yaml
import json
import sys
import os

class TestCase:
    """Represents a node in the xml file"""
    name = ""
    status =""
    time = ""
    classname = ""
    failures = False
    msg = ""
#    points = 0
    def __init__(self,name,status,time,classname):
        self.name = name
        self.status = status
        self.time = time
        self.classname = classname
#        self.points = points
    def Failed(self,msg):
        self.failures = True
        self.msg = msg

class Test:
    """Represents a node in the xml file"""
    tests = 0
    failures = 0
    disabled = 0
    errors = 0
    timestamp = ""
    time =""
    name = ""
    nodes = None
    def __init__(self,tests,failures,disabled,errors,timestamp,time,name,nodes):
        self.tests = tests
        self.failures = failures
        self.disabled = disabled
        self.errors = errors
        self.timestamp = timestamp
        self.time = time
        self.name = name
        self.nodes = nodes

def fetchTestData(node):
    name = node.attributes['name'].value
    status = node.attributes['status'].value
    time = node.attributes['time'].value
    classname = node.attributes['classname'].value
#    points = int(node.attributes["Points"].value)
    testdata = TestCase(name,status,time,classname)
    if len(node.getElementsByTagName("failure"))!= 0:
        msg = node.getElementsByTagName("failure")[0].attributes['message'].value
        testdata.Failed(msg)
    return testdata

def getTestSuite(xmldoc):
    itemlist = xmldoc.getElementsByTagName('testsuites')
    itemlist = itemlist[0]
    tests = itemlist.attributes['tests'].value
    failures = itemlist.attributes['failures'].value
    disabled = itemlist.attributes['disabled'].value
    errors = itemlist.attributes['errors'].value
    timestamp = itemlist.attributes['timestamp'].value
    time = itemlist.attributes['time'].value
    name = itemlist.attributes['name'].value
    return Test(int(tests),int(failures),int(disabled),int(errors),timestamp,time,name,itemlist.getElementsByTagName('testsuite'))

def generateOverallStats(TS):
    total = TS.tests
    total = total- TS.failures
    total = total - TS.disabled
    total = total - TS.errors
    print TS.name+" stats:"
    print "Total Tests: "+str(TS.tests)
    print "Successful:  "+str(total)
    print "Failures:    "+str(TS.failures)
    print "Errors:      "+str(TS.errors)
    print "Disabled:    "+str(TS.disabled)

def gatherData(TS):
    tests = []
    for node in TS.nodes:
        for case in node.getElementsByTagName("testcase"):
            tests.append(fetchTestData(case))
    return tests

def calculatePoints(node,points):
    if node.failures:
        return 0
    else:
        return points

#Generates the json if it fails to compile or runs forever
def generateFailureJSON(error,max_score,testname):
	final_result = {}
	final_result["score"] = 0
        final_result["name"] = testname
	final_result["output"] = error
	final_result["max_score"] = float(max_score)
        return final_result

#Takes in test results from gatherData function. Produces list of objects for ouput
def generateJSON(TR,points):
    final_result = {}
    results_list = []
    for result in TR:
        temp_dict = {}
        if result.status == "error":
            results_list.append(generateFailureJSON(result.name+" crashed the test case and was unable to succesfully complete. You may have a Segmentation Fault in your code. Please re-examine your code and re-upload.",points,result.name))
            continue
        temp_dict["name"] = result.name
        temp_dict["score"] = float(calculatePoints(result,points))
        temp_dict["max_score"] = float(points)
        results_list.append(temp_dict)

    return generateResults(results_list)

###Tests file extension to check for test failure
def testFailure(fname):
    parts = fname.split(".")
    if parts[1] == "fail":
        return (True,parts[0])
    else:
        return (False,parts[0])

def generateResults(results):
    ret = ""
    for result in results:
        ret += json.dumps(result)+","
    return ret

def output(fname):
    f = open(fname,"r")
    outF = open("/autograder/results/results.json","w")
    outString = ""
    outString += '{"tests": ['
    for line in f:
        outString +=line.replace("\n","")
    outString=outString[:len(outString)-1]+"]}\n"
    outF.write(outString)
    outF.close()
    f.close()

##Only runs if things compiled and ran
def grade(fname,points):
	xmldoc = minidom.parse(fname)
	TS = getTestSuite(xmldoc)
	test_results = gatherData(TS)
	return generateJSON(test_results,points)

def write_failed_test(fname,testname,points):
    f = open(fname, 'w')
    f.write('<?xml version="1.0" encoding="UTF-8"?>')
    f.write('<testsuites tests="1" failures="1" disabled="0" errors="0" timestamp="2016-10-16T19:53:42" time="43.087" name="AllTests">')
    f.write( ' <testsuite name="PCTest" tests="1" failures="1" disabled="0" errors="0" time="0">')
    f.write("<testcase name=\"" + testname + "\" status=\"error\" time=\"0\" classname=\"PCTest\" Points=\"" + str(points) + "\" />")
    f.write('</testsuite>')
    f.write('</testsuites>')

def grade_all(test_file_name):
    tests = yaml.load(file(test_file_name, 'r'))
    if os.path.exists("/autograder/results/results_parts"):
        os.remove("/autograder/results/results_parts")
    parts_file = open("/autograder/results/results_parts", 'w')

    for test in tests['tests']:
        out_name = "/autograder/source/" + test['file'] + "_" + test['class'] + "_" + test['name'] + ".xml"
        print "Running: " + test['name']
        if os.path.exists(out_name):
            os.remove(out_name)
        p = subprocess.Popen(['timeout', '2m', "./" + test['file'], "--gtest_output=xml:" + out_name, "--gtest_filter=" + test['class'] + "." + test['name']], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        print "Test return code: " + str(p.returncode)
        if not os.path.exists(out_name):
            print "test failed"
            write_failed_test(out_name,test['name'],test['points'])
        results = grade(out_name, test['points'])
        parts_file.write(results)

    parts_file.close()
    output("/autograder/results/results_parts")

grade_all(sys.argv[1])
