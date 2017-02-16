import Part
import FreeCADGui as Gui
import FreeCAD as App
import random

def run():
	ss=Gui.Selection.getSelectionEx()[0]
	f=ss.SubObjects[0]
	n=ss.SubElementNames[0] + "@"+ 	ss.Object.Label

	
	of=f.makeOffsetShape(5,0.1,fill=True)
	Part.show(of)
	App.ActiveDocument.ActiveObject.Label="exact Pad " +n
	App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(random.random(),random.random(),random.random())

	if 1:
		aa=f.makeOffset2D(1)
		ofaa=aa.makeOffsetShape(3,0.1,fill=True)
		Part.show(ofaa)
		App.ActiveDocument.ActiveObject.Label="outer Pad " + n
		App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(random.random(),random.random(),random.random())


		aa=f.makeOffset2D(-1)
		ofaa=aa.makeOffsetShape(8,0.1,fill=True)
		Part.show(ofaa)
		App.ActiveDocument.ActiveObject.Label="inner Pad " + n
		App.ActiveDocument.ActiveObject.ViewObject.ShapeColor=(random.random(),random.random(),random.random())
