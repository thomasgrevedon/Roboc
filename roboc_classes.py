import copy
import os
import pickle

"""This contains all classes with their fucntions that will be used by the
    program roboc.py"""

class Labyrinth:
    """class Labyrinth that will be used to initialize the map and
        print it"""
    def __init__(self, name):
        """--> The initialize function will receive a map name that is
        chosen by the player and will read the objects  in the
        designed map in the folder: cartes.
          --> the construction of the map follows this way: every object is
          saved in a list of objects that are on the same line. When the object
          is "\n", a new line is created with a new list. The whole set of
          {lines: [objects]} is saved in a dictionary allowing the program to
          analyse any object at a designed line.
           """
        with open(name, "r") as file:
            self.lines = {}
            self.robot_position = {} #the real position of the robot on the map with {line: index}
            self.robot_initial_position = {} #the position of the robot before a move with {line: index}
            self.point = False #will be used to check if the player is on a door
            line = 1
            for object in file.read():
                if object != "\n":
                    if line not in self.lines:
                        self.lines[line] = []
                    self.lines[line].append(object) #we append each object on the list of the line
                    if object == "X":
                        self.robot_position["line"] = line
                        self.robot_position["index"] = self.lines[line].index(object)
                else:
                    line += 1

    def __str__(self):
        map_to_print = ""
        dict_copy_lines = copy.deepcopy(self.lines) #we make a copy to avoid modifying the object attribute
        for position in dict_copy_lines.keys():
            dict_copy_lines[position].append('\n') #we add again the space at the end of each line to create a new line
            for object in dict_copy_lines[position]:
                map_to_print += object
        return map_to_print

    def __getstate__(self):
        """a special method to save the current dictionary of lines of the map.
         This will allow the game to come back to its original state after the
         player quit without finishing the game"""
        dict_attr = dict(self.__dict__)
        dict_attr["lines"] = self.lines
        return dict_attr

    def check_in_map(self, move_direction, position, game):
        """This represents a big part of the program.
        For each move required by the player, we first analyse if the number
        of moves required will not bring the player out of the map.
        If it is fine, we anlyse if the move is "n" or "s" for a move on
        lines or "e", "o" for a move on indexes.
        We analyse then each object on the way of the move to see if it is a wall (O),
        a door(.) or the exit(U).
        For each move we update the real position of the robot on the map.
        The function should return if the player has won or not """
        #we first make a copy of the real position of the robot before sartting the move and update the robot position
        #this will be helpfull when updating the map as we can act on the inital position and on the new position
        self.robot_initial_position = dict(self.robot_position)
        position_line = position["line"] #This is the line where we want the robot to move
        position_index = position["index"] #This is the index where we want the robot to move
        if position_line not in self.lines:
            print("---->You are out of the map, try again")
            return game.win
        if position_index > (len(self.lines[self.robot_position["line"]]) - 1) or \
        position_index < 0:
            print("---->You are out of the map, try again")
            return game.win
        if move_direction == "n":
            while self.robot_position["line"] != position_line:
                object = self.lines[self.robot_position["line"] - 1][self.robot_position["index"]]
                if object == "O":
                    break
                elif object == "U":
                    self.robot_position["line"] -=1
                    print("----->You have won!! Well done! You are out of the labyrinth<--------")
                    game.win = True
                else:
                    self.robot_position["line"] -=1
            return game.win
        if move_direction == "o":
            while self.robot_position["index"] != position_index:
                object = self.lines[self.robot_position["line"]][self.robot_position["index"] - 1]
                if object == "O":
                    break
                elif object == "U":
                    self.robot_position["index"] -=1
                    print("----->You have won!! Well done! You are out of the labyrinth<--------")
                    game.win = True
                else:
                    self.robot_position["index"] -=1
            return game.win
        if move_direction == "s":
            while self.robot_position["line"] != position_line:
                object = self.lines[self.robot_position["line"] + 1][self.robot_position["index"]]
                if object == "O":
                    break
                elif object == "U":
                    self.robot_position["line"] +=1
                    print("----->You have won!! Well done! You are out of the labyrinthe<--------")
                    game.win = True
                else:
                    self.robot_position["line"] +=1
            return game.win
        if move_direction == "e":
            while self.robot_position["index"] != position_index:
                object = self.lines[self.robot_position["line"]][self.robot_position["index"] + 1]
                if object == "O":
                    break
                elif object == "U":
                    self.robot_position["index"] +=1
                    print("----->You have won!! Well done! You are out of the labyrinth<--------")
                    game.win = True
                else:
                    self.robot_position["index"] +=1
            return game.win

    def update_map(self):
        """This will help to update the dictionary lines accoriding the new position
        of the robot after a move.
        If the move ends on a door (.), the attribute self.point will be changed
        to True so we can put the door back on the next move """
        line_to_empty = self.robot_initial_position["line"]
        index_to_empty = self.robot_initial_position["index"]
        line_to_fill = self.robot_position["line"]
        index_to_fill = self.robot_position["index"]
        if self.point:
            self.lines[line_to_empty][index_to_empty] = "."
            self.point = False
        else:
            self.lines[line_to_empty][index_to_empty] = " "
        if self.lines[line_to_fill][index_to_fill] == ".":
            self.point = True
            self.lines[line_to_fill][index_to_fill] = "X"
        else:
            self.lines[line_to_fill][index_to_fill] = "X"


class Robot:
    """We define the obejct robot with its position gotten from its position on the map."""

    def __init__(self, position):
        self.position = dict(position)

    def move(self, move_direction, number):
        """When a player request a move, the position of the robot will be updated and will be
        used in the map to check if the move is possible. """
        if move_direction == "n":
            self.position["line"] -= int(number)
            return self.position
        if move_direction == "s":
            self.position["line"] += int(number)
            return self.position
        if move_direction == "o":
            self.position["index"] -= int(number)
            return self.position
        if move_direction == "e":
            self.position["index"] += int(number)
            return self.position

class Game:
    """This class will be used to show all map availables for the game.
    It has the function to check if a game was on going to take back the map to its previous state.
    It also has the possibily to save automatically each move on the game as well as to delete
    an existing map if the play wants to start a new game"""
    def __init__(self, maps = []):
        self.maps = maps
        self.win = False #will be used to leave the game if True

    def found_map_avaialables(self):
        """This will read the titles of availables maps in the folder "cartes".
        Each map name will be added on the list of maps in the attribute. Then
        when the player will choose, the map name will be used to initialize the Labyrinth.
        We have a counter that we update on each read so we can add this number in the message
        when we ask the player to choose a map"""
        print("Existing labyrinths :")
        i = 1
        for file in os.listdir("cartes"):
            print("  ", i, " - ", file[:-4])
            i += 1
            self.maps.append(file)
        return i

    def unpack_map(self, map_name):
        """This function will be used to check if a previous game was started
        but not finished. It is checked with the map_name in a dictionary of the saved games.
        If it is the case, we will return the map and ask the player if if wants
        to continue playing or start a new party."""
        try:
            with open("map_history", "rb") as file:
                mon_unpickler = pickle.Unpickler(file)
                dictionary = mon_unpickler.load()
                if map_name in dictionary: #there is a previous game not finished
                    map = dictionary[map_name]
                    on_going_game = True
                    return map, on_going_game #we return the map in it previous state
                else: #no previous game was found
                    map = ""
                    on_going_game = False
                    return map, on_going_game
        except FileNotFoundError: #the file is not creatd so we create it
            with open("map_history", "wb") as file:
                mon_pickle = pickle.Pickler(file)
                dictionary = {}
                mon_pickle.dump(dictionary)
                map = ""
                on_going_game = False
                return map, on_going_game

    def delete_existing_game(self, map_name, map):
        """if there was a previous game on going but the player wants to start
        a new game, we delete the previous state of the map"""
        with open("map_history", "rb") as file:
            mon_unpickler = pickle.Unpickler(file)
            dictionary = mon_unpickler.load()
            with open("map_history", "wb") as file:
                my_pickle = pickle.Pickler(file)
                del dictionary[map_name]
                my_pickle.dump(dictionary)

    def automatic_save(self, map_name, map):
        """After each move, this function will be called to save the map states"""
        with open("map_history", "rb") as file:
            mon_unpickler = pickle.Unpickler(file)
            dictionary = mon_unpickler.load()
            with open("map_history", "wb") as file:
                my_pickle = pickle.Pickler(file)
                dictionary[map_name] = map
                my_pickle.dump(dictionary)

    def quit(self, map_name, win, map):
        """if the player decides to quit and did not win, we do a last save.
        if the player won, the map states is deleted so the next time, the game
        will start immediately with a renewed map"""
        with open("map_history", "rb") as file:
            mon_unpickler = pickle.Unpickler(file)
            dictionary = mon_unpickler.load()
            if win == False:
                with open("map_history", "wb") as file:
                    my_pickle = pickle.Pickler(file)
                    dictionary[map_name] = map
                    my_pickle.dump(dictionary)
                    print("Thank you for having played. Your game is saved. "
                    "See you soon!")
            else:
                with open("map_history", "wb") as file:
                    my_pickle = pickle.Pickler(file)
                    if map_name in dictionary:
                        del dictionary[map_name]
                    my_pickle.dump(dictionary)
