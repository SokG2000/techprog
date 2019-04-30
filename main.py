from abc import ABC, abstractmethod
from tkinter import *
from tkinter.messagebox import showinfo
from copy import copy
from MyExceptions import *
import units
import buildings
import constants
from constants import start_money
import creating_armies
from creating_armies import build_army
import battle_strategies
import battle
import turns

class Game():
    cell_income = 100
    def __init__(self, player_num):
        self.player_num = player_num
        self.players = [None] * player_num
        self.turn_num = 1
        self.lands = [None] * (player_num + 1)
        self.is_man = constants.is_man
        for i in range(player_num):
            self.lands[i] = i
    def end_turn(self):
        for player in self.players:
            player.end_turn()
        for player_id in self.lands:
            if player_id is not None:
                self.players[player_id].money += self.cell_income
        self.turn_num += 1
        self.check_end()
    def check_end(self):
        rest_man = 0
        last_man = -1
        rest_computer = 0
        for i in range(self.player_num):
            if not self.players[i].died:
                if self.is_man[i]:
                    rest_man += 1
                    last_man = i
                else:
                    rest_computer += 1
        if rest_man == 0:
            self.end_game('Computer won')
        if rest_computer == 0 and rest_man == 1:
            self.end_game('Player {} won'.format(last_man))
    def end_game(self, s):
        showinfo('', s)
        raise EndGameException()

class Player(ABC):
    def __init__(self, cell):
        self.cell = cell
        self.money = start_money
        self.armies = [None] * (constants.player_num + 1)
        self.buildings = []
        self.died = False
    def __str__(self):
        s = 'money = ' + str(self.money) + '\narmies:'
        for x in self.armies:
            if x is not None:
                #s += str(x.cell) + ': '
                #for unit in x.units:
                #    s += str(unit) + ' ' + str(unit.amount) + '   '
                s += str(x)
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
        if self.armies[cell] is None:
            self.armies[cell] = Army(cell)
    #def find_army(self, cell):
    #    for i in range(len(self.armies)):
    #        if cell == self.armies[i].cell:
    #            return i
    #    return -1
    def end_turn(self):
        for building in self.buildings:
            building.end_turn_action(self)
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
    #loving_unit_id = 4
    #loving_building_id = 3
    loving_unit_id = 3
    loving_building_id = 1
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
    loving_unit_id = 1
    loving_building_id = 2
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
    def __str__(self):
        res = str(self.cell) + ': '
        for unit in self.units:
            res += str(unit) + ' ' + str(unit.amount) + ' '
        return res
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
    def add_unit(self, unit):
        i = self.find_unit(unit)
        if i == -1:
            self.units.push_back(unit)
        else:
            self.units[i].amount += unit.amount        
    def merge_armies(self, other):
        for unit in other.units:
            self.add_unit(unit)
        other.army = []


player_races = [ManPlayer, ElfPlayer]


def create_player(game, race, index, root, cell):
    #print(race)
    game.players[index] = race(cell)
    root.destroy()


def make_man_player(game, index):
    root = Tk()
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.wm_geometry("+%d+%d" % (x, y))
    text = Label(root, height=1, width=20, text='Choose a race')
    text.grid(row=0)
    for i in range(len(player_races)):
        button = Button(root, height=2, width=20, text=player_races[i]._race, command=lambda i=i: create_player(game, player_races[i], index, root, index))
        button.grid(row=i + 1, column=0)
    root.mainloop()
    if game.players[index] is None:
        return
    game.players[index].build_army = creating_armies.BuildPlayerArmyCommand()
    game.players[index].battle_strategy = battle_strategies.ManBattleStrategy()
    game.players[index].turn_strategy = turns.ManTurnStrategy()
    game.players[index].turn_strategy.config(game.players[index])


def make_computer_player(game, index):
    race_id = 0
    race = player_races[race_id]
    game.players[index] = race(index)
    #create_player(game, player_races[race_id], index, root, index)
    game.players[index].build_army = creating_armies.BuildComputerArmyCommand()
    game.players[index].battle_strategy = battle_strategies.ComputerBattleStrategy()
    game.players[index].turn_strategy = turns.ComputerTurnStrategy()
    game.players[index].turn_strategy.config(game.players[index])


def main_loop(game):
    while True:
        for i in range(game.player_num):
            player = game.players[i]
            player.build_army(player)
            player.turn_strategy.make_turn(game)
        game.end_turn()


def main():
    game = Game(constants.player_num)
    for i in range(constants.player_num):
        if constants.is_man[i]:
            make_man_player(game, i)
        else:
            make_computer_player(game, i)
        if game.players[i] is None:
            return
    for i in range(constants.player_num):
        game.players[i].index = i
    for player in game.players:
        player.build_army(player)
    for player in game.players:
        print(player)
    try:
        main_loop(game)
    except EndGameException:
        pass


if __name__ == '__main__':
    main()
