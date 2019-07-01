# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'proje.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
from proje2 import *
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import QSize,QModelIndex
from PyQt5.QtGui import QIcon
import sys
import mysql.connector
import PIL
import pickle
import cv2
import numpy as np

bilgiler = ("admin", "123")
width, height = 500, 500
class Ui_MainWindow(QWidget):
    def Detector(self):
        faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        eyeDetect = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
        cam = cv2.VideoCapture(0)
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("recognizer\\trainingData.yml")
        font = cv2.FONT_HERSHEY_SIMPLEX
        global profile
        def getProfile(id):
            mydb = mysql.connector.connect(host="localhost",user="root",passwd="canimkendi",database="yuz_tanima")
            sql = "SELECT * FROM yoklama WHERE ogr_no="+str(id)
            cursor = mydb.cursor()
            cursor.execute(sql)
            profile = None
            for i in cursor:
                profile = i
            mydb.close()
            return profile
        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            faces = faceDetect.detectMultiScale(gray, scaleFactor=1.2, minNeighbors= 5, minSize=(100,100), flags=cv2.CASCADE_SCALE_IMAGE)
            for(x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 2 )
                roi_gray = gray[y:y+h,x:x+w]
                roi_color = img[y:y+h,x:x+w]
                eyes = eyeDetect.detectMultiScale(roi_gray)
                for(ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color, (ex,ey), (ex+ew,ey+eh), (0,0,255), 2 )
                    id, conf = recognizer.predict(gray[y:y+h, x:x+w])
                    profile = getProfile(id)
                    row = self.tW2.currentRow()
                    column = self.tW2.currentColumn()
                    item = self.tW2.itemAt(row,column)
                for item in profile:
                    if (profile!=None):  
                        cv2.putText(img, str(profile[4]),(x,y+h+30), font, 2, (255,0,0), 2)
                        mydb = mysql.connector.connect(host="localhost",user="root",passwd="canimkendi",database="yuz_tanima")
                        sql = "UPDATE yoklama SET var_yok = 1, sinif_id="+ self.cmb_sinif_2.currentText() +", ogr_gor_id="+ self.cmb_hoca.currentText() +" WHERE ogr_no = "+str(id)+" AND bolum_id LIKE '%" + self.cmb_bolum_2.currentText() + "%' AND ders_id LIKE '%" + self.cmb_ders.currentText() + "%' AND hafta_id LIKE '%" +self.cmb_hafta.currentText()+ "%'"
                        mycursor = mydb.cursor()
                        mycursor.execute(sql)
                        self.tW2.setRowCount(self.tW2.currentRow())
                        for row_number, row_data in enumerate(mycursor):
                            self.tW2.insertRow(row_number)
                            for column_number, data in enumerate(row_data):
                                self.tW2.setItem(row_number,column_number, QtWidgets.QTableWidgetItem(str(data)))
                        mydb.commit()
                        mydb.close()
                    cv2.imshow("Face", img)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        cam.release()
        cv2.destroyAllWindows()

    def Ok(self):
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="canimkendi",database="yuz_tanima")
        sql = "SELECT ogr_no,var_yok,sinif_id,ogr_gor_id FROM yoklama WHERE bolum_id LIKE '%" + self.cmb_bolum_2.currentText() + "%' AND ders_id LIKE '%" + self.cmb_ders.currentText() + "%' AND hafta_id LIKE '%" +self.cmb_hafta.currentText()+ "%'"
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        self.tW2.setRowCount(self.tW2.currentRow())
        for row_number, row_data in enumerate(myresult):
            self.tW2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tW2.setItem(row_number,column_number, QtWidgets.QTableWidgetItem(str(data)))
        mydb.close()
    def Cikis(self):
         sys.exit(app.exec_())
    def YuzKaydet(self):
        faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        eyeDetect = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
        cam = cv2.VideoCapture(0)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        rows = self.tableWidget.item(self.tableWidget.currentRow(),0).text()
        id = rows
        print(id)
        sampleNum = 0
        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            faces = faceDetect.detectMultiScale(gray, 1.3, 5)
            for(x,y,w,h) in faces:
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 2 )
                roi_gray = gray[y:y+h,x:x+w]
                roi_color = img[y:y+h,x:x+w]
                eyes = eyeDetect.detectMultiScale(roi_gray)
                for(ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color, (ex,ey), (ex+ew,ey+eh), (0,0,255), 2 )
                    sampleNum = sampleNum+1
                    cv2.imwrite("dataSet/User." + str(id) + "." + str(sampleNum) + ".jpg" , gray[y:y+h,x:x+w])
                    cv2.waitKey(100)
            cv2.imshow("Face", img)
            cv2.waitKey(1)
            if sampleNum>20:
                break 
                QMessageBox.about(self, 'Bilgi', 'Kayıt tamamlandı')
        cam.release()
        cv2.destroyAllWindows()
    def TabloGoster(self):
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="canimkendi",database="yuz_tanima")
        sql = "SELECT ogrenci_no,ogrenci_ad,ogrenci_soyad FROM ogr WHERE ogrenci_bolum LIKE '%" + self.cmb_bolum.currentText() + "%' AND bolum_sinif LIKE '%" + self.cmb_sinif.currentText() + "%'"
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        self.tableWidget.setRowCount(self.tableWidget.currentRow())
        for row_number, row_data in enumerate(myresult):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number,column_number, QtWidgets.QTableWidgetItem(str(data)))
        mydb.close()
    def Clear():
        self.k_ad.clear()
        self.k_sifre.clear()        
    def Giris(self):
        k_ad = self.k_ad.text()
        k_sifre = self.k_sifre.text()
        print (k_ad, " - ", k_sifre)
        print ("Kontrol ediliyor ...")
        #self.Clear()
        if ((k_ad == bilgiler[0]) and (k_sifre == bilgiler[1])):
            print ("Bilgiler dogru!")
            self.window = QtWidgets.QMainWindow()
            self.ui = S_OlusturDuzenle()
            self.ui.setupUi_S_OlusturDuzenle(self.window)
            self.window.show()
        else:
            print ("Bilgiler yanlis!")
            QMessageBox.about(self, "Hata", "Bilgiler yanlış, tekrar deneyiniz.")
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(694, 472)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tW1 = QtWidgets.QTabWidget(self.centralwidget)
        self.tW1.setGeometry(QtCore.QRect(20, 60, 651, 411))
        self.tW1.setObjectName("tW1")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(40, 50, 81, 16))
        self.label.setObjectName("label")
        
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(40, 90, 47, 13))
        self.label_2.setObjectName("label_2")
        
        self.k_ad = QtWidgets.QLineEdit(self.tab)
        self.k_ad.setGeometry(QtCore.QRect(130, 50, 113, 20))
        self.k_ad.setObjectName("k_ad")
        
        self.k_sifre = QtWidgets.QLineEdit(self.tab)
        self.k_sifre.setGeometry(QtCore.QRect(130, 90, 113, 20))
        self.k_sifre.setObjectName("k_sifre")
        
        self.btn_giris = QtWidgets.QPushButton(self.tab)
        self.btn_giris.setGeometry(QtCore.QRect(160, 150, 75, 23))
        self.btn_giris.setObjectName("btn_giris")
        self.btn_giris.clicked.connect(self.Giris)
        
        self.tW1.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setGeometry(QtCore.QRect(220, 10, 71, 16))
        self.label_3.setObjectName("label_3")
        
        self.gridLayoutWidget = QtWidgets.QWidget(self.tab_2)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 40, 631, 31))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        
        self.cmb_bolum = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.cmb_bolum.setObjectName("cmb_bolum")
        self.gridLayout.addWidget(self.cmb_bolum, 0, 1, 1, 1)
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="canimkendi",database="yuz_tanima")
        sql = "SELECT bolum_ad FROM bolum"
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for i in myresult:
            self.cmb_bolum.addItem(i[0])
        mycursor.close()
        mydb.close()        
        
        self.cmb_sinif = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.cmb_sinif.setObjectName("cmb_sinif")
        self.gridLayout.addWidget(self.cmb_sinif, 0, 3, 1, 1)
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="canimkendi",database="yuz_tanima")
        sql = "SELECT DISTINCT bolum_sinif FROM ogrenci ORDER BY bolum_sinif"
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for i in myresult:
            self.cmb_sinif.addItem(i[0])
        mycursor.close()
        mydb.close()
        
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 2, 1, 1)
        
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        
        self.btn_ok = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_ok.setObjectName("btn_ok")
        self.gridLayout.addWidget(self.btn_ok, 0, 4, 1, 1)
        self.btn_ok.clicked.connect(self.TabloGoster)
        
        self.tableWidget = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget.setGeometry(QtCore.QRect(10, 80, 451, 192))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(10)
        
        self.btn_kaydet = QtWidgets.QPushButton(self.tab_2)
        self.btn_kaydet.setGeometry(QtCore.QRect(470, 160, 161, 31))
        self.btn_kaydet.setObjectName("btn_kaydet")
        self.btn_kaydet.clicked.connect(self.YuzKaydet)

        
        self.tW1.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.tab_3)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 621, 122))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 0, 2, 1, 1)
        
        self.cmb_bolum_2 = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        self.cmb_bolum_2.setObjectName("cmb_bolum_2")
        self.gridLayout_2.addWidget(self.cmb_bolum_2, 0, 3, 1, 1)
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="canimkendi",database="yuz_tanima")
        sql = "SELECT CONCAT(bolum_id) FROM bolum"
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for i in myresult:
            self.cmb_bolum_2.addItem(i[0])
        mycursor.close()
        mydb.close()
        
        self.cmb_hoca = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        self.cmb_hoca.setObjectName("cmb_hoca")
        self.gridLayout_2.addWidget(self.cmb_hoca, 1, 3, 1, 1)
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="canimkendi",database="yuz_tanima")
        sql = "SELECT CONCAT(og_id) AS 'AD SOYAD' FROM ogretim_gorevlisi"
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for i in myresult:
            self.cmb_hoca.addItem(i[0])
        mycursor.close()
        mydb.close()
        
        self.cmb_ders = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        self.cmb_ders.setObjectName("cmb_ders")
        self.gridLayout_2.addWidget(self.cmb_ders, 1, 1, 1, 1)
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="canimkendi",database="yuz_tanima")
        sql = "SELECT DISTINCT CONCAT(ders_id) FROM dersler"
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for i in myresult:
            self.cmb_ders.addItem(i[0])
        mycursor.close()
        mydb.close()
        
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 1, 2, 1, 1)
        
        self.cmb_sinif_2 = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        self.cmb_sinif_2.setObjectName("cmb_sinif_2")
        self.gridLayout_2.addWidget(self.cmb_sinif_2, 0, 1, 1, 1)
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="canimkendi",database="yuz_tanima")
        sql = "SELECT CONCAT(sinif_id) FROM sinif_olusturma"
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for i in myresult:
            self.cmb_sinif_2.addItem(i[0])
        mycursor.close()
        mydb.close()

        
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 1, 0, 1, 1)
        
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1)

        self.label_10 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 3, 0, 1, 1)
        
        self.cmb_hafta = QtWidgets.QComboBox(self.gridLayoutWidget_2)
        self.cmb_hafta.setObjectName("cmb_hafta")
        self.gridLayout_2.addWidget(self.cmb_hafta, 3, 1, 1, 1)
        mydb = mysql.connector.connect(host="localhost",user="root",passwd="canimkendi",database="yuz_tanima")
        sql = "SELECT CONCAT(hafta_id) FROM hafta"
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for i in myresult:
            self.cmb_hafta.addItem(i[0])
        mycursor.close()
        mydb.close()
        
        self.btn_ok_2 = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.btn_ok_2.setObjectName("btn_ok_2")
        self.gridLayout_2.addWidget(self.btn_ok_2, 4, 1, 1, 2)
        self.btn_ok_2.clicked.connect(self.Ok)
        
        self.tW2 = QtWidgets.QTableWidget(self.tab_3)
        self.tW2.setGeometry(QtCore.QRect(20, 170, 541, 192))
        self.tW2.setObjectName("tW2")
        self.tW2.setColumnCount(4)
        self.tW2.setRowCount(50)
        
        self.btn_oku = QtWidgets.QPushButton(self.tab_3)
        self.btn_oku.setGeometry(QtCore.QRect(574, 180, 61, 23))
        self.btn_oku.setObjectName("btn_oku")
        self.btn_oku.clicked.connect(self.Detector)
        
        self.tW1.addTab(self.tab_3, "")
        self.btn_cikis = QtWidgets.QPushButton(self.centralwidget)
        self.btn_cikis.setGeometry(QtCore.QRect(590, 20, 75, 23))
        self.btn_cikis.setObjectName("btn_cikis")
        self.btn_cikis.clicked.connect(self.Cikis)
        
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tW1.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Kullanıcı Adı:"))
        self.label_2.setText(_translate("MainWindow", "Şifre: "))
        self.btn_giris.setText(_translate("MainWindow", "Giriş"))
        self.tW1.setTabText(self.tW1.indexOf(self.tab), _translate("MainWindow", "Giriş Yap"))
        self.label_3.setText(_translate("MainWindow", "Yüz Kaydetme"))
        self.label_5.setText(_translate("MainWindow", "Sınıf : "))
        self.label_4.setText(_translate("MainWindow", "Bölüm :"))
        self.btn_ok.setText(_translate("MainWindow", "Tamam"))
        self.btn_kaydet.setText(_translate("MainWindow", "Seçilen kişinin yüzünü kaydet!"))
        self.tW1.setTabText(self.tW1.indexOf(self.tab_2), _translate("MainWindow", "Yüz Tanıtma"))
        self.label_7.setText(_translate("MainWindow", "Bölüm :"))
        self.label_9.setText(_translate("MainWindow", "Öğretim Görevlisi :"))
        self.label_8.setText(_translate("MainWindow", "Ders : "))
        self.label_6.setText(_translate("MainWindow", "Sınıf : "))
        self.label_10.setText(_translate("MainWindow", "Hafta :"))
        self.btn_ok_2.setText(_translate("MainWindow", "Tamam"))
        self.btn_oku.setText(_translate("MainWindow", "Oku"))
        self.tW1.setTabText(self.tW1.indexOf(self.tab_3), _translate("MainWindow", "Yoklama Sistemi"))
        self.btn_cikis.setText(_translate("MainWindow", "Çıkış"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

