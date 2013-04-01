from PyQt4 import QtCore, QtGui
import sys, cPickle

class Ui_MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi()
        with open('dev_dict.data', 'rb') as fl:
            self.dic = cPickle.load(fl)
        with open('./processed/citation_weights', 'rb') as fl:
            self.cit = cPickle.load(fl)
        self.setupData()
        self.postings = open('dev_postings.data', 'rb')
        
    def setupData(self):
        data = QtGui.QStandardItemModel()
        for k,v in self.dic.iteritems():
            data.appendRow(QtGui.QStandardItem(QtCore.QString(str(k.encode('utf-8'))+str(v).encode('utf-8'))))
        self.lv.setModel(data)
        self.lv.clicked.connect(self.clicked_dict)

        c_data = QtGui.QStandardItemModel()
        for k,v in self.cit.iteritems():
            c_data.appendRow(QtGui.QStandardItem(QtCore.QString(str(k).encode('utf-8')+' -> '+str(v).encode('utf-8'))))
        self.lv_3.setModel(c_data)

        
    def clicked_dict(self, e):
        string = e.data().toPyObject()
        # token = string.split('(')[0]
        seek = int(string.split('(')[1].split(',')[1])
        p = self.postings
        p.seek(seek)
        results = cPickle.load(p)
        self.load_res(results)

    def load_res(self, res):
        data = QtGui.QStandardItemModel()
        for r in res:
            data.appendRow(QtGui.QStandardItem(QtCore.QString(str(r).encode('utf-8'))))
        self.lv_2.setModel(data)
            
    
        
    def setupUi(self):
        self.setObjectName(_fromUtf8("MainWindow"))
        self.resize(890, 521)
        self.centralWidget = QtGui.QWidget(self)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.lv = QtGui.QListView(self.centralWidget)
        self.lv.setGeometry(QtCore.QRect(0, 0, 400, 461))
        self.lv.setObjectName(_fromUtf8("listView"))
        self.lv_2 = QtGui.QListView(self.centralWidget)
        self.lv_2.setGeometry(QtCore.QRect(400, 0, 400, 461))
        self.lv_2.setObjectName(_fromUtf8("listView_2"))
        self.lv_3 = QtGui.QListView(self.centralWidget)
        self.lv_3.setGeometry(QtCore.QRect(800, 0, 400, 461))
        self.lv_3.setObjectName(_fromUtf8("listView_3"))



        self.setCentralWidget(self.centralWidget)



        self.menuBar = QtGui.QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 890, 22))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(self)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(self)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        self.setStatusBar(self.statusBar)

        QtCore.QMetaObject.connectSlotsByName(self)

        
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    u = Ui_MainWindow()
    u.show()
    sys.exit(app.exec_())
