# -*- coding: CP1251 -*-
import copy
from units import *
from buildings import *
from tkinter import *
from constants import button_height, button_width
from tkinter.messagebox import showinfo

class ArmyBuilder:
    def __init__(self, player, army):
        self.player = player
        self.army = army
    def add_unit(self, unit):
        index = self.army.find_unit(unit)
        if index == -1:
            self.army.units.append(unit)
        else:
            self.army.units[index].amount += 1
    def buy_unit(self, factory):
        unit = factory.buy_unit(self.player)
        self.add_unit(unit)


class BuildingsBuilder:
    def __init__(self, player):
        self.player = player
    def buy_building(self, factory):
        self.player.buildings.append(factory.buy_building(self.player))
    

def update(player, money_label, units, hired_armies, hired_units, buildings, builded_buildings):
    i = 0
    for x in units:
        if i < len(hired_armies):
            hired_armies[i].config(text=str(x) + ' ' + str(x.amount))
        else:
            hired_armies.append(Label(hired_units, text=str(x) + ' ' + str(x.amount)))
            hired_armies[i].grid(row=i + 1)
        i += 1
    i = 0
    for x in player.buildings:
        if i < len(buildings):
            buildings[i].config(text=str(x))
        else:
            buildings.append(Label(builded_buildings, text=str(x)))
            buildings[i].grid(row=i + 1)
        i += 1
    money_label.config(text = 'осталось ' + str(player.money) + ' денег')

def hire_button_action(army_builder, factory, money_label, hired_armies, hired_units, buildings, builded_buildings):
    try:
        army_builder.buy_unit(factory)
    except MyError:
        showinfo('', MyError.txt)
    update(army_builder.player, money_label, army_builder.army.units, hired_armies, hired_units, buildings, builded_buildings)


def build_button_action(building_builder, factory, money_label, units, hired_armies, hired_units, buildings, builded_buildings):
    try:
        building_builder.buy_building(factory)
    except MyError:
        showinfo('', MyError.txt)
    update(building_builder.player, money_label, units, hired_armies, hired_units, buildings, builded_buildings)


class BuildArmyCommand:
    pass


class BuildPlayerArmyCommand(BuildArmyCommand):
    def __call__(self, player):
        if player.died:
            return
        #index = player.find_army(player.cell)
        #if index == -1:
        #    player.add_army(player.cell)
        #    index = len(player.armies) - 1
        if player.armies[player.cell] is None:
            player.add_army(player.cell)
        army_builder = ArmyBuilder(player, player.armies[player.cell])
        building_builder = BuildingsBuilder(player)
        try:
            building_builder.buy_building(player.building_factories[0]) #build palace if not exists
        except MyError:
            pass #nothing if exists
        #print(player)
        root = Tk()
        money_label = Label(root, text='осталось ' + str(player.money) + ' денег')
        money_label.grid(columnspan=2, row=0)
        possible_buildings = Frame(root, width=300, height=300)
        builded_buildings = Frame(root, width=300, height=300)
        possible_units = Frame(root, width=300, height=300)
        hired_units = Frame(root, width=300, height=300)
        possible_buildings.grid(row=1, column=0, sticky=N+S+W+E)
        builded_buildings.grid(row=2, column=0, sticky=N+S+W+E)
        possible_units.grid(row=1, column=1, sticky=N+S+W+E)
        hired_units.grid(row=2, column=1, sticky=N+S+W+E)
        possible_buildings_label = Label(possible_buildings, height=button_height, width=button_width, text='построить')
        builded_buildings_label = Label(builded_buildings, height=button_height, width=button_width, text='здания')
        possible_units_label = Label(possible_units, height=button_height, width=button_width, text='нанять')
        hired_units_label = Label(hired_units, height=button_height, width=button_width, text='войска')
        possible_buildings_label.grid(row=0, sticky=N+S+W+E)
        builded_buildings_label.grid(row=0, sticky=N+S+W+E)
        possible_units_label.grid(row=0, sticky=N+S+W+E)
        hired_units_label.grid(row=0, sticky=N+S+W+E)
        build_buttons = []
        i = 0
        for x in player.building_factories:
            build_buttons.append(Button(possible_buildings, height=button_height, width=button_width, text=str(x), command=lambda x=copy.copy(x): build_button_action(building_builder, x, money_label, army_builder.army.units, hired_armies, hired_units, buildings, builded_buildings)))
            build_buttons[i].grid(row=i + 1,  sticky=N+S+W+E)
            i += 1
        i = 0
        hire_buttons = []
        for x in player.units_factories:
            hire_buttons.append(Button(possible_units, height=button_height, width=button_width, text=str(x), command=lambda x=copy.copy(x): hire_button_action(army_builder, x, money_label, hired_armies, hired_units, buildings, builded_buildings)))
            hire_buttons[i].grid(row=i + 1,  sticky=N+S+W+E)
            i += 1
        hired_armies = []
        i = 0
        for x in army_builder.army.units:
            hired_armies.append(Label(hired_units, height=button_height, width=button_width, text=str(x) + ' ' + str(x.amount)))
            hired_armies[i].grid(row=i + 1)
            i += 1
        buildings = []
        i = 0
        for x in player.buildings:
            buildings.append(Label(builded_buildings, height=button_height, width=button_width, text=str(x)))
            buildings[i].grid(row=i + 1)
            i += 1
        quit_button = Button(root, text='Ok', command=root.destroy)
        quit_button.grid(columnspan=2, row=3)
        x_len = 50 * (len(player.units_factories) * 2)
        y_len = 300
        x = (root.winfo_screenwidth() - root.winfo_reqwidth() - x_len) / 2
        y = (root.winfo_screenheight() - root.winfo_reqheight() - y_len) / 2
        root.wm_geometry("+%d+%d" % (x, y))
        root.mainloop()
        print(player)


class BuildComputerArmyCommand(BuildArmyCommand):
    def __call__(self, player):
        if player.died:
            return
        #index = player.find_army(player.cell)
        #if index == -1:
        #    player.add_army(player.cell)
        #    index = len(player.armies) - 1
        if player.armies[player.cell] is None:
            player.add_army(player.cell)
        army_builder = ArmyBuilder(player, player.armies[player.cell])
        #index = player.find_army(player.cell)
        #if index == -1:
        #    player.add_army(player.cell)
        #    index = len(player.armies) - 1
        #army_builder = ArmyBuilder(player, player.armies[index])
        building_builder = BuildingsBuilder(player)
        try:
            building_builder.buy_building(player.building_factories[0]) #build palace if not exists
        except MyError:
            pass #nothing if exists
        #print(player)
        try:
            building_builder.buy_building(player.building_factories[player.loving_building_id]) #build loving building if not exists
        except MyError:
            pass #nothing if exists
        while player.money > 0:
            try:
                army_builder.buy_unit(player.units_factories[player.loving_unit_id]) #hire loving army while possible
            except MyError:
                break           
        print(player)


def build_army(player):
    index = player.find_army(player.cell)
    if index == -1:
        player.add_army(player.cell)
        index = len(player.armies) - 1
    army_builder = ArmyBuilder(player, player.armies[index])
    building_builder = BuildingsBuilder(player)
    try:
        building_builder.buy_building(player.building_factories[0]) #build palace if not exists
    except MyError:
        pass #nothing if exists
    #print(player)
    root = Tk()
    money_label = Label(root, text='осталось ' + str(player.money) + ' денег')
    money_label.grid(columnspan=2, row=0)
    possible_buildings = Frame(root, width=300, height=300)
    builded_buildings = Frame(root, width=300, height=300)
    possible_units = Frame(root, width=300, height=300)
    hired_units = Frame(root, width=300, height=300)
    possible_buildings.grid(row=1, column=0, sticky=N+S+W+E)
    builded_buildings.grid(row=2, column=0, sticky=N+S+W+E)
    possible_units.grid(row=1, column=1, sticky=N+S+W+E)
    hired_units.grid(row=2, column=1, sticky=N+S+W+E)
    possible_buildings_label = Label(possible_buildings, height=button_height, width=button_width, text='построить')
    builded_buildings_label = Label(builded_buildings, height=button_height, width=button_width, text='здания')
    possible_units_label = Label(possible_units, height=button_height, width=button_width, text='нанять')
    hired_units_label = Label(hired_units, height=button_height, width=button_width, text='войска')
    possible_buildings_label.grid(row=0, sticky=N+S+W+E)
    builded_buildings_label.grid(row=0, sticky=N+S+W+E)
    possible_units_label.grid(row=0, sticky=N+S+W+E)
    hired_units_label.grid(row=0, sticky=N+S+W+E)
    build_buttons = []
    i = 0
    for x in player.building_factories:
        build_buttons.append(Button(possible_buildings, height=button_height, width=button_width, text=str(x), command=lambda x=copy.copy(x): build_button_action(building_builder, x, money_label, army_builder.army.units, hired_armies, hired_units, buildings, builded_buildings)))
        build_buttons[i].grid(row=i + 1,  sticky=N+S+W+E)
        i += 1
    i = 0
    hire_buttons = []
    for x in player.units_factories:
        hire_buttons.append(Button(possible_units, height=button_height, width=button_width, text=str(x), command=lambda x=copy.copy(x): hire_button_action(army_builder, x, money_label, hired_armies, hired_units, buildings, builded_buildings)))
        hire_buttons[i].grid(row=i + 1,  sticky=N+S+W+E)
        i += 1
    hired_armies = []
    i = 0
    for x in army_builder.army.units:
        hired_armies.append(Label(hired_units, height=button_height, width=button_width, text=str(x) + ' ' + str(x.amount)))
        hired_armies[i].grid(row=i + 1)
        i += 1
    buildings = []
    i = 0
    for x in player.buildings:
        buildings.append(Label(builded_buildings, height=button_height, width=button_width, text=str(x)))
        buildings[i].grid(row=i + 1)
        i += 1
    quit_button = Button(root, text='Ok', command=root.destroy)
    quit_button.grid(columnspan=2, row=3)
    x_len = 50 * (len(player.units_factories) * 2)
    y_len = 300
    x = (root.winfo_screenwidth() - root.winfo_reqwidth() - x_len) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight() - y_len) / 2
    root.wm_geometry("+%d+%d" % (x, y))
    root.mainloop()
    print(player)


if __name__ == '__main__':
    from main import *
    game = Game(2)
    game.players[0] = ManPlayer(0)
    build_army(game.players[0])
