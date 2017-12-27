import socket,thread,sys
clients = []
serversocket = socket.socket()
hostname = socket.hostname()
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


    
    #end sendmsg



def cpu(client,msg):




    #end cup


def handleClient():



    #end handleClient 


while True:




    #end reciever
