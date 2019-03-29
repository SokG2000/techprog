import unittest
import buildings
import main
import constants
import MyExceptions
import creating_armies

class MakeBuildingBuildTest(unittest.TestCase):
    def setUp(self):
        global player
        player = main.ManPlayer(0)
        player.armies.append(main.Army(0))
        global start_money
        start_money = constants.start_money
        global buildings_builder
        buildings_builder = creating_armies.BuildingsBuilder(player)
        global palace_factory, barack_factory, shooting_ground_factory, magic_academy_factory, wall_factory, market_factory
        palace_factory = buildings.ElfPalaceFactory()
        barack_factory = buildings.ElfBarrackFactory()
        shooting_ground_factory = buildings.ElfShootingGroundFactory()
        magic_academy_factory = buildings.ElfMagicAcademyFactory()
        wall_factory = buildings.ElfWallFactory()
        market_factory = buildings.ElfMarketFactory()
        

    def test_successful_build(self):
        rest_money = start_money
        buildings_builder.buy_building(palace_factory)
        rest_money -= palace_factory.ask_build_cost()
        buildings_builder.buy_building(barack_factory)
        rest_money -= barack_factory.ask_build_cost()
        buildings_builder.buy_building(shooting_ground_factory)
        rest_money -= shooting_ground_factory.ask_build_cost()
        buildings_builder.buy_building(magic_academy_factory)
        rest_money -= magic_academy_factory.ask_build_cost()
        buildings_builder.buy_building(wall_factory)
        rest_money -= wall_factory.ask_build_cost()
        res_buildings = []
        res_buildings.append(buildings.Palace())
        res_buildings.append(buildings.ElfBarrack())
        res_buildings.append(buildings.ElfShootingGround())
        res_buildings.append(buildings.ElfMagicAcademy())
        res_buildings.append(buildings.Wall())
        self.assertCountEqual(player.buildings, res_buildings)
        self.assertEqual(player.money, rest_money)


    def test_need_palace_build(self):
        rest_money = start_money
        self.assertRaises(MyExceptions.BuildError, buildings_builder.buy_building, barack_factory)        


    def test_already_have_building(self):
        rest_money = start_money
        buildings_builder.buy_building(palace_factory)
        rest_money -= palace_factory.ask_build_cost()
        self.assertRaises(MyExceptions.BuildError, buildings_builder.buy_building, palace_factory)


    def test_no_money_build(self):
        rest_money = start_money
        buildings_builder.buy_building(palace_factory)
        rest_money -= palace_factory.ask_build_cost()
        buildings_builder.buy_building(barack_factory)
        rest_money -= barack_factory.ask_build_cost()
        buildings_builder.buy_building(shooting_ground_factory)
        rest_money -= shooting_ground_factory.ask_build_cost()
        buildings_builder.buy_building(magic_academy_factory)
        rest_money -= magic_academy_factory.ask_build_cost()
        buildings_builder.buy_building(wall_factory)
        rest_money -= wall_factory.ask_build_cost()
        res_buildings = []
        res_buildings.append(buildings.Palace())
        res_buildings.append(buildings.ElfBarrack())
        res_buildings.append(buildings.ElfShootingGround())
        res_buildings.append(buildings.ElfMagicAcademy())
        res_buildings.append(buildings.Wall())
        self.assertCountEqual(player.buildings, res_buildings)
        self.assertEqual(player.money, rest_money)
        self.assertRaises(MyExceptions.BuildError, buildings_builder.buy_building, market_factory)


if __name__ == '__main__':
    unittest.main()