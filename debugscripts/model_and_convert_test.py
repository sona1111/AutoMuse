import numpy as np
import vispy.scene
from vispy.scene import visuals
import pickle
import numpy as np

with open("D:/010/spin_joints.pkl", "rb") as f:    
    joints = pickle.load(f)

SKELETON = (0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 12, 12, 13, 14, 16, 17, 18, 19)
def create_skeleton_joints():
    
    cmds.select( d=True )
    
    def append(j, pos):
        cmds.select(j)
        cmds.joint(p=pos)
       
    #joints = {JOINTS[i]: joints[i,:] for i in range(len(JOINTS))}
    
    maya_joints = []
    maya_joints.append(tuple(joints[0, :]))
    for i in range(len(SKELETON)):
        from_j = maya_joints[SKELETON[i]]
        to_pos = joints[i+1])
        append(from_j, to_pos)    
    
    

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



    
    

def plot_debug():
    #model_out = pickle.load(open("D:/010/spin.pkl", "rb"))
    #pos = model_out['body_pose'].reshape((21, 3))
    pos= joints
    #print(model_out)

    #assert False


    #
    # Make a canvas and add simple view
    #
    canvas = vispy.scene.SceneCanvas(keys='interactive', show=True)
    view = canvas.central_widget.add_view()


    # generate data
    # pos = np.random.normal(size=(100000, 3), scale=0.2)
    symbols = np.random.choice(['o', '^'], len(pos))


    # create scatter object and fill in the data
    scatter = visuals.Markers()
    scatter.set_data(pos, edge_width=0, face_color=(1, 1, 1, .5), size=5, symbol=symbols)

    view.add(scatter)

    view.camera = 'turntable'  # or try 'arcball'

    # add a colored 3D axis for orientation
    axis = visuals.XYZAxis(parent=view.scene)

    if __name__ == '__main__':
        import sys
        if sys.flags.interactive != 1:
            vispy.app.run()