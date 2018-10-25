# -*-coding:Latin-1 -*
from roboc_classes import *

"""
This a game called Roboc where the player is driving a robot trough a
Labyrinth and needs to try to find the exit.
The player is first asked to select an avalaible map and to decide to continue
playing a previous game if this map xas previously used without finishing it.
After the player decides, the game starts and the player must enter a letter
with a number to move the robot:
    - "n": moves the robot one step up
    - "s11": moves the robot 11 setps down
    - "o2": moves the robot 2 steps left
    - "e": moves the robot 1 step right
If the robot encounters a wall(O), it will move until the wall and stop.
If the number of move is above the length of the map, the robot will not move at all.
If the robot finds a door(.) it can go trough it.
If the robot finds the exit(U), the player has won and the game is finished
After each moves, the player is asked to quit and saved and can do it by
pressing "q". Any other entry continue the game. After each move, an automatic
save is done (in case the program is stoped for any reason the player would
be allwoed to start at the previous place where he was).
"""

"""first we get the map and when the player decide which map he wants to use,
        we start the game"""
game = Game()
number_of_map_avilables = game.found_map_avaialables() #we check how many maps are availables
print("\n")
valid_entry = False
while valid_entry != True:
    requested_map = str(input("Select a number of map to start playing : "))[:1] #this number - 1 will be the index for getting the map in the attribute self.maps
    try:
        requested_map = int(requested_map)
        assert requested_map < (number_of_map_avilables) and requested_map > 0
        map_name = "cartes/" + game.maps[requested_map - 1] #we can then place this name to request a Labyrinth
        map, on_going_game = game.unpack_map(map_name) #we check if there is an existing game for this map
        if on_going_game:
            continue_play = str(input("Type \"y\" if you want to continue playing"
            " or press anything else if you want to start a new party: "))[:1].lower()
            if continue_play != "y":
                game.delete_existing_game(map_name, map) #we delete the existing game for the map
                map = Labyrinth(map_name) #we start with a renewed map
        else: #no existing game, we start with a new map
            map = Labyrinth(map_name)
        robot = Robot(map.robot_position)
        valid_entry = True
    except ValueError:
        print("\n" + "Please enter a valid number")
    except AssertionError:
        print("Sorry the number you have entered is not valid. You must select "
        "one of the offered number")


print("\n")
print(map)
print("\n")
print("Choose a letter among: \"n\", \"s\", \"o\", \"e\" foolowed by a number "
"to requets a move. The number is optional, so you can only right a letter and "
"the robot will try to move accoriding the" "desired direction by one step")

"""We now
        -let the player ask for a move
        -check if it is possible
        -update the robot position after the check
        -update and print the map
        -save automatically
        -ask to quit and save or continue playing
        """

while exit != "q" and game.win == False:
    valid_entry = False
    allowed_entry = ["n", "s", "o", "e"]
    while valid_entry != True:
        move = input()
        if len(move) == 1:
            move += "1" #in case only a letter has been entered, we add one so we will request one step on the move
        try:
            issue = "wrong letter, you must choose bewteen \"n\", \"s\", \"o\", \"e\""
            assert move[0].isalpha() and move[0].lower() in allowed_entry
            issue = "Please insert a valid number after the direction"
            assert move[1:].isdigit()
            move_direction = move[0].lower()
            number = move[1:]
            robot_move = robot.move(move_direction, number) #we ask the robot to move by updating its position
            game.win = map.check_in_map(move_direction, robot_move, game) #we check in map if the move is possible and if the player has won
            robot.position = dict(map.robot_position) #we update the robot position with the position of robot in map after updating it.
            map.update_map()
            game.automatic_save(map_name, map)
            print("\n")
            print(map)
            valid_entry = True
        except AssertionError:
            print(issue)
            continue
        except IndexError:
            print("You msut enter a letter as you probably pressed enter without entering a letter")
            continue
        if game.win == False:
            exit = str(input("Press q to quit and save or anything else (like enter) to continue: "))[:1].lower()

"""last part is to quit the game and update the file with all existing games
according if the player has won or not"""
game.quit(map_name, game.win, map)
