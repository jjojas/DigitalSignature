from datetime import datetime
import PyQt5.QtWidgets as qtw
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

import modules.digitalsign as digs

cipherCache = ""

class digitalSignWidget(qtw.QWidget):
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)   
        self.initUI()
    
    def initUI(self):
        def pickFile():
            try:
                options = qtw.QFileDialog.Options()
                options |= qtw.QFileDialog.DontUseNativeDialog
                fileName, _ = qtw.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All files (*)", options=options)
                if fileName:
                    ftextLabel.setText(fileName)
                    FileDetail.setPlainText(str(open(fileName,"rb").read().decode("ISO-8859-1")))
                else:
                    ftextLabel.setText("Tidak ada file dipilih")
                    FileDetail.setPlainText("")
            except Exception as e:
                msg = QMessageBox()
                msg.setText("File gagal dipilih")
                msg.setInformativeText(f'File anda gagal dipilih karena {e}')
                msg.setWindowTitle("File gagal")
                msg.exec_()

        def pickKey():
            try:
                options = qtw.QFileDialog.Options()
                options |= qtw.QFileDialog.DontUseNativeDialog
                fileName, _ = qtw.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Private key files (*.pri)", options=options)
                if fileName:
                    D,N = str(open(fileName,"rb").read().decode("ISO-8859-1")).split("|")
                    ktextLabel.setText(f"D: {D}\nN: {N}")
                else:
                    ktextLabel.setText("Tidak ada kunci dipilih")
            except Exception as e:
                msg = QMessageBox()
                msg.setText("File key gagal dipilih")
                msg.setInformativeText(f'File key anda gagal dipilih karena {e}')
                msg.setWindowTitle("File gagal")
                msg.exec_()

        def sign():
            try:
                if ("Tidak ada file dipilih" in ftextLabel.text()):
                        raise(Exception("file belum dipilih!"))
                elif ("Tidak ada kunci dipilih" in ktextLabel.text()):
                        raise(Exception("kunci belum dipilih!"))
                else:
                        D,N = ktextLabel.text().split("\n")
                        D,N = int(D.split(" ")[-1]),int(N.split(" ")[-1])
                        sign = digs.createSignature(ftextLabel.text(),D,N)
                        if (self.b1.isChecked()):
                            digs.embedKey(sign,ftextLabel.text())
                            msg = QMessageBox()
                            msg.setText("Tanda tangan berhasil!")
                            msg.setInformativeText(f'File dengan tanda tangan berhasil dibuat di files/signed_{ftextLabel.text().split("/")[-1]}')
                            msg.setWindowTitle("Signed!")
                            msg.exec_()
                        elif (self.b2.isChecked()):
                            digs.saveKey(sign,ftextLabel.text().split("/")[-1].split(".")[0])
                            msg = QMessageBox()
                            msg.setText("Tanda tangan berhasil!")
                            msg.setInformativeText(f'Tanda tangan berhasil dibuat di signature/{ftextLabel.text().split("/")[-1].split(".")[0]}_signature.txt')
                            msg.setWindowTitle("Signed!")
                            msg.exec_()
            except Exception as e:
                msg = QMessageBox()
                msg.setText("Tanda tangan gagal!")
                msg.setInformativeText(f'Tanda tangan gagal dilakukan karena {e}')
                msg.setWindowTitle("Tanda tangan gagal")
                msg.exec_()


        self.layout = qtw.QGridLayout(self)
        self.setLayout(self.layout)


        FilePickerLayout = qtw.QGroupBox()
        FilePickerLayout.setLayout(qtw.QGridLayout())        

        ftextLabel = qtw.QLabel("Pilih File", self)
        getFont = ftextLabel.font()
        getFont.setBold(True)
        ftextLabel.setFont(getFont)

        FilePickerLayout.layout().addWidget(ftextLabel,0,0,1,2,Qt.AlignTop)

        ftextLabel = qtw.QLabel("Tidak ada file dipilih", self)

        FilePickerLayout.layout().addWidget(ftextLabel,1,0,Qt.AlignLeft)
        
        FilePickButton = qtw.QPushButton("Pilih File")  
        FilePickButton.clicked.connect(lambda: pickFile()) 
        FilePickerLayout.layout().addWidget(FilePickButton,4,0,1,2,Qt.AlignVCenter)

        self.layout.addWidget(FilePickerLayout,0,0)


        KeyPickerLayout = qtw.QGroupBox()
        KeyPickerLayout.setLayout(qtw.QGridLayout())        

        ktextLabel = qtw.QLabel("Pilih Kunci Privat", self)
        ktextLabel.setFont(getFont)

        KeyPickerLayout.layout().addWidget(ktextLabel,0,0,1,2,Qt.AlignTop)

        ktextLabel = qtw.QLabel("Tidak ada kunci dipilih", self)

        KeyPickerLayout.layout().addWidget(ktextLabel,1,0,Qt.AlignLeft)
        
        KeyPickButton = qtw.QPushButton("Pilih File")  
        KeyPickButton.clicked.connect(lambda: pickKey()) 
        KeyPickerLayout.layout().addWidget(KeyPickButton,4,0,1,2,Qt.AlignVCenter)

        self.layout.addWidget(KeyPickerLayout,1,0)
    
        SignTypeLayout = qtw.QGroupBox()
        SignTypeLayout.setLayout(qtw.QGridLayout())        

        stextLabel = qtw.QLabel("Tipe Tanda Tangan", self)
        stextLabel.setFont(getFont)

        SignTypeLayout.layout().addWidget(stextLabel,0,0,1,2,Qt.AlignTop)

        self.b1 = qtw.QRadioButton("Tanda tangan dalam file")
        self.b1.setChecked(True)
        # self.b1.toggled.connect(lambda:self.btnstate(self.b1))

        SignTypeLayout.layout().addWidget(self.b1,1,0,Qt.AlignLeft)

        self.b2 = qtw.QRadioButton("Tanda tangan terpisah")
        # self.b2.toggled.connect(lambda:self.btnstate(self.b2))

        SignTypeLayout.layout().addWidget(self.b2,2,0,Qt.AlignLeft)
        
        self.layout.addWidget(SignTypeLayout,2,0)

        FileDisplayLayout = qtw.QGroupBox()
        FileDisplayLayout.setLayout(qtw.QVBoxLayout())

        FileDisplayTitle = qtw.QLabel("Konten File",self)
        FileDisplayTitle.setFont(getFont)

        FileDetail = qtw.QPlainTextEdit(self)
        FileDetail.setReadOnly(True)
        FileDetail.setPlainText("")

        FileDisplayLayout.layout().addWidget(FileDisplayTitle,0,Qt.AlignTop)
        FileDisplayLayout.layout().addWidget(FileDetail,1,Qt.AlignVCenter)

        self.layout.addWidget(FileDisplayLayout,0,1,2,1)

        SignMeButton = qtw.QPushButton("Tanda Tangan")  
        SignMeButton.clicked.connect(lambda: sign()) 
        self.layout.addWidget(SignMeButton,2,1,Qt.AlignVCenter)


