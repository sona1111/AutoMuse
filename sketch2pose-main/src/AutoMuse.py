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

# for importing the HRnet libs
import sys
sys.path.insert(0, 'C:/Users/sunli/Documents/AutoMuse/sketch2pose-main/src')


from pose import main_infer, main_infer_get_models
from scipy.spatial.transform import Rotation as R

joint_search_terms = (
    ("Hips",),
    ("LeftUpLeg", "Left Upper Leg",),
    ("RightUpLeg", "Right Upper Leg",),
    ("Spine",),
    ("LeftLeg","Left Leg"),
    ("RightLeg", "Right Leg",),
    ("Spine1",),
    ("LeftFoot", "Left Foot",),
    ("RightFoot", "Right Foot",),
    ("Spine2", "Thorax",),
    ("LeftToeBase", "Left Toe",),
    ("RightToeBase", "Right Toe",),
    ("Neck",),
    ("LeftShoulder", "Left Shoulder",),
    ("RightShoulder", "Right Shoulder",),
    ("Head",),    
    ("LeftArm", "Left Arm",),
    ("RightArm", "Right Arm",),
    ("LeftForeArm", "Left ForeArm",),
    ("RightForeArm", "Right ForeArm",),
    ("LeftHand", "Left Hand",),
    ("RightHand", "Right Hand",),
)

JOINTS = (
        "Hips",
        "Left Upper Leg",
        "Right Upper Leg",
        "Spine",
        "Left Leg",
        "Right Leg",
        "Spine1",
        "Left Foot",
        "Right Foot",
        "Thorax",
        "Left Toe",
        "Right Toe",
        "Neck",
        "Left Shoulder",
        "Right Shoulder",
        "Head",
        "Left ForeArm",
        "Right ForeArm",
        "Left Arm",
        "Right Arm",
        "Left Hand",
        "Right Hand",
)

post_model_paths = {
    "s2p": "C:/Users/sunli/Documents/AutoMuse/sketch2pose-main/models/hrn_w48_384x288.onnx",
    "dhrn": "C:/Users/sunli/Documents/AutoMuse/sketch2pose-main/models/retrain/pose_hrnet_w48_384x288_real.onnx",
    "retrained": ""
}


class AutoMuse():

    def __init__(self, cmds, pose_model="s2p-150-60"):
        print("Loading models")
        self.load_model(pose_model)
        self.only_rough = True
        self.cmds = cmds
        
    def load_model(self, pose_model):
        print("Loading model", pose_model)
        self.model_name, self.iterations_rough, self.iterations_opt = pose_model.split('-')
        self.loaded_model_args = main_infer_get_models(use_contacts=True, use_msc=True, pose_model_path=post_model_paths[self.model_name])        
        print("Models loaded")
    
        
    
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
            
    def update_skel_with_smpl(self, skel_root, smpl_results):

        search_results = [None] * len(joint_search_terms)       
        
        result = set()
        children = set(self.cmds.listRelatives(skel_root, fullPath=True) or [])
        
        while children:
            result.update(children)
            children = set(self.cmds.listRelatives(children, fullPath=True) or []) - result
            
        result.update(skel_root)
            
        for i, names in enumerate(joint_search_terms):
            for name in names:
                for exist_joint in result:
                    if not self.cmds.nodeType(exist_joint) == "joint":
                        continue
                    leaf = exist_joint.split('|')[-1].lower()
                    if leaf.endswith(name.lower()):
                        
                        x, y, z = smpl_results[i]
                        print(f"setting joint {leaf} - {JOINTS[i]}", x, y, z, "(deg)")
                        self.cmds.joint(exist_joint, e=True, ax=x, ay=y, az=z, roo='xyz')
                        
                        search_results[i] = exist_joint
                        break
                if search_results[i]:
                    break
            if search_results[i] is None:
                raise Exception(f"Couldn't find joint {names} in skeleton")
            
    def reset_skel(self):
        
        skel_root = self.cmds.ls(selection=True)
        search_results = [None] * len(joint_search_terms)       
        
        result = set()
        children = set(self.cmds.listRelatives(skel_root, fullPath=True) or [])
        
        while children:
            result.update(children)
            children = set(self.cmds.listRelatives(children, fullPath=True) or []) - result
            
        result.update(skel_root)
            
        for i, names in enumerate(joint_search_terms):
            for name in names:
                for exist_joint in result:
                    if not self.cmds.nodeType(exist_joint) == "joint":
                        continue
                    leaf = exist_joint.split('|')[-1].lower()
                    if leaf.endswith(name.lower()):
                        
                        x, y, z = 0, 0, 0
                        print(f"setting joint {leaf} - {JOINTS[i]}", x, y, z, "(deg)")
                        self.cmds.joint(exist_joint, e=True, ax=x, ay=y, az=z, roo='xyz')
                        
                        search_results[i] = exist_joint
                        break
                if search_results[i]:
                    break
            if search_results[i] is None:
                raise Exception(f"Couldn't find joint {names} in skeleton")
        
            
    def run_model_single(self, imgPath, scale=1.0):
        _joints_pos, joints_rot = self.process(imgPath)
        joints_rot = joints_rot.reshape(22, 3)
        return joints_rot.tolist()
        rotations = [R.from_rotvec(aa) for aa in joints_rot]
        eulers = [r.as_euler('xyz', degrees=True).tolist() for r in rotations]
        #eulers = [[0,0,0]] + eulers  # account for hips / root
        
        return eulers
        
    def generate_single(self, imgPath, scale=1.0):
        """
        In maya, make a single new skeleton based on a single drawing
        """
        #joints = self.process("C:/Users/sunli/Documents/AutoMuse/sketch2pose-main/data/images/IMG_0013_000125.jpg")
        joints, _joints_rot = self.process(imgPath)
        joints[:, 1:] = joints[:, 1:] * -1 # -1 as it seems to be flipped
        joints = (joints * scale).tolist() 
        self.create_skeleton_joints(joints)
        
    def edit_single(self, imgPath, use_global_orient=False, xo=-1, yo=-1, zo=-1, ro='xyz'):
        _joints_pos, joints_rot = self.process(imgPath)
        joints_rot = joints_rot.reshape(22, 3)
        rotations = [R.from_rotvec(aa) for aa in joints_rot]
        eulers = [r.as_euler('xyz', degrees=True).tolist() for r in rotations]
        #eulers = [[0,0,0]] + eulers  # account for hips / root
        print('global', eulers[0])
        # - - y
        if use_global_orient:
            #eulers[0] = [0.0, 0.0, -1.0 * eulers[0][2]]
            print(eulers[0])
            
            eulers[0] = [xo*eulers[0][ro.index('x')], yo*eulers[0][ro.index('y')], zo*eulers[0][ro.index('z')]]            
        else:
            eulers[0] = [0.0, 0.0, 0.0]
        edit_skel = self.cmds.ls(selection=True)
        self.update_skel_with_smpl(edit_skel, eulers)
        
        
    def process(self, imgPath):    
        joints_pos_return, joints_rot_return = main_infer([imgPath], self.only_rough, self.iterations_rough, self.iterations_opt, True, True, *self.loaded_model_args)
        return joints_pos_return[0], joints_rot_return[0]
        
    
    
        
        
        

if __name__ == "__main__":
    am = AutoMuse(None, pose_model="dhrn") # dhrn
    joints = am.run_model_single("C:/Users/sunli/Documents/AutoMuse/sketch2pose-main/data/images/Sketch13z.png", scale=1.0)

    from pprint import pprint
    pprint(joints)
    