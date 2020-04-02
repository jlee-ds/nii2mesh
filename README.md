# nii2mesh
segment the left hippocampus from .nii files, and then make them as mesh files (.obj).

- - - 
### 1. Install FSL 
Because the **FIRST** will be used for the segmetation, please install the FSL by following the instructions in https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation.

### 2. Segmentation
By using **FIRST**, segment the parts of brain from target .nii file.  

` > run_first_all -d -i target.nii -s L_Hipp -o output `
* -d : prevents FIRST from deleting the masks for individual structures
* -i : input file name
* -s : target part of brain
* -o : output namespace, will get several files like output-L_Hipp_first.vtk, output_to_std_sub.mat, and etc

more details in https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FIRST/UserGuide

### 3. .vtk to .obj
Fortunately, **FRIST** automatically provides .vtk file. But .vtk file is not readable for many mesh libs for python. So, maybe you want to use different kinds of mesh file format. There will be several ways to do this job, but **Slicer3D** is choosed in my case. You can install it in https://download.slicer.org/.

In **Slicer**, python(v2.7) interpreter can be used. Mesh can be processed before converting the format. In my case, three preprocessing was done.
* alignment to template mesh
* translation to origin
* scaling by maximum of absolute value per patients

If you want to know the details, please confirm the python file which name is **aling_center_scale.py**
