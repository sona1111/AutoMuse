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

from pose import main_infer, main_infer_get_models

class AutoMuse():

    def __init__(self, cmds):
        print("Loading models")
        self.loaded_model_args = main_infer_get_models(use_contacts=False, use_msc=False)
        # model_pose, device, model_contact, model_hmr, smpl, c_new_mse, checkpoint, selector, loss_parallel
        print("Models loaded")
        self.cmds = cmds
        
    
    def create_skeleton_joints(self, joints):
        SKELETON = (0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 12, 12, 13, 14, 16, 17, 18, 19)
        
        self.cmds.select( d=True )
        
        maya_joints = []
        
        def append(j, pos):
            self.cmds.select(j)
            maya_joints.append(self.cmds.joint(p=pos))
           
        #joints = {JOINTS[i]: joints[i,:] for i in range(len(JOINTS))}
        
        
        maya_joints.append(self.cmds.joint(p=joints[0]))
        for i in range(len(SKELETON)):
            from_j = maya_joints[SKELETON[i]]
            to_pos = joints[i+1]
            append(from_j, to_pos) 
        
    def generate_single(self, imgPath, scale=1.0):
        """
        In maya, make a single new skeleton based on a single drawing
        """
        #joints = self.process("C:/Users/sunli/Documents/AutoMuse/sketch2pose-main/data/images/IMG_0013_000125.jpg")
        joints = self.process(imgPath)
        joints = (-1 * joints * scale).tolist() # -1 as it seems to be flipped
        self.create_skeleton_joints(joints)
        
        
    def process(self, imgPath):
        return main_infer([imgPath], *self.loaded_model_args)[0]