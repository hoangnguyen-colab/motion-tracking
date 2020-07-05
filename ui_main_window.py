from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1080, 500)
        
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.background_sub = QtWidgets.QLabel(Form)
        self.background_sub.setObjectName("image_label_1")
        self.process_vid = QtWidgets.QLabel(Form)
        self.process_vid.setObjectName("image_label_2")
        self.horizontalLayout.addWidget(self.background_sub)
        self.horizontalLayout.addWidget(self.process_vid)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout.setObjectName("verticalLayout")
        self.control_bt = QtWidgets.QPushButton(Form)
        self.control_bt.setObjectName("control_bt")
        self.verticalLayout.addWidget(self.control_bt)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Cam view"))
        self.background_sub.setText(_translate("Form", "Background Subtract"))
        self.process_vid.setText(_translate("Form", "Process Video"))
        self.control_bt.setText(_translate("Form", "Start"))