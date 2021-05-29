from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import client

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
port = 5614

class Connection():
  def __init__(self):
    self.requestConnection()

  def requestConnection(self):
    self.clientIP = client.ClientSocket(self)

class Chat():
  def inputStream(self):
    return self.sendmsg.toPlainText()

  def checkNull(self, stream):
    if len(stream) == 0:
      return True
    else :
      return False

class Sender(Chat):
  def sendChat(self):
    sendmsg = super().inputStream()

    if super().checkNull(sendmsg):
      pass
    else :
      self.clientIP.send(sendmsg)
      self.sendmsg.clear()

class Displayer():
  def displayChat(self):
    self.setWindowTitle('Clinic System Client')

    # 클라이언트 설정 부분
    ipbox = QHBoxLayout()

    gb = QGroupBox('Server Connection')
    ipbox.addWidget(gb)

    box = QHBoxLayout()

    label = QLabel('Server IP')
    self.ip = QLineEdit()
    self.ip.setInputMask('000.000.000.000;_')
    box.addWidget(label)
    box.addWidget(self.ip)

    label = QLabel('Server Port')
    self.port = QLineEdit(str(port))
    box.addWidget(label)
    box.addWidget(self.port)

    self.btn = QPushButton('Connect')
    self.btn.clicked.connect(self.connectClicked)
    box.addWidget(self.btn)

    gb.setLayout(box)

    # 채팅창 부분
    infobox = QHBoxLayout()
    gb = QGroupBox('Chatting')
    infobox.addWidget(gb)

    box = QVBoxLayout()

    label = QLabel('Received Message')
    box.addWidget(label)

    self.recvmsg = QListWidget()
    box.addWidget(self.recvmsg)

    label = QLabel('Send Message')
    box.addWidget(label)

    self.sendmsg = QTextEdit()
    self.sendmsg.setFixedHeight(50)
    box.addWidget(self.sendmsg)

    hbox = QHBoxLayout()

    box.addLayout(hbox)
    self.sendbtn = QPushButton('Send')
    self.sendbtn.setAutoDefault(True)
    self.sendbtn.clicked.connect(self.sendChat)

    self.clearbtn = QPushButton('Clear Chat')
    self.clearbtn.clicked.connect(self.clearMsg)

    hbox.addWidget(self.sendbtn)
    hbox.addWidget(self.clearbtn)
    gb.setLayout(box)

    # 전체 배치
    vbox = QVBoxLayout()
    vbox.addLayout(ipbox)
    vbox.addLayout(infobox)
    self.setLayout(vbox)

    self.show()

  def clearMsg(self):
    self.recvmsg.clear()

  def closeEvent(self, e):
    self.clientIP.stop()

class DatabaseConnection(Chat):
  def connectClicked(self):
    if self.clientIP.bConnect == False:
      ip = self.ip.text()
      port = self.port.text()
      if self.clientIP.connectServer(ip, int(port)):
        self.btn.setText('Shutdown')
      else:
        self.clientIP.stop()
        self.sendmsg.clear()
        self.recvmsg.clear()
        self.btn.setText('Connect')
    else:
      self.clientIP.stop()
      self.sendmsg.clear()
      self.recvmsg.clear()
      self.btn.setText('Connect')

  def updateMsg(self, msg):
    self.recvmsg.addItem(QListWidgetItem(msg))

  def updateDisconnect(self):
    self.btn.setText('Connect')

class Controller(QWidget, Connection, Sender, Displayer, DatabaseConnection):
  def __init__(self):
    self.enterClinic()
    self.displayChat()

  def enterClinic(self):
    super().__init__()

  def __del__(self):
    self.clientIP.stop()


if __name__ == '__main__':
  app = QApplication(sys.argv)
  w = Controller()
  sys.exit(app.exec_())
