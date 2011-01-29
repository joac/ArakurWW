from __future__ import with_statement

import numpy as np

import sys

from PyQt4 import QtCore
from PyQt4 import QtGui
from qtdesigner import Ui_MplMainWindow
import string

class DesignerMainWindow(QtGui.QMainWindow, Ui_MplMainWindow):
    def  __init__(self, parent = None):
        super(DesignerMainWindow, self).__init__(parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.mplpushButton, QtCore.
                    SIGNAL("clicked()"), self.update_graph)
        QtCore.QObject.connect(self.mplactionOpen, QtCore.
                    SIGNAL('triggered()'), self.select_file)
        QtCore.QObject.connect(self.mplactionQuit, QtCore.
                    SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT("quit()"))
    def select_file(self):
        file = QtGui.QFileDialog.getOpenFileName()
        if file:
            self.mpllineEdit.setText(file)
    def parse_file(self, filename):
        letters = {}
        for i in set(string.letters.lower()):
            letters[i] = 0
        
        with open(filename) as f:
            for line in f:
                for char in line:
                    char = char.lower()
                    if char in letters:
                        letters[char] += 1
        k = sorted(letters.keys())
        v = [letters[ki] for ki in k]
        return k, v
    
    def update_graph(self):
        l, v = self.parse_file(self.mpllineEdit.text())
        self.mpl.canvas.ax.clear()
        self.mpl.canvas.ax.bar(np.arange(len(l))-0.25, v, width=0.5)
        self.mpl.canvas.ax.set_xlim(xmin=-0.25, xmax=len(l)-0.75)
        self.mpl.canvas.ax.set_xticks(range(len(l)))
        self.mpl.canvas.ax.set_xticklabels(l)
        self.mpl.canvas.ax.get_yaxis().grid(True)
        self.mpl.canvas.draw()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    dmw = DesignerMainWindow()
    dmw.show()
    sys.exit(app.exec_())
