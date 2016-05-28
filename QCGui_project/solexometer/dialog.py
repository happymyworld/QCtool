# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/mtruglio/Desktop/Solexometer/QCGui_project/solexometer/QC_dialog/dialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(660, 448)
        self.gridLayout_2 = QtGui.QGridLayout(Dialog)
        self.gridLayout_2.setMargin(11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setMargin(10)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.scrollArea = QtGui.QScrollArea(Dialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 618, 376))
        self.scrollAreaWidgetContents.setStyleSheet(_fromUtf8("font: 12pt \"Sans Serif\";"))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.gridLayout_3 = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setMargin(11)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 2)
        self.dial_ok = QtGui.QPushButton(Dialog)
        self.dial_ok.setObjectName(_fromUtf8("dial_ok"))
        self.gridLayout_2.addWidget(self.dial_ok, 1, 1, 1, 1)
        self.dial_cancel = QtGui.QPushButton(Dialog)
        self.dial_cancel.setObjectName(_fromUtf8("dial_cancel"))
        self.gridLayout_2.addWidget(self.dial_cancel, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Pipeline setup", None))
        self.dial_ok.setText(_translate("Dialog", "Ok", None))
        self.dial_cancel.setText(_translate("Dialog", "Cancel", None))

