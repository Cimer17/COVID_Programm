from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
from PyQt5 import QtGui



def image_processing(path):
    model = load_model('keras_model.h5')
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(path).convert('RGB')
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    if prediction[0][0] > prediction[0][1]:
        return f' Пневмания с вероятностью  {prediction[0][0] * 100}%'
    else:
        return f' Лёгкие чистые с вероятностью  {prediction[0][1] * 100}%'


class MainWindow(QDialog):
    
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("gui.ui",self)
        self.browse.clicked.connect(self.browsefiles)
        self.btn_go.clicked.connect(self.btn_clicker)
        self.btn_go.setEnabled(False)

    def browsefiles(self):
        fname=QFileDialog.getOpenFileName(self, 'Open file', 'D:\codefirst.io\PyQt5 tutorials\Browse Files', 'Images (*.png, *.xmp *.jpg *.jpeg)')
        self.filename.setText(fname[0])
        self.total.setText('')
        if self.filename.text() != '':
            self.btn_go.setEnabled(True)
        else:
            self.btn_go.setEnabled(False)
    
    def btn_clicker(self):
        self.path = self.filename.text()
        if self.path == '':
            self.total.setText('Ошибка : Вы не загрузили фотографию')
        else:
            self.result = image_processing(self.path)
            self.total.setText(self.result)


app=QApplication(sys.argv)
mainwindow=MainWindow()
mainwindow.setWindowTitle('ПневмоТестер')
mainwindow.setWindowIcon(QtGui.QIcon('ico.png'))
app.setWindowIcon(QtGui.QIcon('ico.png'))
widget=QtWidgets.QStackedWidget()
widget.setWindowIcon(QtGui.QIcon('ico.png'))
widget.addWidget(mainwindow)
widget.setFixedWidth(400)
widget.setFixedHeight(300)
widget.show()
sys.exit(app.exec_())