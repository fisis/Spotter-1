# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tab_blindspotUi.ui'
#
# Created: Tue May 15 16:08:01 2018
#      by: PyQt4 UI code generator 4.10
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

class Ui_tab_regions(object):
    def setupUi(self, tab_regions):
        tab_regions.setObjectName(_fromUtf8("tab_regions"))
        tab_regions.resize(447, 448)
        self.gridLayout = QtGui.QGridLayout(tab_regions)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setSpacing(1)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.toolBox = QtGui.QToolBox(tab_regions)
        self.toolBox.setFrameShape(QtGui.QFrame.NoFrame)
        self.toolBox.setFrameShadow(QtGui.QFrame.Plain)
        self.toolBox.setLineWidth(0)
        self.toolBox.setObjectName(_fromUtf8("toolBox"))
        self.page_regions_overview = QtGui.QWidget()
        self.page_regions_overview.setGeometry(QtCore.QRect(0, 0, 445, 404))
        self.page_regions_overview.setObjectName(_fromUtf8("page_regions_overview"))
        self.gridLayout_6 = QtGui.QGridLayout(self.page_regions_overview)
        self.gridLayout_6.setMargin(0)
        self.gridLayout_6.setSpacing(0)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.label = QtGui.QLabel(self.page_regions_overview)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_5.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout_10 = QtGui.QGridLayout()
        self.gridLayout_10.setSpacing(0)
        self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btn_remove_shape = QtGui.QPushButton(self.page_regions_overview)
        self.btn_remove_shape.setMinimumSize(QtCore.QSize(30, 0))
        self.btn_remove_shape.setObjectName(_fromUtf8("btn_remove_shape"))
        self.horizontalLayout.addWidget(self.btn_remove_shape)
        self.gridLayout_10.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_10, 24, 0, 1, 2)
        self.radioRect = QtGui.QRadioButton(self.page_regions_overview)
        self.radioRect.setObjectName(_fromUtf8("radioRect"))
        self.gridLayout_5.addWidget(self.radioRect, 8, 0, 1, 1)
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setContentsMargins(3, 0, -1, -1)
        self.gridLayout_3.setHorizontalSpacing(1)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_X = QtGui.QLabel(self.page_regions_overview)
        self.label_X.setObjectName(_fromUtf8("label_X"))
        self.gridLayout_3.addWidget(self.label_X, 0, 0, 1, 1)
        self.spin_X = QtGui.QDoubleSpinBox(self.page_regions_overview)
        self.spin_X.setObjectName(_fromUtf8("spin_X"))
        self.gridLayout_3.addWidget(self.spin_X, 0, 1, 1, 1)
        self.spin_Y = QtGui.QDoubleSpinBox(self.page_regions_overview)
        self.spin_Y.setObjectName(_fromUtf8("spin_Y"))
        self.gridLayout_3.addWidget(self.spin_Y, 1, 1, 1, 1)
        self.label_Y = QtGui.QLabel(self.page_regions_overview)
        self.label_Y.setObjectName(_fromUtf8("label_Y"))
        self.gridLayout_3.addWidget(self.label_Y, 1, 0, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_3, 1, 0, 1, 2)
        self.tree_blindspot_shapes = QtGui.QTreeWidget(self.page_regions_overview)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tree_blindspot_shapes.sizePolicy().hasHeightForWidth())
        self.tree_blindspot_shapes.setSizePolicy(sizePolicy)
        self.tree_blindspot_shapes.setProperty("showDropIndicator", False)
        self.tree_blindspot_shapes.setAlternatingRowColors(True)
        self.tree_blindspot_shapes.setIndentation(0)
        self.tree_blindspot_shapes.setObjectName(_fromUtf8("tree_blindspot_shapes"))
        self.gridLayout_5.addWidget(self.tree_blindspot_shapes, 6, 0, 1, 2)
        self.radioCircle = QtGui.QRadioButton(self.page_regions_overview)
        self.radioCircle.setObjectName(_fromUtf8("radioCircle"))
        self.gridLayout_5.addWidget(self.radioCircle, 8, 1, 1, 1)
        self.radioLine = QtGui.QRadioButton(self.page_regions_overview)
        self.radioLine.setObjectName(_fromUtf8("radioLine"))
        self.gridLayout_5.addWidget(self.radioLine, 23, 0, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.toolBox.addItem(self.page_regions_overview, _fromUtf8(""))
        self.page_regions_IO = QtGui.QWidget()
        self.page_regions_IO.setGeometry(QtCore.QRect(0, 0, 158, 92))
        self.page_regions_IO.setObjectName(_fromUtf8("page_regions_IO"))
        self.gridLayout_7 = QtGui.QGridLayout(self.page_regions_IO)
        self.gridLayout_7.setMargin(0)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.gridLayout_9 = QtGui.QGridLayout()
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.combo_label = QtGui.QComboBox(self.page_regions_IO)
        self.combo_label.setEnabled(False)
        self.combo_label.setEditable(True)
        self.combo_label.setObjectName(_fromUtf8("combo_label"))
        self.gridLayout_9.addWidget(self.combo_label, 0, 1, 1, 2)
        self.pushButton_15 = QtGui.QPushButton(self.page_regions_IO)
        self.pushButton_15.setEnabled(False)
        self.pushButton_15.setObjectName(_fromUtf8("pushButton_15"))
        self.gridLayout_9.addWidget(self.pushButton_15, 1, 1, 1, 1)
        self.pushButton_14 = QtGui.QPushButton(self.page_regions_IO)
        self.pushButton_14.setEnabled(False)
        self.pushButton_14.setObjectName(_fromUtf8("pushButton_14"))
        self.gridLayout_9.addWidget(self.pushButton_14, 2, 1, 1, 1)
        self.pushButton_13 = QtGui.QPushButton(self.page_regions_IO)
        self.pushButton_13.setEnabled(False)
        self.pushButton_13.setObjectName(_fromUtf8("pushButton_13"))
        self.gridLayout_9.addWidget(self.pushButton_13, 2, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_9.addItem(spacerItem, 3, 1, 2, 2)
        self.pushButton_12 = QtGui.QPushButton(self.page_regions_IO)
        self.pushButton_12.setEnabled(False)
        self.pushButton_12.setObjectName(_fromUtf8("pushButton_12"))
        self.gridLayout_9.addWidget(self.pushButton_12, 1, 2, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_9, 0, 2, 1, 1)
        self.toolBox.addItem(self.page_regions_IO, _fromUtf8(""))
        self.gridLayout_2.addWidget(self.toolBox, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.retranslateUi(tab_regions)
        self.toolBox.setCurrentIndex(0)
        self.toolBox.layout().setSpacing(0)
        QtCore.QMetaObject.connectSlotsByName(tab_regions)

    def retranslateUi(self, tab_regions):
        tab_regions.setWindowTitle(_translate("tab_regions", "Form", None))
        self.label.setText(_translate("tab_regions", "Areas to be ignored", None))
        self.btn_remove_shape.setText(_translate("tab_regions", "&Remove", None))
        self.radioRect.setText(_translate("tab_regions", "Rectangle", None))
        self.label_X.setText(_translate("tab_regions", "X", None))
        self.label_Y.setText(_translate("tab_regions", "Y", None))
        self.tree_blindspot_shapes.headerItem().setText(0, _translate("tab_regions", "Shapes", None))
        self.radioCircle.setText(_translate("tab_regions", "Circle", None))
        self.radioLine.setText(_translate("tab_regions", "Line", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_regions_overview), _translate("tab_regions", "Shapes", None))
        self.pushButton_15.setText(_translate("tab_regions", "Open", None))
        self.pushButton_14.setText(_translate("tab_regions", "Clone", None))
        self.pushButton_13.setText(_translate("tab_regions", "Delete", None))
        self.pushButton_12.setText(_translate("tab_regions", "Save", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_regions_IO), _translate("tab_regions", "In/Out", None))

