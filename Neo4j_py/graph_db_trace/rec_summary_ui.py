# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 're_summary_ui.ui'
#
# Created: Tue Jan 30 11:09:52 2018
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui, Qt

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(600, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))

        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_qry = QtGui.QLabel(self.centralwidget)
        self.label_qry.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_qry)
        self.lineEdit_query = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_query.setObjectName(_fromUtf8("lineEdit_2"))
        self.horizontalLayout.addWidget(self.lineEdit_query)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem = QtGui.QSpacerItem(138, 20, QtGui.QSizePolicy.Expanding,
                                       QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)

        self.rgd_chk_box = QtGui.QCheckBox(self.centralwidget)
        self.rgd_chk_box.setObjectName(_fromUtf8("lbl_loctn"))
        self.horizontalLayout_4.addWidget(self.rgd_chk_box)

        self.chkbl_ComboBox = CheckableComboBox()
        self.horizontalLayout_4.addWidget(self.chkbl_ComboBox)

        self.chkbl_objtype_ComboBox = CheckableObjComboBox()
        self.horizontalLayout_4.addWidget(self.chkbl_objtype_ComboBox)

        # Export location.....
        # self.lbl_loctn = QtGui.QLabel(self.centralwidget)
        # self.lbl_loctn.setObjectName(_fromUtf8("lbl_loctn"))
        # self.horizontalLayout_4.addWidget(self.lbl_loctn)
        # self.lne_edit_loctn = QtGui.QLineEdit(self.centralwidget)
        # self.lne_edit_loctn.setObjectName(_fromUtf8("lne_edit_loctn"))
        # self.horizontalLayout_4.addWidget(self.lne_edit_loctn)
        # self.tool_btn_loctn = QtGui.QToolButton(self.centralwidget)
        # self.tool_btn_loctn.setObjectName(_fromUtf8("tool_btn_loctn"))
        # self.horizontalLayout_4.addWidget(self.tool_btn_loctn)

        self.pushButton_export = QtGui.QPushButton(self.centralwidget)
        self.pushButton_export.setObjectName(_fromUtf8("pushButton_export"))
        self.horizontalLayout_4.addWidget(self.pushButton_export)
        self.pushButton_interpret = QtGui.QPushButton(self.centralwidget)
        self.pushButton_interpret.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_4.addWidget(self.pushButton_interpret)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_5.addWidget(self.label_4)
        self.rec_lst_wdgt = QtGui.QListWidget(self.centralwidget)
        self.rec_lst_wdgt.setObjectName(_fromUtf8("listWidget"))
        self.horizontalLayout_5.addWidget(self.rec_lst_wdgt)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.lineEdit_recname = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_recname.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout_3.addWidget(self.lineEdit_recname)
        # self.verticalLayout.addLayout(self.horizontalLayout_3)

        # spacerItem = QtGui.QSpacerItem(138, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        # self.horizontalLayout_3.addItem(spacerItem)
        self.pushButton_fetch = QtGui.QPushButton(self.centralwidget)
        self.pushButton_fetch.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_3.addWidget(self.pushButton_fetch)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.summ_txt_edt = QtGui.QTextEdit(self.centralwidget)
        self.summ_txt_edt.setObjectName(_fromUtf8("textEdit"))
        self.horizontalLayout_2.addWidget(self.summ_txt_edt)
        self.verticalLayout.addLayout(self.horizontalLayout_2)



        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 490, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "CREST", None))
        self.label.setText(_translate("MainWindow", "Recording Name: ", None))
        self.rgd_chk_box.setText(_translate("MainWindow", "Rigid ", None))
        # self.lbl_loctn.setText(_translate("MainWindow", "Export location : ", None))

        self.pushButton_fetch.setText(_translate("MainWindow", "Fetch", None))
        self.pushButton_export.setText(_translate("MainWindow", "Export", None))
        self.pushButton_interpret.setText(_translate("MainWindow", "Interpret", None))
        self.label_2.setText(_translate("MainWindow", "Output Summary: ", None))
        self.label_qry.setText(_translate("MainWindow", "Query: ", None))
        self.label_4.setText(_translate("MainWindow", "Result: ", None))

class CheckableComboBox(QtGui.QComboBox):
    def __init__(self):
        super(CheckableComboBox, self).__init__()
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QtGui.QStandardItemModel(self))

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)

    def flags(self, index):

        return Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled

class CheckableObjComboBox(QtGui.QComboBox):
    def __init__(self):
        super(CheckableObjComboBox, self).__init__()
        self.view().pressed.connect(self.handleItemPressed)
        self.setModel(QtGui.QStandardItemModel(self))

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)

    def flags(self, index):

        return Qt.ItemIsUserCheckable | Qt.ItemIsSelectable | Qt.ItemIsEnabled


# if __name__ == "__main__":
#     import sys
#     app = QtGui.QApplication(sys.argv)
#     MainWindow = QtGui.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())

