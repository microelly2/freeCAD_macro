# -*- coding: utf-8 -*-
#-------------------------------------------------
#-- bspline on top of a sketch
#--
#-- microelly 2016 v 0.2
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------
# bspline von poles erzeugen


class PartFeature:
	def __init__(self, obj):
		obj.Proxy = self


class MyBSpline(PartFeature):
	def __init__(self, obj):
		PartFeature.__init__(self, obj)
		obj.addProperty("App::PropertyLink","wire","Wire","")
		obj.addProperty("App::PropertyEnumeration","mode","Wire","").mode=["poles","interpolate","approximate"]

	def recompute(self,fp,pts):
		if fp.mode=="poles":
			sp.buildFromPoles(pts)
		elif fp.mode=="interpolate":
			sp.interpolate(pts)
		elif fp.mode=="approximate":
			sp.approximate(pts)
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

			sp=Part.BSplineCurve()
			sp.increaseDegree(3)

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
		pass



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


a=makeMySpline()
a.wire=App.ActiveDocument.Sketch
