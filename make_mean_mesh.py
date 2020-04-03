from pip._internal import main as pipmain
pipmain(['install','pandas'])

import numpy as np
import os
import pandas as pd

ad_ids = pd.read_csv('/Users/jlee/Desktop/JONG/tum/thesis/data/adni2/AD_PTID_IMGID.csv')
ad_ids = ad_ids['mesh_filename']
ad_ids = [i.split('_')[0] for i in ad_ids]
cn_ids = pd.read_csv('/Users/jlee/Desktop/JONG/tum/thesis/data/adni2/CN_PTID_IMGID.csv')
cn_ids = cn_ids['mesh_filename']
cn_ids = [i.split('_')[0] for i in cn_ids]

vtk_dir_path = '/Users/jlee/Desktop/JONG/tum/thesis/data/adni2/obj_acs/'

for i in cn_ids :
    f = vtk_dir_path + i + '-L_Hipp_first.obj'
    slicer.util.loadModel(f)

ns = slicer.util.getNodesByClass('vtkMRMLModelNode')[3:]
pts = []

for n in ns :
    pt = arrayFromModelPoints(n)
    ct = np.mean(pt, axis=0)
    if np.sum(ct) != 0 :
        print('WTF')
    pts.append(pt)

pts = np.asarray(pts)
mean_mesh = np.mean(pts, axis=0)
print(mean_mesh.shape)

pt[:] = mean_mesh[:]
slicer.util.saveNode(n, '/Users/jlee/Desktop/JONG/tum/thesis/data/adni2/mean_cn-L_Hipp_first.obj')
