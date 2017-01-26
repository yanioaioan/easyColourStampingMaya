
import maya.cmds as cmds
from random import randint,random
import math,os


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
def locate_object(stringChoice,x,y,z):
	
			#place a shape depending on what the user has selected
			if stringChoice == 'cones':
				cmds.polyCone()		
			if stringChoice == 'spheres':
				cmds.polySphere()		
			if stringChoice == 'cubes':
				cmds.polyCube()		
			
			scaleFactor=0.2
			cmds.scale(scaleFactor,scaleFactor,scaleFactor)
			cmds.move( x,y,z)


#
def apply_texture(object,textureNameUnderTexturesdir):
        
        cmds.sets(name='imageMaterialGroup', renderable=True, empty=True)
        shaderNode = cmds.shadingNode('phong', name='shaderNode', asShader=True)
        fileNode = cmds.shadingNode('file', name='fileTexture', asTexture=True)
        myfile = (currentDir+"/textures"+ "/" +textureNameUnderTexturesdir)
        cmds.setAttr('fileTexture'+'.fileTextureName', myfile, type="string")
        shadingGroup = cmds.sets(name='textureMaterialGroup', renderable=True, empty=True)
        cmds.connectAttr('shaderNode'+'.outColor','textureMaterialGroup'+'.surfaceShader', force=True)
        cmds.connectAttr('fileTexture'+'.outColor','shaderNode'+'.color', force=True)
        cmds.surfaceShaderList('shaderNode', add='imageMaterialGroup')
        cmds.sets(object, e=True, forceElement='imageMaterialGroup')

#At areas where the underlying vertex color is red, place cones
def checkSampleAndPlace(sample):
	if sample[0] > 0.9 and sample[1] < 0.2 and sample[2] < 0.2: # checks if the red component is more than 0.9 and the other to channels have significantly smaller values
		print "sample=%s"%sample
		print "vertexnumber=%s"%vertexnumber
		#cmds.select(mysphere[0]+'.vtx['+str(vertexnumber)+']')
		locate_object('cones',sphereVertexPosList[vertexnumber][0], sphereVertexPosList[vertexnumber][1], sphereVertexPosList[vertexnumber][2])	
	
	#At areas where the underlying vertex color is white, place sphere
	if sample[0] > 0.9 and sample[1] > 0.9 and sample[2] > 0.9: # checks if all components are more than 0.9, white areas
		print "sample=%s"%sample
		print "vertexnumber=%s"%vertexnumber
		#cmds.select(mysphere[0]+'.vtx['+str(vertexnumber)+']')
		locate_object('spheres',sphereVertexPosList[vertexnumber][0], sphereVertexPosList[vertexnumber][1], sphereVertexPosList[vertexnumber][2])	
		
	
	#At areas where the underlying vertex color is black, place cubes
	if sample[0] < 0.2 and sample[1] < 0.2 and sample[2] < 0.2: # checks if all components are les than 0.2, black areas
		print "sample=%s"%sample
		print "vertexnumber=%s"%vertexnumber
		#cmds.select(mysphere[0]+'.vtx['+str(vertexnumber)+']')
		locate_object('cubes',sphereVertexPosList[vertexnumber][0], sphereVertexPosList[vertexnumber][1], sphereVertexPosList[vertexnumber][2])	
				
	
currentDir=os.getcwd()
cmds.file(new=True, force=True)
#create a sphere    
mysphereradius=5
mysphere=cmds.polySphere(r=mysphereradius)

#now assign a texture to selected sphere
#create one shader		
#myshadingNodeName1=createShaderwithText(1)
cmds.select(mysphere[0])
apply_texture(mysphere[0],"1637192.jpg")
cmds.DisplayShadedAndTextured()

#save a list of all shapes world positions
sphereVertexPosList=getVtxPos('pSphereShape1')
size=len(sphereVertexPosList)
vertexCount=0

#for all positions of the vertices on the sphere
for vertexnumber in range(size):
	
	#cmds.select(mysphere[0]+'.vtx['+str(vertexnumber)+']', r=True)	
	#####Works just fine keep on working on it!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	#vertexnumber=203
	#cmds.select(mysphere[0]+'.vtx['+str(vertexnumber)+']')
	
	#convert each vtx, from vertex to uv
	r= cmds.polyListComponentConversion( mysphere[0]+'.vtx['+str(vertexnumber)+']', fv=True, tuv=True, internal=True )
	#cmds.select(r)
	
	#and then use this uv to query its values
	uvs=cmds.polyEditUV(r, query=True )
	#and then assing these uv vales to the colorAtPoint u and v flags to retrieve the color sample at this particular uv coordinate(of that vertex)
	sample = cmds.colorAtPoint( 'fileTexture.fileTextureName', output ='RGBA', u =uvs[0], v = uvs[1] )
	#pass the sample down to the function checkSampleAndPlace which is responsible for placing the appropriate shapes depending on the colour found on a particular vertex 
	checkSampleAndPlace(sample)
	
	
	
	
	
	  