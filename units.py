from abc import ABC, abstractmethod
import buildings
import spells
from MyExceptions import *

class Unit(ABC):
    @abstractmethod
    def move(self):
        pass
    @abstractmethod
    def attack(self):
        pass
    def __init__(self, amount=1):
        self.amount = amount
    def __str__(self):
        return self._name
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.amount != other.amount:
            return False
        if self.characteristics != other.characteristics:
            return False
        return True
    

class AttackCommand(ABC):
    @abstractmethod
    def __call__(self):
        pass


class RangeAttack(AttackCommand):
    def __call__(self, unit, other_unit, canvas):
        other_unit.take_damage(unit.amount, unit.min_damage, unit.max_damage, unit.attack, unit.name, canvas)
        #print(unit._name + 'attacked')
        return True


class InfantryAttack(AttackCommand):
    def __call__(self, unit, other_unit, canvas):
        new_x = other_unit.x
        new_y = other_unit.y
        if canvas.dist[new_x][new_y] == 1:
            #now_army.rest_speed = 0
            other_unit.take_damage(unit.amount, unit.min_damage, unit.max_damage, unit.attack, unit.name, canvas)
            if (other_unit.make_hit_back and (not other_unit.died)):
                unit.take_damage(other_unit.amount, other_unit.min_damage, other_unit.max_damage, other_unit.attack, other_unit.name, canvas)
            return True
        if canvas.dist[new_x][new_y] <= unit.rest_speed:
            newx, newy = canvas.prev[new_x][new_y]
            dx = canvas.cells[newx][newy][0] - canvas.cells[unit.x][unit.y][0]
            dy = canvas.cells[newx][newy][1] - canvas.cells[unit.x][unit.y][1]
            canvas.move_unit(unit, dx, dy)
            canvas.blocked.remove((unit.x, unit.y))
            del canvas.positions[(unit.x, unit.y)]
            unit.x = newx
            unit.y = newy
            canvas.blocked.add((unit.x, unit.y))
            canvas.positions[(unit.x, unit.y)] = unit
            other_unit.take_damage(unit.amount, unit.min_damage, unit.max_damage, unit.attack, unit.name, canvas)
            if (other_unit.make_hit_back and(not other_unit.died)):
                unit.take_damage(other_unit.amount, other_unit.min_damage, other_unit.max_damage, other_unit.attack, other_unit.name, canvas)
            return True
        return False



class Infantry(Unit):
    def move(self):
        print(self._name + ' moved')
    attack = InfantryAttack()

class Magican(Unit):
    def move(self):
        print(self._name + ' moved')
    def cast(self, unit, spell, spell_time):
        return spell(unit, spell_time)
    attack = RangeAttack()



class Rifleman(Unit):
    def move(self):
        print(self._name + ' moved')
    attack = RangeAttack()



class Archer(Rifleman):
    _name = 'Archer'
    def __init__(self):
        super().__init__()
        self.characteristics = {"max_health" : 30, "defense": 16, "min_damage" : 2, "max_damage" : 3, "attack" : 3, "speed" : 2, "initiative" : 4}
        #print(self._name + ' created')


class Peasant(Infantry):
    _name = 'Peasant'
    def __init__(self):
        super().__init__()
        self.characteristics = {"max_health" : 6, "defense": 1, "min_damage" : 1, "max_damage" : 2, "attack" : 1, "speed" : 2, "initiative" : 2}
        #print(self._name + ' created')


class Swordman(Infantry):
    _name = 'Swordman'
    def __init__(self):
        super().__init__()
        self.characteristics = {"max_health" : 50, "defense": 16, "min_damage" : 3, "max_damage" : 4, "attack" : 5, "speed" : 3, "initiative" : 4}
        #print(self._name + ' created')


class Knight(Infantry):
    _name = 'Knight'
    def __init__(self):
        super().__init__()
        self.characteristics = {"max_health" : 160, "defense": 27, "min_damage" : 16, "max_damage" : 18, "attack" : 27, "speed" : 2, "initiative" : 4}
        #print(self._name + ' created')


class Mage(Magican):
    _name = 'Mage'
    def __init__(self):
        super().__init__()
        self.characteristics = {"max_health" : 70, "defense": 16, "min_damage" : 3, "max_damage" : 4, "attack" : 15, "speed" : 2, "initiative" : 6}
        #print(self._name + ' created')
        self.spell = spells.SlowSpell
        self.spell_time = 3


class ElfArcher(Rifleman):
    _name = 'Elf'
    def __init__(self):
        super().__init__()
        self.characteristics = {"max_health" : 30, "defense": 16, "min_damage" : 4, "max_damage" : 4, "attack" : 15, "speed" : 2, "initiative" : 5}
        #print(self._name + ' created')
    

class ElfSwordman(Infantry):
    _name = 'Elf swordman'
    def __init__(self):
        super().__init__()
        self.characteristics = {"max_health" : 35, "defense": 16, "min_damage" : 3, "max_damage" : 4, "attack" : 5, "speed" : 3, "initiative" : 4}
        #print(self._name + ' created')


class ArcherMaster(Rifleman):
    _name = 'Archer master'
    def __init__(self):
        super().__init__()
        self.characteristics = {"max_health" : 50, "defense": 16, "min_damage" : 8, "max_damage" : 12, "attack" : 30, "speed" : 3, "initiative" : 7}
        #print(self._name + ' created')

class Druid(Magican):
    _name = 'Druid'
    def __init__(self):
        super().__init__()
        self.characteristics = {"max_health" : 70, "defense": 16, "min_damage" : 3, "max_damage" : 4, "attack" : 15, "speed" : 2, "initiative" : 6}
        #print(self._name + ' created')
        self.spell = spells.StrengthSpell
        self.spell_time = 2
    

class Hobbit(Rifleman):
    _name = 'Hobbit'
    def __init__(self):
        super().__init__()
        self.characteristics = {"max_health" : 4, "defense": 1, "min_damage" : 1, "max_damage" : 2, "attack" : 1, "speed" : 2, "initiative" : 4}
        #print(self._name + ' created')
    

class UnitFactory(ABC):
    @abstractmethod
    def ask_cost(self):
        pass
    @abstractmethod
    def create_unit(self):
        pass
    @abstractmethod
    def get_unit_type(self):
        pass
    @abstractmethod
    def check_buildings(self, player):
        pass    
    def buy_unit(self, player):
        if not self.check_buildings(player):
            raise HireError('Not all required buildings builded')
        if player.money < self.ask_cost():
            raise HireError('No money')
        player.money -= self.ask_cost()
        return self.create_unit()


class ManUnitFactory(UnitFactory):
    _race = 'man'


class PeasantFactory(ManUnitFactory):
    __cost = 10
    def __str__(self):
        return 'Hire peasant'
    def check_buildings(self, player):
        return player.has_building(buildings.ManBarrack)   
    def ask_cost(self):
        return self.__cost
    def create_unit(self):
        return Peasant()
    def get_unit_type(self):
        Peasant


class ArcherFactory(ManUnitFactory):
    __cost = 75
    def __str__(self):
        return 'Hire archer'
    def check_buildings(self, player):
        return player.has_building(buildings.ManShootingGround)   
    def ask_cost(self):
        return self.__cost
    def create_unit(self):
        return Archer()
    def get_unit_type(self):
        Archer


class MageFactory(ManUnitFactory):
    __cost = 150
    def __str__(self):
        return 'Hire mage'
    def check_buildings(self, player):
        return player.has_building(buildings.ManMagicAcademy)   
    def ask_cost(self):
        return self.__cost
    def create_unit(self):
        return Mage()
    def get_unit_type(self):
        Mage


class KnightFactory(ManUnitFactory):
    __cost = 500
    def __str__(self):
        return 'Hire knight'
    def check_buildings(self, player):
        return player.get_building_level(buildings.ManBarrack) >= 2   
    def ask_cost(self):
        return self.__cost
    def create_unit(self):
        return Knight()
    def get_unit_type(self):
        Knight


class SwordmanFactory(ManUnitFactory):
    __cost = 100
    def __str__(self):
        return 'Hire swordman'
    def check_buildings(self, player):
        return player.has_building(buildings.ManBarrack)   
    def ask_cost(self):
        return self.__cost
    def create_unit(self):
        return Swordman()
    def get_unit_type(self):
        Swordman


class ElfUnitFactory(UnitFactory):
    _race = 'elf'


class ElfSwordmanFactory(ElfUnitFactory):
    __cost = 100
    def __str__(self):
        return 'Hire elf swordman'
    def check_buildings(self, player):
        return player.has_building(buildings.ElfBarrack)   
    def ask_cost(self):
        return self.__cost
    def create_unit(self):
        return ElfSwordman()
    def get_unit_type(self):
        ElfSwordman


class ElfArcherFactory(ElfUnitFactory):
    __cost = 100
    def __str__(self):
        return 'Hire elf'
    def check_buildings(self, player):
        return player.has_building(buildings.ElfShootingGround)   
    def ask_cost(self):
        return self.__cost
    def create_unit(self):
        return ElfArcher()
    def get_unit_type(self):
        ElfArcher


class DruidFactory(ElfUnitFactory):
    __cost = 150
    def __str__(self):
        return 'Hire druid'
    def check_buildings(self, player):
        return player.has_building(buildings.ElfMagicAcademy)   
    def ask_cost(self):
        return self.__cost
    def create_unit(self):
        return Druid()
    def get_unit_type(self):
        Druid


class ArcherMasterFactory(ElfUnitFactory):
    __cost = 300
    def __str__(self):
        return 'Hire archer master'
    def check_buildings(self, player):
        return player.get_building_level(buildings.ElfShootingGround) >= 2   
    def ask_cost(self):
        return self.__cost
    def create_unit(self):
        return ArcherMaster()
    def get_unit_type(self):
        ArcherMaster


class HobbitFactory(ElfUnitFactory):
    __cost = 10
    def __str__(self):
        return 'Hire hobbit'
    def check_buildings(self, player):
        return player.has_building(buildings.ElfShootingGround)   
    def ask_cost(self):
        return self.__cost
    def create_unit(self):
        return Hobbit()
    def get_unit_type(self):
        Hobbit


all_unit_factories = (PeasantFactory, ArcherFactory, KnightFactory, SwordmanFactory, MageFactory, ElfSwordmanFactory, ElfArcherFactory, DruidFactory, ArcherMasterFactory, HobbitFactory)
x = 0

if __name__ == '__main__':
    from main import *
    a = Swordman()
    a.c = 5
    b = a
    b.c = 6
    print(a.c)
    print(type(a))
    print(Swordman)
    factories = [PeasantFactory(), ArcherFactory(), KnightFactory(), SwordmanFactory(), MageFactory()]
    player = ManPlayer()
    player.buildings = [buildings.ManPalace(), buildings.ManBarrack(), buildings.ManShootingGround(), buildings.ManMagicAcademy(), buildings.ManWall()]
    units = []
    for e in factories:
        units.append(e.buy_unit(player))
    print(player.money)