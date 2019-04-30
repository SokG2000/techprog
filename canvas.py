# -*- coding: CP1251 -*-
from tkinter import *
from scrolledtext import ScrolledText
from collections import deque
from constants import Measure

class Mycanvas(Canvas):
    lines_num = 7
    def hexagon(self, x, y, r, string_nomber):
        polygon = self.create_polygon(x, y - r, x + int(r * (0.75) ** 0.5), y - r // 2, x + int(r * (0.75) ** 0.5), y + r // 2, x, y + r, x - int(r * (0.75) ** 0.5), y + r // 2, x - int(r * (0.75) ** 0.5), y - r // 2, fill='white', outline='black')
        self.hexagons[string_nomber].append(polygon)
        self.cells[string_nomber].append((x, y))
    def line(self, x, y, radius):
        self.hexagon(x, y, radius, 3)
        self.hexagon(x + int(radius * (0.75) ** 0.5), y - 2 * radius + radius // 2, radius, 2)
        self.hexagon(x + int(radius * (0.75) ** 0.5), y + 2 * radius - radius // 2, radius, 4)
        self.hexagon(x, y + radius * 3, radius, 5)
        self.hexagon(x, y - radius * 3, radius, 1)
        self.hexagon(x + int(radius * (0.75) ** 0.5), y + 4 * radius + radius // 2, radius, 6)
        self.hexagon(x + int(radius * (0.75) ** 0.5), y - 5 * radius + radius // 2, radius, 0)
    def bfs(self, x, y, rad):
        self.dist = [None] * self.lines_num
        self.prev = [None] * self.lines_num
        for i in range(self.lines_num):
            self.dist[i] = [None] * len(self.cells[i])
            self.prev[i] = [None] * len(self.cells[i])
        q = deque()
        self.dist[x][y] = 0;
        q.append((x, y))
        while q:
            u = q.popleft()
            for v in self.graf[u]:
                if self.dist[v[0]][v[1]] is None:
                    self.dist[v[0]][v[1]] = self.dist[u[0]][u[1]] + 1
                    self.prev[v[0]][v[1]] = u
                    if not v in self.blocked:
                        q.append(v)
        for i in range(self.lines_num):
            for j in range(len(self.cells[i])):
                if self.dist[i][j] is not None and self.dist[i][j] != 0 and self.dist[i][j] <= rad:
                    if not((i, j) in self.blocked and (x, y) in self.blocked and self.positions[(i, j)].is_attack == self.positions[(x, y)].is_attack):
                        self.itemconfig(self.hexagons[i][j], fill = 'grey')
        unit = self.positions[(x, y)]
        self.itemconfig(self.defend_button, fill='grey')
        if hasattr(unit, 'spell'):
            self.itemconfig(self.spell_button, fill='grey')
    def mark_range_attack(self, unit):
        for cell in self.blocked:
            if self.positions[cell].is_attack != unit.is_attack:
                x, y = cell
                self.itemconfig(self.hexagons[x][y], fill = 'grey')
    def clear(self):
        for i in range(self.lines_num):
            for j in range(len(self.cells[i])):
                self.itemconfig(self.hexagons[i][j], fill='white')
        self.itemconfig(self.spell_button, fill='white')
        self.itemconfig(self.wait_button, fill='white')
        self.itemconfig(self.defend_button, fill='white')
    def battle_field(self, radius, x1, y1):
        self.radius = radius
        self.cells = [None] * self.lines_num
        self.hexagons = [None] * self.lines_num
        for i in range(self.lines_num):
            self.cells[i] = []
            self.hexagons[i] = []
        self.hexagon(x1 - int(radius * (0.75) ** 0.5), y1 - 2 * radius + radius // 2, radius, 2)
        self.hexagon(x1 - int(radius * (0.75) ** 0.5), y1 + 2 * radius - radius // 2, radius, 4)
        self.line(x1, y1, radius)
        self.line(x1 + 2 * int(radius * (0.75) ** 0.5), y1, radius)
        self.line(x1 + 4 * int(radius * (0.75) ** 0.5), y1, radius)
        self.line(x1 + 6 * int(radius * (0.75) ** 0.5), y1, radius)
        self.line(x1 + 8 * int(radius * (0.75) ** 0.5), y1, radius)
        self.line(x1 + 10 * int(radius * (0.75) ** 0.5), y1, radius)
        self.line(x1 + 12 * int(radius * (0.75) ** 0.5), y1, radius)
        self.hexagon(x1 + 14 * int(radius * (0.75) ** 0.5), y1, radius, 3)
        self.hexagon(x1 + 14 * int(radius * (0.75) ** 0.5) + int(radius * (0.75) ** 0.5), y1 - 2 * radius + radius // 2, radius, 2)
        self.hexagon(x1 + 14 * int(radius * (0.75) ** 0.5) + int(radius * (0.75) ** 0.5), y1 + 2 * radius - radius // 2, radius, 4)
        self.hexagon(x1 + 14 * int(radius * (0.75) ** 0.5), y1 + radius * 3, radius, 5)
        self.hexagon(x1 + 14 * int(radius * (0.75) ** 0.5), y1 - radius * 3, radius, 1)
        self.graf = dict()
        for i in range(self.lines_num):
            for j in range(len(self.cells[i])):
                self.graf[(i, j)] = []
        tmp = radius * (3 ** 0.5)
        for i in range(self.lines_num):
            for j in range(len(self.cells[i])):
                for i1 in range(self.lines_num):
                    for j1 in range(len(self.cells[i1])):
                        dist = ((self.cells[i][j][0] - self.cells[i1][j1][0]) ** 2 + (self.cells[i][j][1] - self.cells[i1][j1][1]) ** 2) ** 0.5
                        if (abs(dist - tmp) < radius * 0.1):
                            self.graf[(i, j)].append((i1, j1))
        self.blocked = set()
        self.positions = dict()
        self.square_len = radius // 2
        self.spell_button = self.square(x1 + radius * 14, y1 + radius * 4, radius // 2, text='Cast')
        self.spell_button_coor = (x1 + radius * 14, y1 + radius * 4)
        self.wait_button = self.square(x1 + radius * 16, y1 + radius * 4, radius // 2, text='Wait')
        self.wait_button_coor = (x1 + radius * 16, y1 + radius * 4)
        self.defend_button = self.square(x1 + radius * 18, y1 + radius * 4, radius // 2, text='Pass')
        self.defend_button_coor = (x1 + radius * 18, y1 + radius * 4)
    def square(self, x, y, r, text=''):
        res = self.create_polygon(x - r, y - r, x + r, y - r, x + r, y + r, x - r, y + r, fill='white', outline='black')
        txt = self.create_text(x, y, text=text)
        return res
    def in_square(self, square_center, point, r):
        if square_center[0] - r > point[0]:
            return False
        if square_center[0] + r < point[0]:
            return False
        if square_center[1] - r > point[1]:
            return False
        if square_center[1] + r < point[1]:
            return False
        return True
    def move_army(self, army, dx, dy):
        self.move(army.image, dx, dy)
        self.move(army.label, dx, dy)
        self.move(army.band, dx, dy)
        self.move(army.health_band, dx, dy)
    def nearest(self, event_x, event_y):
        if self.in_square(self.spell_button_coor, (event_x, event_y), self.square_len):
            return 'spell'
        if self.in_square(self.wait_button_coor, (event_x, event_y), self.square_len):
            return 'wait'
        if self.in_square(self.defend_button_coor, (event_x, event_y), self.square_len):
            return 'defend'
        best_dist = None
        for i in range(self.lines_num):
            for j in range(len(self.cells[i])):
                tmp_x, tmp_y = self.cells[i][j][0], self.cells[i][j][1]
                dist = ((event_x - tmp_x) ** 2 + (event_y - tmp_y) ** 2) ** 0.5
                if best_dist == None or best_dist > dist:
                    best_x, best_y, best_dist = i, j, dist
        e = 5
        if best_dist > self.radius + e:
            return -1 # not cell
        return best_x, best_y
    def move_unit(self, unit, dx, dy):
        self.move(unit.image, dx, dy)
        self.move(unit.label, dx, dy)
        self.move(unit.band, dx, dy)
        self.move(unit.health_band, dx, dy)
    def check_spell_possible(self, cell, unit, is_positive_spell):
        if cell in self.blocked:
            if self.positions[cell].is_attack ^ unit.is_attack ^ unit.spell.is_positive:
                return True
        return False
    def make_spell_variants(self, unit):
        for cell in self.blocked:
            if self.check_spell_possible(cell, unit, 0):
                i, j = cell
                self.itemconfig(self.hexagons[i][j], fill = 'grey')
        

if __name__ == '__main__':
    def start(root):
        cells = [None] * 7
        for i in range(7):
            cells[i] = []
        canvas = Mycanvas(root, width=int(Measure * 1900 / 90), height=int(Measure * 1010 / 90), bg='white') # 0,0 - верхний левый угол
        canvas.battle_field(Measure, 2 * Measure, int(Measure * 500 / 90)) # было 90 180 500
        canvas.text = ScrolledText(text='Хроники боя\n')
        canvas.textid = canvas.create_window(int(Measure * 1420 / 90), int (Measure * 100 / 90), window=canvas.text, anchor=NW) # было 1420 100
        canvas.pack(expand=YES, fill=BOTH) # рост вниз и вправо
        return canvas
    root = Tk()
    start(root)
    root.mainloop()
