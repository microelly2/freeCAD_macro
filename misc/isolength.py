#---------------------



import FreeCAD, Draft, Part
import FreeCADGui
Gui=FreeCADGui
App=FreeCAD


import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate
import Points

import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate
import Points


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



def showHeightMap(x,y,z,zi):
	''' show height map in maptplotlib '''
	zi=zi.transpose()

	plt.imshow(zi, vmin=z.min(), vmax=z.max(), origin='lower',
			   extent=[ y.min(), y.max(),x.min(), x.max()])

	plt.colorbar()

	CS = plt.contour(zi,15,linewidths=0.5,colors='k',
			   extent=[ y.min(), y.max(),x.min(), x.max()])
	CS = plt.contourf(zi,15,cmap=plt.cm.rainbow, 
			   extent=[ y.min(), y.max(),x.min(), x.max()])

	z=z.transpose()
	plt.scatter(y, x, c=z)

	plt.show()
	return




#----------------------

import Draft
A=(-100,0,0)
C=(130,70,0)
D=(160,80,0)
E=(250,0,0)



ss=Gui.Selection.getSelectionEx()[0]
pts=ss.Object.Points
ptsobj=pts
pp=ss.PickedPoints[0]

sb=Gui.Selection.getSelectionEx()[1]
bb=sb.Object.Shape.BoundBox


ss.Object.ViewObject.hide()
sb.Object.ViewObject.hide()

ip=None
for i,p in enumerate(pts):
	print p-pp
	if p.isEqual(pp,0.0001):
		ip=i
		break

print ip

assert(ip<>None)

pa= pts[:ip]
pe=pts[ip+1:]

pts=[FreeCAD.Vector(p) for p in pa+pe]
Draft.makeBSpline(pts)
obj=App.ActiveDocument.ActiveObject
obj.ViewObject.LineColor=(1.0,0.0,0.0)
obj.ViewObject.LineWidth=5



lls=[]
ra=10
bsp3=[]
for ix in range(0,ra+1):
	bsp2=[]
	for iy in range(0,ra+1):
		# B=(10*ix,10*iy,0)
		B=[bb.XMin+1.0/ra*ix*(bb.XMax-bb.XMin),bb.YMin+1.0/ra*iy*(bb.YMax-bb.YMin),0]
		pts=[FreeCAD.Vector(p) for p in pa+[B]+pe]
		try:
			obj.Points=pts
			rc=App.activeDocument().recompute()
			_t=lls.append((B[0],B[1],0.1*obj.Shape.Edge1.Length))
			bsp2.append(FreeCAD.Vector(B[0],B[1],0.1*obj.Shape.Edge1.Length))
		except:
			print ("!",ix,iy)
			_t=lls.append((B[0],B[1],0))
	bsp3.append(bsp2)

obj.Points=ptsobj
rc=App.activeDocument().recompute()


if 0:
	import Points
	Points.show(Points.Points([FreeCAD.Vector(l) for l in lls]))


bs=Part.BSplineSurface()
bs.interpolate(bsp3)
bss=bs.toShape()

if 0:
	prof=FreeCAD.getDocument("Unnamed").addObject("Part::Feature","Length Profile")
	prof.Shape=bss



lls2=np.array(lls).swapaxes(0,1)
(y,x,z)=lls2

mode="linear"
gridsize=5
if 0:
	rbf,xi,yi,zi1 = interpolate(x,y,z, gridsize,mode)
	showHeightMap(x,y,z,zi1)

import random



lan=50
ll=[[l[0],l[1]] for l in lls if l[2]<lan+1 and l[2]>=lan]

'''
from scipy.spatial import Voronoi, voronoi_plot_2d
vor = Voronoi(ll)

import matplotlib.pyplot as plt
voronoi_plot_2d(vor)
plt.show()
vor.vertices

llr=[FreeCAD.Vector(p[0],p[1],0) for p in vor.ridge_points]
Draft.makeWire(llr)
'''

from scipy.spatial import ConvexHull

for lan in range(int(round(z.min())),int(round(z.max()))):
	print lan

	wires=list()
	for i in bss.slice(FreeCAD.Vector(0,0,1),lan):
		wires.append(i)
	comp=Part.Compound(wires)
	slice=FreeCAD.getDocument("Unnamed").addObject("Part::Feature","Lenght " + str(lan*10))
	slice.Shape=comp
	slice.purgeTouched()
	slice.Placement.Base.z=-lan-1
	slice.ViewObject.LineColor=(random.random(),random.random(),random.random())
	Gui.updateGui()
	


'''

	ll=[[l[0],l[1]] for l in lls if l[2]<lan+0.5 and l[2]>=lan-0.5]
	ll3=[l for l in lls if l[2]<lan+0.5 and l[2]>=lan-0.5]
	if ll<>[]:

		Points.show(Points.Points([FreeCAD.Vector(l) for l in ll3]))
		App.ActiveDocument.ActiveObject.Label="Lenght " + str(lan*10)
		App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(random.random(),random.random(),random.random())

		ll=np.array(ll)
		try:
			hull = ConvexHull(ll)
		except:
			continue
		v=np.array([ll[hull.vertices,0],ll[hull.vertices,1]]).swapaxes(0,1)
		llr=[FreeCAD.Vector(p[0],p[1],0) for p in v]
		Draft.makeWire(llr,closed=True,face=False)
		#Draft.makeBSpline(llr,closed=True,face=False)

		App.ActiveDocument.ActiveObject.Label="Lenght " + str(lan*10)
		App.ActiveDocument.ActiveObject.ViewObject.LineColor=(random.random(),random.random(),random.random())
'''


FreeCAD.Console.PrintMessage("Length:" + str(App.ActiveDocument.BSpline.Shape.Curve.length())

 
 
 
 
 
