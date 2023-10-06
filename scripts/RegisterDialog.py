# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RegisterDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RegisterDialog(object):
    def setupUi(self, RegisterDialog):
        RegisterDialog.setObjectName("RegisterDialog")
        RegisterDialog.resize(513, 416)
        self.acc_register_label = QtWidgets.QLabel(RegisterDialog)
        self.acc_register_label.setGeometry(QtCore.QRect(130, 20, 281, 31))
        font = QtGui.QFont()
        font.setFamily("Bodoni MT")
        font.setPointSize(22)
        font.setBold(False)
        font.setUnderline(True)
        font.setWeight(50)
        self.acc_register_label.setFont(font)
        self.acc_register_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.acc_register_label.setObjectName("acc_register_label")
        self.username_label = QtWidgets.QLabel(RegisterDialog)
        self.username_label.setGeometry(QtCore.QRect(50, 70, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(13)
        self.username_label.setFont(font)
        self.username_label.setObjectName("username_label")
        self.username_input_field = QtWidgets.QLineEdit(RegisterDialog)
        self.username_input_field.setGeometry(QtCore.QRect(40, 100, 391, 31))
        font = QtGui.QFont()
        font.setFamily("Bodoni MT")
        font.setPointSize(13)
        self.username_input_field.setFont(font)
        self.username_input_field.setText("")
        self.username_input_field.setObjectName("username_input_field")
        self.password_label = QtWidgets.QLabel(RegisterDialog)
        self.password_label.setGeometry(QtCore.QRect(50, 140, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(13)
        self.password_label.setFont(font)
        self.password_label.setObjectName("password_label")
        self.pwd_input_field = QtWidgets.QLineEdit(RegisterDialog)
        self.pwd_input_field.setGeometry(QtCore.QRect(40, 170, 391, 31))
        font = QtGui.QFont()
        font.setFamily("Bodoni MT")
        font.setPointSize(13)
        self.pwd_input_field.setFont(font)
        self.pwd_input_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pwd_input_field.setObjectName("pwd_input_field")
        self.confirm_pwd_label = QtWidgets.QLabel(RegisterDialog)
        self.confirm_pwd_label.setGeometry(QtCore.QRect(50, 210, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Verdana")
        font.setPointSize(13)
        self.confirm_pwd_label.setFont(font)
        self.confirm_pwd_label.setObjectName("confirm_pwd_label")
        self.confirm_pwd_input_field = QtWidgets.QLineEdit(RegisterDialog)
        self.confirm_pwd_input_field.setGeometry(QtCore.QRect(40, 240, 391, 31))
        font = QtGui.QFont()
        font.setFamily("Bodoni MT")
        font.setPointSize(13)
        self.confirm_pwd_input_field.setFont(font)
        self.confirm_pwd_input_field.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_pwd_input_field.setObjectName("confirm_pwd_input_field")
        self.register_button = QtWidgets.QPushButton(RegisterDialog)
        self.register_button.setGeometry(QtCore.QRect(80, 320, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Bookman Old Style")
        font.setPointSize(12)
        self.register_button.setFont(font)
        self.register_button.setObjectName("register_button")
        self.cancel_button = QtWidgets.QPushButton(RegisterDialog)
        self.cancel_button.setGeometry(QtCore.QRect(290, 320, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Bookman Old Style")
        font.setPointSize(12)
        self.cancel_button.setFont(font)
        self.cancel_button.setObjectName("cancel_button")
        self.username_error_label = QtWidgets.QLabel(RegisterDialog)
        self.username_error_label.setGeometry(QtCore.QRect(160, 70, 341, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.username_error_label.setFont(font)
        self.username_error_label.setStyleSheet("color: red;")
        self.username_error_label.setObjectName("username_error_label")
        self.password_error_label = QtWidgets.QLabel(RegisterDialog)
        self.password_error_label.setGeometry(QtCore.QRect(160, 140, 341, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.password_error_label.setFont(font)
        self.password_error_label.setStyleSheet("color: red;")
        self.password_error_label.setObjectName("password_error_label")
        self.confirm_pwd_error_label = QtWidgets.QLabel(RegisterDialog)
        self.confirm_pwd_error_label.setGeometry(QtCore.QRect(220, 210, 281, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.confirm_pwd_error_label.setFont(font)
        self.confirm_pwd_error_label.setStyleSheet("color: red;")
        self.confirm_pwd_error_label.setObjectName("confirm_pwd_error_label")
        self.pwd_visible_checkbox = QtWidgets.QCheckBox(RegisterDialog)
        self.pwd_visible_checkbox.setGeometry(QtCore.QRect(410, 180, 16, 17))
        self.pwd_visible_checkbox.setObjectName("pwd_visible_checkbox")
        self.confirm_pwd_visible_checkbox = QtWidgets.QCheckBox(RegisterDialog)
        self.confirm_pwd_visible_checkbox.setGeometry(QtCore.QRect(410, 250, 16, 17))
        self.confirm_pwd_visible_checkbox.setObjectName("confirm_pwd_visible_checkbox")

        self.retranslateUi(RegisterDialog)
        QtCore.QMetaObject.connectSlotsByName(RegisterDialog)

    def retranslateUi(self, RegisterDialog):
        _translate = QtCore.QCoreApplication.translate
        RegisterDialog.setWindowTitle(_translate("RegisterDialog", "Registration"))
        self.acc_register_label.setText(_translate("RegisterDialog", "Account Registration"))
        self.username_label.setText(_translate("RegisterDialog", "Username"))
        self.password_label.setText(_translate("RegisterDialog", "Password"))
        self.confirm_pwd_label.setText(_translate("RegisterDialog", "Confirm Password"))
        self.register_button.setText(_translate("RegisterDialog", "Register"))
        self.cancel_button.setText(_translate("RegisterDialog", "Cancel"))
        self.username_error_label.setText(_translate("RegisterDialog", "*username_error_label"))
        self.password_error_label.setText(_translate("RegisterDialog", "*password_error_label"))
        self.confirm_pwd_error_label.setText(_translate("RegisterDialog", "*confirm_pwd_error_label"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RegisterDialog = QtWidgets.QDialog()
    ui = Ui_RegisterDialog()
    ui.setupUi(RegisterDialog)

        # Create an instance of your QDialog
    dialog = RegisterDialog

    # Connect the exit_button click event to close the dialog
    ui.cancel_button.clicked.connect(dialog.close)

    RegisterDialog.show()
    sys.exit(app.exec_())
