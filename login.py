# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'username.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import pandas as pd
import sqlite3
from passlib.hash import pbkdf2_sha256
from random import randint
import pickle,glob
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon 
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMessageBox,QMainWindow,QFileDialog,QWidget,QInputDialog
import subprocess
import time
import cv2
import face_recognition
import base64
import os

def strEncode(strvar):
    encoded = base64.b64encode(strvar.encode())
    return encoded.decode() # decoded to string

def strDecode(encoded):
    encoded = encoded.encode()
    data = base64.b64decode(encoded)
    return data.decode() # decoded to string
    
def getResult(face,source):
    image_of_bill = face
    try:
        bill_face_encoding = face_recognition.face_encodings(image_of_bill)[0]
    except:
        return False
    # face_recognition.load_image_file(source)
    encode = face_recognition.face_encodings(source)
    if len(encode) == 0:
        return False
    else:
        unknown_face_encoding = encode[0]
    
    
    # Compare faces
    results = face_recognition.compare_faces(
        [bill_face_encoding], unknown_face_encoding)
    
    if results[0]:
        return True
    else:
        return False



class FaceLock(object):
    def setupUi(self, Dialog, uname, data_path, face_path):
        self.d = Dialog
        self.user_name = uname
        self.data_path = data_path
        self.face_path = face_path
        self.d = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(629, 328)
        Dialog.setStyleSheet("background-color: rgb(43, 147, 116);")
        self.txt = 'Not yet started...'
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(20, 180, 581, 121))
        self.frame.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(20, 20, 54, 17))
        self.label_5.setObjectName("label_5")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 151, 31))
        self.label_2.setStyleSheet("color: rgb(0, 255, 0);\n"
"font: 13pt \"Monospace\";")
        self.label_2.setObjectName("label_2")
        self.status = QtWidgets.QLabel(self.frame)
        self.status.setGeometry(QtCore.QRect(140, 60, 431, 31))
        self.status.setStyleSheet("color: rgb(255, 0, 0);\n"
"font: 13pt \"Monospace\";")
        self.status.setObjectName("status")
        self.label_7 = QtWidgets.QLabel(self.frame)
        self.label_7.setGeometry(QtCore.QRect(60, 20, 451, 31))
        self.label_7.setStyleSheet("color: rgb(0, 255, 0);\n"
"font: 13pt \"Monospace\";")
        self.label_7.setObjectName("label_7")
        self.frame_3 = QtWidgets.QFrame(Dialog)
        self.frame_3.setGeometry(QtCore.QRect(20, 110, 331, 41))
        self.frame_3.setStyleSheet("background-color: rgb(0, 42, 62);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label = QtWidgets.QLabel(self.frame_3)
        self.label.setGeometry(QtCore.QRect(20, 10, 131, 21))
        self.label.setStyleSheet("font: 12pt \"Monospace\";\n"
"color: red;")
        self.label.setObjectName("label")
        self.uname = QtWidgets.QLabel(self.frame_3)
        self.uname.setGeometry(QtCore.QRect(160, 10, 141, 21))
        self.uname.setStyleSheet("font: 12pt \"Monospace\";\n"
"color: rgb(85, 255, 255);")
        self.uname.setObjectName("uname")
        self.frame_4 = QtWidgets.QFrame(Dialog)
        self.frame_4.setGeometry(QtCore.QRect(20, 30, 581, 51))
        self.frame_4.setStyleSheet("background-color: rgb(127, 255, 105);")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.label_3 = QtWidgets.QLabel(self.frame_4)
        self.label_3.setGeometry(QtCore.QRect(150, 10, 321, 31))
        self.label_3.setStyleSheet("font: 20pt \"Monospace\";\n"
"")
        self.label_3.setObjectName("label_3")
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setGeometry(QtCore.QRect(369, 99, 231, 61))
        self.frame_2.setStyleSheet("background-color: rgb(6, 102, 104);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.pushButton = QtWidgets.QPushButton(self.frame_2)
        self.pushButton.setGeometry(QtCore.QRect(20, 20, 80, 25))
        self.pushButton.setStyleSheet("color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.back_operation)
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_2.setGeometry(QtCore.QRect(120, 20, 80, 25))
        self.pushButton_2.setStyleSheet("color:rgb(255, 255, 255)")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.detect)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def back_operation(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.window)
        self.window.show()
        self.d.hide()

    def detect(self):
        video_capture = cv2.VideoCapture(0)
        # initial values
        f = open(self.face_path, 'rb')
        faces = pickle.load(f)
        f.close()

        count = 0 # video frame will only run for 5 times...
        detection_status = False
        while True:

            # Capture frame-by-frame
            ret, frame = video_capture.read()
            # img_cpy = deepcopy(frame)
            # height, width = frame.shape[:2]
            # cv2.imwrite('output.jpg',frame)
            self.txt = 'started detection...'
            time.sleep(1)
            self.retranslateUi(self.d)
            self.txt = 'processing...'
            self.retranslateUi(self.d)

            self.retranslateUi(self.d)
            if getResult(faces[0],frame):
                self.txt = "[ trial 1 : face found ] [ "+str(count)+" ]"
                self.retranslateUi(self.d)
                time.sleep(1)
                detection_status = True
                break
            elif getResult(faces[1],frame):
                self.txt = "trial 2 : face found [ "+str(count)+" ]"
                self.retranslateUi(self.d)
                time.sleep(1)
                detection_status = True
                break
            else:
                self.txt = "[ face not found ] [ frame : "+str(count)+" ]"
                self.retranslateUi(self.d)
                if count >= 5:
                    break
                else:
                    count += 1
            print(' frame status : ',self.txt)
            # font = cv2.FONT_HERSHEY_SIMPLEX
            # cv2.putText(frame, txt, (41, 40), font, 1.3, (57, 20,50), 4, cv2.LINE_AA)
            
            # cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything is done, release the capture
        video_capture.release()
        cv2.destroyAllWindows()

        if detection_status:
            
            self.window = QtWidgets.QMainWindow()
            self.ui = Main_App()
            self.ui.setupUi(self.window,self.user_name,self.data_path)
            self.window.show()
            self.d.hide()


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_5.setText(_translate("Dialog", "TextLabel"))
        self.label_2.setText(_translate("Dialog", "[ status ] :  "))
        self.status.setText(_translate("Dialog", self.txt))
        self.label_7.setText(_translate("Dialog", "| [ - - - processing face detection - - -] | "))
        self.label.setText(_translate("Dialog", "[ USER NAME ]"))
        self.uname.setText(_translate("Dialog", "[ "+self.user_name+" ]"))
        self.label_3.setText(_translate("Dialog", "FACE AUTHENTICATION"))
        self.pushButton.setText(_translate("Dialog", "back"))
        self.pushButton_2.setText(_translate("Dialog", "detect"))



class auth:
    '''
    DOC STR: 
    topic: Authentication class
    usage: the authentication for the project
           is provided in this code.

    functionalities: the 2 kind of authentication

          1. new user ( sign up )
          2. existing user ( login )

    '''

    @staticmethod
    def Login(uname,passkey):
        '''
           Check for the every authentication steps
           all 2 kind of authentication is taken in consider...
        '''

        # --- read the database --- 

        # Create your connection.
        conn = sqlite3.connect('file.db')
        df = pd.read_sql_query("SELECT * FROM df", conn)

        # USER NAME
        # uname = input(' # [ uname ] : ')
        user_list = df['username'].tolist()
        user_list = [ strDecode(x) for x in user_list ]

        if uname not in user_list:
            # exist in db
            return False,'username not exist in database'
        else:
            # PASSWORD
            # passkey = input(' # [ password ] : ') # password
            cur = conn.cursor()
            cur.execute('SELECT * FROM df WHERE username == "{0}"'.format(strEncode(uname)))
            res = cur.fetchall()
            res = res[0]
            hashkey = strDecode(res[2])

            # CROSSCHECKING password...
            if not pbkdf2_sha256.verify(passkey,hashkey):
                # password not matched
                return False,'password is wrong'


            cur.close()
            conn.close()
            # print('hai existing user:',uname)

            # --- end of db connection ---
            # return value with bool,tuple
            return True,('access allowed',strDecode(res[-1]),strDecode(res[-2]))
        # end



class Main_App(QMainWindow):

    def setupUi(self, Dialog, user_name, data_path):
        self.d = Dialog
        self.user_name = user_name
        self.data_path = data_path
        self.file_list = []
        self.dis_list = []
        self.dis_count = []

        Dialog.setObjectName("Dialog")
        Dialog.resize(1133, 629)
        Dialog.setStyleSheet("background-color: rgb(33, 33, 33);")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(10, 70, 1111, 551))
        self.frame.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(630, 20, 461, 41))
        self.frame_2.setStyleSheet("background-color: rgb(79, 188, 176);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.add_btn = QtWidgets.QPushButton(self.frame_2)
        self.add_btn.setGeometry(QtCore.QRect(10, 10, 80, 25))
        self.add_btn.setObjectName("add_btn")
        self.add_btn.clicked.connect(self.add_file)
        self.lock_btn = QtWidgets.QPushButton(self.frame_2)
        self.lock_btn.setGeometry(QtCore.QRect(370, 10, 80, 25))
        self.lock_btn.setObjectName("lock")
        self.lock_btn.clicked.connect(self.lock_file)

        self.unlock_btn = QtWidgets.QPushButton(self.frame_2)
        self.unlock_btn.setGeometry(QtCore.QRect(280, 10, 80, 25))
        self.unlock_btn.setObjectName("unlock")
        self.unlock_btn.clicked.connect(self.unlock_file)

        self.remove_btn = QtWidgets.QPushButton(self.frame_2)
        self.remove_btn.setGeometry(QtCore.QRect(100, 10, 80, 25))
        self.remove_btn.setObjectName("remove_btn")
        self.remove_btn.clicked.connect(self.remove_file)

        self.clear_btn = QtWidgets.QPushButton(self.frame_2)
        self.clear_btn.setGeometry(QtCore.QRect(190, 10, 80, 25))
        self.clear_btn.setObjectName("clear_btn")
        self.clear_btn.clicked.connect(self.clear_operation)

        self.frame_3 = QtWidgets.QScrollArea(self.frame)
        self.frame_3.setGeometry(QtCore.QRect(20, 80, 1081, 461))
        self.frame_3.setStyleSheet("\n"
                                   "background-color: rgb(0, 0, 0);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        self.label_2.setGeometry(QtCore.QRect(20, 10, 161, 17))
        self.label_2.setStyleSheet("color: rgb(0, 255, 0);\n"
                                   "font: 11pt \"Monospace\";")
        self.label_2.setObjectName("label_2")
        self.content1 = QtWidgets.QLabel(self.frame_3)
        self.content1.setGeometry(QtCore.QRect(100, 40, 451, 20))
        self.content1.setStyleSheet("color: rgb(0, 255, 0);\n"
                                    "font: 11pt \"Monospace\";")
        self.content1.setObjectName("content1")
        self.count1 = QtWidgets.QLabel(self.frame_3)
        self.count1.setGeometry(QtCore.QRect(20, 40, 71, 20))
        self.count1.setStyleSheet("color: rgb(255, 170, 0);\n"
                                  "font: 11pt \"Monospace\";")
        self.count1.setObjectName("count1")
        self.filecount = QtWidgets.QLabel(self.frame_3)
        self.filecount.setGeometry(QtCore.QRect(190, 10, 151, 20))
        self.filecount.setStyleSheet("\n"
                                     "color: rgb(85, 255, 255);\n"
                                     "font: 11pt \"Monospace\";")
        self.filecount.setObjectName("filecount")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(90, 10, 271, 51))
        self.label.setStyleSheet("\n"
                                 "font: 87 36pt \"Noto Sans CanAborig Bk\";\n"
                                 "color: rgb(166, 11, 57);")
        self.label.setObjectName("label")
        self.frame_4 = QtWidgets.QFrame(Dialog)
        self.frame_4.setGeometry(QtCore.QRect(10, 10, 1111, 51))
        self.frame_4.setStyleSheet("background-color: rgb(144, 144, 144);")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.logout_btn = QtWidgets.QPushButton(self.frame_4)
        self.logout_btn.setGeometry(QtCore.QRect(970, 10, 121, 31))
        self.logout_btn.setObjectName("logout_btn")
        self.logout_btn.clicked.connect(self.log_out)
        pos = 40
        for i in range(20):
            self.dis_list.append(QtWidgets.QLabel(self.frame_3))
            temp1 = self.dis_list[-1]
            temp1.setGeometry(QtCore.QRect(100, pos, 951, 20))
            temp1.setStyleSheet("color: rgb(0, 255, 0);font: 11pt \"Monospace\";")

            self.dis_count.append(QtWidgets.QLabel(self.frame_3))
            temp2 = self.dis_count[-1]

            temp2.setGeometry(QtCore.QRect(20, pos, 71, 20))
            temp2.setStyleSheet("color: rgb(255, 170, 0);font: 11pt \"Monospace\";")
            pos += 20
        self.frame_5 = QtWidgets.QFrame(self.frame_4)
        self.frame_5.setGeometry(QtCore.QRect(19, 10, 931, 31))
        self.frame_5.setStyleSheet("background-color: rgb(3, 3, 3);")
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.label_3 = QtWidgets.QLabel(self.frame_5)
        self.label_3.setGeometry(QtCore.QRect(50, 0, 141, 31))
        self.label_3.setStyleSheet("font: 11pt \"Monospace\";\n"
                                   "color: rgb(255, 0, 0);")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.frame_5)
        self.label_4.setGeometry(QtCore.QRect(220, 0, 131, 31))
        self.label_4.setStyleSheet("font: 11pt \"Monospace\";\n"
                                   "color: rgb(0, 255, 0);\n"
                                   "")
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        self.get_data()
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.add_btn.setText(_translate("Dialog", "add"))
        self.remove_btn.setText(_translate("Dialog", "remove"))
        self.clear_btn.setText(_translate("Dialog", "clear"))
        self.lock_btn.setText(_translate("Dialog", "lock"))
        self.unlock_btn.setText(_translate("Dialog","unlock"))
        self.label_2.setText(_translate("Dialog", "[ no of files ] : "))

        for i, obj in enumerate(self.dis_count):
            obj.setText(_translate("Dialog", "[ " + str(i + 1) + " ] :"))
        for i, obj in enumerate(self.dis_list):
            try:
                f_path = self.file_list[i]
            except:
                f_path = ''

            obj.setText(_translate("Dialog", f_path))

        self.filecount.setText(_translate("Dialog", str(len(self.file_list))))
        self.label.setText(_translate("Dialog", "FILES LIST"))
        self.logout_btn.setText(_translate("Dialog", "LOG OUT"))
        self.label_3.setText(_translate("Dialog", "[ user name ] : "))
        self.label_4.setText(_translate("Dialog", self.user_name))

    #  the code for operation involved in
    #  the final executing page...

    # data input and output process...
    def unlock_file(self):
        for files in self.file_list:
            command = 'attrib -r -a -s -h '+'"'+files+'"'
            os.system(command)

    def get_data(self):
        f = open(self.data_path, 'rb')
        self.file_list = pickle.load(f)
        self.file_list = [ strDecode(x) for x in self.file_list ]
        f.close()

    def set_data(self):
        f = open(self.data_path, 'wb')
        self.file_list = [ strEncode(x) for x in self.file_list ]
        pickle.dump(self.file_list, f)
        f.close()

    def lock_file(self):
        for files in self.file_list:
            command = 'attrib -r -a -s -h '+'"'+files+'"'
            os.system(command)

    # operations...
    def add_file(self):
        # open browse window
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        data = ''

        if dlg.exec_():
            data = dlg.selectedFiles()

        if data != '':
            print("content:", data)
            file = data[0]
            self.file_list.append(file)
            self.set_data()
            self.retranslateUi(self)

    def remove_file(self, file):
        # pop input box
        text, ok = QInputDialog.getText(self, 'Input box', 'Enter the file index:')

        if ok:
            try:
                file = self.file_list[int(text) - 1]
                self.file_list.remove(file)
                self.set_data()
                self.retranslateUi(self)
            except:
                QMessageBox.about(self, "warning", 'invalid index given')

    def clear_operation(self):
        self.file_list = []
        self.set_data()
        self.retranslateUi(self)

    def log_out(self):
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_Dialog()
            self.ui.setupUi(self.window)
            self.window.show()
            self.d.hide()

class Ui_Dialog(QMainWindow):
    def setupUi(self, Dialog):
        self.d = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(80, 90, 91, 17))
        self.label.setObjectName("label") # username label
        self.proceedbtn = QtWidgets.QPushButton(Dialog)
        self.proceedbtn.setGeometry(QtCore.QRect(220, 210, 80, 25))
        self.proceedbtn.setObjectName("proceedbtn")
        self.backbtn = QtWidgets.QPushButton(Dialog)
        self.backbtn.setGeometry(QtCore.QRect(100, 210, 80, 25))
        self.backbtn.setObjectName("backbtn")
        self.backbtn.clicked.connect(self.backaction)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(80, 130, 54, 17))
        self.label_2.setObjectName("label_2") # password label
        self.unameinput = QtWidgets.QLineEdit(Dialog)
        self.unameinput.setGeometry(QtCore.QRect(170, 90, 161, 25))
        self.unameinput.setObjectName("unameinput") # username input box
        self.passinput = QtWidgets.QLineEdit(Dialog)
        self.passinput.setGeometry(QtCore.QRect(170, 130, 161, 25))
        self.passinput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passinput.setObjectName("passinput") # password input box
        self.proceedbtn.clicked.connect(self.btnstate)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "user name"))
        self.proceedbtn.setText(_translate("Dialog", "next"))
        self.label_2.setText(_translate("Dialog", "password"))
        self.backbtn.setText(_translate("Dialog","back"))

    def backaction(self):
        pass
        # subprocess.call(['mainpage.exe']) # mainpage.exe
        # self.d.hide()
        # sys.exit()

    def btnstate(self):

        un_input = self.unameinput.text()
        pass_input = self.passinput.text()
        if '' in [un_input,pass_input]:
            QMessageBox.about(self, "warning", ' username or password may be empty')
        else:
            status,info = auth.Login(un_input,pass_input)
            if status:
                print('True : [ info ] : ',info)
                # QMessageBox.about(self, "Information", ' INFO : '+info[0])
                # opening main window...
                self.window = QtWidgets.QMainWindow()
                self.ui = FaceLock()
                self.ui.setupUi(self.window,uname = un_input,data_path = info[1],face_path = info[2])
                self.window.show()
                self.d.hide()
                # call the data collect box
            else:
                print('False : [ info ] : ',info)
                QMessageBox.about(self, "warning", ' INFO : '+info)
        self.unameinput.setText('')
        self.passinput.setText('')




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


def nextStep(username):
    # after authentication complete
    conn = sqlite3.connect('file.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM df WHERE username == "{0}"'.format(username))
    data = cur.fetchall()[0]
    data_path = data[3] # json file path...
    
    cur.close()
    conn.close()

    # call finalpage
    # finalpage.openpage(username,data_path)

