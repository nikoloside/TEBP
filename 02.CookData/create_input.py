import numpy as np
import commonLib
import glob, os
import json
import pprint
import time

def getBoundary(posList, sizeT):
    limit = sizeT / 3.0;
    maxPos = [-1,-1,-1]
    minPos = [1,1,1]
    for pos in posList:
        min = pos - limit
        max = pos + limit
        for ind in range(3):
            value = pos.item(ind)
            if minPos[ind] > value:
                minPos[ind] = value
            if maxPos[ind] < value:
                maxPos[ind] = value
    return minPos, maxPos
        

def proceedImp(field, offset, sizeT, impList, dirList, posList):
    size = np.array([field.shape[0], field.shape[1], field.shape[2]])
    delta = sizeT / size.max()
    zero = size / 2
    print(size[0], delta)

    minPos, maxPos = getBoundary(posList, sizeT)
    minPosList = np.array(minPos)
    maxPosList = np.array(maxPos)
    minPosList[minPosList>1] = 1
    minPosList[minPosList<-1] = -1
    maxPosList[maxPosList>1] = 1
    maxPosList[maxPosList<-1] = -1
    minPosInt = minPosList / delta + zero - offset
    maxPosInt = maxPosList / delta + zero - offset
    sizeAdjustList = []
    for ind in range(3):
        # if (maxPosInt[ind] >= minPosInt[ind]):
        #     sizeAdjustList.append(range(int(maxPosInt[ind]), int(minPosInt[ind]),1))
        # else:
        sizeAdjustList.append(range(size[ind]));

    for i in sizeAdjustList[0]:
        for j in sizeAdjustList[1]:
            for k in sizeAdjustList[2]:
                loc = (np.array([i, j, k]) + offset - zero) * delta
                index = -1
                for imp in impList:
                    index += 1
                    if impList[index] == 0 :
                        continue
                    pos = posList[index]
                    dir = dirList[index]
                    vec = loc - pos 
                    normImp = decFunc(impList[index], np.linalg.norm(vec), sizeT)
                    normVec = vec / np.linalg.norm(vec)
                    dist = normImp * normVec
                    value = sum(dist * dir)
                    if value < 0:
                        value = 0
                    value = field[i, j, k] + value
                    if value > 1:
                        value = 1
                    field[i, j, k] = value
    return field


def decFunc(normImp, lenT, sizeT):
    limit = sizeT / 3.0;
    index = 1 - lenT / limit
    if index < 0:
        index = 0
    res = normImp * index
    return res


def normData(data):
    totalValue = 0.2
    newData = (data / totalValue) * 2.0 - 1.0
    return newData

size = (128, 128, 128)
vdbTransform = np.array([0, 0, 0])
voxelSize = 0.1
meshSize = 0.01
maxDist=0
minDist=0
sizeT = 2

# folderPath = "/nashome/yhuang/yhuang/Workspace/FractureRB/FractureRB-with-hyena/examples/"
# workspacePath = "/nashome/yhuang/yhuang/Workspace/BulletCreateDataSet/data/input/_out_bunny/"
# savePath = "/nashome/yhuang/yhuang/Workspace/BulletCreateDataSet/result/_out_bunny/im/"

folderPath = "/Users/yuhanghuang/FractureTest/resultAndData/test/timeTest/"
workspacePath = "/Users/yuhanghuang/FractureTest/resultAndData/test/timeTest/json/"
savePath = "/Users/yuhanghuang/FractureTest/resultAndData/test/timeTest/"

# spcList = ["spc01", "spc02", "spc03", "spc04", "spc05", "spc06", ]
# dataStartList = [1, 201, 251, 301, 351, 401]
# dataEndList = [180, 212, 280, 329, 386, 431]
spcList = [ "spcxx"]
# dataStartList = [1, 201, 251, 301, 351]
# dataEndList = [57, 212, 280, 329, 386]

for spcName in spcList:
    spcPath = folderPath + spcName +  "/_out_bunny/"
    targetList = objList=sorted(glob.glob(spcPath + "out_vdb/*.obj"), key=os.path.getmtime)

    
    for target in targetList:
        expTime = os.path.basename(target).split(".")[0]
        expPath = spcPath + "bunny-" + str(expTime)
        print(expPath)

        fileExist = glob.glob(savePath + "vox/" + str(expTime) + ".im")

        if len(fileExist) > 0:
            print(fileExist, " exist skip.")
            continue

        time_start = time.time()

        csvName = sorted(glob.glob(expPath + "/bunny_bunny1-*.txt"), key=os.path.getmtime)[0]
        jsonName = workspacePath + str(expTime) + ".txt"

        lineCount = 0
        with open(csvName) as old, open(jsonName, 'w') as new:
            oldLines = old.readlines()
            for line in oldLines:
                newLine = line.replace("\n","")
                if(lineCount == 0):
                    newLine = "[" + newLine
                if (lineCount >= len(oldLines) - 1):
                    newLine = newLine + "]\n"
                else:
                    newLine = newLine + ",\n"
                new.write(newLine)
                lineCount += 1

        # Main Process

        data = np.ndarray(size, float)
        data.fill(0)

        maxImpulse = 3045276
        impList = []
        dirList = []
        posList = []

        with open(jsonName) as f:
            jsonInput = json.load(f)
            for imp in jsonInput:
                normImp = imp["collImpulse"] / maxImpulse
                impList.append(normImp)
                dirList.append(np.array([imp["collDirections"][0], imp["collDirections"][1],imp["collDirections"][2]]))
                posList.append(np.array([imp["collPoints"][0],imp["collPoints"][1],imp["collPoints"][2]]))

        data = proceedImp(data, vdbTransform,  sizeT, impList, dirList, posList)
        # data = normData(data)

        maxValue = np.max(data)
        if maxValue > maxDist:
            maxDist = maxValue

        minValue = np.min(data)
        if minValue < minDist:
            minDist = minValue

        print("max value ", maxDist, maxValue)
        print("min value ", minDist, minValue)

        time_end = time.time()
        time_result = time_end - time_start
        print(time_result)

        niiPath = savePath + "nii/" + str(expTime) + ".nii"
        voxPath = savePath + "vox/" + str(expTime) + ".im"
        gifPath =  savePath + "gif/" + str(expTime) + ".gif"

        # commonLib.save_as_nib(niiPath, data)
        # commonLib.save_as_h5py(voxPath, data)
        # commonLib.save_as_gif(gifPath, data)
