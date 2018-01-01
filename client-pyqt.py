from PyQt4 import QtGui, QtCore,QtNetwork
import vlc
import socket,sys,threading,json

ships = None
name = None

def getMyShips(name) :
    '''
    Return the ship list of the requester
    '''
    global ships
    return ships[name]

def getOpponentShips(name) :
    '''
    Return the ship list of opponent of the requester
    '''
    global ships
    for player in ships :
        if player != name :
            return ships[player]


class battle(QtGui.QWidget):
    '''
    The main gameplay Widget
    '''
    
    def __init__(self):
        super(battle, self).__init__()
        self.initUI()
        self.setMouseTracking(True)
        self.customInit()

        print "init sounds"
        self.soundhit = vlc.MediaPlayer("soundfile/hit.wav")
        self.soundmiss = vlc.MediaPlayer("soundfile/miss.wav")
        print "sound initialized"


    def customInit(self):
        '''
        To initialize the data that are dependent on
        components not loading before the __init__ is called
        '''
        self.myAttackedBlocks = []
        self.opponentAttackedBlocks = []
        self.turn = False
        self.mouseOn = [9999,9999]


    def resetMouseOn(slef) :
        self.mouseOn = [9999,9999]

    def setMouseOn(self, x, y) :
        self.mouseOn = [x,y]

    def myInit(self):
        '''
        
        '''
        global name
        self.myShips = getMyShips(name)
        self.opponentShips =getOpponentShips(name)
        
    def initTurn(self) :
        '''
        Initialize the turn variable
        '''
        self.turn = True

        
    def initUI(self):      
        '''
        Set default dimensions and title for the window
        '''
        self.setGeometry(50, 50, 1050, 500)
        self.setWindowTitle('Battle captains ..!')
        self.show()

    def paintEvent(self, e):
        '''
        Update the board drawings
        '''
        qp = QtGui.QPainter()
        qp.begin(self)
        #self.myInit()
        self.drawBoards(qp)
        qp.end()

        if not self.soundmiss.is_playing():
            self.soundmiss.stop()

        if not self.soundhit.is_playing():
            self.soundhit.stop()

    def drawBoards(self, qp):
        '''
        handles the drawing part
        
        Input : painter object
        Output : Updatation of the canvas
        '''
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
                
                #draw the attacked blocks in red
                flag = True
                if [x,y] in self.myAttackedBlocks :
                    qp.setBrush(QtGui.QColor(255,100,100,fade))
                    flag = False

                if flag :
                    for ship in self.myShips :
                        if [x,y] in ship :
                            pen = QtGui.QPen(QtGui.QColor(0,0,0), 2, QtCore.Qt.SolidLine)
                            qp.setPen(pen)
                            qp.setBrush(QtGui.QColor(255,255,255,fade))
                            break
                    
                qp.drawRect(x*50,y*50, 50,50)
                
                #draw the ship blocks in white. Keep border black
                pen = QtGui.QPen(QtGui.QColor(0,0,0), 2, QtCore.Qt.SolidLine)
                qp.setPen(pen)
                qp.setBrush(QtGui.QColor(255,255,255,fade))
                for ship in self.myShips :
                    for coord in ship :
                        qp.drawRect(coord[0]*50,coord[1]*50, 50,50)
                
                for coord in self.myAttackedBlocks :
                    qp.setBrush(QtGui.QColor(255,100,100,fade))
                    qp.drawRect(coord[0]*50,coord[1]*50, 50,50)               

        #keep the part of the current turn holder normal
        #and other'sfaded
        fade = 255
        try :
            if self.turn :
                fade = 255
            else:
                fade = 140
        except : 
            print ""

        #draw opponent board
        pen = QtGui.QPen(QtCore.Qt.white, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        
        for x in range(10) :
            for y in range(10) :
                qp.setBrush(QtGui.QColor(150, 170, 255,fade))

                #change the color of block on which
                #the mouse pointer is
                if [x+11,y] == self.mouseOn and self.turn:
                    qp.setBrush(QtGui.QColor(255,69,0,140))
                if [x,y] in self.opponentAttackedBlocks :
                    qp.setBrush(QtGui.QColor(255,100,100,fade))
                qp.drawRect((x+11)*50,y*50, 50,50)
        
        #print whose turn is it currently
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
        Todo's when player clicks
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
    
        #if player has turn
        #consider click as an attack
        x = x - 11
        if self.turn :
            if x in range(10) and y in range(10) :
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
        '''
        Handle todo's with the current mouse position
        '''
        x = event.x()/50
        y = event.y()/50
        self.setMouseOn(x,y)
        self.update()

    def attackOnMe(self, coords) :
        '''
        Event when the client is attacked
        '''
        print "i am attacked"
        for ship in self.myShips :
            if coords in ship :
                self.myAttackedBlocks.append(coords)
                self.soundhit.play()
            else:
                self.soundmiss.play()

        self.turn = True
        self.update()

    def attackOnOpponent(self, coords) :
        '''
        Event when client's opponent is attacked
        '''
        for ship in self.opponentShips :
            if coords in ship :
                self.opponentAttackedBlocks.append(coords)
                self.soundhit.play()
            else:
                self.soundmiss.play()

        self.turn = False

        self.update()


    def get(self) :
        return self.myShips



class setBoats(QtGui.QWidget):
    '''
    The widget where player arranges his ships
    '''
    def __init__(self):
        super(setBoats, self).__init__()
        self.initUI()
        self.setMouseTracking(True)
        self.myInit()
    
    def myInit(self):
        '''
        Handle initialization of dependent attributes
        '''
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
        '''
        The painter
        '''
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()
        
    def drawLines(self, qp):
        '''
        Handle drawing of blocks on board
        '''
        pen = QtGui.QPen(QtCore.Qt.white, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        
        #draw 10x10 grid
        for x in range(10) :
            for y in range(10) :
                #if a block isn't part of arranged ship keep it blue
                #and white otherwise
                if (x,y) not in self.brownBoxes and (x,y) not in self.selectedBlocks :
                    qp.setBrush(QtGui.QColor(150, 170, 255))
                    qp.drawRect(x*50,y*50,50,50)
                else :
                    qp.setBrush(QtGui.QColor(255,255,255))
                    qp.drawRect(x*50,y*50,50,50)
                    
        #type sensile messages to keep player informed
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        font = qp.font()
        font.setPointSize(15)
        qp.setFont(font)
        
        if len(self.boats[self.currentBoat : ]) > 1 :
            setShipText = "Size of ships you have : " + reduce(lambda x,y : str(x)+ ", " +str(y), self.boats[self.currentBoat : ])
        elif len(self.boats[self.currentBoat : ]) == 1 :
            setShipText = "Size of ships you have : " + str(self.boats[self.currentBoat : ][0])
        else : #when player puts all his ships before his opponent, he waits
            setShipText = "Waiting for opponent while he prepares for battle"
            
        qp.drawText(10,11*50, setShipText)
        

    def updateBoxes(self, headBoxX, headBoxY) :
        '''
        Maintain the state of boats
        '''
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
        
        #if it's a right click, change orientation of boats
        if button == 2 :
            if self.orientation == 0 :
                self.orientation = 1
            else :
                self.orientation = 0
            self.update()
            return

        if self.clickable : #when user leftclicks
            self.selectedBoats.append(self.brownBoxes)
            self.selectedBlocks += self.brownBoxes
            self.currentBoat += 1
        
        #when user clicks, tell server he set a boat
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
        '''
        Move ships along with mouse
        '''
        if len(self.boats) == self.currentBoat :
            return
        self.clickable = True
        headX = event.x()
        headY = event.y()
        headBoxX = headX/50
        headBoxY = headY/50
        self.updateBoxes(headBoxX, headBoxY)


class WinLoseMsg(QtGui.QDialog):

    '''
    MessageBox for Win or Lose Message
    '''


    def __init__(self,iswin, game,parent=None):
        super(WinLoseMsg, self).__init__(parent)

        self.game=game
        msgBox = QtGui.QMessageBox()

        if iswin:
            msgBox.setText('         You win')
        else:
            msgBox.setText('         You lose')


        anotherplayerbutton = QtGui.QPushButton('  Play with another player ')
        anotherplayerbutton.clicked.connect(self.anotherplayerclicked)



        msgBox.addButton(anotherplayerbutton, QtGui.QMessageBox.YesRole)

        ret = msgBox.exec_()


    def anotherplayerclicked(self):
        '''
        Close the messagebox when another player accept the challenge
        '''
        self.game.hide()
        self.game.selectplayerwidget.show()



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

        self.startsound = vlc.MediaPlayer("soundfile/start.mp3")
        
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
        global mysocket
        print " < aborting game >"
        msg = {"type":"abortGame","data":None}
        msg = json.dumps(msg)

        mysocket.send(msg)

        self.selectplayerwidget.show()
        self.hide()

        event.ignore() # let the window close
        
        
    def enterName(self):
        '''
        Input Dialog for the name
        '''
        global name


        name , ok = QtGui.QInputDialog.getText(self, 'name', 'Enter your name:') 
        name = str(name)
        if not ok:     
            self.close()
            sys.exit(1)
        else:
            self.sendName()
      
    def sendName(self):
        '''
        Send the name when user enters the name and press button
        '''
        global name
        msg = {"type":"register","data":name}
        msg = json.dumps(msg)

        mysocket.send(msg)



    def sendChallenge(self):
        '''
        send challenge message when user select the user and press button
        '''
        
        if self.playerlistwidget.currentItem() and self.playerlistwidget.currentItem().isSelected():
            toname = self.playerlistwidget.currentItem().text()
            #print name
            msg = {"type":"sendChallenge","data":{"to":str(toname)}}
            msg = json.dumps(msg)
            mysocket.send(msg)

            print "challange request sending to server"

            
            class customMsg(QtGui.QDialog):
                def __init__(self, parent=None):
                    super(customMsg, self).__init__(parent)

                    self.msgBox = QtGui.QMessageBox()

                    self.msgBox.setText('waiting for opponent...')
                    self.msgBox.addButton(QtGui.QMessageBox.NoButton)
            
            self.waitbox = customMsg()
            self.waitbox.msgBox.open()
            
            print "before wait"
            print "after wait"
            

            
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
            msg = {"type":"declineChallenge","data":{"challenger":playername}}
            msg = json.dumps(msg)

            mysocket.send(msg)


    
    def cpu(self,msg):
        try:
            global mysocket
        except:
            print "mysocket is not gloabal lol  "
        msg = str(msg)
        msg = json.loads(msg)

        msgtype = msg["type"]
        msgdata = msg["data"]



        global ships
        if msgtype == "playerlist":
            '''
            got new player list, update the listWidget
            '''
            print "got player list"
            self.playerlist = msgdata
            self.playerlistwidget.clear()


            for each in self.playerlist:
                if each != name:
                    self.playerlistwidget.addItem(each)

        elif msgtype == "sendChallenge":
            '''
            got a challenge from the player
            '''
            print "got challange from " + msgdata["from"]
            self.gotChallenge(mysocket,msgdata["from"])


        elif msgtype == "startGame":
            '''
            when challenge is accepted start the game window and start widget to get the ships
            '''           
            if hasattr(self, 'waitbox'):
                self.waitbox.msgBox.accept()


            else:
                "no waitbox in self"
            

            self.startsound.play()
            self.selectplayerwidget.hide()
            self.battlewidget.hide()
            self.show()
            self.selectplayerwidget.repaint()
            self.selectBoatWidget.myInit()
            self.selectBoatWidget.show()

        elif msgtype == "beginBattle":
            '''
            ship is set of both players, now start the game
            '''
            self.startsound.stop()
            ships = msgdata['shipData']

            self.selectBoatWidget.hide()
            self.battlewidget.customInit()
            self.battlewidget.myInit()
            self.battlewidget.repaint()
            
            if name == msgdata['turn'] :
                self.battlewidget.initTurn()

            #self.resize(1050,500)
            self.battlewidget.show()            


            # third module

        elif msgtype == "oppIsOut":
            '''
            opponent is out when user was playing a game
            '''
            print "opponent is out"
            self.selectBoatWidget.hide()
            self.battlewidget.hide()
            self.hide()
            self.selectplayerwidget.show()




        elif msgtype == "verdict" :

            winflag = False
            if msgdata["result"] == "win" :
                winflag = True
               
            
            result = WinLoseMsg(winflag,self)
            result.open()


        elif msgtype == "updateAttackCoords" :
            coords = msgdata['coordinates']
            self.battlewidget.attackOnMe([coords[0], coords[1]])

        elif msgtype == "challengeDeclined" :

            if hasattr(self, 'waitbox'):
                #eve.set()
                self.waitbox.msgBox.setText("Challenge Rejected..")


        else:
            print "unhandled msgtype :" + msgtype
            






class ListenerThread(QtCore.QThread):

    def __init__(self,mysocket,game):
        
        QtCore.QThread.__init__(self)
        self.mysocket = mysocket
        self.game = game

    def listener(self,mysocket,game):
    

        while True:

            msg = mysocket.recv(2048)
            msg = str(msg)
            if msg == "":
                return
            
            msg = QtCore.QString(msg)

            self.emit(QtCore.SIGNAL("gamecpu(QString)"),msg)
            #game.cpu(mysocket,msgtype,msgdata)

        
    def run(self):

        self.listener(self.mysocket,self.game)

if __name__ == "__main__":

    mysocket = socket.socket()
    host = socket.gethostname()

    port  = 7064

    try:        
        mysocket.connect((host,port))
    except Exception as e:
        print e
        print "could not connect to server"
        sys.exit(1)

    print "connected"
    app = QtGui.QApplication(sys.argv)
    game = Game()
    #thread.start_new_thread(listener,(mysocket,game))
    
    listenerthread = ListenerThread(mysocket,game)
    listenerthread.connect(listenerthread,QtCore.SIGNAL("gamecpu(QString)"),game.cpu)
    listenerthread.start()

    #game.show()
    game.resize(1200, 680)
    sys.exit(app.exec_())
