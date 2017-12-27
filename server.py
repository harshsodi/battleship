import socket,thread,sys,json
playerlist = []
serversocket = socket.socket()
hostname = socket.gethostname()
port = 764

try:
    serversocket.bind((hostname,port))
except:
    print "server could not start"


print " server running..."


'''
    ((desctiptor,name),(desctiptor,name),(desctiptor,name),(desctiptor,name),(desctiptor,name))

'''

class player :
	name = None
	socketDesc = None

class game:
	def __init__(self, socketDesc, name) :
		self.name = name
		self.socketDesc = socketDesc

class game:
	player1 = None
	player2 = None
	gameId = None

	shipsPlayer1 = None
	shipsPlayer2 = None
	attackedBLocksPlayer1 = None
	attackedBLocksPlayer2 = None

	def __init__(self, player1, player2) : #player objects
		self.player1 = player1
		self.player2 = player2

	def attack(self, victim, block) :
		'''
		Drop bomb on block of victim's board
		Update board if block is part of ship
		Return True if attack successful and False otherwise
		'''
    #end game

def sendMsg(msg,fromclient,toclient):


    pass
    #end sendmsg



def cpu(client,msgtype,msgdata):

    if msgtype == "register":

        name = msgdata
        registerClient(client,name)


    pass
    #end cup

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
    msgtype = message.type
    msgdata = message.data["name"]
    cpu(client,msgtype,msgdata)

    return
    #end handleClient 


serversocket.listen(5)


"""
Receiver:
    -it will wait for the new connections.when a new connection is made it will start listening to the particular client

"""

while True:
    client, address = serversocket.accept()
    thread.start_new_thread(handleClient,(client,))

    #end reciever
