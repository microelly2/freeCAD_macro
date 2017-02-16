# -*- coding: utf-8 -*-
#-------------------------------------------------
#--
#-- edge to Draft Bspline
#--
#-- microelly 2016 v 0.1
#--
#-- GNU Lesser General Public License (LGPL)
#-------------------------------------------------

import Draft
import FreeCADGui,FreeCAD

def run():
	e=FreeCADGui.Selection.getSelection()[0]

	pts=e.Shape.Edge1.Curve.discretize(20)
	Draft.makeBSpline(pts)
	FreeCAD.ActiveDocument.ActiveObject.Label="BSpline for " + e.Label
	e.ViewObject.hide()
