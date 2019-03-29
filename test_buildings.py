import unittest
import buildings
import main
import constants
import MyExceptions

class MakeManBuildingTest(unittest.TestCase):
    def setUp(self):
        global player
        player = main.ManPlayer(0)
        global start_money
        start_money = constants.start_money
    
    def test_palace_build(self):
        factory = buildings.ManPalaceFactory()
        palace = factory.buy_building(player)
        res_building = buildings.Palace()
        self.assertEqual(palace, res_building)
        self.assertEqual(player.money, start_money - factory.ask_build_cost())
    
    def test_wall_build(self):
        player.buildings.append(buildings.Palace())
        factory = buildings.ManWallFactory()
        wall = factory.buy_building(player)
        res_building = buildings.Wall()
        self.assertEqual(wall, res_building)
        self.assertEqual(player.money, start_money - factory.ask_build_cost())
    
    def test_market_build(self):
        player.buildings.append(buildings.Palace())
        factory = buildings.ManMarketFactory()
        wall = factory.buy_building(player)
        res_building = buildings.Market()
        self.assertEqual(wall, res_building)
        self.assertEqual(player.money, start_money - factory.ask_build_cost())
    
    def test_barrack_build(self):
        player.buildings.append(buildings.Palace())
        factory = buildings.ManBarrackFactory()
        barrack = factory.buy_building(player)
        res_building = buildings.ManBarrack()
        self.assertEqual(barrack, res_building)
        self.assertEqual(player.money, start_money - factory.ask_build_cost())
    
    def test_shooting_ground_build(self):
        player.buildings.append(buildings.Palace())
        factory = buildings.ManShootingGroundFactory()
        shooting_ground = factory.buy_building(player)
        res_building = buildings.ManShootingGround()
        self.assertEqual(shooting_ground, res_building)
        self.assertEqual(player.money, start_money - factory.ask_build_cost())
    
    def test_magic_academy_build(self):
        player.buildings.append(buildings.Palace())
        factory = buildings.ManMagicAcademyFactory()
        magic_academy = factory.buy_building(player)
        res_building = buildings.ManMagicAcademy()
        self.assertEqual(magic_academy, res_building)
        self.assertEqual(player.money, start_money - factory.ask_build_cost())
    
    def test_market_need_palace(self):
        factory = buildings.ManMarketFactory()
        self.assertRaises(MyExceptions.BuildError, factory.buy_building, player)
    
    def test_wall_need_palace(self):
        factory = buildings.ManWallFactory()
        self.assertRaises(MyExceptions.BuildError, factory.buy_building, player)
     
    def test_barrack_need_palace(self):
        factory = buildings.ManBarrackFactory()
        self.assertRaises(MyExceptions.BuildError, factory.buy_building, player)
    
    def test_shooting_ground_need_palace(self):
        factory = buildings.ManShootingGroundFactory()
        self.assertRaises(MyExceptions.BuildError, factory.buy_building, player)
    
    def test_magic_academy_need_palace(self):
        factory = buildings.ManMagicAcademyFactory()
        self.assertRaises(MyExceptions.BuildError, factory.buy_building, player)


class MakeElfBuildingTest(unittest.TestCase):
    def setUp(self):
        global player
        player = main.ElfPlayer(0)
        global start_money
        start_money = constants.start_money
    
    def test_palace_build(self):
        factory = buildings.ElfPalaceFactory()
        palace = factory.buy_building(player)
        res_building = buildings.Palace()
        self.assertEqual(palace, res_building)
        self.assertEqual(player.money, start_money - factory.ask_build_cost())
    
    def test_wall_build(self):
        player.buildings.append(buildings.Palace())
        factory = buildings.ElfWallFactory()
        wall = factory.buy_building(player)
        res_building = buildings.Wall()
        self.assertEqual(wall, res_building)
        self.assertEqual(player.money, start_money - factory.ask_build_cost())
    
    def test_market_build(self):
        player.buildings.append(buildings.Palace())
        factory = buildings.ElfMarketFactory()
        wall = factory.buy_building(player)
        res_building = buildings.Market()
        self.assertEqual(wall, res_building)
        self.assertEqual(player.money, start_money - factory.ask_build_cost())
    
    def test_barrack_build(self):
        player.buildings.append(buildings.Palace())
        factory = buildings.ElfBarrackFactory()
        barrack = factory.buy_building(player)
        res_building = buildings.ElfBarrack()
        self.assertEqual(barrack, res_building)
        self.assertEqual(player.money, start_money - factory.ask_build_cost())
    
    def test_shooting_ground_build(self):
        player.buildings.append(buildings.Palace())
        factory = buildings.ElfShootingGroundFactory()
        shooting_ground = factory.buy_building(player)
        res_building = buildings.ElfShootingGround()
        self.assertEqual(shooting_ground, res_building)
        self.assertEqual(player.money, start_money - factory.ask_build_cost())
    
    def test_magic_academy_build(self):
        player.buildings.append(buildings.Palace())
        factory = buildings.ElfMagicAcademyFactory()
        magic_academy = factory.buy_building(player)
        res_building = buildings.ElfMagicAcademy()
        self.assertEqual(magic_academy, res_building)
        self.assertEqual(player.money, start_money - factory.ask_build_cost())
    
    def test_wall_need_palace(self):
        factory = buildings.ElfWallFactory()
        self.assertRaises(MyExceptions.BuildError, factory.buy_building, player)
    
    def test_market_need_palace(self):
        factory = buildings.ElfMarketFactory()
        self.assertRaises(MyExceptions.BuildError, factory.buy_building, player)
    
    def test_barrack_need_palace(self):
        factory = buildings.ElfBarrackFactory()
        self.assertRaises(MyExceptions.BuildError, factory.buy_building, player)
    
    def test_shooting_ground_need_palace(self):
        factory = buildings.ElfShootingGroundFactory()
        self.assertRaises(MyExceptions.BuildError, factory.buy_building, player)
    
    def test_magic_academy_need_palace(self):
        factory = buildings.ElfMagicAcademyFactory()
        self.assertRaises(MyExceptions.BuildError, factory.buy_building, player)

        
if __name__ == '__main__':
    unittest.main()