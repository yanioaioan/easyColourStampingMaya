
import maya.cmds as cmds
from random import randint,random
import math


def getVtxPos( shapeNode ) :
 
	vtxWorldPosition = []    # will contain positions un space of all object vertex
 
	vtxIndexList = cmds.getAttr( shapeNode+".vrts", multiIndices=True )
 
	for i in vtxIndexList :
		curPointPosition = cmds.xform( str(shapeNode)+".pnts["+str(i)+"]", query=True, translation=True, worldSpace=True )    # [1.1269192869360154, 4.5408735275268555, 1.3387055339628269]
		vtxWorldPosition.append( curPointPosition )
 
	return vtxWorldPosition


def getVertexColor():
    """
    return a dict of vertex and their color
    """
    selection = cmds.ls(sl=True)
    colors = {}
    for obj in selection:
        colors[obj] = {}
        for v in range(cmds.polyEvaluate(v=True)):
            cmds.select(obj+'.vtx['+str(v)+']', r=True)
            colors[obj][v] = cmds.polyColorPerVertex(query=True, g=True, b=True)
            
    return colors
    
    
# this simple function is called each time the script below decides an object should be located
def locate_object(x,z):
			cmds.polyCone()		
			cmds.scale(0.5, 0.5, 0.5)
			cmds.move( x-50.0, 0.0, z-50.0)
    
    
mysphereradius=5
mysphere=cmds.polySphere(r=sphereradius)
#now assign a texture to sphere


#save a list of all shapes world positions
sphereVertexList=getVtxPos('pSphereShape1')
size=len(sphereVertexList)
vertexCount=0
#loop and print all positions of the vertices on the sphere
for vertexnumber in range(size):
	
	cmds.select(mysphere[0]+'.vtx['+str(vertexnumber)+']', r=True)
	
	#####Works just fine keep on working on it!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	#vertexnumber=203
	cmds.select(mysphere[0]+'.vtx['+str(vertexnumber)+']')
	r= cmds.polyListComponentConversion( mysphere[0]+'.vtx['+str(vertexnumber)+']', fv=True, tuv=True, internal=True )
	cmds.select(r)
	uvs=cmds.polyEditUV(r, query=True )
	sample = cmds.colorAtPoint( 'file1', output ='RGBA', u =uvs[0], v = uvs[1] )
	print sample
	if sample[0] > 0.7 and sample[1] > 0.2 and sample[2] > 0.2: # checks if the red component is more than 0.7 and the other to channels have significantly smaller values
		locate_object(x,z)	
		


  