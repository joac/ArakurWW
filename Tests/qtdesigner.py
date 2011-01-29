# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtdesigner.ui'
#
# Created: Sat Sep 11 23:36:27 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MplMainWindow(object):
    def setupUi(self, MplMainWindow):
        MplMainWindow.setObjectName("MplMainWindow")
        MplMainWindow.resize(800, 600)
        self.mplcentralwidget = QtGui.QWidget(MplMainWindow)
        self.mplcentralwidget.setObjectName("mplcentralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.mplcentralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mplhorizontalLayout = QtGui.QHBoxLayout()
        self.mplhorizontalLayout.setObjectName("mplhorizontalLayout")
        self.mpllineEdit = QtGui.QLineEdit(self.mplcentralwidget)
        self.mpllineEdit.setObjectName("mpllineEdit")
        self.mplhorizontalLayout.addWidget(self.mpllineEdit)
        self.mplpushButton = QtGui.QPushButton(self.mplcentralwidget)
        self.mplpushButton.setObjectName("mplpushButton")
        self.mplhorizontalLayout.addWidget(self.mplpushButton)
        self.verticalLayout.addLayout(self.mplhorizontalLayout)
        self.mpl = MplWidget(self.mplcentralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mpl.sizePolicy().hasHeightForWidth())
        self.mpl.setSizePolicy(sizePolicy)
        self.mpl.setObjectName("mpl")
        self.verticalLayout.addWidget(self.mpl)
        MplMainWindow.setCentralWidget(self.mplcentralwidget)
        self.mplmenubar = QtGui.QMenuBar(MplMainWindow)
        self.mplmenubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.mplmenubar.setObjectName("mplmenubar")
        self.mplmenuFile = QtGui.QMenu(self.mplmenubar)
        self.mplmenuFile.setObjectName("mplmenuFile")
        MplMainWindow.setMenuBar(self.mplmenubar)
        self.mplactionOpen = QtGui.QAction(MplMainWindow)
        self.mplactionOpen.setObjectName("mplactionOpen")
        self.mplactionQuit = QtGui.QAction(MplMainWindow)
        self.mplactionQuit.setObjectName("mplactionQuit")
        self.mplmenuFile.addAction(self.mplactionOpen)
        self.mplmenuFile.addSeparator()
        self.mplmenuFile.addAction(self.mplactionQuit)
        self.mplmenubar.addAction(self.mplmenuFile.menuAction())

        self.retranslateUi(MplMainWindow)
        QtCore.QMetaObject.connectSlotsByName(MplMainWindow)

    def retranslateUi(self, MplMainWindow):
        MplMainWindow.setWindowTitle(QtGui.QApplication.translate("MplMainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.mplpushButton.setText(QtGui.QApplication.translate("MplMainWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.mplmenuFile.setTitle(QtGui.QApplication.translate("MplMainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.mplactionOpen.setText(QtGui.QApplication.translate("MplMainWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.mplactionQuit.setText(QtGui.QApplication.translate("MplMainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))

from mplwidget import MplWidget
