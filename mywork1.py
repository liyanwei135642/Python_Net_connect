from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from threading import Thread
from PySide2.QtGui import  QIcon
from socket import *
import random

ip='49.232.135.178'
port=51801
socket_byte_max=1024
data_socket=socket(AF_INET,SOCK_STREAM)
# 登录注册对话框定义：
class main_window:
    def __init__(self):
        self.window=QUiLoader().load("form2.ui")
        self.window.button_add.clicked.connect(self.button_add)
        self.window.button_del.clicked.connect(self.button_del)
        self.window.button_send.clicked.connect(self.button_send)


    def updata_friends(self):
        try:
            data_socket.send("updata_friends---...***".encode())
        except:
            QMessageBox.about(self.window,"错误提示","服务器未启动\n请联系管理员启动服务器")
            exit(-1)

    def button_add(self):
        dialog_add1.add.show()

    def button_del(self):
        try:
            i=self.window.friend_table.currentRow()
            item=self.window.friend_table.item(i,0)
            name=item.text()
        except:
            QMessageBox.about(self.window, "错误提示", "请先选中联系人！")
            return
        try:
            data_socket.send(("del_friend"+"---...***"+name).encode())
        except:
            QMessageBox.about(self.window,"错误提示","服务器中断：\n请联系管理员重新连接！")
            exit(-1)
        while dialog.del_friend:
            if dialog.del_friend=='0':
                dialog.del_friend=True
                QMessageBox.about(window.window, "错误提示", "警告：\n不要删除自己！")
                window.updata_friends()
                return
            elif dialog.del_friend=='1':
                dialog.del_friend=True
                window.updata_friends()
                return

    def button_send(self):
        message=self.window.sendbox.toPlainText().strip()
        try:
            i = self.window.friend_table.currentRow()
            item = self.window.friend_table.item(i, 0)
            name = item.text()
        except:
            QMessageBox.about(self.window, "错误提示", "请先选中联系人！")
            return
        self.window.sendbox.clear()
        item=QListWidgetItem()
        item.setText(f"给{name}发送 ：\n{message}")
        self.window.messagebox.addItem(item)
        try:
            data_socket.send((name+"---...***"+message).encode())
        except:
            QMessageBox.about(self.window,"错误提示","服务器中断：\n请联系管理员重新连接！")
            exit(-1)
        while dialog.send:
            if dialog.send=='0':
                dialog.send=True
                QMessageBox.about(window.window, "错误提示", "对方已下线！")
                window.updata_friends()
                return
            elif dialog.send=='1':
                dialog.send = True
                window.updata_friends()
                return




class dialog_add:
    def __init__(self):
        self.add=QUiLoader().load("form3.ui")
        self.add.button.clicked.connect(self.button_click)

    def button_click(self):
        name = self.add.text.text()
        if len(name)<8:
            QMessageBox.about(self.add,"错误提示","用户名格式错误！\n至少8位字符：")
            self.add.text.clear()
            return
        try:
            data_socket.send(("add_friend---...***"+name).encode())
        except:
            QMessageBox.about(self.add,"错误提示","服务器未启动\n请联系管理员启动服务器！")
            exit(-1)
        while dialog.add:
            if dialog.add=='0':
                dialog.add=True
                QMessageBox.about(dialog_add1.add, "错误提示", "添加联系人不能是自己！\n请重新输入：")
                return
            elif dialog.add=='1':
                dialog.add=True
                QMessageBox.about(dialog_add1.add, "错误提示", "您要添加的联系人不存在！\n请重新输入：")
                return
            elif dialog.add=='2':
                dialog.add=True
                QMessageBox.about(dialog_add1.add, "错误提示", f"您已经添加过联系人{name}！\n请重新输入：")
                return
            elif dialog.add=='3':
                dialog.add=True
                window.updata_friends()
                dialog_add1.add.close()
                return


class dialog_DL:
    def __init__(self):
        self.dialog=QUiLoader().load("form1.ui")
        self.dialog.button_zc.clicked.connect(self.button_ZC)
        self.dialog.button_dl.clicked.connect(self.button_DL)
        self.dialog.username.returnPressed.connect(self.set_cursor)
        self.dialog.password.returnPressed.connect(self.password_press)
        self.thread1 = Thread(target=self.thread_1, daemon=True)
        self.zc=True
        self.dl=True
        self.add=True
        self.del_friend=True
        self.send=True
    def thread_1(self):
        while True:
            try:
                rec = data_socket.recv(socket_byte_max)
            except:
                exit(-1)
            info = rec.decode().split("---...***")
            title = info[0].strip()
            if title == "zc":
                recv = info[1].strip()
                if recv == '0':
                    self.dialog.username.clear()
                    self.dialog.password.focusNextPrevChild(False)
                    self.dialog.username.focusNextPrevChild(False)
                    self.zc='0'
                    continue
                else:
                    self.zc='1'
                    continue
            elif title == "dl":
                recv = info[1].strip()
                if recv == '0':
                    self.dialog.username.clear()
                    self.dialog.password.focusNextPrevChild(False)
                    self.dialog.username.focusNextPrevChild(False)
                    self.dialog.username.focusNextPrevChild(False)
                    self.dl='0'
                    continue
                elif recv == '1':
                    self.dialog.password.clear()
                    self.dialog.username.focusNextPrevChild(False)
                    self.dialog.username.focusNextPrevChild(False)
                    self.dl='1'
                    continue
                else:
                    self.dl='2'
                    continue
            elif title == "updata_friends":
                recv = info[1].strip()
                friends = []
                n = int(recv)
                try:
                    for i in range(n):
                        data_socket.send("1".encode())
                        rec = data_socket.recv(socket_byte_max).decode().split(',')
                        friends.append((rec[0], rec[1]))
                except:
                    exit(-1)
                window.window.friend_table.setRowCount(n)
                for i in range(n):
                    window.window.friend_table.setItem(i, 0, QTableWidgetItem(friends[i][0]))
                    window.window.friend_table.setItem(i, 1, QTableWidgetItem(friends[i][1]))
                continue
            elif title == "add_friend":
                recv=info[1].strip()
                if recv == '0':
                    dialog_add1.add.text.clear()
                    self.add='0'
                    continue
                elif recv == '1':
                    self.add='1'
                    dialog_add1.add.text.clear()
                    continue
                elif recv == '2':
                    self.add='2'
                    dialog_add1.add.text.clear()
                    continue
                else:
                    self.add='3'
                    continue
            elif title == "del_friend":
                recv=info[1].strip()
                if recv == '0':
                    self.del_friend='0'
                else:
                    self.del_friend='1'
                continue
            elif title == "send":
                recv=info[1].strip()
                if recv == '0':
                    self.send='0'
                else:
                    self.send='1'
                continue
            elif title:
                name = title
                message = info[1].strip()
                item = QListWidgetItem()
                item.setText(f"收到{name}来信 :\n{message}")
                window.window.messagebox.addItem(item)
                continue
            else:
                exit(-1)

    def button_ZC(self):
        username=self.dialog.username.text()
        if len(username)<8:
            QMessageBox.about(self.dialog,"错误提示","用户名输入格式错误：\n至少8个字符或文字")
            self.dialog.username.clear()
            self.dialog.username.focusNextPrevChild(False)
            self.dialog.username.focusNextPrevChild(False)
            return
        password=self.dialog.password.text()
        if len(password)<8:
            QMessageBox.about(self.dialog, "错误提示", "密码输入格式错误：\n至少8个字符")
            self.dialog.password.clear()
            self.dialog.username.focusNextPrevChild(False)
            return
        cmd="zc---...***"+username+"---...***"+password
        try:
            data_socket.send(cmd.encode())
        except:
            QMessageBox.about(self.dialog, "错误提示", "服务器未启用\n请联系管理员启动服务器！")
            exit(-1)
        while self.zc:
            if self.zc=='0':
                self.zc=True
                QMessageBox.about(self.dialog, "错误提示", "用户名已经注册过：\n请重新注册！")
                return
            elif self.zc=='1':
                self.zc=True
                window.window.show()
                window.updata_friends()
                self.dialog.hide()
                return

    def button_DL(self):
        username = self.dialog.username.text()
        if len(username) < 8:
            QMessageBox.about(self.dialog, "错误提示", "用户名输入格式错误：\n至少8个字符或文字")
            self.dialog.username.clear()
            self.dialog.username.focusNextPrevChild(False)
            self.dialog.username.focusNextPrevChild(False)
            self.dialog.username.focusNextPrevChild(False)
            return
        password = self.dialog.password.text()
        if len(password) < 8:
            QMessageBox.about(self.dialog, "错误提示", "密码输入格式错误：\n至少8个字符")
            self.dialog.password.clear()
            self.dialog.username.focusNextPrevChild(False)
            self.dialog.username.focusNextPrevChild(False)
            return
        cmd = "dl---...***" + username + "---...***" + password
        try:
            data_socket.send(cmd.encode())
        except:
            QMessageBox.about(self.dialog, "错误提示", "服务器未启用\n请联系管理员启动服务器！")
            exit(-1)
        while self.dl:
            if self.dl=='0':
                self.dl=True
                QMessageBox.about(self.dialog, "错误提示", "用户名不存在：\n请重新登录！")
                return
            elif self.dl=='1':
                self.dl=True
                QMessageBox.about(self.dialog, "错误提示", "密码输入错误：\n请重新登录！")
                return
            elif self.dl=='2':
                self.dl=True
                window.window.show()
                window.updata_friends()
                self.dialog.hide()
                return

    def set_cursor(self):
        self.dialog.username.focusNextChild()

    def password_press(self):
        username = self.dialog.username.text()
        if len(username) < 8:
            QMessageBox.about(self.dialog, "错误提示", "用户名输入格式错误：\n至少8个字符或文字")
            self.dialog.username.clear()
            self.dialog.username.focusNextPrevChild(False)
            return
        password = self.dialog.password.text()
        if len(password) < 8:
            QMessageBox.about(self.dialog, "错误提示", "密码输入格式错误：\n至少8个字符")
            self.dialog.password.clear()
            return
        cmd = "dl---...***" + username + "---...***" + password
        try:
            data_socket.send(cmd.encode())
        except:
            QMessageBox.about(self.dialog, "错误提示", "服务器未启用\n请联系管理员启动服务器！")
            exit(-1)
        while self.dl:
            if self.dl=='0':
                self.dl=True
                QMessageBox.about(self.dialog, "错误提示", "用户名不存在：\n请重新登录！")
                return
            elif self.dl=='1':
                self.dl = True
                QMessageBox.about(self.dialog, "错误提示", "密码输入错误：\n请重新登录！")
                return
            elif self.dl=='2':
                self.dl=True
                window.window.show()
                window.updata_friends()
                self.dialog.hide()
                return

app=QApplication([])
app.setWindowIcon(QIcon('logo.png'))
dialog_add1=dialog_add()
window=main_window()
dialog=dialog_DL()
dialog.dialog.show()
try:
    data_socket.connect((ip,port))
except:
    QMessageBox.about(dialog.dialog,'错误提示',"远程服务器未启用!\n请联系管理员启动服务器再登录：")
    exit(-1)
dialog.thread1.start()
app.exec_()