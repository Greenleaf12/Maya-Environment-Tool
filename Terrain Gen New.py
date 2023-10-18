# Terrain Generator 

import maya.cmds as cmds
import random
import math
import MASH.api as mapi
  
    #Create Trees    
def mashTrees(winID, numberTrees, scaleTrees, *pArgs):

    Landscape01="Landscape01"
    Tree()
    
    cmds.select("TreeOriginal")
    cmds.scale(scaleTrees,scaleTrees,scaleTrees)
    
    # create MASH network
    mashNetwork = mapi.Network()
    mashNetwork.createNetwork(name="Trees")
    mashNetwork.meshDistribute(Landscape01)
    
    # set MASH points 
    mashNetwork.setPointCount(numberTrees)
    cmds.setAttr ("Trees_Distribute.calcRotation", 0)
    cmds.setAttr ("Trees_Distribute.distanceAlongNormal", 8) 
    
    mashNetwork.addNode("MASH_Random")
    cmds.setAttr ("Trees_Random.rotationY", 360)
    cmds.setAttr ("Trees_Random.rotationX", 5)
    cmds.setAttr ("Trees_Random.rotationZ", 5)
    cmds.setAttr ("Trees_Random.scaleX", 0.2)
    cmds.setAttr ("Trees_Random.scaleY", 1)
    cmds.setAttr ("Trees_Random.scaleZ", 0.2)
    
    nodes = mashNetwork.getAllNodesInNetwork()
    
    for node in nodes:
        mashNode = mapi.Node(node)
        falloffs = mashNode.getFalloffs()
    
    # Create grass    
def mashGrass(winID, numberGrass, scaleGrass, *pArgs):  

    Landscape01="Landscape01"   
    grass()
    cmds.select("grassBlade")
    cmds.scale(scaleGrass,scaleGrass,scaleGrass)
    # create MASH network
    mashNetwork = mapi.Network()
    mashNetwork.createNetwork(name="Grass")
    mashNetwork.meshDistribute(Landscape01)
    cmds.setAttr ("Grass_Distribute.meshType", 1)
    cmds.setAttr ("Grass_Distribute.pointCount", 400)
    
    # set MASH points 
    mashNetwork.setPointCount(numberGrass)
    cmds.setAttr ("Grass_Distribute.calcRotation", 0)
    
    # add nodes
    mashNetwork.addNode("MASH_World")
    cmds.setAttr ("Grass_World.randomPointsPerCluster", 10)
    cmds.setAttr ("Grass_World.clusterMode", 4)
    cmds.setAttr ("Grass_World.pointsPerCluster", 14)
    cmds.setAttr ("Grass_World.radius", 4)
    cmds.setAttr ("Grass_World.clusterRadius", 3)
    
    mashNetwork.addNode("MASH_Random")
    cmds.setAttr ("Grass_Random.positionZ", 20)
    cmds.setAttr ("Grass_Random.positionX", 20)
    cmds.setAttr ("Grass_Random.rotationX", 20)
    cmds.setAttr ("Grass_Random.rotationY", 360)
    cmds.setAttr ("Grass_Random.rotationZ", 20)
    cmds.setAttr ("Grass_Random.scaleX", 10)
    cmds.setAttr ("Grass_Random.scaleY", 25)
    cmds.setAttr ("Grass_Random.scaleZ", 10)
    
    nodes = mashNetwork.getAllNodesInNetwork()
    
    for node in nodes:
        mashNode = mapi.Node(node)
        falloffs = mashNode.getFalloffs()
        
    #tree group        
def treeGroup():
    newObj = Tree() 
    cmds.move(random.uniform(-50,50),random.random()/2,random.uniform(-50,50),r=True,os=True,wd=True)
    cmds.rotate(0, random.uniform(0,360), 0, r=True) 
    cmds.select(newObj)
    
    #Create river      
def createRiver(winID, *pArgs):
    Landscape01="Landscape01"
    percent = 0.002
    vertex = []
    cmds.select(Landscape01)
    
    for obj in cmds.ls(sl=1, long=1):
        indexes = list(range(cmds.polyEvaluate(obj, vertex=True)))
        random.shuffle(indexes)
        indexes = indexes[:int(4)]	
        for i in range(len(indexes)):
            indexes[i] = obj+'.vtx['+str(indexes[i])+']'
        vertex.extend(indexes)
    cmds.select(vertex, r=1)
    a=indexes[0]
    b=indexes[1]
    c=indexes[2]
    d=indexes[3]
    
    a=a.strip("|Landscape01.vtx[]")
    b=b.strip("|Landscape01.vtx[]")
    c=c.strip("|Landscape01.vtx[]")
    d=d.strip("|Landscape01.vtx[]")
    
    a=int(a)
    b=int(b)
    c=int(c)
    d=int(d)
    
    cmds.polySelect( 'Landscape01', shortestEdgePath=(a, b))
    cmds.polySelect( 'Landscape01', shortestEdgePath=(b, c))
    cmds.polySelect( 'Landscape01', shortestEdgePath=(c, d))
    
    cmds.ConvertSelectionToFaces()
    cmds.move(0.0, -80, 0.0, r=True)
    
    #Set Colour
def setColour(winID, *pArgs):    
    
    rgb = cmds.colorSliderGrp( 'polygonColour', query = True, rgbValue = True )
    myShader = cmds.shadingNode( 'lambert', asShader = True)    
    cmds.setAttr( myShader + '.color', rgb[ 0 ], rgb[ 1 ], rgb[ 2 ], type = 'double3' )
    cmds.select('Landscape01')
    cmds.hyperShade(assign = myShader) 
    
    #Creates land
def createLand (subControl, sizeControl, heightControl ):

    cmds.select(all=True)
    cmds.delete()
    
    landsub = subControl 
    landsize = sizeControl 
    maxheight = heightControl
    land = cmds.polyPlane( sx=subControl, sy=subControl, w=landsize, h=landsize)
    vtxCount = list(range(cmds.polyEvaluate(v=True)))
    random.shuffle(vtxCount)
    values = [random.triangular(0,1,0) for i in range(10)]
    values_count = len(values)
    optimize_setter = []
    
    for x in vtxCount:
        mod = x % values_count
        optimize_setter += [float(0),values[mod-1]*maxheight,float(0)]
    cmds.setAttr('pPlane1.vtx[:]', *optimize_setter)
    cmds.select(land[0])
    cmds.rename ("Landscape01") 
	
	#Create Terrain
def actionProc(winID, subControl, sizeControl, heightControl, *pArgs):
    
    createLand (subControl, sizeControl, heightControl)
	
	#Close UI
def cancelProc(winID, *pArgs):
    cmds.deleteUI(winID)
	
	# Smoothing	
def smoothing(winID, *pArgs):
    cmds.select("Landscape01")
    cmds.polySmooth(c=1,dv=1,kb=True,ro=1)   
    cmds.pause( sec=1 )
    return True
    cmds.select(clear=True)
    
    #Hills preset
def hillPreset (winID, subControl, sizeControl, heightControl, hillHeight, ditchDepth, rock1amountControl, rock2amountControl, rockscaleControl, *pArgs):

    createLand (15, sizeControl, heightControl)
    for i in range (6):
        createHill(winID, 60)
    for j in range (4):
        createDetail(winID, 60)
    for k in range (4):
        createDitch(winID, 30)
    
    smoothing(winID)
    rockSpawn(winID, 25, 25, 0.5, 0)
    rockSpawn(winID, 25, 25, 0.8, 0)
    mashTrees(winID, 400, 2.0)
    hillShader = cmds.shadingNode( 'lambert', asShader = True)    
    cmds.setAttr( hillShader + '.color', 0.13, 0.25, 0.057, type = 'double3' )
    cmds.select('Landscape01')
    cmds.hyperShade(assign = hillShader) 
    cmds.select(clear=True)
    
    #Plains preset
def plainPreset (winID, subControl, sizeControl, heightControl, hillHeight, ditchDepth, rock1amountControl, rock2amountControl, rockscaleControl, *pArgs):

    createLand (30, sizeControl, heightControl)
    for i in range (12):
        createHill(winID, 20)
        
    smoothing(winID)
    mashGrass(winID, 200, 9, 30, 3, 3)      
    rockSpawn(winID, 50, 50, 1, 0)
    rockSpawn(winID, 50, 50, 0.5, 0)
    plainShader = cmds.shadingNode( 'lambert', asShader = True)    
    cmds.setAttr( plainShader + '.color', 0.3, 0.42, 0.0, type = 'double3' )
    cmds.select('Landscape01')
    cmds.hyperShade(assign = plainShader) 
    cmds.select(clear=True)
    
    #Forest preset
def forestPreset (winID, subControl, sizeControl, heightControl, hillHeight, ditchDepth, rock1amountControl, rock2amountControl, rockscaleControl, *pArgs):

    createLand (30, sizeControl, heightControl)
    for i in range (6):
        createHill(winID, 40)
    
    smoothing(winID)
    mashTrees(winID, 3000, 1.5)
    
    forestShader = cmds.shadingNode( 'lambert', asShader = True)    
    cmds.setAttr( forestShader + '.color', 0.2, 0.6, 0.06, type = 'double3' )
    cmds.select('Landscape01')
    cmds.hyperShade(assign = forestShader) 
    cmds.select(clear=True)
    
    #Mountains preset
def mountainPreset (winID, subControl, sizeControl, heightControl, mountainHeight, hillHeight, ditchDepth, rock1amountControl, rock2amountControl, rockscaleControl, *pArgs):

    createLand (25, sizeControl, heightControl)
    for i in range (4):
        createMountins(winID, 60)
    for j in range (4):
        createHill(winID, 60)
    for k in range (4):
        createDetail(winID, 30)
        
    smoothing(winID)
    rockSpawn(winID, 50, 50, 1, 0)
    rockSpawn(winID, 50, 50, 0.5, 0)
    cmds.select(clear=True)
    
    #Lakes preset   
def riverPreset (winID, waterHeight, subControl, sizeControl, heightControl, mountainHeight, hillHeight, rock1amountControl, rock2amountControl, rockscaleControl, *pArgs):

    createLand (25, sizeControl, heightControl)
    for i in range (2):
        createMountins(winID, mountainHeight)
    for j in range (6):
        createHill(winID, 60)
    for k in range (2):
        createDetail(winID, 30)
        
    smoothing(winID)
    createRiver(winID)
    for k in range (2):
        createDitch(winID, 60)
    mashTrees(winID, 400, 1)
    rockSpawn(winID, 50, 50, 1, 0)
    rockSpawn(winID, 50, 50, 0.5, 0)
    Water(winID, 20)
    riverShader = cmds.shadingNode( 'lambert', asShader = True)    
    cmds.setAttr( riverShader + '.color', 0.2, 0.4, 0.03, type = 'double3' )
    cmds.select('Landscape01')
    cmds.hyperShade(assign = riverShader) 
    cmds.select(clear=True)
    
    #Desert preset   
def desertPreset (winID, subControl, sizeControl, heightControl, mountainHeight, hillHeight, rock1amountControl, rock2amountControl, rockscaleControl,  *pArgs):

    createLand (25, sizeControl, heightControl)
    
    for j in range (8):
        createHill(winID, 30)        
    smoothing(winID)
    rockSpawn(winID, 20, 20, 5, 0)
    rockSpawn(winID, 40, 40, 2, 0)
    rockSpawn(winID, 30, 30, 3, 0)
    desertShader = cmds.shadingNode( 'lambert', asShader = True)    
    cmds.setAttr( desertShader + '.color', 0.67, 0.44, 0.18, type = 'double3' )
    cmds.select('Landscape01')
    cmds.hyperShade(assign = desertShader) 
    cmds.select(clear=True)
    
    #Canyons preset   
def canyonsPreset (winID, subControl, sizeControl, heightControl, mountainHeight, hillHeight, rock1amountControl, rock2amountControl, rockscaleControl,  *pArgs):

    createLand (35, sizeControl, heightControl)
     
    for k in range (5):
        createDetail(winID, 60)
        
    smoothing(winID)
    createRiver(winID)
    createRiver(winID)
    createRiver(winID)
    createRiver(winID)
    
    rockSpawn(winID, 50, 50, 1, 0)
    rockSpawn(winID, 50, 50, 2, 0)
    cmds.select(clear=True)
    
    #Islands preset   
def islandsPreset (winID, waterHeight, subControl, sizeControl, heightControl, mountainHeight, hillHeight, rock1amountControl, rock2amountControl, rockscaleControl, *pArgs):

    createLand (25, sizeControl, heightControl)
    for i in range (4):
        createMountins(winID, 20)
    for j in range (8):
        createHill(winID, 60)
    for k in range (2):
        createDetail(winID, 30)
        
    smoothing(winID)
    Water(winID, 120)
    islandShader = cmds.shadingNode( 'lambert', asShader = True)    
    cmds.setAttr( islandShader + '.color', 0.2, 0.4, 0.03, type = 'double3' )
    cmds.select('Landscape01')
    cmds.hyperShade(assign = islandShader) 
    cmds.select(clear=True)
    
    #Create Water           
def Water(winID, waterHeight, *pArgs):

    if cmds.objExists('water'):
        cmds.delete('water')
    waterShader = cmds.shadingNode( 'aiStandardSurface', asShader = True)    
    cmds.setAttr( waterShader + '.baseColor', 0.0, 0.104, 0.34, type = 'double3' )
    cmds.setAttr ( waterShader + '.specularRoughness',  0.027436)
    cmds.setAttr ( waterShader + '.transmission', 0.45)

    cmds.polyPlane(w=2000,h=2000,name='water')
    cmds.ls('water*')
    
    cmds.hyperShade(assign = waterShader) 
    cmds.select('water')
    cmds.move (0, waterHeight, 0, a=True)
    
    #Creates a rock   
def Rock():
    
    #Make rock
    Cube=cmds.polyCube(h=8,w=8,d=8,sx=3,sy=3,sz=3,name='RockOriginal')
    cubeFaces = (Cube[0]+'.f[25]',Cube[0]+'.f[37]',Cube[0]+'.f[1]',Cube[0]+'.f[46]')
    #Make adjust
    for i in range (1):
        cmds.select(cubeFaces)   
        cmds.scale (random.uniform(1.5,2.5),random.uniform(1,1.2),random.uniform(1.5,2.5),r=True)
    
    cubeFaces2 = (Cube[0]+'.f[45]',Cube[0]+'.f[0]',Cube[0]+'.f[38]',Cube[0]+'.f[36]')
    #Make adjust
    for i in range (1):
        cmds.select(cubeFaces2)   
        cmds.scale (random.uniform(0.5,1.5),random.uniform(1,1.2),random.uniform(0.5,1.5),r=True)
        
    cubeFaces3 = (Cube[0]+'.f[43]',Cube[0]+'.f[19]',Cube[0]+'.f[7]',Cube[0]+'.f[52]')
    #Make adjust
    for i in range (1):
        cmds.select(cubeFaces3)   
        cmds.scale (random.uniform(1.5,2),random.uniform(0.5,2.2),random.uniform(1.5,2),r=True)
    
    cmds.select(Cube[0]+'.f[13]') 
    cmds.move (1,random.uniform(2.5,5.2),1,r=True)
    cmds.select(Cube[0]+'.f[31]') 
    cmds.move (1,random.uniform(-2.5,-5.2),1,r=True)
    
    cmds.select(cl=True) 
    cmds.polySelect('RockOriginal',el=22)
    cmds.move (0,random.uniform(1.1,1.8),0,r=True)
    
    cmds.select(Cube[0]+'.vtx[36]',Cube[0]+'.vtx[32]',Cube[0]+'.vtx[39]',Cube[0]+'.vtx[35]',Cube[0]+'.vtx[3]',Cube[0]+'.vtx[7]',Cube[0]+'.vtx[0]',Cube[0]+'.vtx[4]') 
    
    cmds.scale (random.uniform(1.4,2.6),random.uniform(1,2),random.uniform(1.4,2.6),r=True)  
    cmds.select(Cube)      
    cmds.polySmooth(c=1,dv=1,kb=True,ro=1)
    rockShader = cmds.shadingNode( 'lambert', asShader = True)    
    cmds.setAttr( rockShader + '.color', 0.185, 0.185, 0.185, type = 'double3' )
    cmds.select(Cube)
    #cmds.polySmooth(c=1,dv=2,kb=True,ro=1) 
    addNoise(2)
    cmds.move(random.uniform(-100,100),0,random.uniform(-100,100))
    cmds.hyperShade(assign = rockShader)  

def smallRock():
    
    randomFloat = random.uniform(0.01,2.5)
    #Make rock
    Cube=cmds.polyCube(h=8,w=8,d=8,sx=3,sy=3,sz=3,name='RockOriginal')
    cubeFaces = (Cube[0]+'.f[25]',Cube[0]+'.f[37]',Cube[0]+'.f[1]',Cube[0]+'.f[46]')
    #Make adjust
    cmds.select(cubeFaces)   
    cmds.scale (random.uniform(1.5,2.5),random.uniform(1,1.2),random.uniform(1.5,2.5),r=True)
          
    cubeFaces2 = (Cube[0]+'.f[45]',Cube[0]+'.f[0]',Cube[0]+'.f[38]',Cube[0]+'.f[36]')
    cmds.select(cubeFaces2)   
    cmds.scale (random.uniform(0.5,1.5),random.uniform(1,1.2),random.uniform(0.5,1.5),r=True)    
           
    cubeFaces3 = (Cube[0]+'.f[43]',Cube[0]+'.f[19]',Cube[0]+'.f[7]',Cube[0]+'.f[52]')
    cmds.select(cubeFaces3)   
    cmds.scale (random.uniform(1.5,2),random.uniform(0.5,2.2),random.uniform(1.5,2),r=True) 
          
    cmds.select(Cube[0]+'.f[13]') 
    cmds.move (1,random.uniform(2.5,5.2),1,r=True)
    cmds.select(Cube[0]+'.f[31]') 
    cmds.move (1,random.uniform(-2.5,-5.2),1,r=True)
    
    cmds.select(cl=True) 
    cmds.polySelect('RockOriginal',el=22)
    cmds.move (0,random.uniform(1.1,1.8),0,r=True)
    
    cmds.select(Cube[0]+'.vtx[36]',Cube[0]+'.vtx[32]',Cube[0]+'.vtx[39]',Cube[0]+'.vtx[35]',Cube[0]+'.vtx[3]',Cube[0]+'.vtx[7]',Cube[0]+'.vtx[0]',Cube[0]+'.vtx[4]') 
    cmds.scale (random.uniform(1.4,2.6),random.uniform(1,2),random.uniform(1.4,2.6),r=True) 
    
    cmds.select(Cube)  
    cmds.scale (random.uniform(0.5,2.0),random.uniform(0.5,2.0),random.uniform(0.5,2.0),a=True)    
    cmds.scale (randomFloat,randomFloat,randomFloat,r=True)      
    cmds.polySmooth(c=1,dv=2,kb=True,ro=1) 
    addNoise(1)
    cmds.select('RockOriginal', r=True ) 
    cmds.rotate(random.uniform(10,120),random.uniform(10,120),random.uniform(10,1200),a=True)
    cmds.move(random.uniform(-100,100),0,random.uniform(-100,100))
    cmds.rename('Rock_Single_01')
    #cmds.group( em=True, name='Rock_Singles')
    #cmds.group('Rock_Single_*', name='Rock_Singles', a=True)
    #cmds.select('Rock_Singles', r=True )
    #cmds.rename('Rock_Single_Group')
        
    #Creates a tree    
def Tree():

    leafShader = cmds.shadingNode( 'blinn', asShader = True)    
    cmds.setAttr( leafShader + '.color', 0.0440, 0.203, 0, type = 'double3' )
    
    cmds.setAttr ( leafShader + '.eccentricity', 0.25)
    cmds.setAttr ( leafShader + '.specularRollOff', 0.3)
    
    barkShader = cmds.shadingNode( 'blinn', asShader = True)    
    cmds.setAttr( barkShader + '.color', 0.4, 0.08, 0, type = 'double3' )
    cmds.setAttr ( barkShader + '.eccentricity', 0.45)
    cmds.setAttr ( barkShader + '.specularRollOff', 0.1)
    
    randomFloat = random.uniform(1,1.2)
    randomFloat2 = random.uniform(0.5,0.8)
    randomFloat3 = random.uniform(1.3,1.5) 
    randomFloat4 = random.uniform(-0.2,-0.4)
     
    randomFloat5 = random.uniform(0.6,1) 
    randomFloat6 = random.uniform(0.6,1) 
    randomFloat7 = random.uniform(0.6,1)
    randomFloat8 = random.uniform(0.6,1)
    
    #Make Trunk
    ''' Makes the tree trunk '''  
    Cylinder=cmds.polyCylinder (h=8,r=0.5,sx=8,sy=3,name='TreeOriginal')
    
    #Make Bush
    cmds.select(Cylinder[0]+'.f[25]')
    cmds.polyExtrudeFacet(s=(random.uniform(1,1.2),random.uniform(0.8,1.1),random.uniform(1,1.2)), t=(0, randomFloat2, 0))
    cmds.scale (2,randomFloat,2)
    cmds.polyExtrudeFacet(s=(randomFloat,randomFloat,randomFloat), t=(0, randomFloat2, 0))
    cmds.scale (randomFloat3,randomFloat,randomFloat3)
    
    cmds.polyExtrudeFacet(s=(randomFloat,randomFloat,randomFloat), t=(0, randomFloat2, 0))
    cmds.scale (randomFloat3,randomFloat,randomFloat3)
    cmds.polyExtrudeFacet(s=(randomFloat,randomFloat,randomFloat), t=(0, randomFloat2, 0))
    cmds.scale (1.1,randomFloat,1.1)
    
    #Make Tree Top
    ''' Makes the tree top '''  
    cmds.polyExtrudeFacet(s=(1,1,1), t=(0, random.uniform(1.2,2.6), 0))
    cmds.scale (random.uniform(0.8,0.9),1,random.uniform(0.8,0.9))
    cmds.polyExtrudeFacet(s=(1,1,1), t=(0, random.uniform(1.2,1.6), 0))
    cmds.scale (random.uniform(0.7,0.8),1,random.uniform(0.7,0.8))
    cmds.polyExtrudeFacet(s=(1,1,1), t=(0, random.uniform(1.2,1.6), 0))
    cmds.scale (random.uniform(0.6,0.7),1,random.uniform(0.6,0.7))
    cmds.polyExtrudeFacet(s=(1,1,1), t=(0, 2, 0))
    cmds.scale (0.05,1,0.05)
    
    #Adjust Trunk
    ''' Adjusts tree trunk '''  
    cmds.select(Cylinder[0]+'.e[8:15]')
    cmds.scale (1.4,randomFloat3,1.4)
    cmds.select(Cylinder[0]+'.e[0:7]')
    cmds.scale (1.6,randomFloat3,1.6)
    
    #Make bottom Edge
    ''' Adjusts bottom edge '''  
    cmds.select(Cylinder[0]+'.f[42:49]')
    cmds.move (0,-2,0,r=True,os=True,wd=True)
    cmds.scale (randomFloat3,1,randomFloat3)
    
    #Extra Branch 1   
    ''' Makes a branch '''   
    cmds.select(Cylinder[0]+'.f[21]')
    cmds.polyExtrudeFacet(s=(1,1,1), t=(0, 0, 0))
    cmds.scale (0.3,0.1,0.3, r=True, ls=True)
    cmds.polyCircularize(divisions=1) 
    cmds.select(Cylinder[0]+'.f[21]') 
    cmds.move(0.2,2,0.4,r=True,os=True,wd=True)
    cmds.rotate(0, -35, 0, r=True, cs=True)
    
    for i in range (2):
        cmds.polyExtrudeFacet (s = (1,1,1), t=(0, 0, 0))
        cmds.rotate(0, -15, 0, r=True, cs=True)
        cmds.move (random.uniform(0.4,1.2), random.uniform(0.8,1.8), random.uniform(0.4,1.2), r=True, os=True, wd=True)
        cmds.scale (random.uniform(0.8,1.5),random.uniform(0.8,1.5),random.uniform(0.8,1.5), r=True, cs=True)
    
    #Extra Branch 2 
    ''' Makes a branch '''     
    cmds.select(Cylinder[0]+'.f[11]')
    cmds.polyExtrudeFacet(s=(1,1,1), t=(0, 0, 0))   
    cmds.scale (0.3,0.1,0.3, r=True, ls=True)
    cmds.polyCircularize(divisions=1)
    cmds.select(Cylinder[0]+'.f[11]')
    cmds.move(-0.5, 0, 0.2, r=True, os=True, wd=True)
    cmds.rotate(0, -35, 0, relative=True, componentSpace=True)  
    
    for i in range (2):
        cmds.polyExtrudeFacet (s = (1,1,1), t=(0, 0, 0))
        cmds.rotate(0, -15, 0, r=True, cs=True)
        cmds.move (-random.uniform(0.4,1.2), random.uniform(0.8,1.1), random.uniform(0.4,1.2), r=True, os=True, wd=True)
        cmds.scale (random.uniform(0.8,1.1),random.uniform(0.8,1.1),random.uniform(0.8,1.1), r=True, cs=True)
        
    #Extra Branch 3  
    ''' Makes a branch '''     
    cmds.select(Cylinder[0]+'.f[15]')
    cmds.polyExtrudeFacet(s=(1,1,1), t=(0, 0, 0))   
    cmds.scale (0.3,0.1,0.3, r=True, ls=True)
    cmds.polyCircularize(divisions=1)
    cmds.select(Cylinder[0]+'.f[15]')
    cmds.move(0.5, 0, -0.2, r=True, os=True, wd=True)
    cmds.rotate(0, -35, 0, relative=True, componentSpace=True)  
    
    for i in range (1):
        cmds.polyExtrudeFacet (s = (1,1,1), t=(0, 0, 0))
        cmds.rotate(0, -15, 0, r=True, cs=True)
        cmds.move (random.uniform(0.5,0.6), random.uniform(0.8,1.2), random.uniform(-0.2,-0.5), r=True, os=True, wd=True)
        cmds.scale (random.uniform(0.8,1.5),random.uniform(0.8,1.5),random.uniform(0.8,1.5), r=True, cs=True)
        
    #Extra Branch 4   
    ''' Makes a branch '''     
    cmds.select(Cylinder[0]+'.f[17]')
    cmds.polyExtrudeFacet(s=(1,1,1), t=(0, 0, 0))   
    cmds.scale (0.3,0.1,0.3, r=True, ls=True)
    cmds.polyCircularize(divisions=1)
    cmds.select(Cylinder[0]+'.f[17]')
    cmds.move(-0.2, 3, -0.5, r=True, os=True, wd=True)
    cmds.rotate(0, -35, 0, relative=True, componentSpace=True)  
    
    for i in range (3):
        cmds.polyExtrudeFacet (s = (1,1,1), t=(0, 0, 0))
        cmds.rotate(0, -15, 0, r=True, cs=True)
        cmds.move (-random.uniform(0.5,0.6), random.uniform(0.8,1.2), random.uniform(-0.6,-0.9), r=True, os=True, wd=True)
        cmds.scale (random.uniform(0.8,1),random.uniform(0.8,1),random.uniform(0.8,1), r=True, cs=True)
    
    #Make Ridges
    ''' Makes Ridges '''     
    cmds.polySelect(el = 94)
    cmds.polyExtrudeEdge()    
    cmds.scale (1.1,1.1,1.1, r=True, ls=True)
    cmds.move (0, -2, 0, r=True, os=True, wd=True)
    cmds.polyNormal()
    
    cmds.polySelect(el = 119)
    cmds.polyExtrudeEdge()        
    cmds.move (0, -2, 0, r=True, os=True, wd=True)
    cmds.scale (1.2,1,1.2, r=True, ls=True)
    cmds.polyNormal()
    
    cmds.polySelect(el = 122)
    cmds.polyExtrudeEdge()    
    cmds.scale (1.2,1,1.2, r=True, ls=True)
    cmds.move (0, -1, 0, r=True, os=True, wd=True)
    cmds.polyNormal()
    
    cmds.polySelect(el = 144)
    cmds.polyExtrudeEdge()    
    cmds.scale (1.4,1,1.4, r=True, ls=True)
    cmds.move (0, -1, 0, r=True, os=True, wd=True)
    cmds.polyNormal()
    
    cmds.polySelect(el = 166)
    cmds.polyExtrudeEdge()    
    cmds.scale (1.4,1,1.4, r=True, ls=True)
    cmds.move (0, -4.5, 0, r=True, os=True, wd=True)
    cmds.polyNormal()
    
    #Move Edges and Verts
    ''' Moves Edges and Verts '''   
    cmds.select(Cylinder[0]+'.vtx[40]')
    cmds.move(0,-random.uniform(0.2,0.6),0,r=True,os=True,wd=True)
    cmds.select(Cylinder[0]+'.vtx[42]')
    cmds.move(0,-random.uniform(0.2,0.6),0,r=True,os=True,wd=True)
    cmds.select(Cylinder[0]+'.vtx[44]')
    cmds.move(0,-random.uniform(0.2,0.6),0,r=True,os=True,wd=True)
    cmds.select(Cylinder[0]+'.vtx[46]')
    cmds.move(0,-random.uniform(0.2,0.6),0,r=True,os=True,wd=True)
    
    cmds.select(Cylinder[0]+'.vtx[193]')
    cmds.move(random.random()/4,-random.uniform(0.2,0.6),random.random()/4,r=True,os=True,wd=True)
    cmds.select(Cylinder[0]+'.vtx[199]')
    cmds.move(random.random()/4,-random.uniform(0.2,0.6),random.random()/4,r=True,os=True,wd=True)
    cmds.select(Cylinder[0]+'.vtx[197]')
    cmds.move(random.random()/4,-random.uniform(0.2,0.6),random.random()/4,r=True,os=True,wd=True)
    cmds.select(Cylinder[0]+'.vtx[195]')
    cmds.move(random.random()/4,-random.uniform(0.2,0.6),random.random()/4,r=True,os=True,wd=True)
    
    cmds.select(Cylinder[0]+'.vtx[200]')
    cmds.move(0,-random.uniform(0.2,0.6),0,r=True,os=True,wd=True)
    cmds.select(Cylinder[0]+'.vtx[202]')
    cmds.move(0,-random.uniform(0.2,0.6),0,r=True,os=True,wd=True)
    cmds.select(Cylinder[0]+'.vtx[204]')
    cmds.move(0,-random.uniform(0.2,0.6),0,r=True,os=True,wd=True)
    cmds.select(Cylinder[0]+'.vtx[206]')
    cmds.move(0,-random.uniform(0.2,0.6),0,r=True,os=True,wd=True)
    
    cmds.select(Cylinder[0]+'.vtx[210]')
    cmds.move(0,-random.uniform(0.2,0.6),0,r=True,os=True,wd=True)
    cmds.select(Cylinder[0]+'.vtx[212]')
    cmds.move(0,-random.uniform(0.2,0.6),0,r=True,os=True,wd=True)
    cmds.select(Cylinder[0]+'.vtx[214]')
    cmds.move(0,-random.uniform(0.2,0.6),0,r=True,os=True,wd=True)
    cmds.select(Cylinder[0]+'.vtx[208]')
    cmds.move(0,-random.uniform(0.2,0.6),0,r=True,os=True,wd=True)
    
    cmds.select(Cylinder[0]+'.vtx[220]')
    cmds.move(0,-random.uniform(0.2,0.4),0,r=True,os=True,wd=True)
    cmds.select(Cylinder[0]+'.vtx[222]')
    cmds.move(0,-random.uniform(0.2,0.4),0,r=True,os=True,wd=True)
    cmds.select(Cylinder[0]+'.vtx[216]')
    cmds.move(0,-random.uniform(0.2,0.4),0,r=True,os=True,wd=True)
    cmds.select(Cylinder[0]+'.vtx[218]')
    cmds.move(0,-random.uniform(0.2,0.4),0,r=True,os=True,wd=True)
    
    cmds.select(Cylinder[0]+'.vtx[228]')
    cmds.move(0,-random.uniform(0.2,0.4),0,r=True,os=True,wd=True)
    cmds.select(Cylinder[0]+'.vtx[230]')
    cmds.move(0,-random.uniform(0.2,0.4),0,r=True,os=True,wd=True)
    cmds.select(Cylinder[0]+'.vtx[224]')
    cmds.move(0,-random.uniform(0.2,0.4),0,r=True,os=True,wd=True)
    cmds.select(Cylinder[0]+'.vtx[226]')
    cmds.move(0,-random.uniform(0.2,0.4),0,r=True,os=True,wd=True)    
    
    cmds.select(Cylinder)    
    cmds.hyperShade(assign = barkShader) 
    
    cmds.select(Cylinder[0]+'.f[42:89]')
    cmds.hyperShade(assign = leafShader)
    cmds.select(Cylinder[0]+'.f[170:209]')
    cmds.hyperShade(assign = leafShader)
    cmds.select(Cylinder[0]+'.f[25]')
    cmds.hyperShade(assign = leafShader)
    
    cmds.select(Cylinder)
    
    #Distributes Objects on terrain    
def rockSpawn(winID, rock1amountControl, rock2amountControl, rockscaleControl, mushroomControl, *pArgs):

    RockOrg1=smallRock()
    cmds.rename('RockOrg1')
    RockOrg2=smallRock()
    cmds.rename('RockOrg2')
    RockOrg3=Rock()
    cmds.rename('RockOrg3')
    RockOrg4=Rock()
    cmds.rename('RockOrg4')
    
    MushroomOrg1=mushroom()
    cmds.rename('MushroomOrg1')
    MushroomOrg2=mushroom()
    cmds.rename('MushroomOrg2')
    MushroomOrg3=mushroom()
    cmds.rename('MushroomOrg3')
    MushroomOrg4=mushroom()
    cmds.rename('MushroomOrg4')
    
    terrainShape ="Landscape01"
    #rockNames = ["RockOrg1", "RockOrg2"]
    rockData = {"RockOrg1": rock1amountControl//2, "RockOrg2": rock1amountControl//2, "RockOrg3": rock2amountControl//2, "RockOrg4": rock2amountControl//2,"MushroomOrg1": mushroomControl//4, "MushroomOrg2": mushroomControl//4, "MushroomOrg3": mushroomControl//4, "MushroomOrg4": mushroomControl//4} 
    
    numVertex = cmds.polyEvaluate(terrainShape, vertex=True)
    selectedVertices = random.sample(range(numVertex), numVertex)
      
    currentIndex = 0
    for pair in rockData.items():
        for i in range(pair[1]):
            if currentIndex>numVertex-1:
                break
            pos = cmds.pointPosition (terrainShape+".vtx["+str(selectedVertices[currentIndex])+"]", world=True)
            
            newobj = cmds.instance(pair[0])
            
            cmds.move(pos[0],pos[1],pos[2],newobj)
            #cmds.scale (rockscaleControl/random.uniform(0.5,2.0), rockscaleControl/random.uniform(0.5,2), rockscaleControl/random.uniform(0.5,2),newobj)
            cmds.scale (rockscaleControl/random.uniform(0.8,1.2), rockscaleControl/random.uniform(0.5,2.0), rockscaleControl/random.uniform(0.8,1.2),newobj)
            cmds.rotate(0, random.randint(0,360),0,newobj)
            if pos[1] > 200:
                cmds.delete(newobj) 
                    
            currentIndex+=1
    
    cmds.delete("RockOrg1", "RockOrg2", "RockOrg3", "RockOrg4", "MushroomOrg1", "MushroomOrg2", "MushroomOrg3", "MushroomOrg4")
    
    if cmds.objExists('Rock*'):
        cmds.select("Rock*")
        cmds.group(name="Rocks")
    if cmds.objExists('MushroomOrg*'):
        cmds.select("MushroomOrg*")
        cmds.group(name="Mushrooms")

def mushroom():
   
    StemShader = cmds.shadingNode( 'lambert', asShader = True)    
    cmds.setAttr( StemShader + '.color', 0.497, 0.426, 0.312, type = 'double3' )

    CapShader = cmds.shadingNode( 'lambert', asShader = True)    
    cmds.setAttr( CapShader + '.color', 0.358, 0.092, 0.049, type = 'double3' )
    
    #Random Numbers
    randomFloatScaleZXY = random.uniform(-0.1,0.1)
    randomTrunk = random.randint(6,10)
    
    #Make Stalk primitive
    Cylinder=cmds.polyCylinder (h=0.5,r=1,sx=42,sy=1,name='MushroomOriginal')
    cmds.hyperShade(assign = StemShader)
    
    #Adjust Stalk
    for i in range (randomTrunk):
        randomFloatScale = random.uniform(0.95,1.1)
        randomFloatZX = random.uniform(-0.3,0.3)
        randomFloatY = random.uniform(0.8,1.2)
        randomFloatTopY = random.uniform(0.8,3.2)
        randomFloatTopYsmall = random.uniform(0.1,0.3)
        
        cmds.select(Cylinder[0]+'.f[43]')
        cmds.polyExtrudeFacet(s=(randomFloatScale,randomFloatScale,randomFloatScale), t=(randomFloatZX, randomFloatY, randomFloatZX), d=1)   
    
    #Scale the top stalk extrusion    
    cmds.scale(1.2,1.0,1.2, r=True)
    
    #Create Volva    
    cmds.select(Cylinder[0]+'.f[254:295]')
    cmds.polyExtrudeFacet( d=1)
    cmds.scale (1.3,0.95,1.3, r=True, ws=True) 

       
    #Create Gills
    morphUnder = random.uniform(0.01, 0.05)
    cmds.select(Cylinder[0]+'.f[43]')
    cmds.polyExtrudeFacet(s=(1.4+randomFloatScaleZXY,1.4+randomFloatScaleZXY,1.4+randomFloatScaleZXY+morphUnder), t=(0, randomFloatTopYsmall, 0), d=1)   
    cmds.polyExtrudeFacet(s=(1.5+randomFloatScaleZXY,1.5+randomFloatScaleZXY,1.5+randomFloatScaleZXY+morphUnder), t=(0, randomFloatTopYsmall, 0), d=1)    
    cmds.polyExtrudeFacet(s=(1.6+randomFloatScaleZXY,1.6+randomFloatScaleZXY,1.6+randomFloatScaleZXY+morphUnder), t=(0, randomFloatTopYsmall, 0), d=1)      
    cmds.polyExtrudeFacet(s=(1.3+randomFloatScaleZXY,1.3+randomFloatScaleZXY,1.3+randomFloatScaleZXY+morphUnder), t=(0, randomFloatTopYsmall-0.4, 0), d=1)
    cmds.polyExtrudeFacet(s=(1.2+randomFloatScaleZXY,1.2+randomFloatScaleZXY,1.2+randomFloatScaleZXY+morphUnder), t=(0, randomFloatTopYsmall-0.5, 0), d=1)  
    cmds.hyperShade(assign = CapShader) 
      
    #Create Cap  
    step = 0.9
    topStep=0.05
    
    for i in range (5):
       morph = random.uniform(-0.15,-0.05)
       cmds.polyExtrudeFacet(s=(step+morph,step,step), t=(0, randomFloatTopY-topStep, 0), d=3)   
       step-=0.1
       topStep+=0.2
       cmds.hyperShade(assign = CapShader)
       
    #Scale top of Cap    
    cmds.scale(0.5,1.0,0.5, r=True)
    cmds.select(Cylinder)
    
    #Create Base
    cmds.select(Cylinder[0]+'.f[42]')
    cmds.scale(4.5,6.0,4.5, r=True)
    cmds.polySubdivideFacet (dv=1)  
    cmds.select(clear=True)
    cmds.select('MushroomOriginal')
  
    #Add Noise 
    vtxCount = list(range(cmds.polyEvaluate(v=True)))
    random.shuffle(vtxCount)
    values = [random.triangular(0,0.3,0) for i in range(10)]
    values_count = len(values)
    optimize_setter = []
    
    for x in vtxCount:
        mod = x % values_count
        optimize_setter += [values[mod-1]*1,values[mod-1]*1,values[mod-1]*1]
    cmds.setAttr('MushroomOriginal.vtx[:]', *optimize_setter)
    cmds.polySmooth(c=1,dv=2,kb=True,ro=1) 
     
    #Smooth   
    #cmds.polySmooth(divisions=1)
    
    #Creates Grass
def grass():
    
    #Shader    
    myShader = cmds.shadingNode( 'lambert', asShader = True)    
    cmds.setAttr( myShader + '.color', 0.25, 0.65, 0.06, type = 'double3' )
    
    #Create Main Shape
    polycone=cmds.polyCone (h=0.5,r=0.5,sx=4,sy=4,name='grassBlade')
    cmds.select(polycone[0]+'.f[12]')
    cmds.scale (0.05,1,0.05)
    cmds.select(polycone[0]+'.f[4:7]')
    cmds.scale (0.05,1,0.05)
    cmds.select(polycone[0]+'.f[13:16]')
    cmds.scale (0.1,1,0.1)
    
    #Move Edges and Verts
    ''' Moves Edges and Verts ''' 
    cmds.select(polycone[0]+'.e[4:7]')
    cmds.move(random.random()/20,0,random.random()/20,r=True,os=True,wd=True)
    
    cmds.select(polycone[0]+'.e[8:11]')
    cmds.move(random.random()/20,0,random.random()/20,r=True,os=True,wd=True)
    
    cmds.select(polycone[0]+'.e[12:15]')
    cmds.move(random.random()/20,0,random.random()/20,r=True,os=True,wd=True)
    
    cmds.select(polycone[0]+'.vtx[16]')
    cmds.move(random.random()/20,random.random()/5,random.random()/20,r=True,os=True,wd=True)
    
    cmds.select(polycone)
    
    cmds.ls('grassBlade*')
    cmds.hyperShade(assign = myShader) 
    
    cmds.select(polycone)
    cmds.polySmooth(c=1,dv=1,kb=True,ro=1)
    
    #Creates a Hill
def createHill(winID, hillHeight, *pArgs):

    Landscape01="Landscape01"
    percent = 0.02 
    faces = []
    cmds.select(Landscape01)
    for obj in cmds.ls(sl=1, long=1):
        indexes = list(range(cmds.polyEvaluate(obj, face=1)))
        random.shuffle(indexes)
        indexes = indexes[:int(percent*len(indexes))]	
        for i in range(len(indexes)):
            indexes[i] = obj+'.f['+str(indexes[i])+']'
        faces.extend(indexes)
    cmds.select(faces, r=1)
    cmds.polySelectConstraint( pp=5 ) 
    rn = random.random()
    tmpValueY = hillHeight*(rn)
    
    if(tmpValueY < 0):
        tmpValueY = 0.0
    
    cmds.move(0.0, tmpValueY, 0.0, r=True)
    
    #Creates elevation detail   
def createDetail(winID, detailHeight, *pArgs):

    Landscape01="Landscape01"
    percent = 0.02 
    faces = []
    cmds.select(Landscape01)
    for obj in cmds.ls(sl=1, long=1):
        indexes = list(range(cmds.polyEvaluate(obj, face=1)))
        random.shuffle(indexes)
        indexes = indexes[:int(percent*len(indexes))]	
        for i in range(len(indexes)):
            indexes[i] = obj+'.f['+str(indexes[i])+']'
        faces.extend(indexes)
    cmds.select(faces, r=1)
    cmds.polySelectConstraint( pp=5 ) 
    rn = random.random()
    tmpValueY = detailHeight*(rn)
    
    if(tmpValueY < 0):
        tmpValueY = 0.0
    
    cmds.move(0.0, tmpValueY, 0.0, r=True)
    cmds.polySubdivideFacet()
    
    #Creates a ditch    
def createDitch(winID, ditchDepth, *pArgs):

    Landscape01="Landscape01"
    percent = 0.02
    faces = []
    cmds.select(Landscape01)
    for obj in cmds.ls(sl=1, long=1):
        indexes = list(range(cmds.polyEvaluate(obj, face=1)))
        random.shuffle(indexes)
        indexes = indexes[:int(percent*len(indexes))]	
        for i in range(len(indexes)):
            indexes[i] = obj+'.f['+str(indexes[i])+']'
        faces.extend(indexes)
    cmds.select(faces, r=1)
    cmds.polySelectConstraint( pp=5 ) 
    rn = random.random()
    tmpValueY = ditchDepth*(rn)
    
    if(tmpValueY < 0):
        tmpValueY = 0.0
    
    cmds.move(0.0, -tmpValueY, 0.0, r=True)
    
    #Creates Mountains
def createMountins(winID, mountainHeight, *pArgs):

    Landscape01="Landscape01"
    percent = 0.008
    faces = []
    cmds.select(Landscape01)
    for obj in cmds.ls(sl=1, long=1):
        indexes = list(range(cmds.polyEvaluate(obj, face=1)))
        random.shuffle(indexes)
        indexes = indexes[:int(percent*len(indexes))]
        for i in range(len(indexes)):
            indexes[i] = obj+'.f['+str(indexes[i])+']'
        faces.extend(indexes)
    cmds.select(faces, r=1)
    cmds.polySelectConstraint( pp=1 ) 
    rn = random.randint(mountainHeight,mountainHeight)
    tmpValueY = rn  
    
    if(tmpValueY < 0):
        tmpValueY = 10
    
    cmds.move(0.0, tmpValueY, 0.0, r=True)
    cmds.polyExtrudeFacet(s=(1,1,1), t=(1, 1, 1))
    cmds.scale(0.62,0.64,0.66,cs=True,r=True)
    cmds.move(0.0, tmpValueY/1.5, 0.0, r=True)
    cmds.polyExtrudeFacet(s=(1,1,1), t=(1, 1, 1))
    cmds.scale(0.66,0.62,0.68,cs=True,r=True)
    cmds.move(0.0, tmpValueY/2, 0.0, r=True)
    cmds.polySelectConstraint( pp=2 )
    cmds.move(0.0, tmpValueY/10, 0.0, r=True)
    cmds.select(Landscape01)
    cmds.polySoftEdge(a=180, ch=1)

def smallRockStack(noiseControl):
    
    randomFloat = random.uniform(0.1,0.2)
    #Make rock
    Cube=cmds.polyCube(h=8,w=8,d=8,sx=3,sy=3,sz=3,name='RockOriginal')
    cubeFaces = (Cube[0]+'.f[25]',Cube[0]+'.f[37]',Cube[0]+'.f[1]',Cube[0]+'.f[46]')
    #Make adjust
    for i in range (1):
        cmds.select(cubeFaces)   
        cmds.scale (random.uniform(1.5,2.5),random.uniform(1,1.2),random.uniform(1.5,2.5),r=True)
    
    cubeFaces2 = (Cube[0]+'.f[45]',Cube[0]+'.f[0]',Cube[0]+'.f[38]',Cube[0]+'.f[36]')
    #Make adjust
    for i in range (1):
        cmds.select(cubeFaces2)   
        cmds.scale (random.uniform(0.5,1.5),random.uniform(1,1.2),random.uniform(0.5,1.5),r=True)
        
    cubeFaces3 = (Cube[0]+'.f[43]',Cube[0]+'.f[19]',Cube[0]+'.f[7]',Cube[0]+'.f[52]')
    #Make adjust
    for i in range (1):
        cmds.select(cubeFaces3)   
        cmds.scale (random.uniform(1.5,2),random.uniform(0.5,2.2),random.uniform(1.5,2),r=True)
    
    cmds.select(Cube[0]+'.f[13]') 
    cmds.move (1,random.uniform(2.5,5.2),1,r=True)
    cmds.select(Cube[0]+'.f[31]') 
    cmds.move (1,random.uniform(-2.5,-5.2),1,r=True)
    
    cmds.select(cl=True) 
    cmds.polySelect('RockOriginal',el=22)
    cmds.move (0,random.uniform(1.1,1.8),0,r=True)
    
    cmds.select(Cube[0]+'.vtx[36]',Cube[0]+'.vtx[32]',Cube[0]+'.vtx[39]',Cube[0]+'.vtx[35]',Cube[0]+'.vtx[3]',Cube[0]+'.vtx[7]',Cube[0]+'.vtx[0]',Cube[0]+'.vtx[4]') 
    cmds.scale (random.uniform(1.4,1.6),random.uniform(1,2),random.uniform(1.4,1.6),r=True) 
     
    cmds.select(Cube)  
    cmds.scale (random.uniform(0.8,1.0),random.uniform(0.8,1.0),random.uniform(0.8,1.0),a=True)    
    cmds.scale (randomFloat,randomFloat,randomFloat,r=True)
    
    cmds.polySmooth(c=1,dv=2,kb=True,ro=1) 
    addNoise(noiseControl)
    cmds.select('RockOriginal', r=True ) 
    #cmds.rotate(random.uniform(10,120),random.uniform(10,120),random.uniform(10,1200),a=True)
    cmds.rename('Rock_Small_01')
    
def rockFlatStack(winID, noiseControl, sizeControl, stackSizeControl):
    
    randomStackSize = random.uniform(stackSizeControl+1,stackSizeControl+2.5)
    randomFloatStack = random.uniform(0.5,1.0)
    randomFloatX = random.uniform(-sizeControl/2,sizeControl/2)
    randomFloatY = random.uniform(-sizeControl/2,sizeControl/2)
    
    moveY=11
    scaleUni=1.5
    scaleUniY=1.1
    step=1
    
    for i in range (10):
        RockOrg=smallRockStack(noiseControl)
        cmds.select()
        cmds.move(randomFloatX,moveY,randomFloatY)
        cmds.rotate(random.uniform(1,15),random.uniform(10,360),random.uniform(1,15),a=True)
        cmds.scale(scaleUni,scaleUniY,scaleUni)
        
        scaleUni-=0.1
        scaleUniY-=0.1
        moveY+=11-step
        step+=1
               
    cmds.select('Rock_Small*')
    cmds.group(name="Rock_Flat_Stack_01",r=True)  
    cmds.select(clear=True)
    
    cmds.select('Rock_Flat_Stack_*')
    cmds.move(0, 100, 0, absolute=True)
    cmds.move(0, 0, 0, "Rock_Flat_Stack_*.scalePivot","Rock_Flat_Stack_*.rotatePivot", absolute=True)
    cmds.scale(randomFloatStack,randomFloatStack,randomFloatStack)  
    
    cmds.select(clear=True)
         
    cmds.select('Rock_Flat_Stack_*')
    cmds.rename('New_Rock_Flat_Stack_01')
    cmds.xform(r=True, centerPivots = True)
    cmds.scale(randomStackSize,randomStackSize,randomStackSize) 
    
    for i in range(10):       
        cmds.select('Rock_Small*')
        cmds.rename('New_Stack_Memeber_01')
        
    cmds.select(clear=True)
        
def rockStackLarge(winID, noiseControl, sizeControl, stackSizeControl):
    
    randomStackSize = random.uniform(stackSizeControl-0.5,stackSizeControl+1.5)
    randomFloatStack = random.uniform(0.3,0.5)
    randomFloatX = random.uniform(-sizeControl,sizeControl)
    randomFloatY = random.uniform(-sizeControl,sizeControl)
    
    moveY=20
    scaleUni=2
    step=1
    
    for i in range (20):
        RockOrg=smallRockStack(noiseControl)

        cmds.select()
        cmds.move(randomFloatX,moveY,randomFloatY)
        cmds.rotate(random.uniform(10,360),random.uniform(10,360),random.uniform(10,360),a=True)
        cmds.scale(scaleUni,scaleUni,scaleUni)
        scaleUni-=0.1
        moveY+=20-step
        step+=1
        
    cmds.select('Rock_Small*')
    cmds.group(name="Rock_Large_Stack_01",r=True)  
    cmds.select(clear=True)
    
    cmds.select('Rock_Large_Stack_*')
    cmds.move(0, 100, 0, absolute=True)
    cmds.move(0, 0, 0, "Rock_Large_Stack_*.scalePivot","Rock_Large_Stack_*.rotatePivot", absolute=True)
    cmds.scale(randomFloatStack,randomFloatStack,randomFloatStack)  
    
    cmds.select(clear=True)
         
    cmds.select('Rock_Large_Stack_*')
    cmds.rename('New_Large_Rock_Stack_01')
    cmds.xform(r=True, centerPivots = True)
    cmds.scale(randomStackSize,randomStackSize,randomStackSize) 
    
    for i in range(20):       
        cmds.select('Rock_Small*')
        cmds.rename('New_Large_Stack_Memeber_01')
        
    cmds.select(clear=True) 
    
def addNoise(noiseControl):
    
    cmds.select('RockOriginal')

    vtxCount = list(range(cmds.polyEvaluate(v=True)))
    random.shuffle(vtxCount)
    values = [random.triangular(0,noiseControl,0) for i in range(10)]
    values_count = len(values)
    optimize_setter = []
    
    for x in vtxCount:
        mod = x % values_count
        optimize_setter += [values[mod-1]*1,values[mod-1]*1,values[mod-1]*1]
    cmds.setAttr('RockOriginal.vtx[:]', *optimize_setter)
    cmds.polySmooth(c=1,dv=2,kb=True,ro=1)   
    
def moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax):
    
    #cmds.polyExtrudeFacet(s=(1,1,1), t=(0, 1, 0))  
    cmds.move (random.uniform(-minZ,maxZ),random.uniform(minY,maxY),random.uniform(-minZ,maxZ),r=True,os=True,wd=True)     
    cmds.scale (random.uniform(scaleMin,scaleMax),random.uniform(scaleMin,scaleMax),random.uniform(scaleMin,scaleMax),r=True)
    
def Mountain(WinID, sizeControl):
    
    minY = 10
    maxY = 40
    minZ = 0.1
    maxZ = 1.9
    scaleMin = 0.6
    scaleMax = 1.0
    randomFloat = random.uniform(2,2.5)
    
    #Make rock
    Cube=cmds.polyCube(h=12,w=64,d=64,sx=6,sy=1,sz=6,name='RockOriginal')
    #Make adjust
    for i in range (1):
        #cmds.select(Cube[0]+'.f[3'+str(next)+']')
        cmds.select(Cube[0]+'.f[31]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[32]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[33]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[34]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[19]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[20]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[21]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[22]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[13]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[14]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[15]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[16]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[25]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[26]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[27]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[28]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)

        
    cmds.select(Cube)
    cmds.polySubdivideFacet (dv=3,m=0,ch=1)
    addNoise(1)
    cmds.select('RockOriginal', r=True )
    cmds.scale (random.uniform(0.5,1.0),random.uniform(0.2,0.8),random.uniform(0.5,1.0)) 
    cmds.move(random.uniform(-sizeControl/2,sizeControl/2),-5,random.uniform(-sizeControl/2,sizeControl/2))
    cmds.scale (randomFloat,randomFloat,randomFloat,r=True)
    cmds.rename('Mountain_01')

def megaMountain(winID, sizeControl):
    
    randomFloat = random.uniform(0.8,1.6)
    minY = 20
    maxY = 80
    minZ = 0.0
    maxZ = 2.0
    scaleMin = 0.8
    scaleMax = 1.0
    
    Cube=cmds.polyCube(h=12,w=64,d=64,sx=6,sy=1,sz=6,name='RockOriginal')
    for i in range (1):

        cmds.select(Cube[0]+'.f[31]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[32]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[33]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[34]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[19]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[20]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[21]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[22]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[13]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[14]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[15]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[16]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[25]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[26]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[27]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        cmds.select(Cube[0]+'.f[28]')
        moveUp(minY,maxY,minZ,maxZ,scaleMin,scaleMax)
        
    cmds.select(Cube)
    cmds.polySubdivideFacet (dv=2,m=0,ch=1)
    addNoise(1)
    addNoise(1)
    cmds.scale(2,1,2)
    cmds.select('RockOriginal', r=True ) 
    cmds.move(random.uniform(-sizeControl/2,sizeControl/2),-5,random.uniform(-sizeControl/2,sizeControl/2))
    cmds.scale (randomFloat,randomFloat,randomFloat,r=True)
    cmds.rotate(random.uniform(1,3),random.uniform(10,360),random.uniform(1,3),a=True)
    cmds.rename('Large_Mountain_01') 
    
def basicLighting(winID):
    
    # Create a directional light
    directLight = cmds.directionalLight(rotation=(-33, 0, -52), intensity=10.0, n='Light1')
    cmds.setAttr('Light1.color', 1.0, 0.813, 0.391, type = 'double3')
    directLight2 = cmds.directionalLight(rotation=(-145.041, 12.882, 0.980), intensity=2.0, n='Light2')
    cmds.setAttr('Light2.color', 0.731, 0.979, 1.0, type = 'double3')
    
def moveCentre(winID):
    selectionList = cmds.ls(selection=True)
    
    if len (selectionList ) >= 1:    
        for objectName in selectionList:    
            cmds.move(0,0,0, a=True,ws=True)
    		            
def removeAll(winID):   
    cmds.select(all=True)
    cmds.delete()
    
    #Create UI            
def createUI():

    winID = cmds.window( title = 'Terrain Generator', w = 120)
    if cmds.window(winID, exists = True):
        cmds.deleteUI(winID)
    winID = cmds.window( title = 'Terrain Generator', w = 120)
    cmds.rowColumnLayout( numberOfRows=20, cs=[10,10], rs=[10,10], rh=[40,40], adjustableColumn=True)
    cmds.image( image='C:\\Users\\Rory\\OneDrive\\Pictures\\logo.jpg', h=120 ,w=400)

    ######Terrain Presets######	
    ''' Terrain Presets ''' 
    cmds.image( image='C:\\Users\\Rory\\OneDrive\\Pictures\\presets.jpg', h=60 ,w=400)
    sizeControl2 = cmds.intSliderGrp(label='Preset Terrain Size', minValue=500, maxValue=4000, value=2000, field=True)
    
    cmds.button(label = "Hills", h=30, command = lambda *args: hillPreset(winID, cmds.intSliderGrp(subControl, query=True, value=True), cmds.intSliderGrp(sizeControl2, query=True, value=True), cmds.intSliderGrp(heightControl, query=True, value=True), cmds.intSliderGrp(ditchDepth, query=True, value=True), cmds.intSliderGrp(hillHeight, query=True, value=True), cmds.intSliderGrp(rock1amountControl, query=True, value=True), cmds.intSliderGrp(rock2amountControl, query=True, value=True),cmds.floatSliderGrp(rockscaleControl, query=True, value=True)))
    cmds.button(label = "Mountains", h=30, command = lambda *args: mountainPreset(winID, cmds.intSliderGrp(subControl, query=True, value=True), cmds.intSliderGrp(sizeControl2, query=True, value=True), cmds.intSliderGrp(mountainHeight, query=True, value=True), cmds.intSliderGrp(heightControl, query=True, value=True), cmds.intSliderGrp(ditchDepth, query=True, value=True), cmds.intSliderGrp(hillHeight, query=True, value=True), cmds.intSliderGrp(rock1amountControl, query=True, value=True), cmds.intSliderGrp(rock2amountControl, query=True, value=True),cmds.floatSliderGrp(rockscaleControl, query=True, value=True)))
    cmds.button(label = "Plains", h=30, command = lambda *args: plainPreset(winID, cmds.intSliderGrp(subControl, query=True, value=True), cmds.intSliderGrp(sizeControl2, query=True, value=True), cmds.intSliderGrp(heightControl, query=True, value=True), cmds.intSliderGrp(ditchDepth, query=True, value=True), cmds.intSliderGrp(hillHeight, query=True, value=True), cmds.intSliderGrp(rock1amountControl, query=True, value=True), cmds.intSliderGrp(rock2amountControl, query=True, value=True),cmds.floatSliderGrp(rockscaleControl, query=True, value=True)))   
    cmds.button(label = "Forest", h=30, command = lambda *args: forestPreset(winID, cmds.intSliderGrp(subControl, query=True, value=True), cmds.intSliderGrp(sizeControl2, query=True, value=True), cmds.intSliderGrp(heightControl, query=True, value=True), cmds.intSliderGrp(ditchDepth, query=True, value=True), cmds.intSliderGrp(hillHeight, query=True, value=True), cmds.intSliderGrp(rock1amountControl, query=True, value=True), cmds.intSliderGrp(rock2amountControl, query=True, value=True),cmds.floatSliderGrp(rockscaleControl, query=True, value=True)))
    cmds.button(label = "Lakes", h=30, command = lambda *args: riverPreset(winID, cmds.floatSliderGrp(waterHeight, query=True, value=True), cmds.intSliderGrp(subControl, query=True, value=True), cmds.intSliderGrp(sizeControl2, query=True, value=True), cmds.intSliderGrp(heightControl, query=True, value=True), cmds.intSliderGrp(ditchDepth, query=True, value=True), cmds.intSliderGrp(hillHeight, query=True, value=True), cmds.intSliderGrp(rock1amountControl, query=True, value=True), cmds.intSliderGrp(rock2amountControl, query=True, value=True),cmds.floatSliderGrp(rockscaleControl, query=True, value=True)))
    cmds.button(label = "Desert", h=30, command = lambda *args: desertPreset(winID, cmds.intSliderGrp(subControl, query=True, value=True), cmds.intSliderGrp(sizeControl2, query=True, value=True), cmds.intSliderGrp(mountainHeight, query=True, value=True), cmds.intSliderGrp(heightControl, query=True, value=True), cmds.intSliderGrp(ditchDepth, query=True, value=True), cmds.intSliderGrp(hillHeight, query=True, value=True), cmds.intSliderGrp(rock1amountControl, query=True, value=True), cmds.intSliderGrp(rock2amountControl, query=True, value=True),cmds.floatSliderGrp(rockscaleControl, query=True, value=True)))
    cmds.button(label = "Canyons", h=30, command = lambda *args: canyonsPreset(winID, cmds.intSliderGrp(subControl, query=True, value=True), cmds.intSliderGrp(sizeControl2, query=True, value=True), cmds.intSliderGrp(heightControl, query=True, value=True), cmds.intSliderGrp(ditchDepth, query=True, value=True), cmds.intSliderGrp(hillHeight, query=True, value=True), cmds.intSliderGrp(rock1amountControl, query=True, value=True), cmds.intSliderGrp(rock2amountControl, query=True, value=True),cmds.floatSliderGrp(rockscaleControl, query=True, value=True)))   
    cmds.button(label = "Islands", h=30, command = lambda *args: islandsPreset(winID, cmds.floatSliderGrp(waterHeight, query=True, value=True), cmds.intSliderGrp(subControl, query=True, value=True), cmds.intSliderGrp(sizeControl2, query=True, value=True), cmds.intSliderGrp(heightControl, query=True, value=True), cmds.intSliderGrp(ditchDepth, query=True, value=True), cmds.intSliderGrp(hillHeight, query=True, value=True), cmds.intSliderGrp(rock1amountControl, query=True, value=True), cmds.intSliderGrp(rock2amountControl, query=True, value=True),cmds.floatSliderGrp(rockscaleControl, query=True, value=True)))
	
    ######Custom Terrain######
    ''' Custom Terrain ''' 
    cmds.image( image='C:\\Users\\Rory\\OneDrive\\Pictures\\custom.jpg', h=60 ,w=400)
	
    #Terrain Variables
    subControl = cmds.intSliderGrp(label='Terrain Sub Divisions', minValue=5, maxValue=100, value=25, field=True)
    sizeControl = cmds.intSliderGrp(label='Terrain Size', minValue=100, maxValue=4000, value=2000, field=True)
    heightControl = cmds.intSliderGrp(label='Terrain Noise Height', minValue=10, maxValue=100, value=40, field=True)
    
    #Create Terrain - Set Colour
    cmds.button(label = "Create Terrain", h=30,command = lambda *args: actionProc(winID, cmds.intSliderGrp(subControl, query=True, value=True), cmds.intSliderGrp(sizeControl, query=True, value=True),cmds.intSliderGrp(heightControl, query=True, value=True)))
    cmds.colorSliderGrp( 'polygonColour', h=30,label = "Colour", hsv = ( 103, 0.9, 0.6 ) )	
    cmds.button(label = "Set Colour", h=30, command = lambda *args: setColour(winID))
    
    #Smoothing
    cmds.button(label = "Smooth Terrain", h=30,command = lambda *args: smoothing(winID))
    
    #Mountains
    cmds.button(label = "Create Mountains", h=30,command = lambda *args: createMountins(winID, cmds.intSliderGrp(mountainHeight, query=True, value=True)))
    mountainHeight = cmds.intSliderGrp(label='Mountain Height', h=30,minValue=20, maxValue=200, value=40, field=True)
    
    #Hills
    cmds.button(label = "Create Hills", h=30,command = lambda *args: createHill(winID, cmds.intSliderGrp(hillHeight, query=True, value=True)))
    hillHeight = cmds.intSliderGrp(label='Hill Height', h=30,minValue=5, maxValue=100, value=30, field=True)
    
    #Ditches
    cmds.button(label = "Create Ditches", h=30,command = lambda *args: createDitch (winID, cmds.intSliderGrp(ditchDepth, query=True, value=True)))
    ditchDepth = cmds.intSliderGrp(label='Ditch Depth', minValue=5, maxValue=100, value=30, field=True)
    
    #Elevation Detail
    cmds.button(label = "Create Elevation Detail", h=30,command = lambda *args: createDetail(winID, cmds.intSliderGrp(detailHeight, query=True, value=True)))
    detailHeight = cmds.intSliderGrp(label='Detail Height', h=30,minValue=5, maxValue=100, value=30, field=True)
    
    #River
    cmds.button(label = "Create River", h=30, command = lambda *args: createRiver(winID))
    
    #Objects
    ''' Create Objects ''' 
    cmds.separator(io=True,style='none')
    cmds.image( image='C:\\Users\\Rory\\OneDrive\\Pictures\\objects.jpg', h=60 ,w=400)
    cmds.separator()
    
    #Mashtrees
    cmds.button(label = "Create Trees", h=30,command = lambda *args: mashTrees(winID, cmds.intSliderGrp(numberTrees, query=True, value=True), cmds.floatSliderGrp(scaleTrees, query=True, value=True)))
    numberTrees = cmds.intSliderGrp(label='Tree Amount', minValue=100, maxValue=8000, value=500, field=True)
    scaleTrees = cmds.floatSliderGrp(label='Tree Size', minValue=1, maxValue=25, value=2.5, step=1, field=True)
    
    #Rock Stacks
    cmds.button(label = "Spawn Rock Stack", h=40, command = lambda *args: rockStackLarge(winID, cmds.floatSliderGrp(noiseControl, query=True, value=True), cmds.intSliderGrp(sizeControl, query=True, value=True), cmds.floatSliderGrp(stackSizeControl, query=True, value=True)))
    cmds.button(label = "Spawn Flat Rock Stack", h=40, command = lambda *args: rockFlatStack(winID, cmds.floatSliderGrp(noiseControl, query=True, value=True), cmds.intSliderGrp(sizeControl, query=True, value=True), cmds.floatSliderGrp(stackSizeControl, query=True, value=True)))
    stackSizeControl = cmds.floatSliderGrp(label='Stack Size', minValue=1, maxValue=10, value=1.0, step=1.0, field=True)
    #Mountains
    cmds.button(label = "Spawn Mountain", h=40, command = lambda *args: Mountain(winID, cmds.intSliderGrp(sizeControl, query=True, value=True)))
    cmds.button(label = "Spawn Large Mountain", h=40, command = lambda *args: megaMountain(winID, cmds.intSliderGrp(sizeControl, query=True, value=True)))
    
    #MashGrass
    cmds.button(label = "Create Grass", h=30,command = lambda *args: mashGrass (winID, cmds.intSliderGrp(numberGrass, query=True, value=True), cmds.intSliderGrp(scaleGrass, query=True, value=True)))
    #cmds.button(label = "Create Grass", h=30,command = lambda *args: mashGrass (winID, cmds.intSliderGrp(numberGrass, query=True, value=True), cmds.intSliderGrp(scaleGrass, query=True, value=True), cmds.intSliderGrp(clusterPoints, query=True, value=True), cmds.floatSliderGrp(clusterSize, query=True, value=True), cmds.floatSliderGrp(clusterRadius, query=True, value=True)))
    numberGrass = cmds.intSliderGrp(label='Grass Amount', minValue=100, maxValue=2000, value=250, field=True)
    scaleGrass = cmds.intSliderGrp(label='Grass Scale', minValue=1, maxValue=25, value=3, field=True)
    #clusterPoints = cmds.intSliderGrp(label='Clump Points', minValue=1, maxValue=100, value=14, field=True)
    #clusterSize = cmds.floatSliderGrp(label='Clump Size', minValue=0, maxValue=10, value=4, field=True)
    #clusterRadius = cmds.floatSliderGrp(label='Clump Radius', minValue=0, maxValue=50, value=3, field=True)
    
    #Rocks
    cmds.button(label = "Create Objects", h=30,command = lambda *args: rockSpawn(winID, cmds.intSliderGrp(rock1amountControl, query=True, value=True), cmds.intSliderGrp(rock2amountControl, query=True, value=True),cmds.floatSliderGrp(rockscaleControl, query=True, value=True), cmds.intSliderGrp(mushroomControl, query=True, value=True)))
    rock1amountControl = cmds.intSliderGrp(label='Rock 1 Amount', minValue=0, maxValue=400, value=40, step=2.0, field=True) #bgc=(0.3,0.2,0.1))
    rock2amountControl = cmds.intSliderGrp(label='Rock 2 Amount', minValue=0, maxValue=400, value=40, step=2.0, field=True)
    mushroomControl = cmds.intSliderGrp(label='Mushroom Amount', minValue=0, maxValue=400, value=24, step=4.0, field=True)
    rockscaleControl = cmds.floatSliderGrp(label='Object Size', minValue=0.1, maxValue=20, value=1, step=1, field=True)
    
    cmds.button(label = "Create Basic Lighting Setup", h=30,command = lambda *args: basicLighting(winID)) 
    
    #Water
    cmds.button(label = "Create Water", h=30,command = lambda *args: Water(winID, cmds.floatSliderGrp(waterHeight, query=True, value=True)))    
    waterHeight = cmds.floatSliderGrp(label='Water Height', minValue=-50, maxValue=200, value=35, step=1, field=True)
    
    #Noise Control
    noiseControl = cmds.floatSliderGrp(label='Global Noise Amount',h=30, minValue=0, maxValue=5, value=1.0, field=True) 
    
    #Remove All
    cmds.button(label = "Remove All", h=30,command = lambda *args: removeAll(winID))  
    
    #Exit
    
    cmds.button(label = "Exit", command = lambda *args: cancelProc(winID))
    cmds.showWindow()
    
if __name__ == "__main__":
    createUI()
    #cmds.setAttr ("persp.translateX", 2639.818)
    #cmds.setAttr ("persp.translateY", 2083.655)
    #cmds.setAttr ("persp.translateZ", 2634.182)