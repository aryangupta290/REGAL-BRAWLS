# File Structure :

Inside the main folder , I have 6 files , here are the functioanlities of each one of them :

a) game.py : This is the file where we declare the game loop and also handle the code for replay function

b) player.py : This is the main file where the all the major functionalies of the game are declared .

c) Building.py : This contains the parent building class and also the decleration of the child classes ( TownHall , Cannon , Hut)

d) Troops.py : Similar to Building.py , this class contains the parent troop class and the corresponding child classes (Barb King , Barbarian)

e) Constants.py : Here I have declared all the constants related to my game like the size , height , width of each of the componenets

f) spell.py : This class is used for implementing the rage and heal spells.

# Fuctionalities :

The following keyboard presses are relevent for the following jobs :

a) W -> move king up
b) S -> move king down
c) D -> move king right
d) A -> Move king left
e) 1 -> Spawn a barbarian at the first location
f) 2 -> Spawn a barbarian at the second location
g) 3 -> Spawn a barbarian at the third location
h) 4 -> Spawn king at the first location
g) 5 -> Spawn king at the second location
h) 6-> Spawn king at the third location
i) 7 -> To use heal spell
j) 8 -> To use Rage spell
h) Space -> For normal attack of the king
i) e -> For leviathan attack of the king
j) z -> Spawn a archer at the first location
k) x -> Spawn a archer at the second location
l) c -> Spawn a archer at the third location
m) v -> Spawn a balloon at the first location
n) b -> Spawn a balloon at the second location
o) n -> Spawn a balloon at the third location
p) 9 -> Special attack of queen

# Features : 

1) The outer wall can't be breached and it acts as the boundary within which we play the game .
2) There are 5 huts , 1 Townhall and different number of cannons and wizards for each level:
	Level 0 : 2 cannon , 2 wizard
	Level 1 : 3 cannon , 3 wizard
	Level 2 : 4 cannon , 4 wizard
3) Cannon and Wizard  have a range of 7
4) The barbarians can move diagonally and attack on the nreaest building found ( manhatten distance) . At max , a player can spawn 6 barbarians , 6 archers and 3 balloons at three different locations in total . 
5) The Rage and Heal spell can be user at max 7 times(separately) .

# Run Instruction :

Run the commannd python3 game.py on your terminal after installing the colorama library
