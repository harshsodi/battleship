from PyQt4 import QtGui, QtCore
import socket,sys,thread,json

class Game(QtGui.QMainWindow):
    def __init__(self,master=None):
        QtGui.QMainWindow.__init__(self, master)
        self.setWindowTitle("Ba Ba BattleShip")

        self.createUI()
        self.getList(["Jay","Harsh"])
        self.fillList()

    def createUI(self):

        self.widget = QtGui.QWidget(self)
        self.container = QtGui.QVBoxLayout()
        self.setCentralWidget(self.widget)
       

        self.selectplayerwidget = QtGui.QWidget()

        self.VBox = QtGui.QVBoxLayout()

        self.playerlistwidget = QtGui.QListWidget()

        self.ChallangeButton = QtGui.QPushButton("Challange")
        self.connect(self.ChallangeButton,QtCore.SIGNAL("clicked()"),self.sendChallenge)

        
        self.VBox.addWidget(self.playerlistwidget)
        self.VBox.addWidget(self.ChallangeButton)

        self.selectplayerwidget.setLayout(self.VBox)


        self.container.addWidget(self.selectplayerwidget)
        self.widget.setLayout(self.container)

    def sendChallenge(self):
        
        if self.playerlistwidget.currentItem().isSelected():
            name = self.playerlistwidget.currentItem().text()
            #print name
            self.gotChallenge(name)
        else:
            msg = QtGui.QMessageBox()
            msg.setText("please select an online player")
            msg.exec_()

        

    def gotChallenge(self,playername):
        result = QtGui.QMessageBox.question(self, 'challenge',playername +" challenged you \n\n accept challange ?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
        if result == QtGui.QMessageBox.Yes:
            pass
        else:
            pass

    def getList(self,plist):

        self.playerlist = plist

    def fillList(self):

        for eachplayer in self.playerlist:
            self.playerlistwidget.addItem(eachplayer)


def cpu(mysocket,msgtype,msgdata):
    pass

def listener(mysocket):
    while True:
        msg = mysocket.recv(1024)

        msg = json.loads(msg)

        msgtype = msg["type"]
        msgdata = msg["data"]




if __name__ == "__main__":

    mysocket = socket.socket()
    host = socket.gethostname()

    port  = 7064

    try:
        mysocket.connect((host,port))
    except:
        print "could not connect to server"
        sys.exit(1)

    print "connected"

    thread.start_new_thread()

    app = QtGui.QApplication(sys.argv)
    game = Game()
    game.show()
    game.resize(640, 480)
    sys.exit(app.exec_())
