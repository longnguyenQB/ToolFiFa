# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import Auth.icons_rc  # pylint: disable=unused-import
from Auth.customized import PasswordEdit
import machineid
import requests
import hashlib
import sys
import pytz
from datetime import datetime

class Auth:
    def __init__(self) -> None:
        self.job_name = "fifa"
        self.machine_id = str(machineid.hashed_id()) + str(int(hashlib.sha256(self.job_name.encode('utf-8')).hexdigest(), 16) % 10**8)
        self.payload = {'machine_id': self.machine_id, 'job_name': self.job_name}
        
        
        self.BASE_URL = 'https://nguyenlongqblt.pythonanywhere.com'

        # Tạo một đối tượng Session để lưu cookie
        self.session = requests.Session()
        # Định nghĩa url của trang đăng nhập và trang thêm sản phẩm
        login_url = 'https://nguyenlongqblt.pythonanywhere.com/login'

        # Định nghĩa thông tin đăng nhập
        login_data = {
            'username': 'nguyenlongqbtt',
            'password': 'longqblt123'
        }

        # Gửi yêu cầu POST đến trang đăng nhập với thông tin đăng nhập
        self.response = self.session.post(login_url, data=login_data)

    def get_machineid(self):
        if self.response.status_code == 200:
            url = self.BASE_URL + "/add"
            product_data = {
                            'name': '',
                            'category': 'fifa',
                            'code': self.machine_id
                            }
            response = self.session.post(url, data=product_data)
            # Kiểm tra xem yêu cầu có thành công không
            if response.status_code == 200:
                # In ra thông báo thành công
                print('Thêm thông tin key thành công')
            else:
                # In ra thông báo lỗi
                print('Thêm thông tin key thất bại')
        else:
            print('Đăng nhập thất bại')
    
    def register_machineid(self, username, phonenumber):
        if self.response.status_code == 200:
            url = self.BASE_URL +  "/edit_user"
            
            # Định nghĩa thông tin sản phẩm mới
            product_data = {
                            'name': username + "|" + phonenumber,
                            'category': 'fifa',
                            'code': self.machine_id,
                            'created_at': '2023-12-05',
                            'expired_at': '2023-12-15',
                            'status': 'Đã kích hoạt!'
                            }

            # Gửi yêu cầu POST đến trang chỉnh sửa thông tin sản phẩm với thông tin sản phẩm mới
            response = self.session.post(url, params=product_data)

            # Kiểm tra xem yêu cầu có thành công không
            if response.status_code == 200:
                # In ra thông báo thành công
                print('Chỉnh sửa thông tin sản phẩm thành công')
            else:
                # In ra thông báo lỗi
                print('Chỉnh sửa thông tin sản phẩm thất bại')
    
    def check_machineind(self):
        if self.response.status_code == 200:
            url = self.BASE_URL + "/get_product"
            params = {
                        'code': self.machine_id
                    }
            response = self.session.get(url, params=params)
            # Kiểm tra xem yêu cầu có thành công không
            if response.status_code == 200:
                # Lấy nội dung trả về dưới dạng json
                data = response.json()
                # Lấy thông tin sản phẩm từ json
                product = data.get('product')
                # Nếu có thông tin sản phẩm
                if product:
                    expired = datetime.strptime(product["expired_at"].replace(",", ""), '%a %d %b %Y %H:%M:%S %Z') - datetime.strptime(datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
                    return {'expired' : expired.days, 'status' : product["status"] }
                else:
                    return {'expired' : -9999, 'status' : "Chưa kích hoạt!"}
        
    
class LoginForm(QtWidgets.QWidget):
    """Basic login form.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setup_ui()
        

    def setup_ui(self):
        """Setup the login form.
        """
        self.authentication = Auth()
        self.authentication.get_machineid()
        
        self.resize(480, 600)
        # remove the title bar
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.setStyleSheet(
            """
            QPushButton {
                border-style: outset;
                border-radius: 0px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #cf7500;
                border-style: inset;
            }
            QPushButton:pressed {
                background-color: #ffa126;
                border-style: inset;
            }
            """
        )

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()

        self.widget = QtWidgets.QWidget(self)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget.setStyleSheet(".QWidget{background-color: rgb(20, 20, 40);}")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(9, 0, 0, 0)

        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setMinimumSize(QtCore.QSize(35, 25))
        self.pushButton_3.setMaximumSize(QtCore.QSize(35, 25))
        self.pushButton_3.setStyleSheet("color: white;\n"
                                        "font: 13pt \"Verdana\";\n"
                                        "border-radius: 1px;\n"
                                        "opacity: 200;\n")
        self.pushButton_3.clicked.connect(self.close)
        self.verticalLayout_2.addWidget(self.pushButton_3, 0, QtCore.Qt.AlignRight)

        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 15, -1, -1)

        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMinimumSize(QtCore.QSize(100, 150))
        self.label.setMaximumSize(QtCore.QSize(150, 150))
        self.label.setStyleSheet("image: url(./Auth/icons/logo.png);")
        self.verticalLayout_3.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)

        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setContentsMargins(50, 35, 59, -1)

        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setStyleSheet("color: rgb(231, 231, 231);\n"
                                   "font: 15pt \"Verdana\";")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)

        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit.setStyleSheet("QLineEdit {\n"
                                    "color: rgb(231, 231, 231);\n"
                                    "font: 15pt \"Verdana\";\n"
                                    "border: None;\n"
                                    "border-bottom-color: white;\n"
                                    "border-radius: 10px;\n"
                                    "padding: 0 8px;\n"
                                    "background: rgb(20, 20, 40);\n"
                                    "selection-background-color: darkgray;\n"
                                    "}")
        self.lineEdit.setFocus(True)
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)

        self.label_4 = QtWidgets.QLabel(self.widget)
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        pixmap = QPixmap('./Auth/icons/phone_32x32.png')
        self.label_4.setPixmap(pixmap)

        self.label_3 = QtWidgets.QLabel(self.widget)
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)

        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit_3.setStyleSheet("QLineEdit {\n"
                                      "color: rgb(231, 231, 231);\n"
                                      "font: 15pt \"Verdana\";\n"
                                      "border: None;\n"
                                      "border-bottom-color: white;\n"
                                      "border-radius: 10px;\n"
                                      "padding: 0 8px;\n"
                                      "background: rgb(20, 20, 40);\n"
                                      "selection-background-color: darkgray;\n"
                                      "}")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_3)

        self.lineEdit_2 = PasswordEdit(self.widget)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(0, 40))
        self.lineEdit_2.setStyleSheet("QLineEdit {\n"
                                      "color: orange;\n"
                                      "font: 15pt \"Verdana\";\n"
                                      "border: None;\n"
                                      "border-bottom-color: white;\n"
                                      "border-radius: 10px;\n"
                                      "padding: 0 8px;\n"
                                      "background: rgb(20, 20, 40);\n"
                                      "selection-background-color: darkgray;\n"
                                      "}")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)

        self.line = QtWidgets.QFrame(self.widget)
        self.line.setStyleSheet("border: 2px solid white;")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.line)

        self.line_3 = QtWidgets.QFrame(self.widget)
        self.line_3.setStyleSheet("border: 2px solid white;")
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.line_3)

        self.line_2 = QtWidgets.QFrame(self.widget)
        self.line_2.setStyleSheet("border: 2px solid orange;")
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.line_2)

        self.pushButton = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())

        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 60))
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setStyleSheet("color: rgb(231, 231, 231);\n"
                                      "font: 17pt \"Verdana\";\n"
                                      "border: 2px solid orange;\n"
                                      "padding: 5px;\n"
                                      "border-radius: 3px;\n"
                                      "opacity: 200;\n"
                                      "")
        self.pushButton.setAutoDefault(True)
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.SpanningRole, self.pushButton)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_2.setItem(6, QtWidgets.QFormLayout.SpanningRole, spacerItem)
        self.verticalLayout_3.addLayout(self.formLayout_2)

        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)

        self.horizontalLayout_3.addWidget(self.widget)
        self.horizontalLayout_3.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        
        # Connect
        self.pushButton.clicked.connect(self.auth)
        self.wrong = 0 
        
    def auth(self):
        print(self.lineEdit_3.text(), self.lineEdit.text(), self.lineEdit_2.text()
        )
        if self.wrong < 5:
            if (self.lineEdit.text() == '') | (self.lineEdit_3.text() == ''):
                self.show_warning_messagebox("Vui lòng nhập đủ thông tin!")
            elif self.lineEdit_2.text() == self.authentication.machine_id:
                self.authentication.register_machineid(username=self.lineEdit.text(),
                                                    phonenumber=self.lineEdit_3.text())
                self.show_warning_messagebox("Kích hoạt thành công, hãy vào lại tool!")
                self.close()
            else:
                self.wrong +=1
                self.show_warning_messagebox("Nhập sai key, quá 5 lần folder sẽ tự xóa!")
        else:
            self.show_warning_messagebox("Nhập sai key, quá 5 lần folder sẽ tự xóa!")
            self.close()
    
    def show_warning_messagebox(self, mess):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    
        # setting message for Message Box
        msg.setText(mess)
        
        # declaring buttons on Message Box
        msg.setStandardButtons(QMessageBox.Ok)
        
        # start the app
        retval = msg.exec_()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_3.setText(_translate("Form", "X"))
        self.label_2.setText(_translate(
            "Form",
            "<html><head/><body><p><img src=\":/icons/icons/user_32x32.png\"/></p></body></html>"))
        self.label_3.setText(_translate(
            "Form",
            "<html><head/><body><p><img src=\":/icons/icons/lock_or_32x32.png\"/></p></body></html>"))
        # self.label_4.setText(_translate(
        #     "Form",
        #     "<html><head/><body><p><img src=\":/icons/icons/mail_32x32.png\"/></p></body></html>"))
        self.pushButton.setText(_translate("Form", "Đăng nhập"))

def bullshit():
    authentication = Auth()
    response = authentication.check_machineind()
    print("response:  ", response)
    if (response['expired'] >=0) & (response['status'] == 'Đã kích hoạt!'):
        return response['expired']
    else:
        app = QtWidgets.QApplication(sys.argv)
        login_form = LoginForm()
        login_form.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    

    app = QtWidgets.QApplication(sys.argv)
    login_form = LoginForm()
    login_form.show()

    sys.exit(app.exec_())