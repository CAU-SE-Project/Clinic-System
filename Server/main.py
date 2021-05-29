from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import socket
import server
import logging

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
port = 5614

class Connection():
  def __init__(self):
    self.requestConnection()

  def requestConnection(self):
    self.serverIP = server.Server(self)
    #self.dbIP =

class Chat():
  def inputStream(self):
    return self.sendmsg.text()

  def checkNull(self, stream):
    if len(stream) == 0:
      return True
    else :
      return False

class Sender(Chat):
  def sendChat(self):
    if not self.serverIP.bListen:
      self.sendmsg.clear()
      return
    #sendmsg = self.sendmsg.text()
    sendmsg = super().inputStream()

    if super().checkNull(sendmsg):
      pass
    else :
      self.updateMsg(sendmsg)
      #print(self.ip.text(),self.port.text(), sendmsg)
      self.serverIP.send(sendmsg)
      self.sendmsg.clear()

class Displayer(Chat):
  def displayChat(self):
    self.setWindowTitle('Clinic System Server')

    # 서버 설정 부분
    ipbox = QHBoxLayout()

    gb = QGroupBox('Server Setting')
    ipbox.addWidget(gb)

    box = QHBoxLayout()

    label = QLabel('Server IP')
    self.ip = QLineEdit(socket.gethostbyname(socket.gethostname()))
    box.addWidget(label)
    box.addWidget(self.ip)

    label = QLabel('Server Port')
    self.port = QLineEdit(str(port))
    box.addWidget(label)
    box.addWidget(self.port)

    self.btn = QPushButton('Run')
    self.btn.setCheckable(True)
    self.btn.toggled.connect(self.toggleButton)
    box.addWidget(self.btn)

    gb.setLayout(box)

    # 접속자 정보 부분
    infobox = QHBoxLayout()
    gb = QGroupBox('Client Info')
    infobox.addWidget(gb)

    box = QHBoxLayout()

    self.guest = QTableWidget()
    self.guest.setColumnCount(2)
    self.guest.setHorizontalHeaderItem(0, QTableWidgetItem('IP'))
    self.guest.setHorizontalHeaderItem(1, QTableWidgetItem('Port'))

    box.addWidget(self.guest)
    gb.setLayout(box)

    # 채팅창 부분
    gb = QGroupBox('Message')
    infobox.addWidget(gb)

    box = QVBoxLayout()

    label = QLabel('Received Message')
    box.addWidget(label)

    self.msg = QListWidget()
    box.addWidget(self.msg)

    label = QLabel('Send Message')
    box.addWidget(label)

    self.sendmsg = QLineEdit()
    box.addWidget(self.sendmsg)

    hbox = QHBoxLayout()

    self.sendbtn = QPushButton('Send')
    self.sendbtn.clicked.connect(self.sendChat)
    hbox.addWidget(self.sendbtn)

    self.clearbtn = QPushButton('Clear Chat')
    self.clearbtn.clicked.connect(self.clearMsg)
    hbox.addWidget(self.clearbtn)

    box.addLayout(hbox)

    gb.setLayout(box)

    # 전체 배치
    vbox = QVBoxLayout()
    vbox.addLayout(ipbox)
    vbox.addLayout(infobox)
    self.setLayout(vbox)

    self.show()

  def toggleButton(self, state):
    if state:
      ip = self.ip.text()
      port = self.port.text()
      if self.serverIP.start(ip, int(port)):
        self.btn.setText('Shutdown')
    else:
      self.serverIP.stop()
      self.msg.clear()
      self.btn.setText('Run')

  def clearMsg(self):
    self.msg.clear()

  def closeEvent(self, e):
      self.serverIP.stop()

class DatabaseConnection(Chat):
  def updateClient(self, addr, isConnect=False):
    row = self.guest.rowCount()
    if isConnect:
      self.guest.setRowCount(row + 1)
      self.guest.setItem(row, 0, QTableWidgetItem(addr[0]))
      self.guest.setItem(row, 1, QTableWidgetItem(str(addr[1])))
      #print(addr[0], addr[1])
    else:
      for r in range(row):
        ip = self.guest.item(r, 0).text()  # ip
        port = self.guest.item(r, 1).text()  # port
        if addr[0] == ip and str(addr[1]) == port:
          self.guest.removeRow(r)
          break

  def updateMsg(self, msg):
    self.msg.addItem(QListWidgetItem(msg))
    self.msg.setCurrentRow(self.msg.count() - 1)

class Controller(QWidget, Connection, Sender, Displayer, DatabaseConnection):
  def __init__(self):
    self.enterClinic()
    self.displayChat()

  def enterClinic(self):
    super().__init__()



if __name__ == '__main__':
  app = QApplication(sys.argv)
  w = Controller()
  sys.exit(app.exec_())