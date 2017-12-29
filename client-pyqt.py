from PyQt4 import QtGui, QtCore
import socket,sys,threading,json

ships = None
name = None

def getMyShips(name) :
    global ships
    return ships[name]

def getOpponentShips(name) :
    global ships
    for player in ships :
        if player != name :
            return ships[player]


class battle(QtGui.QWidget):

    def __init__(self):
        super(battle, self).__init__()
        self.initUI()
        self.setMouseTracking(True)
        self.customInit()

    def customInit(self):
        self.myAttackedBlocks = []
        self.opponentAttackedBlocks = []
        self.turn = False
        self.mouseOn = [9999,9999]


    def resetMouseOn(slef) :
        self.mouseOn = [9999,9999]

    def setMouseOn(self, x, y) :
        self.mouseOn = [x,y]

    def myInit(self):
        global name
        self.myShips = getMyShips(name)
        self.opponentShips =getOpponentShips(name)
        print self.myShips
        print self.opponentShips

    def initTurn(self) : 
        self.turn = True

        
    def initUI(self):      

        self.setGeometry(50, 50, 1050, 500)
        self.setWindowTitle('Battle captains ..!')
        self.show()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        #self.myInit()
        self.drawBoards(qp)
        qp.end()

    def mapCoords(self, coords, baseX, baseY) :
        return (coords[0]+baseX, coords[1]+baseY)

    def drawBoards(self, qp):
        pen = QtGui.QPen(QtCore.Qt.white, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        
        #print "drawing now xD" + str(self.myShips)

        #if opponent's turn I fade to white
        fade = 140
        try :
            if not self.turn :
                fade = 255
            else:
                fade = 140
        except :
            print ""

        #draw my board
        for x in range(10) :
            for y in range(10) :
                qp.setBrush(QtGui.QColor(150, 170, 255,fade))
                pen = QtGui.QPen(QtCore.Qt.white, 2, QtCore.Qt.SolidLine)
                qp.setPen(pen)
                
                flag = True
                if [x,y] in self.myAttackedBlocks :
                    qp.setBrush(QtGui.QColor(255,100,100,fade))
                    flag = False

                if flag :
                    for ship in self.myShips :
                        if [x,y] in ship :
                            pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
                            qp.setPen(pen)
                            qp.setBrush(QtGui.QColor(255,255,255,fade))
                            break
                    
                qp.drawRect(x*50,y*50, 50,50)

        fade = 255
        try :
            if self.turn :
                fade = 255
            else:
                fade = 140
        except : 
            print ""

        #draw opponent board
        for x in range(10) :
            for y in range(10) :
                qp.setBrush(QtGui.QColor(150, 170, 255,fade))

                if [x+11,y] == self.mouseOn and self.turn:
                    qp.setBrush(QtGui.QColor(255,69,0,140))
                if [x,y] in self.opponentAttackedBlocks :
                    qp.setBrush(QtGui.QColor(255,100,100,fade))
                qp.drawRect((x+11)*50,y*50, 50,50)
        
        if not self.turn :
            opponentsString = "OPPONENT'S"
            turnString = "TURN"
            pen = QtGui.QPen(QtCore.Qt.white, 2, QtCore.Qt.SolidLine)
            qp.setPen(pen)
            qp.setBrush(QtGui.QColor(255,0,0))
            for x in range(len(opponentsString)) :
                qp.drawText((x+11)*50+25, 4*50-25, opponentsString[x])
            for x in range(len(turnString)) :
                qp.drawText((x+11)*50+25, 5*50-25, turnString[x])

        else :
            turnString = "YOUR TURN"
            pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
            qp.setPen(pen)
            qp.setBrush(QtGui.QColor(255,0,0))
            for x in range(len(turnString)) :
                qp.drawText((x)*50+25, 4*50-25, turnString[x])
        

    def mousePressEvent(self, event):
        """
        mouse clicks events
        """
        button = event.button()
        x = event.x()/50
        y = event.y()/50
        
        qp1 = QtGui.QPainter()
        qp1.begin(self)
        qp1.setBrush(QtGui.QColor(255, 100, 100))
        #self.myInit()
        qp1.drawRect((x)*50,y*50, 50,50)
        qp1.end()

        x = x - 11
        if self.turn :
            if x in range(10) and y in range(10) :
                print "attack on ",x,y
                self.attackOnOpponent([x,y])
                
                #send message of attack to server
                dictData = {
                    'type' : 'attack',
                    'data' : {
                        'coordinates' : (x,y)
                    }
                }
                jsonData = json.dumps(dictData)
                mysocket.send(jsonData)
            
    def mouseMoveEvent(self, event):
        x = event.x()/50
        y = event.y()/50
        self.setMouseOn(x,y)
        self.update()

    def attackOnMe(self, coords) :
        print "i am attacked"
        print self.myShips
        for ship in self.myShips :
            if coords in ship :
                self.myAttackedBlocks.append(coords)
            #if set(ship).issubset(set(self.myAttackedBlocks)) : #ship sunk
             #   self.myShips.remove(ship)
              
              #  for coord in ship :
               #     self.myAttackedBlocks.remove(coord)
        print self.myAttackedBlocks
        self.turn = True
        self.update()

    def attackOnOpponent(self, coords) :
        for ship in self.opponentShips :
            if coords in ship :
                self.opponentAttackedBlocks.append(coords)
        self.turn = False
            #if set(ship).issubset(set(self.opponentAttackedBlocks)) : #ship sunk
             #   self.opponentShips.remove(ship)
              #  for coord in ship :
               #     self.opponentAttackedBlocks.remove(coord)

        self.update()

    def win(self) :
        print "You win"

    def loose(self) :
        print "You loose"

    def get(self) :
        return self.myShips



class setBoats(QtGui.QWidget):

    def __init__(self):
        super(setBoats, self).__init__()
        self.initUI()
        self.setMouseTracking(True)
        self.myInit()
    
    def myInit(self):
        self.boats = [5,4,3,2]
        self.currentBoat = 0
        self.selectedBlocks = []
        self.selectedBoats = []
        self.orientation = 0 #0->horizontal and 1->vertical

        self.brownBoxes = []
        self.clickable = True
        self.update()

    def initUI(self):      

        self.setGeometry(50, 50, 500, 500)
        self.setWindowTitle('Pen styles')
        self.show()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()
        
    def drawLines(self, qp):
        pen = QtGui.QPen(QtCore.Qt.white, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        for x in range(10) :
            for y in range(10) :
                if (x,y) not in self.brownBoxes and (x,y) not in self.selectedBlocks :
                    qp.setBrush(QtGui.QColor(150, 170, 255))
                    qp.drawRect(x*50,y*50,50,50)
                else :
                    qp.setBrush(QtGui.QColor(255,255,255))
                    qp.drawRect(x*50,y*50,50,50)

    def updateBoxes(self, headBoxX, headBoxY) :
        self.clickable = True
        self.brownBoxes = []
        for i in range(self.boats[self.currentBoat]) :
            if self.orientation == 0 :
                if headBoxX+i > 9 or (headBoxX+i, headBoxY) in self.selectedBlocks:
                    self.clickable = False
                self.brownBoxes.append((headBoxX+i , headBoxY)) 
            if self.orientation == 1 :
                if headBoxY+i > 9 or (headBoxX, headBoxY+i) in self.selectedBlocks:
                    self.clickable = False
                self.brownBoxes.append((headBoxX , headBoxY+i)) 
        self.update()

    def mousePressEvent(self, event):
        """
        mouse clicks events
        """
        button = event.button()
        if button == 2 :
            if self.orientation == 0 :
                self.orientation = 1
            else :
                self.orientation = 0
            self.update()
            return

        if self.clickable :
            self.selectedBoats.append(self.brownBoxes)
            self.selectedBlocks += self.brownBoxes
            self.currentBoat += 1

        if self.currentBoat == len(self.boats) :
            dictData = {
                'type' : 'setBoats',
                'data' : {
                    'coords' : self.selectedBoats
                }
            }
            
            jsonData = json.dumps(dictData)
            mysocket.send(jsonData)

    def mouseMoveEvent(self, event):
        if len(self.boats) == self.currentBoat :
            return
        self.clickable = True
        headX = event.x()
        headY = event.y()
        headBoxX = headX/50
        headBoxY = headY/50
        self.updateBoxes(headBoxX, headBoxY)

class SelectPlayerWidget(QtGui.QWidget):
    def __init__(self,parent):
        super(SelectPlayerWidget, self).__init__()
        
        self.parent = parent
        self.VBox = QtGui.QVBoxLayout()
        parent.playerlistwidget = QtGui.QListWidget()
        self.ChallangeButton = QtGui.QPushButton("Challange")
        self.connect(self.ChallangeButton,QtCore.SIGNAL("clicked()"),parent.sendChallenge)
        self.VBox.addWidget(parent.playerlistwidget)
        self.VBox.addWidget(self.ChallangeButton)
        self.setLayout(self.VBox)
        self.setWindowTitle("Player List")

    def closeEvent(self, event):
        # do stuff
        global mysocket

        print " < I am Out >"
        msg = {"type":"iAmOut","data":None}
        msg = json.dumps(msg)

        mysocket.send(msg)


        event.accept() # let the window close
      


class Game(QtGui.QMainWindow):
    def __init__(self,master=None):
        QtGui.QMainWindow.__init__(self, master)
        self.setWindowTitle("Ba Ba BattleShip")

        self.createUI()
        

        self.hide()


        self.enterName()

        self.selectplayerwidget.show()


    def createUI(self):

        self.widget = QtGui.QWidget(self)
        self.container = QtGui.QVBoxLayout()
        self.setCentralWidget(self.widget)
       

        self.selectplayerwidget = SelectPlayerWidget(self)

        self.selectBoatWidget = setBoats()        
        self.selectBoatWidget.hide()

        self.battlewidget = battle()
        self.battlewidget.hide()
        #print "adding last part"




        #self.container.addWidget(self.selectplayerwidget)
        self.container.addWidget(self.selectBoatWidget)
        self.container.addWidget(self.battlewidget)

        self.widget.setLayout(self.container)

    def closeEvent(self, event):
        # do stuff
        global mysocket
        print " < aborting game >"
        msg = {"type":"abortGame","data":None}
        msg = json.dumps(msg)

        mysocket.send(msg)

        self.selectplayerwidget.show()
        self.hide()

        event.ignore() # let the window close
        
        
    def enterName(self):

        global name


        name , ok = QtGui.QInputDialog.getText(self, 'name', 'Enter your name:') 
        name = str(name)
        if not ok:     
            self.close()
            sys.exit(1)
        else:
            self.sendName()
      
    def sendName(self):
        global name
        msg = {"type":"register","data":name}
        msg = json.dumps(msg)

        mysocket.send(msg)



    def sendChallenge(self):
        
        global eve

        if self.playerlistwidget.currentItem() and self.playerlistwidget.currentItem().isSelected():
            toname = self.playerlistwidget.currentItem().text()
            #print name
            msg = {"type":"sendChallenge","data":{"to":str(toname)}}
            msg = json.dumps(msg)
            mysocket.send(msg)

            print "challange request sending to server"

            #d = QtGui.QDialog()
            #d.setText("waiting for opponent...")
            #d.show()
            #d.exec_()


            class customMsg(QtGui.QDialog):
                def __init__(self,eve, parent=None):
                    super(customMsg, self).__init__(parent)

                    self.msgBox = QtGui.QMessageBox()

                    self.msgBox.setText('waiting for opponent...')
                    self.msgBox.addButton(QtGui.QMessageBox.NoButton)
                    #msgBox.setModal(True)
                    


            self.waitbox = customMsg(eve)
            self.waitbox.msgBox.open()
            
            print "before wait"
            #eve.wait()
            print "after wait"
            #self.waitbox.accept()


            #box =  QtGui.QMessageBox()
            #box.setText(" waiting for response... ")
            #box.addButton(QtGui.QMessageBox.NoButton)
            #box.setStandardButton(QtGui.QMessageBox.NoButton)
            #box.show()
            #if box.exec_():
            #    print " starting.. select Ship"

        else:
            msg = QtGui.QMessageBox()
            msg.setText("please select an online player")
            msg.show()
            msg.exec_()

        

    def gotChallenge(self,mysocket,playername):
        result = QtGui.QMessageBox.question(self, 'challenge',playername +" challenged you \n\n accept challange ?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
        if result == QtGui.QMessageBox.Yes:
            msg = {"type":"acceptChallenge","data":{"player1":playername,"player2":name}}
            msg = json.dumps(msg)

            mysocket.send(msg)


            print " challange accepted :D"
        else:
            pass

    
    def cpu(self,mysocket,msgtype,msgdata,eve):

        global ships
        if msgtype == "playerlist":
            
            print "got player list"
            self.playerlist = msgdata
            self.playerlistwidget.clear()


            for each in self.playerlist:
                if each != name:
                    self.playerlistwidget.addItem(each)

        elif msgtype == "sendChallenge":
            print "got challange from " + msgdata["from"]
            self.gotChallenge(mysocket,msgdata["from"])


        elif msgtype == "startGame":


            print "<<here>>"
            
            if hasattr(self, 'waitbox'):
                #eve.set()
                self.waitbox.msgBox.accept()


            else:
                "no waitbox in self"
            self.selectplayerwidget.hide()
            self.show()
            self.selectBoatWidget.myInit()
            self.selectBoatWidget.show()

        elif msgtype == "beginBattle":

            ships = msgdata['shipData']

            self.selectBoatWidget.hide()
            self.battlewidget.customInit()
            self.battlewidget.myInit()
            print self.battlewidget.get()

            if name == msgdata['turn'] :
                self.battlewidget.initTurn()

            self.resize(1050,500)
            self.battlewidget.show()            


            # third module

        elif msgtype == "oppIsOut":

            self.selectBoatWidget.hide()
            self.battlewidget.hide()
            self.hide()
            self.selectplayerwidget.show()




        elif msgtype == "verdict" :
            print msgdata
            if msgdata["result"] == "win" :
                print 'win'
            if msgdata["result"] == "loose" :
                print 'loose'

        elif msgtype == "updateAttackCoords" :
            coords = msgdata['coordinates']
            self.battlewidget.attackOnMe([coords[0], coords[1]])

        else:
            print "unhandled msgtype :" + msgtype
            

def listener(mysocket,game,eve):
    while True:
        msg = mysocket.recv(1024)
        msg = json.loads(msg)

        msgtype = msg["type"]
        msgdata = msg["data"]

        game.cpu(mysocket,msgtype,msgdata,eve)




class ListenerThread(threading.Thread):

    def __init__(self,mysocket,game,eve):
        threading.Thread.__init__(self)
        self.mysocket = mysocket
        self.game = game
        self.eve = eve

    def run(self):

        listener(self.mysocket,self.game,self.eve)

if __name__ == "__main__":

    mysocket = socket.socket()
    host = socket.gethostname()

    port  = 7064

    try:
        pass
        mysocket.connect((host,port))
    except:
        print "could not connect to server"
        sys.exit(1)

    print "connected"
    app = QtGui.QApplication(sys.argv)
    
    game = Game()
    #thread.start_new_thread(listener,(mysocket,game))
    eve = threading.Event()
    listenerthread = ListenerThread(mysocket,game,eve)
    listenerthread.start()

    #game.show()
    game.resize(640, 480)
    sys.exit(app.exec_())
