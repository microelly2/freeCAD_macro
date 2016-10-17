
# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- map curve to a cylindric face
#--
#-- microelly 2016 v 0.2
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------



def genCylinderFace(w,height=250,radius=100,delta=30,angle=180,xangle=0):


	try: grp=App.ActiveDocument.Gruppe
	except: grp=App.ActiveDocument.addObject("App::DocumentObjectGroup","Gruppe")

	details=30
	details=6

	eds=Part.__sortEdges__(w.Shape.Edges)
	pts=[]
	for e in eds:
		ees=e.discretize(details)
		pts += ees[0:-1]

	pts.append(ees[-1])
	print "Len pts:", len(pts)
##	Draft.makeWire(pts)


	import numpy as np
	pts=np.array(pts)
	xs=pts[:,0]
	ys=pts[:,1]
	
	# tauschen
	xs,ys=ys,xs

	if xangle == 0:
		xs -= xs.min()
		xs /= xs.max()
	else:
		xs /= xangle

#	ys -= ys.min()
#	ys /= ys.max()


	#xs *= 3.1
	xs *= angle*np.pi/180
	xs += 0.2

	ys *= height
	ys += 1

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


#	Draft.makeWire(pts2)
#	ob1=App.ActiveDocument.ActiveObject


	bs=Part.BSplineCurve()
	bs.interpolate(pts2)
	Part.show(bs.toShape())

	grp.addObject(App.ActiveDocument.ActiveObject)
	App.ActiveDocument.ActiveObject.ViewObject.hide()
	ob1=App.ActiveDocument.ActiveObject

	_=Part.makeFilledFace(Part.__sortEdges__(ob1.Shape.Edges))

	f1=App.ActiveDocument.addObject('Part::Feature','Face')
	f1.Shape=_



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

##	Draft.makeWire(pts2)
#	ob1=App.ActiveDocument.ActiveObject

	bs=Part.BSplineCurve()
	bs.interpolate(pts2)
	Part.show(bs.toShape())
	grp.addObject(App.ActiveDocument.ActiveObject)
	App.ActiveDocument.ActiveObject.ViewObject.hide()

	ob1=App.ActiveDocument.ActiveObject

	_=Part.makeFilledFace(Part.__sortEdges__(ob1.Shape.Edges))

	f2=App.ActiveDocument.addObject('Part::Feature','Face')
	f2.Shape=_

	grp.addObject(App.ActiveDocument.ActiveObject)


	loft=App.ActiveDocument.addObject('Part::Loft','Loft')
	loft.Sections=[f1,f2]
	f1.ViewObject.hide()
	f2.ViewObject.hide()
	loft.Solid=True
	grp.addObject(App.ActiveDocument.ActiveObject)

	App.activeDocument().recompute()

# testcase 

'''
try: App.closeDocument("Unbenannt")
except: pass

App.setActiveDocument("")
App.newDocument("Unbenannt")
App.setActiveDocument("Unbenannt")
App.ActiveDocument=App.getDocument("Unbenannt")
Gui.ActiveDocument=Gui.getDocument("Unbenannt")


import Draft

points=[FreeCAD.Vector(-139.340072632,-39.54246521,0.0),FreeCAD.Vector(-72.4945220947,137.457092285,0.0),FreeCAD.Vector(110.153968811,160.994277954,0.0),FreeCAD.Vector(227.839874268,23.5371818542,0.0),FreeCAD.Vector(76.2604675293,-165.701721191,0.0),FreeCAD.Vector(-83.7923278809,-115.802909851,0.0)]
Draft.makeWire(points,closed=False,face=True,support=None)
genCylinderFace(App.ActiveDocument.DWire,height=1250,radius=410,delta=80,angle=40)

points=[FreeCAD.Vector(-196.834311438,-482.062053664,-269.81047364),FreeCAD.Vector(266.80789649,1282.55258679,331.385109598),FreeCAD.Vector(1970.39292347,2.64078762024,2964.18629001),FreeCAD.Vector(703.391176917,-687.969329265,1095.76114336)]
Draft.makeBSpline(points,closed=False,face=True,support=None)
genCylinderFace(App.ActiveDocument.BSpline,height=1250,radius=410,delta=60,angle=90)
App.ActiveDocument.ActiveObject.Placement.Rotation.Angle=3.14
'''
import Draft

#Gui.SendMsgToActiveView("ViewFit")



i=0
for d in App.ActiveDocument.Objects: 
	# if i>15:break
	arc=0
	try:
		if d.Name.startswith('path'):
			#arc=5
			FreeCAD.Console.PrintMessage(str((i,"--",d.Name))+"\n")
			i += 1
			genCylinderFace(d,height=0.4,radius=10.1,delta=0.5,angle=25,xangle=10)
#			print d.Shape.BoundBox.XLength
			arc += d.Shape.BoundBox.YLength  
			
			# App.ActiveDocument.ActiveObject.Placement.Rotation=App.Rotation(App.Vector(0,0,1), arc)
			Gui.updateGui()
			
	except: pass



# genCylinderFace(App.ActiveDocument.path3349_74_1_1,height=1250,radius=2000,delta=60,angle=10,xangle=10)



