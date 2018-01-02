## Ba-Ba Battleship

An implementation of the classic arcade Battleship game on a multi-client supporting server platform.<br>
Here sockets are used as a medium of communication.<br>
The architecture is based on message-passing paradigm.<br>

<hr>

#### Tech-details
The application is made totally using python. <br>
For GUI part, we've used PyQt<bR>

<hr>

#### Gameplay

  ##### Step 1 :
  Run the client and enter your name to connect to the game.<Br>
 

  ##### Step 2 :
  Arrange your ships using mouse clicks.
  Right click will change the orientation of your ship (horizontal / vertical)
  When you have arranged all your ships, wait for the opponent to do the same

  ##### Step 3 :
  The battle will begin as soon as both players have arranged their ships.
  Each player attacks chance by chance.<br>
  Player will see the attacked ship blocks of opponent in red
  The first player to hit all the ship blocks wins

