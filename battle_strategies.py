from abc import ABC, abstractmethod
from tkinter import *
from MyExceptions import FunctionBreakError
from units import RangeAttack


class BattleStrategy:
    @abstractmethod
    def __call__(self):
        pass
    def config(self, canvas, battle):
        #self.unit = unit
        self.canvas = canvas
        self.battle = battle
    def prepare(self, unit):
        #unit = self.unit
        self.canvas.bfs(unit.x, unit.y, unit.rest_speed)
        if isinstance(unit.make_attack, RangeAttack):
            self.canvas.mark_range_attack(unit)
    def go(self, unit, x, y):
        canvas = self.canvas
        #unit = self.unit
        dx = canvas.cells[x][y][0] - canvas.cells[unit.x][unit.y][0]
        dy = canvas.cells[x][y][1] - canvas.cells[unit.x][unit.y][1]
        canvas.move_unit(unit, dx, dy)
        canvas.blocked.remove((unit.x, unit.y))
        del canvas.positions[(unit.x, unit.y)]
        unit.rest_speed -= canvas.dist[x][y]
        unit.x = x
        unit.y = y
        canvas.blocked.add((unit.x, unit.y))
        canvas.positions[(unit.x, unit.y)] = unit
        

class ComputerBattleStrategy(BattleStrategy):
    def __call__(self, unit, index, event, command_type):
        self.prepare(unit)
        #print(self.unit.name, 'computer turn')
        canvas = self.canvas
        nearest = None
        for cell in canvas.blocked:
            if canvas.positions[cell].is_attack != unit.is_attack:
                if nearest is None or canvas.dist[nearest[0]][nearest[1]] > canvas.dist[cell[0]][cell[1]]:
                    nearest = cell
        x, y = nearest
        enemy = canvas.positions[nearest]
        can_attack = unit.make_attack(unit, enemy, canvas)
        if can_attack:
            unit.rest_speed = 0
            unit.update_army(canvas, self.battle)
            enemy.update_army(canvas, self.battle)
            canvas.clear()
            return
        for i in range(canvas.dist[x][y] - unit.rest_speed):
            x, y = canvas.prev[x][y]
        self.go(unit, x, y)
        self.canvas.clear()


class ManBattleStrategy(BattleStrategy):
    def __call__(self, unit, index, event, command_type):
        #self.apply_effects(unit)
        if event is None:
            self.prepare(unit)
            self.canvas.bind("<Button-1>", lambda event, foo=self.battle.turns, i=index: self.battle.get_mouse_click(foo, event, start_id=i))
            raise FunctionBreakError
        else:
            #print('commandtype=', command_type)
            click_place = self.canvas.nearest(event.x, event.y)
            if command_type == 'move':
                if type(click_place) == str:
                    if click_place == 'spell':
                        if hasattr(unit, 'cast'):
                            self.canvas.clear()
                            self.canvas.make_spell_variants(unit)
                            self.canvas.bind("<Button-1>", lambda event, foo=self.battle.turns, i=index, cmd=click_place: self.battle.get_mouse_click(foo, event, start_id=i, command_type=cmd))
                            raise FunctionBreakError
                        else:
                            self.canvas.bind("<Button-1>", lambda event, foo=self.battle.turns, i=index: self.battle.get_mouse_click(foo, event, start_id=i))
                            raise FunctionBreakError
                    elif click_place == 'wait':
                        self.canvas.clear()
                    else:
                        self.canvas.clear()
                elif click_place == -1:
                    self.canvas.bind("<Button-1>", lambda event, foo=self.battle.turns, i=index: self.battle.get_mouse_click(foo, event, start_id=i))
                    raise FunctionBreakError
                else:
                    x, y = click_place
                    self.execute_order(unit, x, y)
                    if unit.rest_speed > 0:
                        self.prepare(unit)
                        self.canvas.bind("<Button-1>", lambda event, foo=self.battle.turns, i=index: self.battle.get_mouse_click(foo, event, start_id=i))
                        raise FunctionBreakError
            else:
                if type(click_place) == str or click_place == -1:
                    self.canvas.clear()
                    self.prepare(unit)
                    self.canvas.bind("<Button-1>", lambda event, foo=self.battle.turns, i=index: self.battle.get_mouse_click(foo, event, start_id=i))
                    raise FunctionBreakError
                if self.canvas.check_spell_possible(click_place, unit, unit.spell.is_positive):
                    spelled_unit = unit.cast(self.canvas.positions[click_place] , unit.spell, unit.spell_time)
                    self.canvas.positions[click_place] = spelled_unit
                    for i in range(len(self.battle.units_in_battle)):
                        if self.battle.units_in_battle[i] is spelled_unit.unit:
                            self.battle.units_in_battle[i] = spelled_unit
                else:
                    self.canvas.clear()
                    self.prepare(unit)
                    self.canvas.bind("<Button-1>", lambda event, foo=self.battle.turns, i=index: self.battle.get_mouse_click(foo, event, start_id=i))
                    raise FunctionBreakError
                    

    
    def execute_order(self, unit, x, y):
        #unit = self.unit
        canvas = self.canvas
        new_cell = (x, y)
        if new_cell in canvas.blocked:
            if canvas.positions[new_cell].is_attack != unit.is_attack:
                enemy = canvas.positions[new_cell]
                can_attack = unit.make_attack(unit, enemy, canvas)
                if can_attack:
                    unit.rest_speed = 0
                    unit.update_army(canvas, self.battle)
                    enemy.update_army(canvas, self.battle)
        elif canvas.dist[x][y] <= unit.rest_speed:
            self.go(unit, x, y)
        self.canvas.clear()
        #print(self.unit.name, 'man turn', x, y)
        

if __name__ == '__main__':
    import battle
    battle.main()