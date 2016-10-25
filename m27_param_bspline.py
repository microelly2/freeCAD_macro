# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- bspline on top of a sketch
#--
#-- microelly 2016 v 0.3
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------
# bspline von poles erzeugen

def printinfo(sp):
		print sp.Degree
		print sp.Continuity
		print len(sp.getPoles())
		print sp.KnotSequence
		print sp.getWeights()


class PartFeature:
	def __init__(self, obj):
		obj.Proxy = self


class MyBSpline(PartFeature):
	def __init__(self, obj):
		PartFeature.__init__(self, obj)
		obj.addProperty("App::PropertyLink","wire","Wire","")
		obj.addProperty("App::PropertyEnumeration","mode","Wire","").mode=["poles","interpolate","approximate"]
		obj.addProperty("App::PropertyEnumeration","paramtype","Wire","")
		obj.paramtype=['Default','Centripetal','Uniform','ChordLength']

	def recompute(self,fp,pts):
		sp=Part.BSplineCurve()
		sp.increaseDegree(3)
		if fp.mode=="poles":
			sp.buildFromPoles(pts)
		elif fp.mode=="interpolate":
			sp.interpolate(pts)
		elif fp.mode=="approximate":
			paramtype=fp.paramtype
			if paramtype<>'Default':
				sp.approximate(Points=pts,ParamType=paramtype,DegMax=3)
			else:
				sp.approximate(pts)
		printinfo(sp)
		return sp


	def onChanged(self, fp, prop):
		if prop=="wire" and fp.wire <> None:
			w=fp.wire
			eds=Part.__sortEdges__(w.Shape.Edges)
			pts=[]
			for e in eds:
				ees=e.discretize(2)
				pts += ees[0:-1]

			pts.append(ees[-1])

			sp=self.recompute(fp,pts)
			fp.Shape=sp.toShape()

	def execute(self, fp):
		if  fp.wire <> None:
			w=fp.wire
			eds=Part.__sortEdges__(w.Shape.Edges)
			pts=[]
			for e in eds:
				ees=e.discretize(2)
				pts += ees[0:-1]

			pts.append(ees[-1])

			sp=self.recompute(fp,pts)

			fp.Shape=sp.toShape()



class ViewProviderMyBSpline:
	def __init__(self, obj):
		obj.Proxy = self
		self.Object=obj

def makeMySpline():

	a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython","MySpline")
	MyBSpline(a)
	ViewProviderMyBSpline(a.ViewObject)
	a.ViewObject.LineColor=(1.00,.00,.00)
	a.ViewObject.LineWidth=1
	return a



# testcase

App.newDocument("Unbenannt")
App.setActiveDocument("Unbenannt")
App.ActiveDocument=App.getDocument("Unbenannt")
Gui.ActiveDocument=Gui.getDocument("Unbenannt")


App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
App.activeDocument().Sketch.Support = (App.activeDocument().XY_Plane, [''])
App.activeDocument().Sketch.MapMode = 'FlatFace'
App.ActiveDocument.recompute()
App.activeDocument().Body.addFeature(App.activeDocument().Sketch)

App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(-182.677419,-87.745679,0),App.Vector(-114.598880,242.057054,0)),False)
App.ActiveDocument.recompute()
App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(-114.598880,242.057054,0),App.Vector(-73.751759,156.580633,0)),False)
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
App.ActiveDocument.recompute()
App.ActiveDocument.recompute()
App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(-73.751759,156.580633,0),App.Vector(-23.827494,266.262755,0)),False)
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
App.ActiveDocument.recompute()
App.ActiveDocument.recompute()
App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(-23.827494,266.262755,0),App.Vector(138.048147,-98.335679,0)),False)
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
App.ActiveDocument.recompute()
App.ActiveDocument.recompute()
App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(138.048147,-98.335679,0),App.Vector(149.394594,-25.718566,0)),False)
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1)) 
App.ActiveDocument.recompute()
App.ActiveDocument.recompute()
App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(149.394594,-25.718566,0),App.Vector(169.061703,-47.654972,0)),False)
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',4,2,5,1)) 
App.ActiveDocument.recompute()
App.ActiveDocument.recompute()
App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(169.061703,-47.654972,0),App.Vector(212.934544,88.502125,0)),False)
App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',5,2,6,1)) 
App.ActiveDocument.recompute()
App.ActiveDocument.recompute()
Gui.getDocument('Unbenannt').resetEdit()
ActiveSketch = App.ActiveDocument.getObject('Sketch')

a=makeMySpline()
a.wire=App.ActiveDocument.Sketch
a.mode="approximate"
