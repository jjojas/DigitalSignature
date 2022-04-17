import PyQt5.QtWidgets as qtw
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

import modules.verifier as ver

cipherCache = ""

class verifierWidget(qtw.QWidget):
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
                fileName, _ = qtw.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Public key files (*.pub)", options=options)
                if fileName:
                    E,N = str(open(fileName,"rb").read().decode("ISO-8859-1")).split("|")
                    ktextLabel.setText(f"E: {E}\nN: {N}")
                else:
                    ktextLabel.setText("Tidak ada kunci dipilih")
            except Exception as e:
                msg = QMessageBox()
                msg.setText("File key gagal dipilih")
                msg.setInformativeText(f'File key anda gagal dipilih karena {e}')
                msg.setWindowTitle("File gagal")
                msg.exec_()

        def pickSign():
            try:
                options = qtw.QFileDialog.Options()
                options |= qtw.QFileDialog.DontUseNativeDialog
                fileName, _ = qtw.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Txt files (*.txt)", options=options)
                if fileName:
                    stextLabel.setText(fileName)
                else:
                    stextLabel.setText("Tidak ada tanda tangan dipilih")
            except Exception as e:
                msg = QMessageBox()
                msg.setText("File gagal dipilih")
                msg.setInformativeText(f'File anda gagal dipilih karena {e}')
                msg.setWindowTitle("File gagal")
                msg.exec_()

        def verify():
            try:
                if ("Tidak ada file dipilih" in ftextLabel.text()):
                        raise(Exception("file belum dipilih!"))
                elif ("Tidak ada kunci dipilih" in ktextLabel.text()):
                        raise(Exception("kunci belum dipilih!"))
                else:
                        E,N = ktextLabel.text().split("\n")
                        E,N = int(E.split(" ")[-1]),int(N.split(" ")[-1])
                        if (self.b1.isChecked()):
                            filebytes,signature = ver.extractFile(ftextLabel.text())
                        else:
                            if ("Tidak ada tanda tangan dipilih" in stextLabel.text()):
                                raise(Exception("tanda tangan belum dipilih!"))
                            else:
                                filebytes,signature = ver.openFile(ftextLabel.text(),stextLabel.text())
                        
                        print(f"Check res {ver.verifyFile(filebytes,signature,E,N)}")
                        if (ver.verifyFile(filebytes,signature,E,N)):
                                msg = QMessageBox()
                                msg.setText("Tanda tangan berhasil diverifikasi!")
                                msg.setInformativeText('File anda tidak mengalami perubahan')
                                msg.setWindowTitle("Verified!")
                                msg.exec_()
                        else:
                            msg = QMessageBox()
                            msg.setText("Tanda tangan gagal diverifikasi!")
                            msg.setInformativeText('File anda mengalami perubahan dan isinya sudah tidak dapat dijamin!')
                            msg.setWindowTitle("Not Verified!")
                            msg.exec_()
            except Exception as e:
                msg = QMessageBox()
                msg.setText("Verifikasi gagal!")
                msg.setInformativeText(f'Verifikasi gagal dilakukan karena {e}')
                msg.setWindowTitle("Verifikasi gagal")
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

        ftextLabel = qtw.QLabel("Tidak ada file dipilih!", self)

        FilePickerLayout.layout().addWidget(ftextLabel,1,0,Qt.AlignLeft)
        
        FilePickButton = qtw.QPushButton("Pilih File")  
        FilePickButton.clicked.connect(lambda: pickFile()) 
        FilePickerLayout.layout().addWidget(FilePickButton,4,0,1,2,Qt.AlignVCenter)

        self.layout.addWidget(FilePickerLayout,0,0)


        KeyPickerLayout = qtw.QGroupBox()
        KeyPickerLayout.setLayout(qtw.QGridLayout())        

        ktextLabel = qtw.QLabel("Pilih Kunci publik", self)
        ktextLabel.setFont(getFont)

        KeyPickerLayout.layout().addWidget(ktextLabel,0,0,1,2,Qt.AlignTop)

        ktextLabel = qtw.QLabel("Tidak ada kunci dipilih", self)

        KeyPickerLayout.layout().addWidget(ktextLabel,2,0,Qt.AlignLeft)
        
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

        SignTypeLayout.layout().addWidget(self.b1,1,0,Qt.AlignLeft)

        self.b2 = qtw.QRadioButton("Tanda tangan terpisah")

        SignTypeLayout.layout().addWidget(self.b2,2,0,Qt.AlignLeft)
        
        self.layout.addWidget(SignTypeLayout,2,0)

        SignPickerLayout = qtw.QGroupBox()
        SignPickerLayout.setLayout(qtw.QGridLayout())        

        stextTitle = qtw.QLabel("Pilih tanda tangan", self)
        stextTitle.setFont(getFont)

        SignPickerLayout.layout().addWidget(stextTitle,0,0,1,2,Qt.AlignTop)

        stextLabel = qtw.QLabel("Tidak ada tanda tangan dipilih", self)

        SignPickerLayout.layout().addWidget(stextLabel,2,0,Qt.AlignLeft)
        
        sPickButton = qtw.QPushButton("Pilih File")  
        sPickButton.clicked.connect(lambda: pickSign()) 
        SignPickerLayout.layout().addWidget(sPickButton,4,0,1,2,Qt.AlignVCenter)

        self.layout.addWidget(SignPickerLayout,3,0)


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

        SignMeButton = qtw.QPushButton("Verifikasi Tanda Tangan")  
        SignMeButton.clicked.connect(lambda: verify()) 
        self.layout.addWidget(SignMeButton,2,1,Qt.AlignVCenter)