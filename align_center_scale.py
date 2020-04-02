import numpy as np
import os

nii_dir_path = '/Users/jlee/Desktop/JONG/tum/thesis/data/adni2/nii/'
imgids = os.listdir(nii_dir_path)
imgids.remove('.DS_Store')

ptid_imgids = np.load('/Users/jlee/Desktop/JONG/tum/thesis/data/adni2/ptid_imgids_py2.npy')

# default three models are loaded in Slicer.
node_idx = 3
for ptid in ptid_imgids.keys() :
    c = 0
    pts = []
    mxs = []
    ofs = []
    for imgid in ptid_imgids[ptid] :
        if str(imgid) in imgids :
            vf = nii_dir_path + str(imgid) + '/' + str(imgid) + '-L_Hipp_first.vtk'
            mf = nii_dir_path + str(imgid) + '/' + str(imgid) + '_to_std_sub.mat'
            of = '/Users/jlee/Desktop/JONG/tum/thesis/data/adni2/obj_acs/' + str(imgid) + '-L_Hipp_first.obj'
            ofs.append(of)
            # load the model on the Slicer using filename
            slicer.util.loadModel(vf)
            # get the model from all models which are loaded Slicer
            # in slicer, they say it as node
            n = slicer.util.getNodesByClass('vtkMRMLModelNode')[-1]
            # get the align matrix to template
            m = np.loadtxt(mf)
            # get the points from the node
            pt = arrayFromModelPoints(n)
            # Align to the template mesh
            tmp_pt = np.c_[pt, np.ones(732)] # 732 * 4
            tmp_pt = np.transpose(tmp_pt) # 4 * 732
            tmp_pt = np.matmul(m, tmp_pt) # 4 * 4 X 4 * 732 = 4 * 732
            tmp_pt = np.transpose(tmp_pt) # 732 * 4
            tmp_pt = tmp_pt[:, :-1] # 732 * 3
            # Move the center to origin
            cen_pt = np.mean(tmp_pt, axis=0)
            tmp_pt = tmp_pt - cen_pt
            pt[:] = tmp_pt[:]
            pts.append(pt)
            mxs.append(np.max(pt))
            c += 1
    if c > 0 :
        # Scaling per patients
        mxv = np.max(mxs)
        print(mxs, mxv, ofs)
        ns = slicer.util.getNodesByClass('vtkMRMLModelNode')[node_idx:]
        for n, of in zip(ns, ofs) :
            pt = arrayFromModelPoints(n)
            pt[:] = pt[:] / mxv
            slicer.util.saveNode(n, of)
    node_idx += c
