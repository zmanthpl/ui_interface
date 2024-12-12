# 在...处填写代码，可以添加函数
import pandas as pd
import sys
from PyQt5.QtWidgets import QTextEdit, QComboBox, QDialog, QHBoxLayout, QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QDesktopWidget, QFormLayout # type: ignore
from PyQt5.QtGui import QIcon # type: ignore
from PyQt5.QtCore import QTimer, QDate, qDebug
import numpy as np

class prompt_win(QDialog):
    def __init__(self, content, parent=None):  
        super(prompt_win, self).__init__(parent)  
        self.content = content
        self.time_left = 10 
        self.samll_win()

    def samll_win(self):
        self.ok_btn = QPushButton('确定', self)
        if self.content == "禁用":
            self.timer = QTimer(self)  
            self.start_countdown()
            self.timer.timeout.connect(self.update_countdown)  
            # 创建并启动定时器  
        self.setWindowTitle('小窗口') 
        self.resize(100, 50)
        vbox = QVBoxLayout()
        self.label_content = QLabel(self.content, self)
        vbox.addStretch(1)
        vbox.addWidget(self.label_content)
        vbox.addStretch(1)

        self.ok_btn.clicked.connect(self.close)
        vbox.addWidget(self.ok_btn) 
        self.setLayout(vbox)  

    def start_countdown(self):  
        self.ok_btn.setEnabled(False)  # 禁用按钮  
        self.timer.start(1000)  # 每秒更新一次  
  
    def update_countdown(self):  
        self.time_left -= 1  
        self.label_content.setText(f"倒计时: {self.time_left}秒")  
        if self.time_left <= 0:  
            self.timer.stop()  
            self.label_content.setText("倒计时结束！")  
            self.ok_btn.setEnabled(True)  # 倒计时结束，重新启用按钮  

class reg_window(QDialog):
    def __init__(self, address, parent=None):  
        super(reg_window, self).__init__(parent)  
        self.address = address
        self.db = self.data_load()
        self.reg_win()

    def reg_win(self):
        self.resize(400, 300)# 定制widget的大小
        self.setWindowIcon(QIcon("log.jpg"))

        center_pointer =  QDesktopWidget().availableGeometry().center()
        x = center_pointer.x()
        y = center_pointer.y()
        old_x, old_y, width, height = self.frameGeometry().getRect()
        self.move(x-width//2, y-height//2)# 移动到对应位置
        self.setWindowTitle('高考查分') # 设置窗口名称

        vbox = QVBoxLayout()
        # 创建定时器
        self.date_label = QLabel('当前日期: ', self)
        vbox.addWidget(self.date_label)
        self.date_label.setGeometry(0, 0, 200, 20)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_date)
        self.timer.start(1000)  # 每秒更新一次

        self.label_account = QLabel('学号：', self)
        self.edit_account = QLineEdit(self)
        self.edit_account.setPlaceholderText("请输入学号")
        fbox = QFormLayout()

        fbox.addRow(self.label_account, self.edit_account)

        self.label_password = QLabel('密码：', self)
        self.edit_password = QLineEdit(self)
        self.edit_password.setPlaceholderText("请输入密码")

        self.label_password2 = QLabel('再次输入密码：', self)
        self.edit_password2 = QLineEdit(self)
        self.edit_password2.setPlaceholderText("请输入再次输入密码")

        fbox.addRow(self.label_password, self.edit_password)
        fbox.addRow(self.label_password2, self.edit_password2)
        self.reg = QPushButton('注册')
        self.reg.clicked.connect(self.reg_btn_clicked)
        vbox.addStretch(1)
        vbox.addLayout(fbox)
        vbox.addWidget(self.reg)
        vbox.addStretch(3)

        self.setLayout(vbox)


    def update_date(self):
        date = QDate.currentDate()
        self.date_label.setText(f"当前日期: {date.toString()}")  # 更新日期标签的文本
    
    def data_load(self):
        db = pd.read_excel(self.address)
        return db

    def reg_btn_clicked(self):
        db = self.data_load()
        account_list = db['学号'].tolist()
        account = self.edit_account.text()
        password =  self.edit_password.text()
        password2 =  self.edit_password2.text()
        if account and password and password2:
            if account.isdigit() == True:
                account = int(account)
                if account in account_list:
                    matching_row = db[db['学号'] == account]
                    if matching_row.iloc[0]['密码'] != 0:
                        self.edit_account.clear()
                        self.edit_password.clear()
                        self.edit_password2.clear()
                        small_win = prompt_win("账户已存在", self)
                        small_win.exec_()
                    else:
                        if password.isalnum() == True and password2.isalnum() ==True:
                            if password==password2:
                                small_win = prompt_win("账号创建成功", self)
                                small_win.exec_()
                                if isinstance(password,str) and password.isdigit():
                                    password = int(password)
                                db.loc[db['学号'] == account, '密码'] = password
                                db.to_excel(self.address)

                        else:
                            self.edit_password.clear()
                            self.edit_password2.clear()
                            small_win = prompt_win("密码格式不正确", self)
                            small_win.exec_()

                else:
                    self.edit_account.clear()
                    self.edit_password.clear()
                    self.edit_password2.clear()
                    small_win = prompt_win("该学号不存在", self)
                    small_win.exec_()

class QT(QWidget):
    def __init__(self, address):
        super().__init__()
        self.address = address
        self.db = self.data_load()
        self.dict_perfect = {}
        self.dict_max = {}
        self.mis_time = 0
        self.time_left = 10  
        self.LoginUI()
    
    def LoginUI(self):
        self.resize(400, 300)# 定制widget的大小
        self.setWindowIcon(QIcon("log.jpg"))

        center_pointer =  QDesktopWidget().availableGeometry().center()
        x = center_pointer.x()
        y = center_pointer.y()
        old_x, old_y, width, height = self.frameGeometry().getRect()
        self.move(x-width//2, y-height//2)# 移动到对应位置
        self.setWindowTitle('高考查分') # 设置窗口名称

        
        vbox = QVBoxLayout()
        # 创建定时器
        self.date_label = QLabel('当前日期: ', self)
        vbox.addWidget(self.date_label)
        vbox.addStretch(2)
        self.date_label.setGeometry(0, 0, 200, 20)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_date)
        self.timer.start(1000)  # 每秒更新一次

        self.label_account = QLabel('学号：', self)
        self.edit_account = QLineEdit(self)
        self.edit_account.setPlaceholderText("请输入学号")
        fbox = QFormLayout()

        fbox.addRow(self.label_account, self.edit_account)

        self.label_password = QLabel('密码：', self)
        self.edit_password = QLineEdit(self)
        self.edit_password.setPlaceholderText("请输入密码")
        fbox.addRow(self.label_password, self.edit_password)
        hbox = QHBoxLayout()
        
        self.login_btn = QPushButton('登录')
        self.login_btn.clicked.connect(self.login_btn_clicked)
        self.reg = QPushButton('注册')
        self.reg.clicked.connect(self.reg_btn_clicked)
        hbox.addWidget(self.login_btn)
        hbox.addWidget(self.reg)
        fbox.addRow(hbox)
        vbox.addLayout(fbox)
        vbox.addStretch(3)

        self.setLayout(vbox)

        
    def update_countdown(self):  
        self.time_left -= 1 
        if self.time_left <= 0:  
            self.timer.stop()  
            self.login_btn.setEnabled(True)  # 倒计时结束，重新启用按钮 
            self.time_left = 10
            self.mis_time = 0 

    def update_date(self):
        date = QDate.currentDate()
        self.date_label.setText(f"当前日期: {date.toString()}")  # 更新日期标签的文本
    
    def data_load(self):
        db = pd.read_excel(self.address)
        return db

    def reg_btn_clicked(self):
        reg_win = reg_window(self.address, self)
        reg_win.exec_()

    def login_btn_clicked(self):
        if self.mis_time == 5:
            self.login_btn.setEnabled(False)  # 禁用按钮  
            self.timer.timeout.connect(self.update_countdown)  
            small_win = prompt_win("禁用", self)
            small_win.exec_()
        else:
            db = self.data_load()
            account_list = db['学号'].tolist()
            account = self.edit_account.text().replace(" ", "")
            password = self.edit_password.text().replace(" ", "")

            if self.edit_account.text() and self.edit_password.text():
                if account.isdigit() == True and password.isalnum() == True:
                    account = int(account)
                    self.edit_account.clear()
                    self.edit_password.clear()
                    matching_row = db[db['学号'] == account]  
                    if account in account_list and str(matching_row.iloc[0]['密码']) == password:
                        small_win = prompt_win("登录成功", self)
                        small_win.exec_()
                        self.close()
                        main_win= main_window(self.address, self)
                        main_win.exec_()
                    elif account not in account_list:
                        small_win = prompt_win("账号不存在", self)
                        small_win.exec_()
                        self.mis_time +=1
                    elif account in account_list and str(matching_row.iloc[0]['密码']) != password:
                        small_win = prompt_win("密码错误", self)
                        small_win.exec_()
                        self.mis_time +=1
                else:
                    self.edit_account.clear()
                    self.edit_password.clear()
                    small_win = prompt_win("请输入正确格式", self)
                    small_win.exec_()
                    self.mis_time +=1


        
class main_window(QDialog):
    def __init__(self, address, parent=None):
        super(main_window, self).__init__(parent)
        self.address = address
        self.db = self.data_load()
        self.dict_perfect = {}
        self.dict_max = {}
        self.InitUI()

    def InitUI(self):
        self.resize(640, 480)# 定制widget的大小
        self.setWindowIcon(QIcon("log.jpg"))

        center_pointer =  QDesktopWidget().availableGeometry().center()
        x = center_pointer.x()
        y = center_pointer.y()
        old_x, old_y, width, height = self.frameGeometry().getRect()
        self.move(x-width//2, y-height//2)# 移动到对应位置
        self.setWindowTitle('高考查分') # 设置窗口名称

        self.date_label = QLabel('当前日期: ', self)
        self.date_label.setGeometry(0, 0, 200, 20)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_date)
        self.timer.start(1000)  # 每秒更新一次


        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.date_label)

        self.output = QTextEdit("",self)

        self.choose_label = QLabel("请选择你要查询的内容", self)
        self.stn = QPushButton("确定", self)
        self.stn.clicked.connect(self.inquire)

        self.cb = QComboBox()
        self.cb.addItems([" ","学号查询", "姓名查询", "特控人数", "单科状元"])

        self.cb.currentIndexChanged.connect(self.choose_F)

        hbox.addWidget(self.choose_label)
        hbox.addWidget(self.cb)
        
        vbox.addLayout(hbox)
        vbox.addWidget(self.output)
        vbox.addWidget(self.stn)
        vbox.addStretch(3)
        self.setLayout(vbox)


    def data_load(self):
        db = pd.read_excel(self.address)
        return db
    
    def update_date(self):
        date = QDate.currentDate()
        self.date_label.setText(f"当前日期: {date.toString()}")  # 更新日期标签的文本
    
    def score_higher_than_532(self):
        result = self.db[self.db["总分"]>532]
        self.dict_perfect = result.set_index('学号')['总分'].to_dict()
        text = ''  
        for key, value in self.dict_perfect.items():  
            text += f"{key}: {value}\n"
        text +='特控率：%.2f' % (len(result["总分"])/len(self.db["总分"]))
        return text

    def max_score(self):
        text = ''
        for i in self.db.columns[2:-2]:
            self.dict_max[self.db.loc[self.db[i].idxmax(), '学号']] = i + ' ' + str(self.db[i].max())
        for key, value in self.dict_max.items():  
            text += f"{key}: {value}\n"  
         
        return text
    
    def choose_F(self):
        if self.cb.currentText() == "学号查询":  
            self.output.clear()  
            self.output.setText("请输入学号：")
        elif self.cb.currentText() == "姓名查询":  
            self.output.clear()  
            self.output.setText("请输入姓名：")
        elif self.cb.currentText() == "特控人数":
            self.output.clear()  
            self.output.setText(self.score_higher_than_532())
        elif self.cb.currentText() == "单科状元":
            self.output.clear() 
            self.output.setText(self.max_score())

    def inquire(self):
        if self.cb.currentText() == "学号查询": 
            st_num = self.output.toPlainText().strip()[6:]  # 去除可能的空白字符
            text = ''  
            if st_num:  # 检查是否有输入  
                # 假设self.db是一个pandas DataFrame  
                matching_row = self.db[self.db['学号'] == int(st_num)]  
                if not matching_row.empty:  # 检查是否有匹配的行  
                    # 设置学号和姓名的基本信息  
                    text = f"{st_num}: {matching_row.iloc[0]['姓名']}\n"   
                    for i in self.db.columns[2:-1]:  # 注意索引可能需要根据实际情况调整    
                        text += f"{i}:{matching_row.iloc[0][i]}\n"  
                    self.output.setText(text)
                    self.cb.setCurrentIndex(0)
        elif self.cb.currentText() == "姓名查询": 
            name = self.output.toPlainText().strip()[6:]  # 去除可能的空白字符
            text = ''  
            if name:  # 检查是否有输入  
                # 假设self.db是一个pandas DataFrame  
                matching_row = self.db[self.db['姓名'] == name]  
                if not matching_row.empty:  # 检查是否有匹配的行  
                    # 设置学号和姓名的基本信息  
                    text = f"{matching_row.iloc[0]['学号']}: {name}\n"   
                    for i in self.db.columns[2:-1]:  # 注意索引可能需要根据实际情况调整    
                        text += f"{i}:{matching_row.iloc[0][i]}\n"  
                self.output.setText(text)
                self.cb.setCurrentIndex(0)

if __name__ == '__main__':
    address = "04.xlsx"
    # inquire()
    app = QApplication(sys.argv)# 创建app对象
    win = QT(address)
    # win = main_window(address)
    win.show() # 显示widget
    
    # 进入事件循环
    sys.exit(app.exec_())
