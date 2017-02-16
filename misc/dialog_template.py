
# dialog template


import PySide
from PySide import  QtGui,QtCore

def run(window):

	anz=int(window.anz.text())
	print anz

	print window.r.isChecked()

	window.r.hide()
	window.hide()


def dialog():

	w=QtGui.QWidget()

	box = QtGui.QVBoxLayout()
	w.setLayout(box)
	w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

	l=QtGui.QLabel("Anzahl" )
	box.addWidget(l)
	w.anz = QtGui.QLineEdit()
	w.anz.setText('3')
	box.addWidget(w.anz)



	w.random=QtGui.QCheckBox("Zufall")
	box.addWidget(w.random)

	w.r=QtGui.QPushButton("run")
	box.addWidget(w.r)
	w.r.pressed.connect(lambda :run(w))

	w.show()
	return w





dialog()
