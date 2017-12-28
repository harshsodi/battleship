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
	name = None
	socketDesc = None

class Game:
	player1 = None
	player2 = None
	gameId = None

	shipsPlayers = []
	#shipsPlayer = None
	attackedBLocksPlayer1 = []
	#attackedBLocksPlayer2 = None

	def __init__(self, player1, player2) : #player objects
		self.player1 = player1
		self.player2 = player2


    def checkResult():

        

        if len(self.shipsPlayer1) == len(self.attackedBLocksPlayer1):
            return self.player1 , self.player2
        if len(self.shipsPlayer2) == len(self.attackedBLocksPlayer2):
            return self.player2 , self.player1

        return None

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
	
	
#end Game

def sendMsg(msg,fromclient,toclient):

    pass
    #end sendmsg



def registerClient(client,name):
    
    """
    -will make a new object of the Player class and will append to the playerList.
    -to maintain the list of the online players.
    """
    player = Player(client,name)
    #playerlist.append(player)
    playerlist[name] = player
    return player



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
   
    elif msgtype == "attack":
        """
        "msgtype":"attack":
            a player will attack on the perticular cordinates (x,y).
        
        "msgdata:":{"cordinates":(x,y)}

        """
        game = gamebox[player]
        game.attack(player,msgdata["cordinates"])
        if winner , loser = game.checkResult():

            msgcontainerforwinner = {"type":"verdict","data":{"result:":True}}
            msgcontainerforloser = {"type":"verdict","data":{"result:":False}}

            msgforwinner = json.dumps(msgcontainerforwinner)
            msgforloser = json.dumps(msgcontainerforloser)

            #winner.socketDesc.send(msgforwinner)
            #loser.socketDesc.send(msgforloser)

            sendMsg(msgforwinner , winner)
            sendMsg(msgforloser , loser)
        else:

    #end cup

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