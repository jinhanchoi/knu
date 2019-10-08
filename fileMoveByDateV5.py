import glob
import datetime
import shutil
import os,sys
import pandas

def getDirFileList(basePath, targetStr):
    return glob.glob(getFilePattern(basePath, targetStr))
def getFilePattern(basePath,targetStr):
    return basePath+targetStr+' 0[0-2]*'

def getTodayStr():
    return datetime.datetime.today().strftime("%Y-%m-%d")
def getYesterdayStr():
    yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")

def isPathValid(path):
    return os.path.exists(path)

def getTodayPath(basePath):
    return basePath+getTodayStr()+"/"
def getYesterdayPath(basePath):
    return basePath+getYesterdayStr()+"/"
def getParamPath(basePath, paramPath):
    return basePath+paramPath+"/"

def fileMove(fileList, destPath):
    print("###### Target File Path ######")
    print(destPath)
    for filename in fileList:
        shutil.move(filename,destPath+os.path.basename(filename))

def fileMoveBasedTodayDate(basePath):
    fileList = getDirFileList(getTodayPath(basePath), getTodayStr())
    print("###### Target File List #######", getParamPath(basePath, targetDateStr))
    print("fileList Length: ",len(fileList))
    if isPathValid(getYesterdayPath(basePath)):
        fileMove(fileList,getYesterdayPath(basePath))
    else:
        print("dest Path is not Exists")
        print("  ***  A: dest Path: ", getParamPath(basePath, destDateStr))

def fileMoveBasedParams(basePath, targetDateStr, destDateStr):
    fileList = getDirFileList(getParamPath(basePath, targetDateStr),targetDateStr)
    print("###### Target File List #######", getParamPath(basePath, targetDateStr))
    print("fileList Length: ",len(fileList))
    if isPathValid(getParamPath(basePath, destDateStr)):
        fileMove(fileList,getParamPath(basePath, destDateStr))
    else:
        print("dest Path is not Exists")
        print("  ***  B: dest Path: ", getParamPath(basePath, destDateStr))

from os import listdir
from os.path import isfile, join

def getAllFiles(basePath):
    onlyfiles = [f for f in listdir(basePath) if isfile(join(basePath, f)) and not f.startswith(".")]
    return onlyfiles
def readAllCsv(basePath,files):
    dataframes = [pandas.read_csv(join(basePath,f)) for f in files]
    return dataframes
def concatAllDataframes(dataframes):
    return pandas.concat(dataframes)

if __name__ == "__main__":
    
    ##path base logic
    if len(sys.argv) == 2:
        print("\n\n")
        print(sys.argv[1])
        fileMoveBasedTodayDate(sys.argv[1])

        mergedFrame = concatAllDataframes(readAllCsv(sys.argv[1],getAllFiles(sys.argv[1])))
        mergedFrame.to_csv(join(sys.argv[1],"merged.csv"),mode="w")

        #remove every file
        
    ##param base logic
    elif len(sys.argv) > 2:
        print("\n\n")
        print(sys.argv)
        basePath = sys.argv[1]
        targetDateStr = sys.argv[2]
        destDateStr = sys.argv[3]
        fileMoveBasedParams(basePath, targetDateStr, destDateStr)
    # else:
    #     print("Use One or Three Parameters : One -> Based TodayDate, Three -> Based Params Date")
    #     print("One Param Useage : python3 fileMoveByDate.py /Users/choijinhan/Desktop/")
    #     print("Three Param Useage : python3 fileMoveByDate.py /Users/choijinhan/Desktop/ 2019-08-10 2019-08-09")
    
