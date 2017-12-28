import socket,thread,sys,json


playerlist = {}

serversocket = socket.socket()
hostname = socket.gethostname()
port = 7064


log = open("log.txt","a")


try:
    serversocket.bind((hostname,port))
except:
    print "server could not start"


print " server running..."

'''
    ((desctiptor,name),(desctiptor,name),(desctiptor,name),(desctiptor,name),(desctiptor,name))

'''

class Player :
    
    def __init__(self, socketDesc, name) :
        self.name = name
        self.socketDesc = socketDesc
    #end player

class Game:    
    shipsPlayer1 = []
    shipsPlayer2 = []
    attackedBLocksPlayer1 = []
    attackedBLocksPlayer1 = []
    
    def __init__(self, player1, player2) : #player objects
        self.player1 = player1
        self.player2 = player2

    def checkResult(self) :
        if len(self.shipsPlayer1) == len(self.attackedBLocksPlayer1):
            return self.player1 , self.player2
        if len(self.shipsPlayer2) == len(self.attackedBLocksPlayer2):
            return self.player2 , self.player1

        return None , None

    def attack(self, attacker, block) :       
        themap = None
        theattackedmap = None
        if attacker == self.player1:
            themap = self.shipsPlayer2
            theattackedmap = self.attackedBLocksPlayer2
        else:
            themap = self.shipsPlayer1
            theattackedmap = self.attackedBLocksPlayer1


        if block in themap:
            if block not in theattackedmap:
                theattackedmap.append(block)
            else:
                log.write(" In attack function - block is already attacked once.! ")


        '''
        victim -> which player will get affected by the attack. (Opponent of the player which had turn)
               -> Player object
        block -> tupple of the cordinates of the attack (x,y)
        Drop bomb on block of victim's board
        Update board if block is part of ship
        Return True if attack successful and False otherwise
        '''
    
    def setBoats(self, player, boatCoords) :
        '''
        player : object
        boatCoords : [[(x,y),(x,y),(x,y), ...],[(x,y),(x,y),(x,y), ...]]
        '''
        if player == self.player1 :
            self.shipsPlayer1 = boatCoords
        else :
            self.shipsPlayer2 = boatCoords
    
    #end game
    
    
#end Game

def startNewGame(player1, player2) :
    game = Game(player1, player2)
    return game

def sendMsg(msg, toclient):

    pass
    #end sendmsg

def cpu(player,msgtype,msgdata):

    if msgtype == "register":
        """
        "Register":
        -register the client to the server
        ->data: {
                    "name": <name of the client>
                }
        """
        name = msgdata
        return registerClient(player,name)
    
    elif msgtype == "sendChallenge" :
        '''
        expected message format : data :  {
                                            'to' : name
                                            }
        '''
        frm = player.name #name
        to = playerlist[msgdata['to']] #an object

        #message the opponent about the incoming challenge
        dictData = {
                        "type" : "sendChallenge",
                        "data" : {
                            "from" : frm #name
                        }
                    }
        jsonData = json.dumps(dictData)
        sendMsg(jsonData, to)
        
    elif msgtype == "acceptChallenge" :
        '''
        expected message format : data : {
                                        'player1' : name,
                                        'player2' : name  
                                    }
        '''
        data = msgdata
        player1 = playerlist[data['player1']] #objeect
        player2 = playerlist[data['player2']]   #object
        
        #register new game
        game = startNewGame(player1, player2)
        gamebox[player1] = game
        gamebox[player2] = game

        #message the players to begin the game
        dictData = {
                        'type' : 'startGame',
                        'data' : { 
                            
                        }
                    }
        jsonData = json.dumps(dictData)
        sendMsg(jsonData, player1)
        sendMsg(jsonData, player2)
        
    elif msgtype == "declineChallenge" :
        '''
        expected message format : data : {
                                        'challenger' : name 
                                    }
        '''
        data = msgdata
        challenger = playerlist[data['challenger']]

        #message the challenger if his challenge is declined
        dictData = { 
                        'type' : 'challengeDeclined',
                        'data' : { }
                    }
        jsonData = dictData.dumps()
        sendMsg(jsonData, challenger)

    elif msgtype == 'abortGame' :
        '''
        expected message format : data : {
                                            
                                            }
        '''
        
        #send message on both sides to abort the game and return to initial stage
        dictMsg = {
            'type' : 'abortGame',
            'data' : {

            }
        }
        jsonMsg = dictMsg.dumps()

        game = gamebox[player]
        sendMsg(jsonMsg, game.player1)
        sendMsg(jsonMsg, game.player2)
   
    elif msgtype == "setBoats" : #arranging done, now register my boat positions
        '''
        Message type : data : {
                            coords : [[],[]]
                        }
        '''
        data = json.loads(msgdata)
        boatcoords = data[coords]
        
        game = gamebox[player]
        game.setBoats(player, boatcoords)

    elif msgtype == "attack":
        """
        "msgtype":"attack":
            a player will attack on the perticular cordinates (x,y).
        
        "msgdata:":{"coordinates":(x,y)}

        """
        game = gamebox[player]
        game.attack(player,msgdata["coordinates"])
        
        winner , loser = game.checkResult()
        if winner and loser:

            msgcontainerforwinner = {"type":"verdict","data":{"result:":True}}
            msgcontainerforloser = {"type":"verdict","data":{"result:":False}}

            msgforwinner = json.dumps(msgcontainerforwinner)
            msgforloser = json.dumps(msgcontainerforloser)

            #winner.socketDesc.send(msgforwinner)
            #loser.socketDesc.send(msgforloser)

            sendMsg(msgforwinner , winner)
            sendMsg(msgforloser , loser)

        else : #send coordinates to client as well
            dictData = {
                'type' = 'updateAttackCoords',
                'coordinates' : msgdata['coordinates']
            }
            jsonData = json.dumps(dictData)

            game = gamebox[player]
            if player == game.player1 :
                sendMsg(jsonData, game.player2)

            if player == game.player2 :
                sendMsg(jsonData, game.player2)

    #end cpu

def registerClient(client,name):
    
    """
    -will make a new object of the Player class and will append to the playerList.
    -to maintain the list of the online players.
    """
    player = Player(client,name)
    #playerlist.append(player)
    playerlist[name] = player
    return player

def handleClient(client):

    """
    -will receive the message from the client and will send it to the cpu for parsing and further process
    -msg is received as a json. so message parsing is mendetory

    Message Structure::

    {"type":<type> , "data" : <data for particular type of message>}


    """    
    while True:
        data = client.recv()
        message = json.loads(data)
        msgtype = message["type"]
        msgdata = message["data"]
        
        if "name" in client:
            cpu(client,msgtype,msgdata)
        else:

            if msgtype != "register":
                log.write("unregistered client is trying to send unvalid messages : " + msgtype)
                sys.exit(1)

            client = cpu(client,msgtype,msgdata)
    
    #end handleClient 


serversocket.listen(5)


"""
Receiver:
    -it will wait for the new connections.when a new connection is made it will start listening to the particular client

"""

def printUsers() :
    for each in playerlist :
        print each.name

while True:
    client, address = serversocket.accept()
    thread.start_new_thread(handleClient,(client,))

    #end reciever


#close the log file
log.close()
