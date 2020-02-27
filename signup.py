# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'username.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from passlib.hash import pbkdf2_sha256
from random import randint
import glob
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon 
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMessageBox,QMainWindow
import sqlite3
import pandas as pd
import cv2
import random
from copy import deepcopy
import time
import pickle
import base64

def strEncode(strvar):
    encoded = base64.b64encode(strvar.encode())
    return encoded.decode() # decoded to string

def strDecode(encoded):
    encoded = encoded.encode()
    data = base64.b64decode(encoded)
    return data.decode() # decoded to string

class Auth:
    '''
    DOC STR:
    topic: Authentication class
    usage: the authentication for the project
           is provided in this code.

    functionalities: the 2 kind of authentication

          1. new user
          2. existing user

    '''

    @staticmethod
    def signup(uname, passkey):
        '''
           Create a new username and store it database.
           all 2 kind of authentication is taken and stored.
        '''

        # --- read the database ---

        # db connecting
        conn = sqlite3.connect('file.db')
        df = pd.read_sql_query("SELECT * FROM df", conn)

        # USER NAME
        # uname = input(' # [ uname ] : ')
        user_list = df['username'].tolist()
        user_list = [strDecode(x) for x in user_list]
        if uname in user_list:
            # exist in db
            return False, 'username exist in database'
        else:
            # PASSWORD
            # passkey = input(' # [ password ] : ') # password
            hashkey = pbkdf2_sha256.hash(passkey) # haskkey

            # FACE IMAGE PASSCODE
            data_path = capture_face()
            

            # storing in the df
            json_files = glob.glob('database/*.pickle')
            f_name = 'database/' + str(randint(10,1000)) + '.pickle'
            while f_name in json_files:
                f_name = 'database/' + str(randint(10,1000)) + '.pickle'

            # create a default pickle data into pickle file
            f = open(f_name, 'wb')
            val = []
            pickle.dump(val, f)
            f.close()

            imgpath = f_name


            # executing sqlite query

            cur = conn.cursor()
            cur.execute("INSERT INTO df (username, hashkey, imgpath, datapath) VALUES ('{0}','{1}','{2}','{3}')".format(strEncode(uname),strEncode(hashkey),strEncode(data_path),strEncode(imgpath)))
            cur.execute('commit;')
            cur.close()
            # df = df.append({'username':uname,'hashkey':hashkey,'imgpath':imgpath},ignore_index=True)
            # storing in the db
            # df.to_sql("df",conn,if_exists="replace")
            # db disconnecting
            conn.close()
            # --- end of db connection ---

            # return value with bool,info
            return True,'new user created successfully'
        # end



def capture_face():
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

    video_capture = cv2.VideoCapture(0)
    # initial values
    count = 0
    col = (51, 204, 255)
    txt = 'record count : 0'
    rc = 0
    slow_down = 10
    s_count = 11

    face_li = []
    while True:
        s_count += 1
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        img_cpy = deepcopy(frame)
        height, width = frame.shape[:2]

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),

        )

        # Draw a rectangle around the faces
        x1c = 0; y1c = 0;  x2c = 0; y2c = 0
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            x1c = x; y1c = y
            x2c = x+w; y2c = y+h

        # draw the blue color box in the image
        x1 = 200; x2 = 450
        y1 = 96; y2 = 346
        cv2.rectangle(frame, (x1, y1), (x2, y2), (222, 117, 64), 2)
        col = (51, 204, 255)
        # Display the resulting frame
        # print(" x => ",x,x1)
        # print(" y => ",y,y1)



        if x1c in range(x1,x2) and y1c in range(y1,y2) and count < 3 and s_count > slow_down:
            print("in the range:")
            count += 1
            cap_face = img_cpy[ y1c:y2c,x1c:x2c ]
            # cv2.imwrite('images/face'+str(random.randint(100,1000))+'.jpg',cap_face)
            face_li.append(cap_face)
            col = (222,169,64)
            cv2.rectangle(frame, (x1, y1), (x2, y2), col, 4)
            time.sleep(2)  # change to your own waiting time 1000 = 1 second
            rc += 1
            txt = 'record count : ' + str(rc)
            s_count = 0
        if count >= 2:
            print('record finished')
            break



        # adding text into the image
        font = cv2.FONT_HERSHEY_SIMPLEX
        # static fonts...
        cv2.putText(frame, 'KEEP YOUR FACE INSIDE', (41, 40), font, 1.3, (57, 20,50), 4, cv2.LINE_AA)
        cv2.putText(frame, 'bounding box', (218, 79), font, 1, (0, 25, 255), 4, cv2.LINE_AA)
        cv2.putText(frame, 'STATUS : ', (94, 383), font, 1.3, (216, 235, 52), 4, cv2.LINE_AA)
        # dynamic fonts...
        cv2.putText(frame, txt, (300, 383), font, 1, (9, 9, 173), 3, cv2.LINE_AA)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    print('record face finished...')
    # face capture finished...
    save_path = 'warehouse/repo_f/'
    files = glob.glob(save_path + '*.pickle')
    f_name = save_path + str(random.randint(10,1000)) + '.pickle'
    while f_name in files:
        f_name = save_path + str(random.randint(10,1000)) + '.pickle'
    f = open(f_name,'wb')
    pickle.dump(face_li,f)
    f.close()
    # face_identification is saved...

    video_capture.release()
    cv2.destroyAllWindows()

    return f_name

class  SignUpWindow(QMainWindow):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(80, 90, 91, 17))
        self.label.setObjectName("label")
        self.proceedbtn = QtWidgets.QPushButton(Dialog)
        self.proceedbtn.setGeometry(QtCore.QRect(220, 210, 80, 25))
        self.proceedbtn.setObjectName("proceedbtn")
        self.backbtn = QtWidgets.QPushButton(Dialog)
        self.backbtn.setGeometry(QtCore.QRect(100, 210, 80, 25))
        self.backbtn.setObjectName("backbtn")
        self.backbtn.clicked.connect(self.backaction)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(80, 130, 54, 17))
        self.label_2.setObjectName("label_2")
        self.unameinput = QtWidgets.QLineEdit(Dialog)
        self.unameinput.setGeometry(QtCore.QRect(170, 90, 161, 25))
        self.unameinput.setObjectName("unameinput")
        self.passinput = QtWidgets.QLineEdit(Dialog)
        self.passinput.setGeometry(QtCore.QRect(170, 130, 161, 25))
        self.passinput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passinput.setObjectName("passinput")
        self.proceedbtn.clicked.connect(self.btnstate)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "user name"))
        self.proceedbtn.setText(_translate("Dialog", "next"))
        self.label_2.setText(_translate("Dialog", "password"))
        self.backbtn.setText(_translate("Dialog", "back"))

    def backaction(self):
        pass

    def btnstate(self):

        un_input = self.unameinput.text()
        pass_input = self.passinput.text()
        if '' in [un_input, pass_input]:
            QMessageBox.about(self, "warning", ' username or password may be empty')
        else:
            status,info = Auth.signup(un_input, pass_input)
            if status:
                print('True : [ info ] : ', info)
                QMessageBox.about(self, "Information", ' INFO : '+info)
            else:
                print('False : [ info ] : ', info)
                QMessageBox.about(self, "warning", ' INFO : '+info)
        self.unameinput.setText('')
        self.passinput.setText('')




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = SignUpWindow()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

