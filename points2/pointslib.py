import FreeCAD
import FreeCADGui
Gui=FreeCADGui
App=FreeCAD

import Points, Part
import random
import numpy as np



import numpy as np
import scipy
import matplotlib.pyplot as plt
import scipy.interpolate
import Points


def run(twoFaces=False):
	sels=Gui.Selection.getSelection()
	if len(sels)<>2: print("Du musst zwei Draft Wire auswaehlen" )
	else: cutwire(sels,twoFaces)


def loadobj():

	fn='/home/thomas/Dokumente/freecad_buch/b231_kscan/body-v2-obj/body-v2.obj'
	fn='/home/thomas/Dokumente/freecad_buch/b231_kscan/model.obj'
	fn='/home/thomas/Dokumente/freecad_buch/b232_blender_banana/banana.obj'

	with open(fn) as f:
		content = f.readlines()

	pts=[]
	for i,l in enumerate(content):
		if l.startswith('v '):
			[a,x,y,z]=l.split(' ')
			
			p=FreeCAD.Vector(float(x),float(z),-float(y))

			p=FreeCAD.Vector(float(x)-float(y),-float(z),float(x)+float(y))

			pts.append(p)

	t=Points.Points(pts)
	Points.show(t)



#-----------------------

# import obj to pcl
def obj2pcl():
	loadobj()
	pass

# bound box to pcl
def boundbox(inside=True) :
	sels=Gui.Selection.getSelection()
	if len(sels)<>2: print("Du musst 1. Volumen und 2. Points auswaehlen" )
	print sels[0]
	print sels[1]
	print sels[1].Points.Points
	print sels[0].Shape.BoundBox
	bb=sels[0].Shape.BoundBox
	pts=sels[1].Points.Points

	if inside:
		pts=[p for p in pts if bb.XMin<= p.x and p.x <=bb.XMax and bb.YMin<= p.y and p.y <=bb.YMax and bb.ZMin<= p.z and p.z <=bb.ZMax]
		rel=" inside "
	else:
		pts=[p for p in pts if not(bb.XMin<= p.x and p.x <=bb.XMax and bb.YMin<= p.y and p.y <=bb.YMax and bb.ZMin<= p.z and p.z <=bb.ZMax)]
		rel=" outside "

	t=Points.Points(pts)
	Points.show(t)
	App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(random.random(),random.random(),random.random())
	
	App.ActiveDocument.ActiveObject.Label=sels[1].Label  + rel + sels[0].Label + " "



# get top points
def toppoints():
	pass

# project to xy plane
def projectxy(d=2):
	sels=Gui.Selection.getSelection()
	if len(sels)<>1: print("Du musst Pointset auswaehlen" )
	pts=np.array(sels[0].Points.Points)
	pts[:,d]=0
	t=Points.Points([tuple(p) for p in pts])
	Points.show(t)
	proj=["yz","xz","xy"][d]
	App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(random.random(),random.random(),random.random())
	App.ActiveDocument.ActiveObject.Label=proj+"-Projection of " +sels[0].Label +" "

# transform by matrix
def transform():
	sels=Gui.Selection.getSelection()
	if len(sels)<>1: print("Du musst Pointset auswaehlen" )
	pts=np.array(sels[0].Points.Points)

	matrix=[float(f) for f in  '2 0  0 500 0 1 0 -500 0 0 0.5 130'.split()]
	matrix=np.array(matrix).reshape(3,4)
	print matrix


	[x,y,z]=np.array(pts).swapaxes(0,1)
	w=[1]*len(x)

	pts2=np.array([x,y,z,w])
	pts3=pts2.swapaxes(0,1)
	

	t=Points.Points([tuple(matrix.dot(p)) for p in pts3])
	Points.show(t)
	App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(random.random(),random.random(),random.random())
	App.ActiveDocument.ActiveObject.Label="Transformed "  +sels[0].Label +" "



import time

def toppoints(mode=5):

	sels=Gui.Selection.getSelection()
	if len(sels)<>1: print("Du musst Pointset auswaehlen" )
	pts=np.array(sels[0].Points.Points)
#	pts=pts[:500]
	print ("pts shape",pts.shape, "mode",mode)
	#if len(pts)>6000:
	if len(pts)>17000:
		print "to much data, abort!"
		return

	x,y,z=pts.swapaxes(0,1)

	if mode in [0,1]:
		zu=np.unique(z)
		yu=np.unique(y)
		pts4=[]

		for iz in zu:
			for iy in yu:
				l=[p[0] for p in pts if p[2]==iz and p[1]==iy]
				if l<>[]:
					if mode==1: 
						pts4.append(FreeCAD.Vector(min(l),iy,iz))
						lab="X min"
					if mode==0: 
						pts4.append(FreeCAD.Vector(max(l),iy,iz))
						lab="X max"

	if mode in [2,3]:
		xu=np.unique(x)
		zu=np.unique(z)
		pts4=[]

		for ix in xu:
			for iz in zu:
				l=[p[1] for p in pts if p[0]==ix and p[2]==iz]
				if l<>[]:
					if mode==3: 
						pts4.append(FreeCAD.Vector(ix,min(l),iz))
						lab="Y min"
					if mode==2: 
						pts4.append(FreeCAD.Vector(ix,max(l),iz))
						lab="Y max"

	if mode in [4,5]:
		xu=np.unique(x)
		yu=np.unique(y)
		pts4=[]

		print xu
		print yu
		print len(xu)
		print len(yu)
		for ix in xu:
			for iy in yu:
				l=[p[2] for p in pts if p[0]==ix and p[1]==iy]
				if l<>[]:
					# print (ix,iy,min(l))
					if mode==5: 
						pts4.append(FreeCAD.Vector(ix,iy,min(l)))
						lab="Z min"
					if mode==4: 
						pts4.append(FreeCAD.Vector(ix,iy,max(l)))
						lab="Z max"



	print ("reduced points",len(pts4))

	pcl=Points.Points(pts4)
	Points.show(pcl)

	colormap=[ 
		(1.,0.,0.),(0.,1.,1.),
		(0.,1.,0.),(1.,0.,1.),
		(0.,0.,1.),(1.,1.,0.),
	]
	
	App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(colormap[mode])
	App.ActiveDocument.ActiveObject.ViewObject.PointSize=4
	App.ActiveDocument.ActiveObject.Label=lab+" "  +sels[0].Label +" "




def reducepoints(k=40):


	sels=Gui.Selection.getSelection()
	if len(sels)<>1: print("Du musst Pointset auswaehlen" )
	pts=np.array(sels[0].Points.Points)

	print ("len start",len(pts))
	pts=np.array(pts)

	ptsm=pts

	if k<>0:
#		ptsm[:]  += [100,300,500]
		ptsm /=k 
		pts2=ptsm.round()
		pts2 *=k
	else:
		pts2=ptsm

	data=pts2
	ncols = data.shape[1]
	dtype = data.dtype.descr * ncols
	struct = data.view(dtype)

	uniq = np.unique(struct)
	uniq = uniq.view(data.dtype).reshape(-1, ncols)

	pts3= uniq
	print len(uniq)

	pts3v=[FreeCAD.Vector(p) for p in pts3]
	pcl=Points.Points(pts3v)
	Points.show(pcl)
	App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(random.random(),random.random(),random.random())
	App.ActiveDocument.ActiveObject.Label="Reduce " +str(k) + " " +sels[0].Label +" "



def center():

	sels=Gui.Selection.getSelection()
	if len(sels)<>1: print("Du musst Pointset auswaehlen" )
	pts=np.array(sels[0].Points.Points)


	x,y,z=pts.swapaxes(0,1)
	xm=x.mean()
	ym=y.mean()
	zm=z.mean()

	x -= xm
	y -= ym
	z -= zm

	pts3v=[FreeCAD.Vector(p) for p in np.array([x,y,z]).swapaxes(0,1)]
	pcl=Points.Points(pts3v)
	Points.show(pcl)
	App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(random.random(),random.random(),random.random())
	App.ActiveDocument.ActiveObject.Label="Centered " + sels[0].Label +" "


gridsize=40
gridsize=8
gridsize=12
gridsize=16
gridsize=25
gridsize=5
gridsize=16



def interpolate(x,y,z, gridsize,mode='thin_plate',rbfmode=True,shape=None):

	grids=gridsize

	dx=np.max(x)-np.min(x)
	dy=np.max(y)-np.min(y)

	if dx>dy:
		gridx=grids
		gridy=int(round(dy/dx*grids))
	else:
		gridy=grids
		gridx=int(round(dx/dy*grids))

	if shape<>None:
		(gridy,gridx)=shape

	xi, yi = np.linspace(np.min(x), np.max(x), gridx), np.linspace(np.min(y), np.max(y), gridy)
	xi, yi = np.meshgrid(xi, yi)

	if rbfmode:
		rbf = scipy.interpolate.Rbf(x, y, z, function=mode)
		rbf2 = scipy.interpolate.Rbf( y,x, z, function=mode)
	else:
		print "interp2d nicht implementiert"
		rbf = scipy.interpolate.interp2d(x, y, z, kind=mode)

	zi=rbf2(yi,xi)
	return [rbf,xi,yi,zi]



def showFace(rbf,x,y,gridsize,zmax,zmin,mode):

	ws=[]
	allpts=[]

	xi, yi = np.linspace(np.min(x), np.max(x), gridsize), np.linspace(np.min(y), np.max(y), gridsize)

	for ix in xi:
		points=[]
		for iy in yi:
			iz=float(rbf(ix,iy))
			if iz>zmax: iz=zmax
			if iz<zmin: iz=zmin

			points.append(FreeCAD.Vector(iy,ix,iz))
			

		allpts.append(points)
		w=Part.makePolygon(points)
		ws.append(w)

	for iy in yi:
		points=[]
		for ix in xi:
			iz=float(rbf(ix,iy))
			if iz>zmax: iz=zmax
			if iz<zmin: iz=zmin

			points.append(FreeCAD.Vector(iy,ix,iz))

#		allpts.append(points)
		w=Part.makePolygon(points)
		ws.append(w)

	t2=Part.Compound(ws)
	Part.show(t2)
	App.ActiveDocument.ActiveObject.Label=mode + " Grid "
	App.ActiveDocument.ActiveObject.ViewObject.LineColor=(random.random(),random.random(),random.random())
	return allpts

#-------------------


import Sketcher 
def createSketchSpline(pts=None):
	
	print "create sketcher Spline deaktivert"
	
	return

	try: body=App.activeDocument().Body
	except:	body=App.activeDocument().addObject('PartDesign::Body','Body')

	sk=App.activeDocument().addObject('Sketcher::SketchObject','Sketch')

#	sk.Support = (App.activeDocument().XY_Plane, [''])

	sk.MapMode = 'FlatFace'

	App.activeDocument().recompute()

	if pts==None:
		pass
		pts=[FreeCAD.Vector(a) for a in [(10,20,30), (30,60,30), (20,50,40),(50,80,90)]]

	for i,p in enumerate(pts):
		sk.addGeometry(Part.Circle(App.Vector(int(round(p.x)),int(round(p.y)),0),App.Vector(0,0,1),10),True)
		if i == 1: sk.addConstraint(Sketcher.Constraint('Radius',0,10.000000)) 
		if i>0: sk.addConstraint(Sketcher.Constraint('Equal',0,i)) 

	k=i+1

	l=[App.Vector(int(round(p.x)),int(round(p.y))) for p in pts]

	sk.addGeometry(Part.BSplineCurve(l,False),False)

	conList = []

	for i,p in enumerate(pts):
		conList.append(Sketcher.Constraint('InternalAlignment:Sketcher::BSplineControlPoint',i,3,k,i))

	sk.addConstraint(conList)

	App.activeDocument().recompute()

 	sk.Placement = App.Placement(App.Vector(0,0,p.z),App.Rotation(App.Vector(1,0,0),0))

	App.activeDocument().recompute()
	print "ZZZZZZZZZZZZZZZZZZZ",p.z

	return sk



#-------------------

def showNurbs(rbf,x,y,gridsize,zmax,zmin,mode):

	ws=[]
	allpts=[]
	ptgr=[]

	xi, yi = np.linspace(np.min(x), np.max(x), gridsize), np.linspace(np.min(y), np.max(y), gridsize)

	for ix in xi:
		points=[]
		for iy in yi:
			iz=float(rbf(ix,iy))
			if iz>zmax: iz=zmax
			if iz<zmin: iz=zmin

			points.append(FreeCAD.Vector(iy,ix,iz))
			

		allpts.append(points)
		ptgr += points
		w=Part.makePolygon(points)
		ws.append(w)

	for iy in yi:
		points=[]
		for ix in xi:
			iz=float(rbf(ix,iy))
			if iz>zmax: iz=zmax
			if iz<zmin: iz=zmin

			points.append(FreeCAD.Vector(iy,ix,iz))

#		allpts.append(points)
		w=Part.makePolygon(points)
		ws.append(w)

#	t2=Part.Compound(ws)
#	Part.show(t2)

	print "make bs"
	color=(random.random(),random.random(),random.random())
	bs=Part.BSplineSurface()
	print ptgr
	bs.interpolate(allpts)
	print bs.getPoles()
	grp=App.ActiveDocument.addObject("App::DocumentObjectGroup","Group for Nurbs " + mode)
	if 10:
		sp=App.ActiveDocument.addObject("Part::Spline","Nurbs " + mode)
		# sp.ViewObject.ControlPoints=True
		sp.Shape=bs.toShape()
	#	Part.show(bs.toShape())
	#	App.ActiveDocument.ActiveObject.Label=mode + " Grid "
		App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=color
		grp.addObject(sp)
		sp.ViewObject.Transparency=70
		sp.ViewObject.hide()

	# die bsplines zeigen

	sks=[]
	for i,j in enumerate(bs.getUKnots()):
		f=bs.uIso(j)

		ppts=f.getPoles()
		ppts2=[FreeCAD.Vector(p.x,p.z,p.y) for p in ppts]
#		createSketchSpline(ppts2)
		sks.append(createSketchSpline(ppts2))

		sp=App.ActiveDocument.addObject("Part::Spline","U Iso " + str(i+1) +"#")
		sp.Shape=f.toShape()
		App.ActiveDocument.ActiveObject.ViewObject.LineColor=color
		grp.addObject(sp)



	loft=App.ActiveDocument.addObject('Part::Loft','Loft on BSPline Sketch ')
	loft.Sections=sks

#	loft.Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,0),90))


	sks=[]
	for i,j in enumerate(bs.getVKnots()):
		f=bs.vIso(j)

		ppts=f.getPoles()
		ppts2=[FreeCAD.Vector(p.z,p.y,p.x) for p in ppts]
		sks.append(createSketchSpline(ppts2))


		sp=App.ActiveDocument.addObject("Part::Spline","V Iso " + str(i+1) +"#")
		sp.Shape=f.toShape()
		App.ActiveDocument.ActiveObject.ViewObject.LineColor=color
		grp.addObject(sp)

#		for s in sks:
#			s.Placement=App.Placement(App.Vector(),App.Rotation(App.Vector(0,1,0),90)).multiply(s.Placement)

	loft=App.ActiveDocument.addObject('Part::Loft','Loft on BSPline Sketch ')
	loft.Sections=sks
#	loft.Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(1,0,1),180))

	App.activeDocument().recompute()
	return allpts




def createQuadMesh(pts4,mode):

	# calculate quadmesh
	[x,y,z]=np.array(pts4).swapaxes(0,1)
	# add some noise to avoid singular matrix

	x+= np.random.random(len(x))
	y+= np.random.random(len(x))


	x,y=y,x
	rbfmode=True

	rbf,xi,yi,zi = interpolate(x,y,z, gridsize,mode,rbfmode)
	rc=showFace(rbf,x,y,gridsize,z.max(),z.min(),mode)
	#showHeightMap(x,y,z,zi)
	return rc


def createNurbs(pts4,mode,gridsize):

	# calculate quadmesh
	[x,y,z]=np.array(pts4).swapaxes(0,1)
	# add some noise to avoid singular matrix

	x+= np.random.random(len(x))
	y+= np.random.random(len(x))


	x,y=y,x
	rbfmode=True

	rbf,xi,yi,zi = interpolate(x,y,z, gridsize,mode,rbfmode)
	rc=showNurbs(rbf,x,y,gridsize,z.max(),z.min(),mode)
	#showHeightMap(x,y,z,zi)
	return rc


def topart(mode='linear'):

	sels=Gui.Selection.getSelection()
	if len(sels)<>1: print("Du musst Pointset auswaehlen" )
	pts=np.array(sels[0].Points.Points)
	if len(pts)>6000:
		print "to much data, abort!"
		return

	createQuadMesh(pts,mode)



def tonurbs(mode='linear',gridsize=10):

	sels=Gui.Selection.getSelection()
	if len(sels)<>1: print("Du musst Pointset auswaehlen" )
	pts=np.array(sels[0].Points.Points)
	if len(pts)>6000:
		print (len(pts),"to much data, abort!")
		return

	createNurbs(pts,mode,gridsize)


def applyplacement():

	sels=Gui.Selection.getSelection()
	if len(sels)<>1: print("Du musst Pointset auswaehlen" )
	pts=sels[0].Points.Points
	p2=sels[0].Points.Placement

	pcl=Points.Points(pts)
	Points.show(pcl)
	App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(random.random(),random.random(),random.random())
	App.ActiveDocument.ActiveObject.Label="Placed " + sels[0].Label +" "


def fusionpoints():
	import Points

	sels=Gui.Selection.getSelection()
	pts=sels[0].Points.Points
	pts2=sels[1].Points.Points


	pcl=Points.Points(pts + pts2)
	Points.show(pcl)


def randomcloud():
	r=1000.0
	pts=[FreeCAD.Vector(r*random.random(),r*random.random(),r*random.random()) for i in range(1000)]
	pcl=Points.Points(pts)
	Points.show(pcl)
	App.ActiveDocument.ActiveObject.Label="Random Cloud "
	App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(random.random(),random.random(),random.random())


import numpy as np

def flatborder():
	sels=Gui.Selection.getSelection()
	obj=sels[0]

	bs=obj.Shape.Face1.Surface

	poles=np.array(bs.getPoles())


 	poles[:,:,2]=poles[:,:,2].mean()
#	poles[:,:,2]=poles[:,:,2].min()
 	poles[:,:,2]=0

	if poles[-1,:,0].max()<poles[0,:,0].min():
		pa=poles[-1,:,0].min()
		pb=poles[0,:,0].max()
	else:
		pa=poles[-1,:,0].max()
		pb=poles[0,:,0].min()

	poles[-1,:,0]=pa
	poles[0,:,0]=pb

	if  poles[:,-1,1].max()< poles[:,0,1].min():
		pa=poles[:,-1,1].min()
		pb=poles[:,0,1].max()
	else:
		pa=poles[:,-1,1].max()
		pb=poles[:,0,1].min()

	poles[:,-1,1]=pa
	poles[:,0,1]=pb


	for i in range(bs.NbUPoles):
		bs.setPole(1,i+1,FreeCAD.Vector(tuple(poles[0,i])))
		bs.setPole(bs.NbVPoles,i+1,FreeCAD.Vector(tuple(poles[-1,i])))

	for i in range(bs.NbVPoles):
		bs.setPole(i+1,1,FreeCAD.Vector(tuple(poles[i,0])))
		bs.setPole(i+1,bs.NbUPoles,FreeCAD.Vector(tuple(poles[i,-1])))

	sp=App.ActiveDocument.addObject("Part::Spline","Spline")
	sp.ViewObject.ControlPoints=True
	sp.Label="flat border for " + obj.Label
	sp.Shape=bs.toShape()


def scale():
	sels=Gui.Selection.getSelection()
	pts=sels[0].Points.Points
	pts2=[p*100 for p in pts]
	pcl=Points.Points(pts2)
	Points.show(pcl)

	
