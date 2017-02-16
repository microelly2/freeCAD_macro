#coding: utf-8 -*-
#-------------------------------------------------
#-- create bubbles in a box
#--
#-- microelly 2017 v 0.0
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import FreeCAD, FreeCADGui
App=FreeCAD
Gui=FreeCADGui

import numpy as np
import cv2
import time
import random
import Points


def run3(countbubbles=5000,radius=20,sizebox=1024,slize=None):
	cc=countbubbles

	if slize==None:
		circles=[[random.random(),random.random(),random.random(),random.random()] for i in range(cc)]
	else:
		circles=[[random.random(),random.random(),random.random(),1] for i in range(cc)]

#	for c in circles:
#		s=App.ActiveDocument.addObject("Part::Sphere","Sphere")
#		s.Radius=c[3]*radius
#		s.Placement.Base=FreeCAD.Vector(tuple(np.array(c[0:3])*sizebox))

	pts=[]
	ptsa=[]
	ct=0
	if slize<>None: slices=[slize]
	else: slices=range(sizebox)
	

	for z in slices:
	#for z in range(101):
		FreeCAD.Console.PrintMessage("--" +str(z) +"---\n")
		s=time.time()
		# Create a black image
		img = np.zeros((sizebox,sizebox), np.uint8)

		for i in range(cc):
			x=int(round(circles[i][0]*sizebox))
			y=int(round(circles[i][1]*sizebox))
			r2= int(round(circles[i][3]*radius))**2 - (int(round(circles[i][2]*sizebox))-z)**2
			if r2>0:
				r=int(round(np.sqrt(r2))) 
				cv2.circle(img,(x,y),r, 255, -1)

		# volumen points
		nzs=np.nonzero(img)
		nzs=np.array(nzs).swapaxes(0,1)

		ptsa += [FreeCAD.Vector(x,y,z)  for [x,y] in nzs]

		for [x,y] in nzs:
				img[x,y]=255 

		kernel = np.ones((5,5),np.uint8)
#		dilation = cv2.dilate(img,kernel,iterations = 1)
		erosion = cv2.erode(img,kernel,iterations = 1)
#		img=dilation
		img=erosion

		# border points
		edges = cv2.Canny(img,1,255)
#		edges2 = cv2.Laplacian(img,cv2.CV_64F)
#		edges += edges2


		nzs=np.nonzero(edges)
		nzs=np.array(nzs).swapaxes(0,1)


		pts += [FreeCAD.Vector(x,y,z)  for [x,y] in nzs]

		FreeCAD.Console.PrintMessage(str(round(time.time()-s,3)) + "\n")
		Gui.updateGui()

		if z % 10 == 0:
			Points.show(Points.Points(pts))
			App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(random.random(),random.random(),random.random())
			App.ActiveDocument.ActiveObject.ViewObject.PointSize=5
			ct +=len(pts)
			FreeCAD.Console.PrintMessage("points added " + str(len(pts)) +"!! \n")
			pts=[]
			Gui.updateGui()
	if len(pts)>0:
		Points.show(Points.Points(pts))
		App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(random.random(),random.random(),random.random())

	Points.show(Points.Points(ptsa))
	App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(.0,.0,.0)
	App.ActiveDocument.ActiveObject.ViewObject.PointSize=1
	App.ActiveDocument.ActiveObject.ViewObject.hide()
	App.ActiveDocument.ActiveObject.Label="Volumen"
	return edges

# run3()

# img=run3(countbubbles=180,radius=20,sizebox=200,slize=0)

def run():
	img=run3(countbubbles=200,radius=20,sizebox=200,slize=0)
	FreeCAD.img=img

