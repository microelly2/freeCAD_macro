# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- map curve to a cylindric face
#--
#-- microelly 2016 v 0.4
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import Draft
import numpy as np
import random



def genCylinderFace(w,yscale=1,radius=100,delta=1, angle=180,xscale=0,flipxy=False,xoffset=0.0,yoffset=1.0,model=10,details=6):
	''' generate a bended wire/surface/solid for wire w
		radius, radius+delta - inner and outer radius of the generated solid
		yscale - factore to scale the height
		xscale and angle - the lenght xscale is mFreeCAD.d to the angle:  radius*angle/180*pi = xscale 
		yscale=0 means normalize y, xscale=0 means normalize x
		flipxy - change the height and arc direction 
		xoffset, yoffset - offset to the starting arc, height
		model - 0 only wire, 1 bspline, 2, surface, 10 solid and all components 
		details - number of discretizion points on each edge (30 is very good quality)
	'''

	try: grp=FreeCAD.ActiveDocument.Gruppe
	except: grp=FreeCAD.ActiveDocument.addObject("App::DocumentObjectGroup","Gruppe")

	# create a fine pointlist for FreeCAD.oximation
	# details=30

	if hasattr(w,"Shape"):
		eds=Part.__sortEdges__(w.Shape.Edges)
	else:
		eds=Part.__sortEdges__(w.Edges)

	pts=[]
	for e in eds:
		ees=e.discretize(details)
		pts += ees[0:-1]

	pts.append(ees[-1])
	print "Len pts:", len(pts)


	pts=np.array(pts)
	xs=pts[:,0]
	ys=pts[:,1]

	if flipxy:
		xs,ys=ys,xs

	if xscale == 0:
		# normalize x
		xs -= xs.min()
		xs /= xs.max()
	else:
		xs /= xscale

	if yscale==0:
		ys -= ys.min()
		ys /= ys.max()


	xs *= angle*np.pi/180
	xs += xoffset

	ys *= yscale
	ys += yoffset

	pts2=[]

	r1=radius
	r2=r1+delta

	for i in range(len(xs)):
		pts2.append(FreeCAD.Vector(r1*np.cos(xs[i]),r1*np.sin(xs[i]),ys[i]))

	# connector between ends
	#print(xs[0],ys[0])
	#print(xs[-1],ys[-1])
	if abs(xs[0]-xs[-1])<0.001  and abs(ys[0]-ys[-1])<0.001:
		pass
	else:
		for k in range(1,10):
			pts2.append(FreeCAD.Vector(r1*np.cos(xs[-1]+(xs[0]-xs[-1])*k/9),
			r1*np.sin(xs[-1]+(xs[0]-xs[-1])*k/9),(ys[-1]+(ys[0]-ys[-1])*k/9)))

	if model==0:
		Draft.makeWire(pts2)
		grp.addObject(FreeCAD.ActiveDocument.ActiveObject)
		return


	# create Curve
	bs=Part.BSplineCurve()
	bs.interpolate(pts2)
	Part.show(bs.toShape())


	grp.addObject(FreeCAD.ActiveDocument.ActiveObject)
	if model==1: return
	FreeCAD.ActiveDocument.ActiveObject.ViewObject.hide()
	ob1=FreeCAD.ActiveDocument.ActiveObject



	f1=FreeCAD.ActiveDocument.addObject('Part::Feature','Face')
	f1.Shape=Part.makeFilledFace(Part.__sortEdges__(ob1.Shape.Edges))

	if model==2: return


	# create upper curve and face
	pts2=[]

	for i in range(len(xs)):
		pts2.append(FreeCAD.Vector(r2*np.cos(xs[i]),r2*np.sin(xs[i]),ys[i]))

	# connector between ends
	if abs(xs[0]-xs[-1])<0.001  and abs(ys[0]-ys[-1])<0.001:
		pass
	else:
		for k in range(1,10):
			pts2.append(FreeCAD.Vector(r2*np.cos(xs[-1]+(xs[0]-xs[-1])*k/9),
			r2*np.sin(xs[-1]+(xs[0]-xs[-1])*k/9),(ys[-1]+(ys[0]-ys[-1])*k/9)))

	#Draft.makeWire(pts2)

	bs=Part.BSplineCurve()
	bs.interpolate(pts2)
	Part.show(bs.toShape())
	grp.addObject(FreeCAD.ActiveDocument.ActiveObject)
	FreeCAD.ActiveDocument.ActiveObject.ViewObject.hide()
	ob1=FreeCAD.ActiveDocument.ActiveObject

	f2=FreeCAD.ActiveDocument.addObject('Part::Feature','Face')
	f2.Shape=Part.makeFilledFace(Part.__sortEdges__(ob1.Shape.Edges))
	grp.addObject(FreeCAD.ActiveDocument.ActiveObject)


	loft=FreeCAD.ActiveDocument.addObject('Part::Loft','Loft')
	loft.Sections=[f1,f2]
	f1.ViewObject.hide()
	f2.ViewObject.hide()
	loft.Solid=True
	grp.addObject(FreeCAD.ActiveDocument.ActiveObject)

	FreeCAD.activeDocument().recompute()






# testcase 

def testcase1():

	try: FreeCAD.closeDocument("Unbenannt")
	except: pass

	FreeCAD.setActiveDocument("")
	FreeCAD.newDocument("Unbenannt")
	FreeCAD.setActiveDocument("Unbenannt")
	FreeCAD.ActiveDocument=FreeCAD.getDocument("Unbenannt")
	Gui.ActiveDocument=Gui.getDocument("Unbenannt")

	points=[FreeCAD.Vector(-139.340072632,-39.54246521,0.0),FreeCAD.Vector(-72.4945220947,137.457092285,0.0),FreeCAD.Vector(110.153968811,160.994277954,0.0),FreeCAD.Vector(227.839874268,23.5371818542,0.0),FreeCAD.Vector(76.2604675293,-165.701721191,0.0),FreeCAD.Vector(-83.7923278809,-115.802909851,0.0)]
	Draft.makeWire(points,closed=False,face=True,support=None)
	genCylinderFace(FreeCAD.ActiveDocument.DWire,radius=410,delta=80,angle=40)

	points=[FreeCAD.Vector(-196.834311438,-482.062053664,-269.81047364),FreeCAD.Vector(266.80789649,1282.55258679,331.385109598),FreeCAD.Vector(1970.39292347,2.64078762024,2964.18629001),FreeCAD.Vector(703.391176917,-687.969329265,1095.76114336)]
	Draft.makeBSpline(points,closed=False,face=True,support=None)
	genCylinderFace(FreeCAD.ActiveDocument.BSpline,radius=410,delta=60,angle=90)
	FreeCAD.ActiveDocument.ActiveObject.Placement.Rotation.Angle=3.14

	Gui.SendMsgToActiveView("ViewFit")

# testcase1()

'''
yscale==0 -> normalize
xscale==0 -> normalize

'''


def testcase3():
	# use PatricksRing file from this post
	# http://forum.freecadweb.org/viewtopic.php?f=13&t=17983#p141520

	FreeCAD.open(u"/home/thomas/Dokumente/freecad_buch/b218_abbildung_auf_flaeche/daten/PatricksRing.FCStd")
	FreeCAD.setActiveDocument("PatricksRing")
	FreeCAD.ActiveDocument=FreeCAD.getDocument("PatricksRing")
	Gui.ActiveDocument=Gui.getDocument("PatricksRing")

	i=0
	for d in FreeCAD.ActiveDocument.Objects: 
		# if i>2:break
		if 1:
			pass
		try:
			if d.Name.startswith('Extrude'):
				FreeCAD.Console.PrintMessage(str((i,"--",d.Name))+"\n")
				i += 1
				db=d.Base
				delta=d.Dir.z
				print (i,d.Name, delta)
				for radius in [10]:
					genCylinderFace(db,yscale=1,radius=radius,delta=delta,angle=90,xscale=10,flipxy=True,model=10)
				Gui.updateGui()
				
		except: 
			print ("problem with ", i,d.Name)


# testcase3()



def testcase4():
	# mauer auf zylinder
	# http://forum.freecadweb.org/viewtopic.php?f=13&t=17795


	rect=FreeCAD.ActiveDocument.Rectangle
	z=FreeCAD.ActiveDocument.addObject("Part::Cylinder","Cylinder")
	radius=rect.Length.Value/np.pi
	z.Radius=rect.Length/np.pi
	z.Height=rect.Height

	for i,d in enumerate(FreeCAD.ActiveDocument.Gruppe001.OutList):
		try:
			FreeCAD.Console.PrintMessage(str((i,"--",d.Name))+"\n")
			
			delta= 60*(0.4+random.random())
			print (i,d.Name, delta)
			genCylinderFace(d,yscale=1,radius=radius,delta=delta,angle=360,xscale=rect.Length.Value,flipxy=False,details=30,model=20)
			Gui.updateGui()
		except: 
			print ("problem with ", i,d.Name)

#testcase4()

def testcase5():
	# anpassung alle Steine in einem Sketch
	s=App.ActiveDocument.Sketch.Shape
	s.Wires

	rect=FreeCAD.ActiveDocument.Rectangle

	z=FreeCAD.ActiveDocument.addObject("Part::Cylinder","Cylinder")
	radius=abs(0.5*rect.Length.Value/np.pi)
	z.Radius=abs(0.5*rect.Length/np.pi)
	z.Height=abs(rect.Height)



	for i,d in enumerate(s.Wires):
		FreeCAD.Console.PrintMessage(str([i,d]) +"\n")
		delta= 60*(0.4+random.random())
		print (i, delta)
		genCylinderFace(d,yscale=1,radius=radius,delta=delta,angle=360,xscale=rect.Length.Value,flipxy=False,details=30,model=20)
		Gui.updateGui()

testcase5()
