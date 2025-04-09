import numpy as np
import commonLib
import glob, os
from PIL import Image
import igl

def convert(v, f, typec):
    # calc sdf
    minV = -1
    maxV = 1
    size = 128
    sizej = 128j

    # convert
    x, y, z = np.mgrid[minV:maxV:sizej, minV:maxV:sizej, minV:maxV:sizej]
    positions = np.dstack([x.ravel(), y.ravel(),z.ravel()])

    s, i, c = igl.signed_distance(positions.squeeze(),v,f,typec,False)

    s_3d = s.reshape((size,size,size))

    return s_3d

def normalizeIm(s_3d):
    s_3d = -s_3d
    s_3d[ s_3d > 1] = 1
    s_3d[ s_3d < 0] = -1
    return s_3d

def normalizeSeg(s_3d):
    # s_3d = (s_3d - 0.15) / 0.15
    # s_3d[ s_3d > 1] = 1
    # s_3d[ s_3d < -1] = -1

    # s_3d[s_3d < 0] *= 2
    return -s_3d

maxDist = 0
minDist = 0

folderPath = "/nashome/yhuang/yhuang/Workspace/FractureRB/FractureRB-with-hyena/examples/"
workspacePath = "/nashome/yhuang/yhuang/Workspace/BulletCreateDataSet/data/input/_out_bunny/"
savePath = "/nashome/yhuang/yhuang/Workspace/BulletCreateDataSet/result/_out_bunny/seg-usdf/"
spcList = ["spc02", "spc03", "spc04"]

for spcName in spcList:
    spcPath = folderPath + spcName +  "/_out_bunny/"
    targetList = objList=sorted(glob.glob(spcPath + "out_vdb/*.obj"), key=os.path.getmtime)

    for target in targetList:
        expTime = os.path.basename(target).split(".")[0]
        # read seg
        print(target)
        v, f = igl.read_triangle_mesh(target)
        # SIGNED_DISTANCE_TYPE_UNSIGNED
        # SIGNED_DISTANCE_TYPE_WINDING_NUMBER
        s_3d = convert(v, f, igl.SIGNED_DISTANCE_TYPE_UNSIGNED)

        s_3d = normalizeSeg(s_3d)

        maxValue = np.max(s_3d)
        if maxValue > maxDist:
            maxDist = maxValue

        minValue = np.min(s_3d)
        if minValue < minDist:
            minDist = minValue

        print("max value ", maxDist, maxValue)
        print("min value ", minDist, minValue)

        niiPath = savePath + "nii/" + str(expTime) + ".nii"
        voxPath = savePath + "vox/" + str(expTime) + ".seg"
        gifPath =  savePath + "gif/" + str(expTime) + ".gif"

        commonLib.save_as_nib(niiPath, s_3d)
        commonLib.save_as_h5py(voxPath, s_3d)
        commonLib.save_as_gif(gifPath, s_3d)

print("Finish")
