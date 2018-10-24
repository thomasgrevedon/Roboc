import copy
import os

class Labyrinth:

    def __init__(self, name):
        with open(name, "r") as file:
            self.lines = {}
            self.robot_position = {}
            self.robot_initial_position = {}
            self.point = False
            line = 1
            for object in file.read():
                if object != "\n":
                    if line not in self.lines:
                        self.lines[line] = []
                    self.lines[line].append(object)
                    if object == "X":
                        self.robot_position["line"] = line
                        self.robot_position["index"] = self.lines[line].index(object)
                else:
                    line += 1

    def __str__(self):
        map_to_print = ""
        dict_copy_lines = copy.deepcopy(self.lines)
        for position in dict_copy_lines.keys():
            dict_copy_lines[position].append('\n')
            for object in dict_copy_lines[position]:
                map_to_print += object
        return map_to_print

    def check_in_map(self, move_direction, position, game):
        self.robot_initial_position = dict(self.robot_position)
        #print("before any check in map", self.robot_position)
        position_line = position["line"]
        position_index = position["index"]
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
                    print("----->You have won!! Well done! You are out of the labyrinthe<--------")
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
                    print("----->You have won!! Well done! You are out of the labyrinthe<--------")
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
                    print("----->You have won!! Well done! You are out of the labyrinthe<--------")
                    game.win = True
                else:
                    self.robot_position["index"] +=1
            return game.win

    def update_map(self):
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

    def __init__(self, position):
        self.position = dict(position)

    def move(self, move_direction, number):
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

    def __init__(self, maps = []):
        self.maps = maps
        self.win = False

    def found_map_avaialables(self):
        print("Existing labyrinths :")
        i = 1
        for file in os.listdir("cartes"):
            print("  ", i, " - ", file[:-4])
            i += 1
            self.maps.append(file)
        return i

    def quit(self):
        print("We are going to leave and save")
