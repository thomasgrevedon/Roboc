# -*-coding:Latin-1 -*
from roboc_classes import *

"""
carte = Labyrinth("cartes/facile.txt")
print(carte)
print(carte.robot_position)
print(carte)
"""
""" we check how manu availables maps we have, what are they and we ask player
 to select one"""
game = Game()
number_of_map_avilables = game.found_map_avaialables()
print("\n")
valid_entry = False
while valid_entry != True:
    requested_map = str(input("Select a number of map to start playing : "))[:1]
    try:
        requested_map = int(requested_map)
        assert requested_map < (number_of_map_avilables) and requested_map > 0
        map_name = "cartes/" + game.maps[requested_map - 1]
        map, on_going_party = game.unpack_map(map_name)
        if on_going_party:
            continue_play = str(input("Type \"y\" if you want to continue playing"
            " or press anything else if you want to start a new party: "))[:1].lower()
            if continue_play != "y":
                map = Labyrinth(map_name)
        else:
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
print("Choose a letter among: \"n\", \"s\", \"o\", \"e\" foolowed by a number"
"to requets a move. The number is optional, so you can only right a letter and"
"the robot will try to move accoriding the" "desired direction by one step")
"""We now let the player insert a move"""
"""un first try pour etre sur que tout est isalpha"""
"""--> while not q on ne quitte pas et idem si sortie trouvée"""
"""--> comment enlever la porte et le x"""
"""--> comment faire pour que ça reste dans le cadre du jeu"""
"""--> comment réagir au mur (while empty ok sinon break)"""
"""--> when click enter on move, starnge"""
while exit != "q" and game.win == False:
    valid_entry = False
    allowed_entry = ["n", "s", "o", "e"]
    while valid_entry != True:
        move = input()
        if len(move) == 1:
            move += "1"
        try:
            issue = "wrong letter, you must choose bewteen \"n\", \"s\", \"o\", \"e\""
            assert move[0].isalpha() and move[0].lower() in allowed_entry
            issue = "Please insert a valid number after the direction"
            assert move[1:].isdigit()
            move_direction = move[0].lower()
            number = move[1:]
            #print("position before asking a move", map.robot_position)
            robot_move = robot.move(move_direction, number)
            #print("robot move", robot_move)
            game.win = map.check_in_map(move_direction, robot_move, game)
            #print(game.win)
            robot.position = dict(map.robot_position)
            #print("position of robot in the map", map.robot_position, "and in the robot itself", robot.position)
            map.update_map()
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

game.quit(map_name, game.win, map)
