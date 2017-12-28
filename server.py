import socket,thread,sys,json

playerlist = []
serversocket = socket.socket()
hostname = socket.gethostname()
port = 7064

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
        return self

    #end player

class Game:
	
	#shipsPlayer1 = None
	#shipsPlayer2 = None
	#attackedBLocksPlayer1 = None
	#attackedBLocksPlayer2 = None

	def __init__(self, player1, player2) : #player objects
		self.player1 = player1
		self.player2 = player2

	def attack(self, victim, block) :
		'''
		Drop bomb on block of victim's board
		Update board if block is part of ship
		Return True if attack successful and False otherwise
		'''
    
    def setBoats() :
        pass
    #end game

def startNewGame(player1, player2) :
    game = Game(player1, player2)
    return game

def sendMsg(msg, toclient):

    pass
    #end sendmsg

def cpu(player,msgtype,msgdata):

    if msgtype == "register":
        name = msgdata
        registerClient(client,name)
    
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
            'type' = 'abortGame',
            'data' = {

            }
        }
        jsonMsg = dictMsg.dumps()

        game = gamebox[player]
        sendMsg(jsonMsg, game.player1)
        sendMsg(jsonMsg, game.player2)

    #end cpu

def registerClient(client,name):
    
	"""
    -will make a new object of the Player class and will append to the playerList.
    -to maintain the list of the online players.
	"""
	player = Player(client,name)
	playerlist.append(player)

def handleClient(client):

	"""
    -will receive the message from the client and will send it to the cpu for parsing and further process
    -msg is received as a json. so message parsing is mendetory

    Message Structure::

    {"type":<type> , "data" : <data for particular type of message>}


    different types of possible data::
    ==================================
    "Register":
        -register the client to the server
        ->data: {
                    "name": <name of the client>
                }
        
	"""

	data = client.recv()
	message = json.loads(data)
	msgtype = message['type']
	msgdata = message['data']
	cpu(client,msgtype,msgdata)
    
	return
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
