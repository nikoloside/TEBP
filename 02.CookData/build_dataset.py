import numpy as np
import commonLib
import glob, os
from PIL import Image


def normalizeSeg(s_3d):
    s_3d = -s_3d
    s_3d = s_3d / 1.14 * 2.0 - 1.0
    return s_3d

def normalizeIm(s_3d):
    s_3d = s_3d / 0.05 - 0.9
    s_3d[ s_3d > 1] = 1
    s_3d[ s_3d < -1] = -1
    return s_3d

maxImValue = 0
minImValue = 0

maxSegValue = 0
minSegValue = 0

trainRate = 0.8

imPath = "/nashome/yhuang/yhuang/Workspace/BulletCreateDataSet/result/_out_bunny/im/vox/"
segPath = "/nashome/yhuang/yhuang/Workspace/BulletCreateDataSet/result/_out_bunny/seg-usdf/vox/"

saveTestPath = "/nashome/yhuang/yhuang/Workspace/data/bunny-no-gravity-usdf/test/"
saveTrainPath = "/nashome/yhuang/yhuang/Workspace/data/bunny-no-gravity-usdf/train/"

targetList = objList=sorted(glob.glob(segPath + "*.seg"), key=os.path.getmtime)

countTrain = 0

for targetSeg in targetList:
    expTime = os.path.basename(targetSeg).split(".")[0]
    targetIm = imPath + str(expTime) + ".im"
    if (len(glob.glob(targetIm))):
        # read seg
        print(targetIm)
        print(targetSeg)

        s_im = commonLib.get_from_h5py(targetIm)
        s_seg = commonLib.get_from_h5py(targetSeg)

        s_im = normalizeIm(s_im)
        s_seg = normalizeSeg(s_seg)

        maxValue = np.max(s_im)
        if maxValue > maxImValue:
            maxImValue = maxValue

        minValue = np.min(s_im)
        if minValue < minImValue:
            minImValue = minValue

        print("max im value ", maxImValue, maxValue)
        print("min im value ", minImValue, minValue)
        
        maxValue = np.max(s_seg)
        if maxValue > maxSegValue:
            maxSegValue = maxValue

        minValue = np.min(s_seg)
        if minValue < minSegValue:
            minSegValue = minValue

        print("max seg value ", maxSegValue, maxValue)
        print("min seg value ", minSegValue, minValue)

        im = saveTrainPath + str(expTime) + ".im"
        seg = saveTrainPath + str(expTime) + ".seg"
        if (countTrain >= len(targetList)*trainRate):
            im = saveTestPath + str(expTime) + ".im"
            seg =  saveTestPath + str(expTime) + ".seg"

        commonLib.save_as_h5py(im, s_im)
        commonLib.save_as_h5py(seg, s_seg)
    countTrain += 1

print("Finish")
