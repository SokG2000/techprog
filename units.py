from abc import ABC, abstractmethod
import buildings
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


class Infantry(Unit):
    def move(self):
        print(self._name + ' moved')
    def attack(self):
        print(self._name + 'attacked')

class Magican(Unit):
    def move(self):
        print(self._name + ' moved')
    def attack(self):
        print(self._name + 'attacked')


class Rifleman(Unit):
    def move(self):
        print(self._name + ' moved')
    def attack(self):
        print(self._name + 'attacked')


class Archer(Rifleman):
    _name = 'Archer'
    def __init__(self):
        super().__init__()
        self.characteristics = {}
        #print(self._name + ' created')


class Peasant(Infantry):
    _name = 'Peasant'
    def __init__(self):
        super().__init__()
        self.characteristics = {}
        #print(self._name + ' created')


class Swordman(Infantry):
    _name = 'Swordman'
    def __init__(self):
        super().__init__()
        self.characteristics = {}
        #print(self._name + ' created')


class Knight(Infantry):
    _name = 'Knight'
    def __init__(self):
        super().__init__()
        self.characteristics = {}
        #print(self._name + ' created')


class Mage(Magican):
    _name = 'Mage'
    def __init__(self):
        super().__init__()
        self.characteristics = {}
        #print(self._name + ' created')


class ElfArcher(Rifleman):
    _name = 'Elf'
    def __init__(self):
        super().__init__()
        self.characteristics = {}
        #print(self._name + ' created')
    

class ElfSwordman(Infantry):
    _name = 'Elf swordman'
    def __init__(self):
        super().__init__()
        self.characteristics = {}
        #print(self._name + ' created')


class ArcherMaster(Rifleman):
    _name = 'Archer master'
    def __init__(self):
        super().__init__()
        self.characteristics = {}
        #print(self._name + ' created')

class Druid(Magican):
    _name = 'Druid'
    def __init__(self):
        super().__init__()
        self.characteristics = {}
        #print(self._name + ' created')
    

class Hobbit(Rifleman):
    _name = 'Hobbit'
    def __init__(self):
        super().__init__()
        self.characteristics = {}
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
    __cost = 50
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