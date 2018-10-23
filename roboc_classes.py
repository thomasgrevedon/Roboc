import copy
import os

class Labyrinth:

    def __init__(self, name):
        with open(name, "r") as file:
            self.lines = {}
            self.robot_position = {}
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

class Robot:

    def __init__(self, position):
        self.position = dict(position)

class Game:

    def __init__(self, maps = []):
        self.maps = maps

    def found_map_avaialables(self):
        print("Labyrinthes existants :")
        i = 1
        for file in os.listdir("cartes"):
            print("  ", i, " - ", file[:-4])
            i += 1
            self.maps.append(file)
        return i
