# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- submesh in a box
#--
#-- microelly 2017 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import FreeCAD
from PySide import QtGui
import numpy as np
import Mesh
import FreeCAD as App
import FreeCADGui as Gui
import sys,traceback,random



def commonMesh(mesh,box): 

	t=Mesh.Mesh()
	Mesh.show(t)
	m_out=App.ActiveDocument.ActiveObject
	App.ActiveDocument.ActiveObject.ViewObject.Lighting="Two side"
	m_out.ViewObject.ShapeColor=(random.random(),random.random(),random.random())
	

	[pts,tris]=mesh.Mesh.Topology

	filter=np.array([0]*len(pts))

	n=1
	for i,p in enumerate(pts):
		if box.Shape.BoundBox.isInside(p):
			filter[i]=n
			if i % 1000 == 0:
				FreeCAD.Console.PrintMessage(" ** " + str(i))

				tris2=[]
				for t in tris:
					(a,b,c)=t
					if filter[a] and filter[b] and filter[c]:
						tris2.append((filter[a]-1,filter[b]-1,filter[c]-1))

				pts2=[]
				for i,p in enumerate(pts):
					if filter[i]:
						pts2.append(pts[i])
				m_out.Mesh=Mesh.Mesh((pts2,tris2))
				m_out.ViewObject.DisplayMode = u"Flat Lines"
				

				Gui.updateGui()
			n += 1

	tris2=[]
	for t in tris:
		(a,b,c)=t
		if filter[a] and filter[b] and filter[c]:
			tris2.append((filter[a]-1,filter[b]-1,filter[c]-1))

	pts2=[]
	for i,p in enumerate(pts):
		if filter[i]:
			pts2.append(pts[i])

	m_out.Mesh=Mesh.Mesh((pts2,tris2))

def showdialog(title="Fehler",text="Schau in den ReportView fuer mehr Details",detail=None):
	msg = QtGui.QMessageBox()
	msg.setIcon(QtGui.QMessageBox.Warning)
	msg.setText(text)
	msg.setWindowTitle(title)
	if detail<>None:   msg.setDetailedText(detail)
	msg.exec_()


def sayexc(title='Fehler',mess=''):
	exc_type, exc_value, exc_traceback = sys.exc_info()
	ttt=repr(traceback.format_exception(exc_type, exc_value,exc_traceback))
	lls=eval(ttt)
	l=len(lls)
	l2=lls[(l-3):]
	FreeCAD.Console.PrintError(mess + "\n" +"-->  ".join(l2))
	showdialog(title,text=mess,detail="--> ".join(l2))



def run():

	sels=Gui.Selection.getSelection()

	if len(sels)<>2: 
		showdialog("Keine Vorauswahl","Du musst 1. Mesh und 2. Bounding Box auswaehlen" )

	else:
		m=sels[0]
		obj=sels[1]
		m.ViewObject.hide()
		obj.ViewObject.hide()
		commonMesh(m,obj)



if __name__ == '__main__':
	run()
