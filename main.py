from abc import ABC, abstractmethod
from tkinter import *
from tkinter.simpledialog import askinteger
from copy import copy
from MyExceptions import *
import units
import sys
import buildings
from constants import start_money
import creating_armies
from creating_armies import build_army

class Game():
    def __init__(self, player_num):
        self.players = [None] * player_num

class Player(ABC):
    def __init__(self, cell):
        self.cell = cell
        self.money = start_money
        self.armies = []
        self.buildings = []
    def __str__(self):
        s = 'money = ' + str(self.money) + '\narmies:'
        for x in self.armies:
            s += str(x.cell) + ': '
            for unit in x.units:
                s += str(unit) + ' ' + str(unit.amount) + '   '
        s += ('\nbuildings: ')
        for x in self.buildings:
            s += str(x) + '   '
        return s + '\n'
    def has_building(self, building_type):
        for x in self.buildings:
            if type(x) == building_type:
                return True
        return False
    def get_building_level(self, building_type):
        for x in self.buildings:
            if type(x) == building_type:
                return x.level
        return 0
    def add_army(self, cell):
        self.armies.append(Army(cell))
    def find_army(self, cell):
        for i in range(len(self.armies)):
            if cell == self.armies[i].cell:
                return i
        return -1
    @abstractmethod
    def f(self):
        pass
    

class ManPlayer(Player):
    _race = 'man'
    units_factories = []
    building_factories = []
    for factory in units.all_unit_factories:
        if factory._race == _race:
            units_factories.append(factory())
    for factory in buildings.all_building_factories:
        if factory._race == _race:
            building_factories.append(factory()) 
    def __init__(self, cell):
        super().__init__(cell)
    def __str__(self):
        return 'ManPlayer\n' + super().__str__()
    def f(self):
        pass


class ElfPlayer(Player):
    _race = 'elf'
    units_factories = []
    building_factories = []
    for factory in units.all_unit_factories:
        if factory._race == _race:
            units_factories.append(factory())
    for factory in buildings.all_building_factories:
        if factory._race == _race:
            building_factories.append(factory()) 
    def __init__(self, cell):
        super().__init__(cell)
    def __str__(self):
        return 'ElfPlayer\n' + super().__str__()
    def f(self):
        pass


class Army:
    def __init__(self, cell):
        self.units = []
        self.cell = cell
    def __eq__(self, other):
        if (self.cell != other.cell):
            return False
        if (self.units != other.units):
            return False
        return True
    def find_unit(self, unit):
        for i in range(len(self.units)):
            if type(unit) == type(self.units[i]):
                return i
        return -1


player_races = [ManPlayer, ElfPlayer]


def create_player(game, race, index, root, cell):
    #print(race)
    game.players[index] = race(cell)
    root.destroy()


if __name__ == '__main__':
    player_num = 2
    game = Game(player_num)
    root = Tk()
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.wm_geometry("+%d+%d" % (x, y))
    text = Label(root, height=1, width=20, text='Choose a race')
    text.grid(row=0)
    for i in range(len(player_races)):
        button = Button(root, height=2, width=20, text=player_races[i]._race, command=lambda i=i: create_player(game, player_races[i], 0, root, 0))
        button.grid(row=i + 1, column=0)
    root.mainloop()
    #print(game.players)
    if game.players[0] is not None:
        build_army(game.players[0])
    
