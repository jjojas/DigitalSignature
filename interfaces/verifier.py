from datetime import datetime
import PyQt5.QtWidgets as qtw
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

import modules.keygen as keyg

cipherCache = ""

class verifierWidget(qtw.QWidget):
    def __init__(self, parent):
        super(qtw.QWidget, self).__init__(parent)   
        self.initUI()
    
    def initUI(self):
        def giveMe():
            try:
                p,q,e = keyg.pickKeyforMe()
                ptextBox.setText(str(p))
                qtextBox.setText(str(q))
                etextBox.setText(str(e))
            except Exception as e:
                msg = QMessageBox()
                msg.setText("Parameter gagal dipilih!")
                msg.setInformativeText(f'Parameter gagal ditentukan karena {e}')
                msg.setWindowTitle("Pengacakan gagal")
                msg.exec_()
        def generate():
            try:
                p = int(ptextBox.text())
                q = int(qtextBox.text())
                e = int(etextBox.text())
                now = datetime.now()
                name = saveLine.text()
                keyg.createKeyFile(name,p,q,e)
                s = datetime.now() - now
                msg = QMessageBox()
                msg.setText("Kunci berhasil dibuat!")
                msg.setInformativeText(f'Kunci berhasil dibuat setelah {str(s)}\nKunci publik Anda dapat diakses di key/{saveLine.text()}.pub\nKunci privat Anda dapat diakses di key/{saveLine.text()}.pri ')
                msg.setWindowTitle("Pembangkitan kunci berhasil")
                msg.exec_()
            except Exception as e:
                msg = QMessageBox()
                msg.setText("Kunci gagal dibuat!")
                msg.setInformativeText(f'Kunci anda gagal dibuat karena {e}')
                msg.setWindowTitle("Pembangkitan kunci gagal")
                msg.exec_()

        self.layout = qtw.QGridLayout(self)
        self.setLayout(self.layout)

        ParameterLayout = qtw.QGroupBox()
        ParameterLayout.setLayout(qtw.QGridLayout())        

        ptextLabel = qtw.QLabel("Parameter", self)
        getFont = ptextLabel.font()
        getFont.setBold(True)
        ptextLabel.setFont(getFont)

        ParameterLayout.layout().addWidget(ptextLabel,0,0,1,2,Qt.AlignTop)

        ptextLabel = qtw.QLabel("P:", self)
        ptextBox = qtw.QLineEdit(self)

        ParameterLayout.layout().addWidget(ptextLabel,1,0,Qt.AlignLeft)
        ParameterLayout.layout().addWidget(ptextBox,1,1,Qt.AlignLeft)

        qtextLabel = qtw.QLabel("Q:", self)
        qtextBox = qtw.QLineEdit(self)

        ParameterLayout.layout().addWidget(qtextLabel,2,0,Qt.AlignLeft)
        ParameterLayout.layout().addWidget(qtextBox,2,1,Qt.AlignLeft)

        etextLabel = qtw.QLabel("E:", self)
        etextBox = qtw.QLineEdit(self)

        ParameterLayout.layout().addWidget(etextLabel,3,0,Qt.AlignLeft)
        ParameterLayout.layout().addWidget(etextBox,3,1,Qt.AlignLeft)
        
        randomButton = qtw.QPushButton("Randomize Parameters")  
        randomButton.clicked.connect(lambda: giveMe()) 
        ParameterLayout.layout().addWidget(randomButton,4,0,1,2,Qt.AlignVCenter)

        self.layout.addWidget(ParameterLayout,0,0)

        saveBoxLayout = qtw.QGroupBox()
        saveBoxLayout.setLayout(qtw.QVBoxLayout())
        saveLabel = qtw.QLabel("Simpan Kunci", self)
        saveLabel.setFont(getFont)
        saveNameLabel = qtw.QLabel("Nama Kunci:", self)
        saveLine = qtw.QLineEdit(self)
        saveButton = qtw.QPushButton("Bangkitkan dan Simpan")  
        saveButton.clicked.connect(lambda: generate()) 

        saveBoxLayout.layout().addWidget(saveLabel,0,Qt.AlignTop)
        saveBoxLayout.layout().addWidget(saveNameLabel,1,Qt.AlignVCenter)   
        saveBoxLayout.layout().addWidget(saveLine,1,Qt.AlignVCenter)
        saveBoxLayout.layout().addWidget(saveButton,2,Qt.AlignVCenter)

        self.layout.addWidget(saveBoxLayout,0,1)
