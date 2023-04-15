import maya.cmds as cmds

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
    ("LeftForeArm", "Left ForeArm",),
    ("RightForeArm", "Right ForeArm",),
    ("LeftArm", "Left Arm",),
    ("RightArm", "Right Arm",),
    ("LeftHand", "Left Hand",),
    ("RightHand", "Right Hand",),
)


def update_skel_with_smpl(skel_root, smpl_results):

    search_results = [None] * len(joint_search_terms)
    #norm_min_x = float("inf")
    #norm_min_y = float("inf")
    #norm_min_z = float("inf")
    #norm_max_x = float("-inf")
    #norm_max_y = float("-inf")
    #norm_max_z = float("-inf")
    
    result = set()
    children = set(cmds.listRelatives(skel_root, fullPath=True) or [])
    print(children) 
    while children:
        result.update(children)
        children = set(cmds.listRelatives(children, fullPath=True) or []) - result
        
    result.update(skel_root)
        
    print(result) 
       
    for i, names in enumerate(joint_search_terms):
        for name in names:
            for exist_joint in result:
                if not cmds.nodeType(exist_joint) == "joint":
                    continue
                leaf = exist_joint.split('|')[-1].lower()
                if name.lower() in leaf:
                    #x, y, z = cmds.joint(exist_joint, q=True, p=True)
                    #norm_min_x = min(x, norm_min_x)
                    #norm_min_y = min(y, norm_min_y)
                    #norm_min_z = min(z, norm_min_z)
                    #norm_max_x = max(x, norm_max_x)
                    #norm_max_y = max(y, norm_max_y)
                    #norm_max_z = max(z, norm_max_z)
                    x, y, z = smpl_results[i]
                    print(f"setting joint {exist_joint}", x, y, z, "(deg)")
                    cmds.joint(exist_joint, e=True, ax=x, ay=y, az=z)
                    
                    search_results[i] = exist_joint
                    break
            if search_results[i]:
                break
        if search_results[i] is None:
            raise Exception(f"Couldn't find joint {names} in skeleton")
            
    #x_scale = (norm_max_x - norm_min_x) / 2.0
    #y_scale = (norm_max_y - norm_min_y) / 2.0
    #z_scale = (norm_max_z - norm_min_z)/ 2.0
    #print("scaling factor found:", x_scale, y_scale, z_scale)

    #for joint, new_joint_pos in zip(search_results, smpl_results):
    #    new_position = [x_scale * new_joint_pos[0], y_scale * new_joint_pos[1], z_scale * new_joint_pos[2]]
    #    
    #    print("Setting joint", exist_joint, new_joint_pos, new_position) 
    #    cmds.joint(joint, e=True, p=new_position)
            
    #cmds.select(skel_root)
        
    return list(result)



model_result = [[-0.0023381635546684265, 0.3791063725948334, -0.00804408174008131],
 [-0.03827338665723801, 0.2735949456691742, -0.00907007697969675],
 [0.06182297319173813, 0.2820501923561096, -0.04949333146214485],
 [-0.035108696669340134, 0.48692891001701355, -0.03394053876399994],
 [0.0838823914527893, -0.09357866644859314, 0.12095794826745987],
 [0.11146008968353271, -0.09783303737640381, 0.014938879758119583],
 [-0.07169269770383835, 0.633406400680542, -0.015261711552739143],
 [0.1943836212158203, -0.4719944894313812, -0.04586539417505264],
 [0.03708748519420624, -0.4941226840019226, -0.14757615327835083],
 [-0.06384644657373428, 0.69282466173172, -0.0031417664140462875],
 [0.2023565024137497, -0.5789896249771118, 0.05616322159767151],
 [0.09348870813846588, -0.596853494644165, -0.05987928807735443],
 [-0.07661273330450058, 0.8636698722839355, -0.0191210750490427],
 [-0.11261866986751556, 0.7761407494544983, 0.019206121563911438],
 [-0.034262411296367645, 0.7834295630455017, -0.028401726856827736],
 [-0.11221739649772644, 1.0373914241790771, -0.023713113740086555],
 [-0.2457880675792694, 0.7959314584732056, 0.047321856021881104],
 [0.041420817375183105, 0.8240439891815186, -0.1133788675069809],
 [-0.2801963984966278, 0.52970290184021, -0.03606979548931122],
 [0.18229404091835022, 0.5858390927314758, -0.20134538412094116],
 [-0.33800843358039856, 0.31053897738456726, 0.11589869856834412],
 [0.39955785870552063, 0.7234692573547363, -0.1236908957362175]]

thetas = [-0.3196, -0.0646, -0.0947, -0.1233,  0.1780,  0.2546,  0.1707,  0.0410,
         -0.0328,  0.6091,  0.0616, -0.0660,  0.5970,  0.1352,  0.0725, -0.1141,
         -0.0398,  0.0813,  0.0472,  0.2528, -0.0483, -0.0745, -0.2065,  0.0840,
          0.0831, -0.0402,  0.0533, -0.2260, -0.0130,  0.1807, -0.1881,  0.0737,
         -0.2839, -0.2526,  0.0000,  0.0579, -0.0100,  0.1760, -0.2325, -0.1451,
         -0.2309,  0.1991,  0.0332,  0.0000, -0.0468,  0.1434,  0.0861, -0.9637,
         -0.0102,  0.0743,  0.7031,  0.0439, -0.6469,  0.1263, -0.3002,  1.4380,
         -0.7054,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000]
thetas = [thetas[i:i + 3] for i in range(0, len(thetas), 3)]
import cv2
import numpy as np
from scipy.spatial.transform import Rotation as R
rotations = [R.from_rotvec(aa) for aa in thetas]
eulers = [r.as_euler('zxy', degrees=True).tolist() for r in rotations]

eulers = [[0,0,0]] + eulers
print(eulers)
#print(rotations)

#cmds.joint("Beta1:Spine", e=True, ax=45, ay=0, az=0)

edit_skel = cmds.ls(selection=True)
print(edit_skel)
update_skel_with_smpl(edit_skel, eulers)


print(cmds.joint("Beta:Spine2", q=True, p=True)[0])
print(cmds.attributeQuery( 'pos', n="Beta:Spine2", le=1))

nodes = cmds.ls(selection=True)

print(cmds.nodeType("|Beta:Hips|Beta:RightUpLeg|Beta:RightLeg|Beta:RightFoot|Beta:RightToeBase|Beta:RightFootToeBase_End"))
print(set(cmds.listRelatives(nodes, fullPath=True) or []))
print(list_all_children(nodes))

cmds.select("Beta:Spine2")
cmds.joint(e=True, p=(0, 8, 4))

#print(cmds.ls(long=True, selection=True, type'dagNode'))
