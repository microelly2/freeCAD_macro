import FreeCAD, FreeCADGui
App=FreeCAD
Gui=FreeCADGui


import networkx as nx
import numpy as np
import cv2
import time
import random
import Points
import Draft



#
# vorher gen_bubbles.py aufrufen
#


def run(img=None):
	''' create Wires for image border edges '''

	if img==None: img=FreeCAD.img

	kern = np.array([[1,1,1],[1,10,1],[1,1,1]])

	img2=img/255

	kk=cv2.filter2D(img2, -1, kern)

	ret, mask = cv2.threshold(kk, 11, 255, cv2.THRESH_BINARY)
	#ret, mask = cv2.threshold(kk, 12, 255, cv2.THRESH_BINARY)
	#ret, mask = cv2.threshold(kk, 13, 255, cv2.THRESH_BINARY)
	ret, mask = cv2.threshold(kk, 10, 255, cv2.THRESH_BINARY)
	#ret, mask = cv2.threshold(kk, 14, 255, cv2.THRESH_BINARY)


	mask/=255

	cv2.imshow("gg",mask*255)


	img2=mask


	g=nx.Graph()

	for x in range(200):
		for y in range(200):
			if img2[x,y]>0:
				g.add_node((x,y),{"val": img2[x,y]})

	cons=0
	for x in range(200):
		for y in range(200):
			if y<200-1:
				if img2[x,y]>0 and img2[x,y+1]>0:
					g.add_edge((x,y),(x,y+1))
					cons += 1
			if x<200-1:
				if img2[x,y]>0 and img2[x+1,y]>0:
					g.add_edge((x,y),((x+1),y))
					cons += 1

			if y<200-1 and x<200-1:
				if img2[x,y]>0 and img2[x+1,y+1]>0:
					if not g.has_node((x+1,y)) and not g.has_node((x,y+1)):
						g.add_edge((x,y),((x+1),y+1))
						cons += 1
			if y>0 and x<200-1:
				if img2[x,y]>0 and img2[x+1,y-1]:
					if not g.has_node((x+1,y)) and not g.has_node((x,y-1)):
						g.add_edge((x,y),(x+1,y-1))
						cons += 1

	def coords(n):
		x=n//200
		y=n%200
		return(x,y)

	if 10:
		for n in g.nodes():
			nbs=g.neighbors(n)
			if nbs <>[]:
				#nbcs=[coords(nb) for nb in nbs] 
				print (n, nbs)




	cons2=0
	for cc in nx.connected_components(g):
		print cc
		cons2 += len(cc)
	#	cps=[coords(c) for c in cc]
	#	print cps

	nx.number_connected_components(g)

	print cons
	print cons2 


	def nbs(x,y):
		for j in [(x,y),(x-1,y-1),(x,y-1),(x+1,y-1),
			(x-1,y),(x,y),(x+1,y),
			(x-1,y+1),(x,y+1),(x+1,y+1)]:
			try:
				print (j, g.neighbors(j))
			except: print ("no",j)





	for cc in nx.connected_components(g):
		cl=list(cc)
		ptss=[]

		for c in cl:
			g.node[c]['wired']=False

		for c in cl:
			if len(g.neighbors(c))==1:
				print "Start", c
				break


		oldnb=[]
		start=c
		g.node[start]['wired']=True
		p=start
		print p
		ptss.append(p)
		ended=False
		while not ended:
			for n in g.neighbors(p):
				ended=True
				if g.node[n]['wired']==False and n not in oldnb:
					g.node[n]['wired']=True
					ended=False
					oldnb=g.neighbors(p)
					p=n
					ptss.append(p)
					break

		pts=[FreeCAD.Vector(p[0],p[1],10) for p in ptss]
		y=Draft.makeWire(pts)




