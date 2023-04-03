"""
Installation guide for windows:

Assuming that REPO is at C:/Users/sunli/Documents/AutoMuse , for example.

mayapy -m pip install -r C:/Users/sunli/Documents/AutoMuse/sketch2pose-main/requirements.txt
mayapy -m pip install torchvision
mayapy -m pip install pyglet==2.0.0

IN GIT BASH
$ patch ~/AppData/Roaming/Python/Python37/site-packages/smplx/body_models.py ~/Documents/AutoMuse/sketch2pose-main/patches/smplx.diff
$ patch ~/AppData/Roaming/Python/Python37/site-packages/selfcontact/body_segmentation.py ~/Documents/AutoMuse/sketch2pose-main/patches/selfcontact.diff

Somewhere around line 300 in C:/Users/sunli/AppData/Roaming/Python/Python37/site-packages/smplx/conversions.py

mask_c0 = mask_d2 * mask_d0_d1
mask_c1 = mask_d2 * ~(mask_d0_d1)
mask_c2 = ~(mask_d2) * mask_d0_nd1
mask_c3 = ~(mask_d2) * ~(mask_d0_nd1)
mask_c0 = mask_c0.view(-1, 1).type_as(q0)
mask_c1 = mask_c1.view(-1, 1).type_as(q1)
mask_c2 = mask_c2.view(-1, 1).type_as(q2)
mask_c3 = mask_c3.view(-1, 1).type_as(q3)

Somewhere around line 248 in C:/Users/sunli/AppData/Roaming/Python/Python37/site-packages/smplx/lbs.py

replace 

return verts, J_transformed

with

return verts, J_transformed, (A, J)


Somewhere around line 71 in C:/Users/sunli/AppData/Roaming/Python/Python37/site-packages/smplx/utils.py

replace

class SMPLXOutput(SMPLHOutput):
    expression: Optional[Tensor] = None
    jaw_pose: Optional[Tensor] = None
    
with

class SMPLXOutput(SMPLHOutput):
    expression: Optional[Tensor] = None
    jaw_pose: Optional[Tensor] = None
    A: Optional[Tensor] = None

-----

import sys
sys.path.insert(0, 'C:/Users/sunli/Documents/AutoMuse/sketch2pose-main/src')


from AutoMuse import AutoMuse
a = AutoMuse()

out = a.process('C:/Users/sunli/Documents/AutoMuse/sketch2pose-main/data/images/010.png')

print(out)

"""

from pose import main_infer

class AutoMuse():

    def __init__(self):
        pass
        
    def process(self, imgPath):
        return main_infer([imgPath])