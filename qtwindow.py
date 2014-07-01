#__author__ = 'sil'
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtXml import *
import cv2
import urllib2
from bs4 import BeautifulSoup

import time

class Form(QDialog):
    thre1 = 100
    thre2 = 200
    filename = ""
    windows = []

    def __del__(self):
        print "destructor!!!"

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        spinBoxThre1 = QSpinBox()
        spinBoxThre1.setMaximum(255)
        spinBoxThre1.setMinimum(0)
        spinBoxThre1.setValue(self.thre1)

        spinBoxThre2 = QSpinBox()
        spinBoxThre2.setMaximum(255)
        spinBoxThre2.setMinimum(0)
        spinBoxThre2.setValue(self.thre2)

        buttonOpen = QPushButton("open")
        buttonSave = QPushButton("save")
        buttonSpider = QPushButton("Spider")

        self.httpEdit = QLineEdit("Please input addr")

        self.browser = QTextBrowser(self)
        layout = QVBoxLayout()
        layout.addWidget(buttonOpen)
        layout.addWidget(buttonSave)
        layout.addWidget(QLabel("Threshold 1:"))
        layout.addWidget(spinBoxThre1)
        layout.addWidget(QLabel("Threshold 2:"))
        layout.addWidget(spinBoxThre2)
        layout.addWidget(self.browser)
        layout.addWidget(self.httpEdit)
        layout.addWidget(buttonSpider)

        self.setLayout(layout)

        self.connect(self.httpEdit, SIGNAL("enterEvent()"), self.spider)
        self.connect(spinBoxThre1, SIGNAL("valueChanged(int)"), self.updateThre1)
        self.connect(spinBoxThre2, SIGNAL("valueChanged(int)"), self.updateThre2)
        self.connect(buttonOpen, SIGNAL("clicked()"), self.openFile)
        self.connect(buttonSpider, SIGNAL("clicked()"), self.spider)

        self.setWindowTitle("My dialog")
        self.setMinimumHeight(300)

    def updateThre1(self, threshold):
        self.thre1 = threshold
        self.process()

    def updateThre2(self, threshold):
        self.thre2 = threshold
        self.process()

    def openFile(self):
        filename = QFileDialog.getOpenFileName(self, "Open File", filter = "Image Files(*.*)")
        print filename
        print type(filename)
        self.filename = filename[0]
        self.process()

    def process(self):
        if self.filename == "":
            print "No image selected"
            return
        else:
            print "Processing file: " + self.filename

        img = cv2.imread(self.filename)
        cv2.imshow("hello", img)
        cv2.setWindowProperty("hello")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imshow("gray", gray)

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv_a = cv2.split(hsv)

        print hsv_a.__len__()
        cv2.imshow("hsv", hsv)

        edges = cv2.Canny(gray, self.thre1, self.thre2)
        cv2.imshow("edges", edges)

        cv2.waitKey(1)

    def spider(self):
        try:
            url = 'proxy.doshisha.ac.jp:8080'
            username = 'dun2102'
            password = 'YUEmao6919'
            password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
            # None, with the "WithDefaultRealm" password manager means
            # that the user/pass will be used for any realm (where
            # there isn't a more specific match).
            password_mgr.add_password(None, url, username, password)
            auth_handler = urllib2.HTTPBasicAuthHandler(password_mgr)
            opener = urllib2.build_opener(auth_handler)
            urllib2.install_opener(opener)
            print urllib2.urlopen("http://www.cnbeta.com")

            content = urllib2.urlopen(self.httpEdit.text()).read()
            soup = BeautifulSoup(content)
            threadlist = soup.find(id="threadlist")
            #print threadlist
            #print type(threadlist)
            lists = threadlist.find_all("tr")
            print "total:",lists.__len__()
            for item in lists:
                print item.text
                print item.find_all(class_="p1")
                print item.find_all(class_="p4")

        except:
            print "unexpected error:", sys.exc_info()[0]
            QMessageBox.information(self, "input error!", "error")

app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
