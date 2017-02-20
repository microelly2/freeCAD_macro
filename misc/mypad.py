# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- offset on faces
#--
#-- microelly 2017 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import Part
import FreeCADGui as Gui
import FreeCAD as App
import random

import PySide
from PySide import  QtGui,QtCore


def _run(window):

	d1=int(window.d1.text())
	d2=int(window.d2.text())
	d3=int(window.d3.text())
	do=int(window.do.text())

	print  Gui.Selection.getSelectionEx()
	for ss in Gui.Selection.getSelectionEx():

		for i,ns in enumerate(ss.SubElementNames):
			f=ss.SubObjects[i]
			n= ns + "@"+ 	ss.Object.Label
			print n

			if window.ceo.isChecked():

				of=f.makeOffsetShape(d1,0.1,fill=True)
				Part.show(of)
				App.ActiveDocument.ActiveObject.Label="exact Pad " +n
				App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(random.random(),random.random(),random.random())


			if window.coo.isChecked():
				aa=f.makeOffset2D(do)
				ofaa=aa.makeOffsetShape(d2,0.1,fill=True)
				Part.show(ofaa)
				App.ActiveDocument.ActiveObject.Label="outer Pad " + n
				App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(random.random(),random.random(),random.random())

			if window.cio.isChecked():

				aa=f.makeOffset2D(-do)
				ofaa=aa.makeOffsetShape(d3,0.1,fill=True)
				Part.show(ofaa)
				App.ActiveDocument.ActiveObject.Label="inner Pad " + n
				App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(random.random(),random.random(),random.random())




	#window.r.hide()
	#window.hide()


def run():

	w=QtGui.QWidget()

	box = QtGui.QVBoxLayout()
	w.setLayout(box)
	w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

	w.ceo=QtGui.QCheckBox("Exact Offset")
	box.addWidget(w.ceo)

	l=QtGui.QLabel("exact Offset Height" )
	box.addWidget(l)
	w.d1 = QtGui.QLineEdit()
	w.d1.setText('8')
	box.addWidget(w.d1)

	l=QtGui.QLabel("Offset Value" )
	box.addWidget(l)
	w.do = QtGui.QLineEdit()
	w.do.setText('1')
	box.addWidget(w.do)

	w.coo=QtGui.QCheckBox("Outer Offset")
	box.addWidget(w.coo)

	l=QtGui.QLabel("outer Offset Height" )
	box.addWidget(l)
	w.d2 = QtGui.QLineEdit()
	w.d2.setText('3')
	box.addWidget(w.d2)

	w.cio=QtGui.QCheckBox("Inner Offset")
	box.addWidget(w.cio)

	l=QtGui.QLabel("inner Offset Height" )
	box.addWidget(l)
	w.d3 = QtGui.QLineEdit()
	w.d3.setText('8')
	box.addWidget(w.d3)

	w.r=QtGui.QPushButton("run")
	box.addWidget(w.r)
	w.r.pressed.connect(lambda :_run(w))

	w.show()
	return w

