# CLASH OF CLANS
# Setup :
To run the game , we need to install colorama library.

```$ pip3 install colorama```

To play the game , 

```$ python3 game.py```


# Fuctionalities :

The following keyboard presses are relevent for the following jobs :

* Move the king or queen using ```W,S,A,D```  
* Spawn King or Queen at assigned locations using ```4,5,6```  
* Spawn Barbarians  using ```1,2,3```  
* Spawn Archer  using ```z,x,c``` 
* Spawn Balloons  using ```v,b,n``` 
* Do regular attack of King or Queen using ```Space```
* Do Leviathan attack of King using ```e```  
* Do Archer attack of Queen using ```9```
* Activate Heal spell and Rage Spell using ```7``` and ```8``` respectively

  

# Features : 

1) The outer wall can't be breached and it acts as the boundary within which we play the game .
2) There are ```5``` huts , ```1``` Townhall and different number of cannons and wizards for each level:

	```Level 1``` : 2 cannon , 2 wizard
	
	```Level 2``` : 3 cannon , 3 wizard
	
	```Level 3``` : 4 cannon , 4 wizard  
3) Cannon and Wizard  have a range of ```7```
4) The barbarians can move diagonally and attack on the nreaest building found ( manhatten distance) . At max , a player can spawn ```6``` barbarians , ```6``` archers and ```3``` balloons at three different locations in total . 
5) The Rage and Heal spell can be user at max ```7``` times(separately) .

# OOPS Principles 

## Inheritence
* The Building class serves as the base class, from which the Town Hall, Wall, Cannon ,Wizard and Hut classes inherit.  
* The King ,Queen , Archer , Balloon and Barbarian classes inherit from the Troops class.  

## Abstraction 

 ```move()``` and ```attack()``` methods of the Troop class are two examples of Abstraction . The inner details and implementation of movement and attacking are hidden from the user and the user can directly use these functions without bothering about their internal implementation . 
 
 ## Encapsulation 
 To realise Encapsulation , all functions or variables pertaining to a particular game entity are grouped under a single class.Then, all that is required to use the feature is to call the method on the class object.  
 
 ## Polymorphism 
The Troop class has an ```attack()``` method.The Queen class has its specific ```attack()``` method that overrides the default Troop's ```attack()``` method.

