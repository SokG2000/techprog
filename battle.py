# -*- coding: CP1251 -*-
from tkinter import *
import copy
import random
#import canvas
from canvas import Mycanvas, ScrolledText
from MyExceptions import FunctionBreakError, catch_break_error
from tkinter.messagebox import showinfo
#Measure = 60
#picture_size = "80"
from constants import Measure, picture_size


class UnitInBattle:
    def __init__(self, unit, battle, x, y, now_tag, strategy, is_attack, index):
        canvas = battle.canvas
        r = canvas.radius
        self.characteristics = {}
        for name, val in unit.characteristics.items():
            self.characteristics[name] = val
            setattr(self, name, val)
        self.amount = unit.amount
        self.make_attack = unit.attack
        self.is_attack = is_attack
        self.name = unit._name
        if hasattr(unit, 'cast'):
            self.cast = unit.cast
            self.spell = unit.spell
            self.spell_time = unit.spell_time
        self.now_health = self.max_health
        self.rest_speed = self.speed
        self.make_hit_back = True
        self.tag = now_tag
        self.x = x
        self.y = y
        self.died = False
        self.act = copy.copy(strategy)
        self.act.config(canvas, battle)
        self.index = index
        #self.act.unit = self
        print('x =', x, 'y =', y)
        now_x = canvas.cells[x][y][0]
        now_y = canvas.cells[x][y][1]
        s = 'pictures\\\\' + picture_size + '\\\\' + self.name + '.gif'    
        self.photo = PhotoImage(file=s)
        self.image = canvas.create_image(now_x - round(r * 0.55), now_y - round(r * 0.72), image=self.photo, anchor=NW, tag=now_tag)
        self.label = canvas.create_text(now_x, now_y + round(r * 0.72), text=self.amount, anchor=NW, tag=now_tag)
        self.band = canvas.create_rectangle(now_x - round(r * 0.33), now_y + round(r * 0.66), now_x + round(r * 0.33), now_y + round(r * 0.77), fill='white', outline='black', tag=now_tag)
        self.band_len = round(r * 0.66) * 2
        self.r = r
        if is_attack:
            self.band_color = 'blue'
        else:
            self.band_color = 'red'
        self.health_band = canvas.create_rectangle(now_x - round(r * 0.33), now_y + round(r * 0.66), now_x + round(r * 0.33), now_y + round(r * 0.77), fill=self.band_color, outline='black', tag = now_tag)
        canvas.blocked.add((self.x, self.y))
        canvas.positions[(self.x, self.y)] = self
    def take_damage(self, amount, min_damage, max_damage, attack, name, canvas):
        minimum = amount * min_damage
        maximum = amount * max_damage
        if self.defense > attack:
            difference = min(self.defense - attack, 60)
            change = (1 + difference / 30)
            minimum = int(minimum / change)
            maximum = int(maximum / change)
        else:
            difference = min(attack - self.defense, 60)
            change = (1 + difference / 30)
            minimum = int(minimum * change)
            maximum = int(maximum * change)
        damage = random.randint(minimum, maximum + 1)
        all_health = self.now_health + (self.amount - 1) * self.max_health
        new_health = max(0, all_health - damage)
        new_amount = (new_health - 1) // self.max_health + 1
        killed = self.amount - new_amount
        if killed > 0:
            canvas.text.insert('2.0', str(name) + ' наносят урон ' + str(damage) + ',\nпогибают ' + str(self.name) + ' ' + str(killed) + '.\n\n')
        else:
            canvas.text.insert('2.0', str(name) + ' наносят урон ' + str(damage) + ', цель - ' + str(self.name) + '.\n\n')
        canvas.text.mark_set('insert', 'end')
        #canvas.text.text.focus()
        self.amount = new_amount
        self.now_health = new_health - (self.amount - 1) * self.max_health
        if self.amount == 0:
            self.died = True
    def update_army(self, canvas, battle):
        canvas.itemconfig(self.label, text=self.amount)
        if self.died:
            canvas.delete(self.label)
            canvas.delete(self.image)
            canvas.delete(self.band)
            canvas.delete(self.health_band)
            canvas.blocked.remove((self.x, self.y))
            del canvas.positions[(self.x, self.y)]
            if self.is_attack:
                battle.attack_units_rest -= 1
            else:
                battle.defense_units_rest -= 1
            if battle.attack_units_rest == 0:
                showinfo('', "Defense player won")
                battle.battle_root.quit()
                raise FunctionBreakError
            if battle.defense_units_rest == 0:
                showinfo('', "Attack player won")
                battle.battle_root.quit()
                raise FunctionBreakError
    def decrease_effects_time(self):
        return self
    #def new_turn(self):
    #    self.rest_speed = self.speed
    #    self.decrease_time()


class Battle:
    def __init__(self, attack_player, defense_player, cell):
        self.attack_player = attack_player
        self.defense_player = defense_player
        if attack_player.armies[cell] is None or attack_player.armies[cell].units == []:
            self.attack_army_id = -1
        else:
            self.attack_army_id = cell
        #self.attack_army_id = attack_player.find_army(cell)
        if self.attack_army_id != -1: # must be always true
            self.attack_army = attack_player.armies[self.attack_army_id]
            self.attack_units_rest = len(self.attack_army.units)
        if defense_player.armies[cell] is None or defense_player.armies[cell].units == []:
            self.defense_army_id = -1
        else:
            self.defense_army_id = cell
        #self.defense_army_id = defense_player.find_army(cell)
        if self.defense_army_id != -1:
            self.defense_army = defense_player.armies[self.defense_army_id]
            self.defense_units_rest = len(self.defense_army.units)
    def start_pos(self):
        order = (3, 1, 5, 2, 4, 0, 6)
        r = self.canvas.radius
        i = 0
        self.units_in_battle = [None] * (len(self.attack_army.units) + len(self.defense_army.units))
        for unit in self.attack_army.units:
            now_tag = str(i)
            self.units_in_battle[i] = UnitInBattle(unit, self, order[i], 0, now_tag, self.attack_player.battle_strategy, True, i)
            i += 1
        attack_num = i
        for unit in self.defense_army.units:
            now_tag = str(i)
            x = order[i - len(self.attack_army.units)]
            print("x =", x)
            self.units_in_battle[i] = UnitInBattle(unit, self, x, len(self.canvas.cells[x]) - 1, now_tag, self.defense_player.battle_strategy, False, i - attack_num)
            i += 1


    def initiative_cmp(self, army):
        res = (-army.initiative, -army.speed, army.max_health)
        return res
    
    
    def on_mouse_click(self, event):
        click_place = self.canvas.nearest(event.x, event.y)
        print(click_place)
        if click_place == -1:
            return
        self.battle_root.quit()
        print(self.canvas.nearest(event.x, event.y))
    
    
    def get_mouse_click(self, foo, event, **quargs):
        foo(event=event, **quargs)
    
    
    def end_game(self):
        for unit in self.units_in_battle:
            if unit.is_attack:
                self.attack_army.units[unit.index].amount = unit.amount
            else:
                self.defense_army.units[unit.index].amount = unit.amount
        print(self.attack_army)
        print(self.defense_army)
        if self.attack_units_rest == 0:
            self.battle_root.destroy()
            return False
        self.battle_root.destroy()
        return True
    
    
    def start_battle(self): # ends when battle is finished, returns result, true if attack was sucsessful
        if self.attack_army_id == -1: # must be always false
            return False
        if self.defense_army_id == -1:
            return True
        self.battle_root = Tk()
        self.canvas = Mycanvas(self.battle_root, width=int(Measure * 1900 / 90), height=int(Measure * 1010 / 90), bg='white')
        self.canvas.battle_field(Measure, 2 * Measure, int(Measure * 500 / 90)) # было 90 180 500
        self.canvas.text = ScrolledText(text='Хроники боя\n')
        self.canvas.textid = self.canvas.create_window(int(Measure * 1420 / 90), int (Measure * 100 / 90), window=self.canvas.text, anchor=NW) # было 1420 100
        self.canvas.pack(expand=YES, fill=BOTH) # рост вниз и вправо
        self.start_pos()
        self.turns()
        self.battle_root.mainloop()
        return self.end_game()
    
    def unit_start_turn(self, unit, i):
        old = unit
        unit = unit.decrease_effects_time()
        unit.rest_speed = unit.speed
        if not unit is old:
            self.canvas.positions[(unit.x, unit.y)] = unit
            self.units_in_battle[i] = unit
            x = 0
    
    def start_turn(self):
        self.units_in_battle.sort(key=self.initiative_cmp)
        for i in range(len(self.units_in_battle)):
            unit = self.units_in_battle[i]
            self.unit_start_turn(unit, i)
            #unit.rest_speed = unit.speed
    
    
    @catch_break_error
    def turns(self, start_id=0, event=None, command_type='move'):
        while True:
            if event is None:
                self.start_turn()
                #self.units_in_battle.sort(key=self.initiative_cmp)
            for i in range(start_id, len(self.units_in_battle)):
                unit = self.units_in_battle[i]
                if not unit.died:
                    unit.act(unit, i, event, command_type)
                event = None
            start_id = 0
        
        


def main():
    import main
    import units
    import creating_armies
    game = main.Game(2)
    main.make_computer_player(game, 0)
    main.make_man_player(game, 1)
    #game.players[1].build_army = creating_armies.BuildComputerArmyCommand()
    game.players[0].build_army(game.players[0])
    game.players[1].build_army(game.players[1])
    game.players[1].armies[0] = game.players[1].armies[1]
    battle = Battle(game.players[0], game.players[1], 0)
    if battle.start_battle():
        print("Attack player won")
    else:
        print("Defense player won")        
    x = 0


if __name__ == '__main__':
    main()