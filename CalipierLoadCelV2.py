import thread
import serial
import os, sys, csv
import numpy as np
import matplotlib.pyplot as plt

from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from random import random
from math import isnan,floor
from time import time,sleep
from conf import *

# Globals
t=0                 #This is the time counter in seconds
t0=0
l=0                 #This is the row to be filled with the next data
flag_run = False    #This is the result of start/stop buttons to log or ignore data
typeofPlot = 0      #This is the counter that makes possible diferent plots from the same button
Sp = 1              #This is the default sampling period, in seconds

def getDataTest():
    global fx
    global dx
    global dy
    global t
    global w
    global flag_run,Sp,l
    while True:
        if flag_run and (t%Sp == 0):
            ts = "%d"%t
            fx = "%2.2f"%(1000*random()/scale)
            dx = "%2.2f"%(1000*random()/100.0)
            dy = "%2.2f"%(1000*random()/100.0)
            ec = "%2.2f"%(float(fx)/area)
            dt = "%2.2f"%(float(dx)*dtang)
            print ts, fx, dx, dy, ec,dt


            newdata = QtGui.QTableWidgetItem(ts)
            w.table.setItem(l,0,newdata)
            newdata = QtGui.QTableWidgetItem(fx)
            w.table.setItem(l,1,newdata)
            newdata = QtGui.QTableWidgetItem(dx)
            w.table.setItem(l,2,newdata)
            newdata = QtGui.QTableWidgetItem(dy)
            w.table.setItem(l,3,newdata)
            newdata = QtGui.QTableWidgetItem(ec)
            w.table.setItem(l,4,newdata)
            newdata = QtGui.QTableWidgetItem(dt)
            w.table.setItem(l,5,newdata)
            
            #Data to Labels
            w.value1.setText(ts)
            w.value2.setText(fx)
            w.value3.setText(dx)
            w.value4.setText(dy)
            w.value5.setText(ec)
            w.value6.setText(dt)
            l = l+1
        t = t+1
        sleep(1)

def getData():
    global fx
    global dx
    global dy
    global t,l,t0
    global w
    global flag_run,Sp
    global ser

    l=0;
    t0 = time()
    while True:
        dataSerial = ser.readline()
        if len(dataSerial)>3:
            dataSerial= dataSerial.split(',')
            if len(dataSerial)==3:
                if flag_run:
                    # GetData
                    t = floor(time()-t0)
                    ts = "%d"%t
                    fx = "%2.2f"%((int(dataSerial[0])/scale)*YCal+XCal)
                    dx = "%2.2f"%(int(dataSerial[1])/100.0)
                    dy = "%2.2f"%(int(dataSerial[2])/100.0)
                    ec = "%2.2f"%(float(fx)/area)
                    dt = "%2.2f"%(float(dx)*dtang)
                    print ts, fx, dx, dy
                    #Data to Labels
                    w.value1.setText(ts)
                    w.value2.setText(fx)
                    w.value3.setText(dx)
                    w.value4.setText(dy)
                    w.value5.setText(ec)
                    w.value6.setText(dt)
                    
                    #Data to table
                    if t%Sp == 0:
                        newdata = QtGui.QTableWidgetItem(ts)
                        w.table.setItem(l,0,newdata)
                        newdata = QtGui.QTableWidgetItem(fx)
                        w.table.setItem(l,1,newdata)
                        newdata = QtGui.QTableWidgetItem(dx)
                        w.table.setItem(l,2,newdata)
                        newdata = QtGui.QTableWidgetItem(dy)
                        w.table.setItem(l,3,newdata)
                        newdata = QtGui.QTableWidgetItem(ec)
                        w.table.setItem(l,4,newdata)
                        newdata = QtGui.QTableWidgetItem(dt)
                        w.table.setItem(l,5,newdata)
                        l=l+1 
                    
def askData():
    global ser

    while True:
        ser.write('d')
        sleep(1)


#thread.start_new_thread( getDataTest, ())
try:
    ser = serial.Serial(port = comport,baudrate = 115200)
    thread.start_new_thread( getData, ())
    thread.start_new_thread( askData, ())

except:
    print ">>>>>>>>>>> Serial Port Error <<<<<<<<<<<<<<"



class PrettyWidget(QtGui.QWidget):
    
    
    def __init__(self):
        super(PrettyWidget, self).__init__()
        self.initUI()
        
        
    def initUI(self):

        fontNumbers = QtGui.QFont("FreeMono",14)
        fontButtons = QtGui.QFont("FreeMono",14)
        
        self.setGeometry(600,300, 1000, 600)
        self.center()
        self.setWindowTitle('Ensayo de Corte Directo')     
        
        #Grid Layout
        grid = QtGui.QGridLayout()
        self.setLayout(grid)
                    
        # Start/Stop/Reset
        btnStart = QtGui.QPushButton('Start', self)
        #btnStart.resize(btnStart.sizeHint())    
        btnStart.setFont(fontButtons)    
        btnStart.clicked.connect(self.start)
        grid.addWidget(btnStart, 0,0,1,1)

        btnStop = QtGui.QPushButton('Stop', self)
        #btnStop.resize(btnStop.sizeHint())    
        btnStop.setFont(fontButtons)    
        btnStop.clicked.connect(self.stop)
        grid.addWidget(btnStop, 0,1,1,1)

        btnReset = QtGui.QPushButton('Reset', self)
        #btnReset.resize(btnReset.sizeHint())    
        btnReset.setFont(fontButtons)    
        btnReset.clicked.connect(self.reset)
        grid.addWidget(btnReset, 0,2,1,1)

        self.labelSp = QtGui.QLabel('Sp(s):', self)
        self.labelSp.setFont(fontNumbers)
        self.labelSp.setAlignment(QtCore.Qt.AlignRight)
        grid.addWidget(self.labelSp,0,4,1,1)

        self.textFrec = QtGui.QLineEdit('1', self)
        self.textFrec.setFont(fontNumbers)
        self.textFrec.setAlignment(QtCore.Qt.AlignLeft)
        grid.addWidget(self.textFrec,0,5,1,1)

        # Import/Export
        btnImport = QtGui.QPushButton('Import CSV', self)
        #btnImport.resize(btnImport.sizeHint())    
        btnImport.setFont(fontButtons  )    
        btnImport.clicked.connect(self.importcsv)
        grid.addWidget(btnImport, 1,0,1,1)

        btnExport = QtGui.QPushButton('Export CSV', self)
        #btnExport.resize(btnExport.sizeHint())    
        btnExport.setFont(fontButtons)    
        btnExport.clicked.connect(self.exportcsv)
        grid.addWidget(btnExport, 1,1,1,1)

        # plot
        btnPlot = QtGui.QPushButton('Plot', self)
        #btnPlot.resize(btnPlot.sizeHint())    
        btnPlot.setFont(fontButtons)    
        btnPlot.clicked.connect(self.plot)
        grid.addWidget(btnPlot, 1,2,1,1)

        # DataLabels
        self.label1 = QtGui.QLabel('t(seg):', self)
        self.label1.setFont(fontNumbers)
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(self.label1,2,0,1,1)

        self.label2 = QtGui.QLabel('Fx(Kg):', self)
        self.label2.setFont(fontNumbers)
        self.label2.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(self.label2,2,1,1,1)

        self.label3 = QtGui.QLabel('Dx(mm):', self)
        self.label3.setFont(fontNumbers)
        self.label3.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(self.label3,2,2,1,1)

        self.label4 = QtGui.QLabel('Dy(mm):', self)
        self.label4.setFont(fontNumbers)
        self.label4.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(self.label4,2,3,1,1)

        self.label5 = QtGui.QLabel('Ec(kg/cm2):', self)
        self.label5.setFont(fontNumbers)
        self.label5.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(self.label5,2,4,1,1)

        self.label6 = QtGui.QLabel('dT(%):', self)
        self.label6.setFont(fontNumbers)
        self.label6.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(self.label6,2,5,1,1)

        # DataValues
        self.value1 = QtGui.QLabel('0.00', self)
        self.value1.setFont(fontNumbers)
        self.value1.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(self.value1,3,0,1,1)

        self.value2 = QtGui.QLabel('0.00', self)
        self.value2.setFont(fontNumbers)
        self.value2.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(self.value2,3,1,1,1)

        self.value3 = QtGui.QLabel('0.00', self)
        self.value3.setFont(fontNumbers)
        self.value3.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(self.value3,3,2,1,1)

        self.value4 = QtGui.QLabel('0.00', self)
        self.value4.setFont(fontNumbers)
        self.value4.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(self.value4,3,3,1,1)

        self.value5 = QtGui.QLabel('0.00', self)
        self.value5.setFont(fontNumbers)
        self.value5.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(self.value5,3,4,1,1)

        self.value6 = QtGui.QLabel('0.00', self)
        self.value6.setFont(fontNumbers)
        self.value6.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(self.value6,3,5,1,1)


        #Canvas and Toolbar
        self.figure = plt.figure(figsize=(10,5))    
        self.canvas = FigureCanvas(self.figure)     
        self.toolbar = NavigationToolbar(self.canvas, self)
        grid.addWidget(self.toolbar, 4,0,1,6)
        grid.addWidget(self.canvas, 5,0,10,4)

        #Empty Table
        items = ["tx(min)","Fx(Kg)","Dx(mm)","Dy(mm)","Ec(kg/cm2)","dT(%)"] 
        self.table = QtGui.QTableWidget(self)
        self.table.setRowCount(1000)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(items)
        grid.addWidget(self.table, 5,4,10,2)

     
        creditsT = 'Tesis: "Diseno e implementacion de un equipo de corte directo para suelos gravosos y su aplicacion en suelos tipicos del Cusco"'
        creditsA = 'Autor: VIRGILIO CHILLIHUANI CHILLIHUANI'

        self.labelCredits = QtGui.QLabel(creditsT, self)
        self.labelCredits.setFont(fontNumbers)
        self.labelCredits.setAlignment(QtCore.Qt.AlignCenter)
        grid.addWidget(self.labelCredits,16,0,1,6)

        self.labelCredits = QtGui.QLabel(creditsA, self)
        self.labelCredits.setFont(fontNumbers)
        self.labelCredits.setAlignment(QtCore.Qt.AlignRight)
        grid.addWidget(self.labelCredits,17,0,1,6)


        """
        #Import CSV Button
        btn1 = QtGui.QPushButton('Import CSV', self)
        #btn1.resize(btn1.sizeHint()) 
        btn1.clicked.connect(self.getCSV)
        grid.addWidget(btn1, 0,0)
        
        #Plot Button
        btn2 = QtGui.QPushButton('Plot', self)
        #btn2.resize(btn2.sizeHint())    
        btn2.clicked.connect(self.plot)
        grid.addWidget(btn2, 0,1)

        #Plot Button
        btn3 = QtGui.QPushButton('Plotty', self)
        #btn3.resize(btn3.sizeHint())    
        btn3.clicked.connect(self.plot)
        grid.addWidget(btn3, 0,2)
        #Label Dx
        lbl1 = QtGui.QLabel('Dx:', self)
        grid.addWidget(lbl1,4,0)
        """
    
        self.show()
    
    def start(self):
        global flag_run,Sp
        Sp = int(w.textFrec.text())
        flag_run = True

    
    def stop(self):
        global flag_run
        flag_run = False
    
    def reset(self):
        global l, w, t0
        w.table.clearContents()
        l=0
        t0=time()

    def importcsv(self):
        global w,l
        filePath = QtGui.QFileDialog.getOpenFileName(self, 
                                                       'Single File',
                                                       '~/Desktop/',
                                                       '*.csv')
        fileHandle = open(filePath, 'r')
        print "Import MDFK!!"
        self.reset()
        while True:
            line = fileHandle.readline()[:-1].split(',')
            if (len(line) != 6) or ((line[0] == '') and (line[2] == '')):
                break

            i=0
            for k in line:
                try:
                    float(k)
                except:
                    break
                newitem = QtGui.QTableWidgetItem(k)
                w.table.setItem(l, i, newitem)
                i = i+1
            print line
            l = l+1

    
    def exportcsv(self):
        path = QtGui.QFileDialog.getSaveFileName(
                self, 'Save File', '', 'CSV(*.csv)')
        if not path.isEmpty():
            with open(unicode(path), 'wb') as stream:
                writer = csv.writer(stream)
                for row in range(self.table.rowCount()):
                    rowdata = []
                    for column in range(self.table.columnCount()):
                        item = self.table.item(row, column)
                        if item is not None:
                            rowdata.append(
                                unicode(item.text()).encode('utf8'))
                        else:
                            rowdata.append('')
                    writer.writerow(rowdata)
        """
        filePath = QtGui.QFileDialog.getOpenFileName(self, 
                                                       'Single File',
                                                       '~/Desktop/',
                                                       '*.csv')
        fileHandle = open(filePath, 'r')
        line = fileHandle.readline()[:-1].split(',')
        for n, val in enumerate(line):
            newitem = QtGui.QTableWidgetItem(val)
            self.table.setItem(0, n, newitem)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()    
        """

    def appendCell(self,vector, f, c):
        try:
            vector.append(float(self.table.item(f, c).text()))
        except:
            print "fatal Error"
            vector.append(np.nan)
            print "nan"
        return vector
    
    def plot(self):
        global typeofPlot
        mt  = []
        mfx = []
        mdx = []
        mdy = []
        mec = []
        mdt = []

        for n in range(l):
            mt  = self.appendCell(mt,n,0)
            mfx = self.appendCell(mfx,n,1)
            mdx = self.appendCell(mdx,n,2)
            mdy = self.appendCell(mdy,n,3)
            mec = self.appendCell(mec,n,4)
            mdt = self.appendCell(mdt,n,5)

        if typeofPlot == 0:
            plt.cla()
            ax = self.figure.add_subplot(111)
            ax.plot(mdt,mec, 'r.-')
            ax.set_title('Esfuezo de corte vs Deformacion Horizontal')
            ax.set_ylabel('Esfuezo de Corte(kg/cm2)')
            ax.set_xlabel('Deformacion Horizontal(%)')
            self.canvas.draw()

        if typeofPlot == 1:
            plt.cla()
            ax = self.figure.add_subplot(111)
            ax.plot(mdt,mdy, 'r.-')
            ax.set_title('Deformacion Vertical vs Horizontal')
            ax.set_ylabel('Deformacion Vertical(mm)')
            ax.set_xlabel('Deformacion Horizontal(%)')
            self.canvas.draw()

        if typeofPlot == 2:
            plt.cla()
            ax = self.figure.add_subplot(111)
            ax.plot(mt,mdx, 'r.-')
            ax.set_title('Deformacion Horizontal vs Tiempo')
            ax.set_ylabel('Deformacion Horizontal(mm)')
            ax.set_xlabel('Tiempo(s)')
            self.canvas.draw()

        if typeofPlot == 3:
            plt.cla()
            ax = self.figure.add_subplot(111)
            ax.plot(mt,mdt, 'r.-')
            ax.set_title('Deformacion Horizontal vs Tiempo')
            ax.set_ylabel('Deformacion Horizontal(%)')
            ax.set_xlabel('Tiempo(s)')
            self.canvas.draw()
            typeofPlot = 0

        typeofPlot = typeofPlot +1; 
    
    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft()) 
    
    
        
def main():
    global w
    app = QtGui.QApplication(sys.argv)
    w = PrettyWidget()
    app.exec_()


if __name__ == '__main__':
    main()