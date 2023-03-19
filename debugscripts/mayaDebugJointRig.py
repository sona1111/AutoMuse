import maya.cmds as cmds

#cube1 = cmds.polyCube()
#cmds.cylinder( r=1, axis=(1, 1, 1), pivot=(0, 0, 1))

#cmds.cylinder( r=0.5,axis=(0, 1, 0), pivot=(0, 0, 0))
#cmds.move(0, 2, 0)
#cmds.scale( 1, 4, 1 )
circle1 = cmds.circle( nr=(0, 1, 0), c=(0, 0, 0))
curve1 = cmds.curve( p=[(0, 0, 0), (0, 4, 0), (0, 8, 0), (0, 8, 4)] )
extrudedCyl = cmds.extrude(circle1[0], curve1 ,ch=True, rn=False, po=0, et=2, ucp=0, fpt=0, upn=1, rotation=0, scale=1, rsp=1)

# Create a 3-joint chain
#
cmds.select( d=True )
rootJoint = cmds.joint( p=(0, 0, 0) )
cmds.joint( p=(0, 4, 0)  )
cmds.joint( 'joint1', e=True, zso=True, oj='xyz' )
cmds.joint( p=(0, 8, 0) )
cmds.joint( 'joint2', e=True, zso=True, oj='xyz' )

# Create a fourth joint with z joint limits of -90 deg for
# the lower limit and 90 deg for the upper limit.  The
# joint will be positioned at (0, 0, 4) in world
# coordinates.
#
cmds.joint( lz=('-90deg', '90deg'), p=(0, 8, 4) )

# Set the joint limits but leave them disabled.
cmds.joint( edit=True, lz=('-90deg', '90deg'), lsz=False )

print(extrudedCyl)
cmds.bindSkin(rootJoint, extrudedCyl[0])
