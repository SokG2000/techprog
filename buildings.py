from abc import ABC, abstractmethod
from MyExceptions import *

class Building():
    def upgrade(self):
        if (self.level == self._max_level):
            raise UpgradeError('Already maximal level')
        self.level += 1
    @abstractmethod
    def end_turn_action(self, player):
        pass
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.level == other.level:
            return True
        return False


class Palace(Building):
    _max_level = 2
    _incomes = (1000, 2000)
    def __str__(self):
        return 'Palace'
    def __init__(self):
        self.level = 1
    def get_income(self):
        return self._incomes[self.level - 1]
    def end_turn_action(self, player):
        player.money += self.get_income()


class ManBarrack(Building):
    _max_level = 2
    def __str__(self):
        return 'ManBarrack'
    def __init__(self):
        self.level = 1
    def end_turn_action(self, player):
        pass


class ManShootingGround(Building):
    _max_level = 1
    def __str__(self):
        return 'ManShootingGround'
    def __init__(self):
        self.level = 1
    def end_turn_action(self, player):
        pass


class ManMagicAcademy(Building):
    _max_level = 1
    def __str__(self):
        return 'ManMagicAcademy'
    def __init__(self):
        self.level = 1
    def end_turn_action(self, player):
        pass


class ElfBarrack(Building):
    _max_level = 1
    def __str__(self):
        return 'ElfBarrack'
    def __init__(self):
        self.level = 1
    def end_turn_action(self, player):
        pass


class ElfShootingGround(Building):
    _max_level = 2
    def __str__(self):
        return 'ElfShootingGround'
    def __init__(self):
        self.level = 1
    def end_turn_action(self, player):
        pass


class ElfMagicAcademy(Building):
    _max_level = 1
    def __str__(self):
        return 'ElfMagicAcademy'
    def __init__(self):
        self.level = 1
    def end_turn_action(self, player):
        pass


class Wall(Building):
    _max_level = 3
    def __str__(self):
        return 'Wall'
    def __init__(self):
        self.level = 1
    def end_turn_action(self, player):
        pass


class Market(Building):
    _max_level = 2
    _incomes = (250, 500)
    def __str__(self):
        return 'Market'
    def __init__(self):
        self.level = 1
    def get_income(self):
        return self._incomes[self.level - 1]
    def end_turn_action(self, player):
        player.money += self.get_income()


class BuildingFactory(ABC):
    @abstractmethod
    def ask_build_cost(self):
        pass
    @abstractmethod
    def check_possibility(self, player):
        pass
    @abstractmethod
    def create_building(self):
        pass
    @abstractmethod
    def get_building_type(self):
        pass
    def is_builded(self, player):
        return player.has_building(self.get_building_type())
    def buy_building(self, player):
        if self.is_builded(player):
            raise BuildError('Building already exists')
        self.check_possibility(player) # if can't build, make BuildError
        player.money -= self.ask_build_cost()
        return self.create_building()

    

class ManBuildingFactory(BuildingFactory):
    _race = 'man'


class ManPalaceFactory(ManBuildingFactory):
    __build_cost = 1000
    __upgrade_cost = (3000)
    def __str__(self):
        return 'Build man palace'
    def ask_build_cost(self):
        return self.__build_cost
    def check_possibility(self, player):
        if player.money < self.ask_build_cost():
            raise BuildError('No money')
    def create_building(self):
        return Palace()
    def get_building_type(self):
        return Palace
    

class ManBarrackFactory(ManBuildingFactory):
    __build_cost = 500
    __upgrade_cost = (3000)
    def __str__(self):
        return 'Build man barrack'
    def ask_build_cost(self):
        return self.__build_cost
    def check_possibility(self, player):
        if not player.has_building(Palace):
            raise BuildError('Not all required buildings builded')
        if player.money < self.ask_build_cost():
            raise BuildError('No money')
    def create_building(self):
        return ManBarrack()
    def get_building_type(self):
        return ManBarrack
    

class ManShootingGroundFactory(ManBuildingFactory):
    __build_cost = 1000
    __upgrade_cost = (3000)
    def __str__(self):
        return 'Build man shooting ground'
    def ask_build_cost(self):
        return self.__build_cost
    def check_possibility(self, player):
        if not player.has_building(Palace):
            raise BuildError('Not all required buildings builded')
        if player.money < self.ask_build_cost():
            raise BuildError('No money')
    def create_building(self):
        return ManShootingGround()
    def get_building_type(self):
        return ManShootingGround
    

class ManMagicAcademyFactory(ManBuildingFactory):
    __build_cost = 1000
    __upgrade_cost = (3000)
    def __str__(self):
        return 'Build man magic academy'
    def ask_build_cost(self):
        return self.__build_cost
    def check_possibility(self, player):
        if not player.has_building(Palace):
            raise BuildError('Not all required buildings builded')
        if player.money < self.ask_build_cost():
            raise BuildError('No money')
    def create_building(self):
        return ManMagicAcademy()
    def get_building_type(self):
        return ManMagicAcademy
    

class ManWallFactory(ManBuildingFactory):
    __build_cost = 1000
    __upgrade_cost = (3000)
    def __str__(self):
        return 'Build man wall'
    def ask_build_cost(self):
        return self.__build_cost
    def check_possibility(self, player):
        if not player.has_building(Palace):
            raise BuildError('Not all required buildings builded')
        if player.money < self.ask_build_cost():
            raise BuildError('No money')
    def create_building(self):
        return Wall()
    def get_building_type(self):
        return Wall


class ManMarketFactory(ManBuildingFactory):
    __build_cost = 1000
    __upgrade_cost = (1500)
    def __str__(self):
        return 'Build man market'
    def ask_build_cost(self):
        return self.__build_cost
    def check_possibility(self, player):
        if not player.has_building(Palace):
            raise BuildError('Not all required buildings builded')
        if player.money < self.ask_build_cost():
            raise BuildError('No money')
    def create_building(self):
        return Market()
    def get_building_type(self):
        return Market


class ElfBuildingFactory(BuildingFactory):
    _race = 'elf'


class ElfPalaceFactory(ElfBuildingFactory):
    __build_cost = 1000
    __upgrade_cost = (3000)
    def __str__(self):
        return 'Build elf palace'
    def ask_build_cost(self):
        return self.__build_cost
    def check_possibility(self, player):
        if player.money < self.ask_build_cost():
            raise BuildError('No money')
    def create_building(self):
        return Palace()
    def get_building_type(self):
        return Palace
    

class ElfBarrackFactory(ElfBuildingFactory):
    __build_cost = 500
    __upgrade_cost = (3000)
    def __str__(self):
        return 'Build elf barrack'
    def ask_build_cost(self):
        return self.__build_cost
    def check_possibility(self, player):
        if not player.has_building(Palace):
            raise BuildError('Not all required buildings builded')
        if player.money < self.ask_build_cost():
            raise BuildError('No money')
    def create_building(self):
        return ElfBarrack()
    def get_building_type(self):
        return ElfBarrack
    

class ElfShootingGroundFactory(ElfBuildingFactory):
    __build_cost = 1000
    __upgrade_cost = (3000)
    def __str__(self):
        return 'Build elf shooting ground'
    def ask_build_cost(self):
        return self.__build_cost
    def check_possibility(self, player):
        if not player.has_building(Palace):
            raise BuildError('Not all required buildings builded')
        if player.money < self.ask_build_cost():
            raise BuildError('No money')
    def create_building(self):
        return ElfShootingGround()
    def get_building_type(self):
        return ElfShootingGround
    

class ElfMagicAcademyFactory(ElfBuildingFactory):
    __build_cost = 1000
    __upgrade_cost = (3000)
    def __str__(self):
        return 'Build elf magic academy'
    def ask_build_cost(self):
        return self.__build_cost
    def check_possibility(self, player):
        if not player.has_building(Palace):
            raise BuildError('Not all required buildings builded')
        if player.money < self.ask_build_cost():
            raise BuildError('No money')
    def create_building(self):
        return ElfMagicAcademy()
    def get_building_type(self):
        return ElfMagicAcademy
    

class ElfWallFactory(ElfBuildingFactory):
    __build_cost = 1000
    __upgrade_cost = (3000)
    def __str__(self):
        return 'Build elf wall'
    def ask_build_cost(self):
        return self.__build_cost
    def check_possibility(self, player):
        if not player.has_building(Palace):
            raise BuildError('Not all required buildings builded')
        if player.money < self.ask_build_cost():
            raise BuildError('No money')
    def create_building(self):
        return Wall()
    def get_building_type(self):
        return Wall


class ElfMarketFactory(ElfBuildingFactory):
    __build_cost = 1000
    __upgrade_cost = (1500)
    def __str__(self):
        return 'Build elf market'
    def ask_build_cost(self):
        return self.__build_cost
    def check_possibility(self, player):
        if not player.has_building(Palace):
            raise BuildError('Not all required buildings builded')
        if player.money < self.ask_build_cost():
            raise BuildError('No money')
    def create_building(self):
        return Market()
    def get_building_type(self):
        return Market


all_building_factories = (ManPalaceFactory, ManBarrackFactory, ManShootingGroundFactory, ManMagicAcademyFactory, ManWallFactory, ManMarketFactory, ElfPalaceFactory, ElfBarrackFactory, ElfShootingGroundFactory, ElfMagicAcademyFactory, ElfWallFactory, ElfMarketFactory)

