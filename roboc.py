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
    requested_map = str(input("Entrez un numéro de labyrinthe pour commencer à jouer : "))[:1]
    try:
        requested_map = int(requested_map)
        assert requested_map < (number_of_map_avilables) and requested_map > 0
        map = "cartes/" + game.maps[requested_map - 1]
        map = Labyrinth(map)
        valid_entry = True
    except ValueError:
        print("Please enter a valid number")
    except AssertionError:
        print("Sorry the number you have entered is not valid. You must select "
        "one of the offered number")

print("\n")
print(map)
print("\n")
