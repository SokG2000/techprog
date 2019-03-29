import unittest
import buildings
import main
import constants
import MyExceptions
import units

class MakeManHireTest(unittest.TestCase):
    def setUp(self):
        global player
        player = main.ManPlayer(0)
        global start_money
        start_money = constants.start_money
        player.buildings.append(buildings.Palace())
    
    def test_peasant_hire(self):
        factory = units.PeasantFactory()
        player.buildings.append(buildings.ManBarrack())
        peasant = factory.buy_unit(player)
        res_unit = units.Peasant()
        self.assertEqual(peasant, res_unit)
        self.assertEqual(player.money, start_money - factory.ask_cost())

    def test_swordman_hire(self):
        factory = units.SwordmanFactory()
        player.buildings.append(buildings.ManBarrack())
        peasant = factory.buy_unit(player)
        res_unit = units.Swordman()
        self.assertEqual(peasant, res_unit)
        self.assertEqual(player.money, start_money - factory.ask_cost())

    def test_knight_hire(self):
        factory = units.KnightFactory()
        player.buildings.append(buildings.ManBarrack())
        player.buildings[-1].level += 1
        peasant = factory.buy_unit(player)
        res_unit = units.Knight()
        self.assertEqual(peasant, res_unit)
        self.assertEqual(player.money, start_money - factory.ask_cost())

    def test_mage_hire(self):
        factory = units.MageFactory()
        player.buildings.append(buildings.ManMagicAcademy())
        peasant = factory.buy_unit(player)
        res_unit = units.Mage()
        self.assertEqual(peasant, res_unit)
        self.assertEqual(player.money, start_money - factory.ask_cost())


    def test_archer_hire(self):
        factory = units.ArcherFactory()
        player.buildings.append(buildings.ManShootingGround())
        peasant = factory.buy_unit(player)
        res_unit = units.Archer()
        self.assertEqual(peasant, res_unit)
        self.assertEqual(player.money, start_money - factory.ask_cost())
        
    def test_peasant_need_barrack(self):
        factory = units.PeasantFactory()
        self.assertRaises(MyExceptions.HireError, factory.buy_unit, player)

    def test_swordman_need_barrack(self):
        factory = units.SwordmanFactory()
        self.assertRaises(MyExceptions.HireError, factory.buy_unit, player)

    def test_knight_need_barrack(self):
        factory = units.KnightFactory()
        self.assertRaises(MyExceptions.HireError, factory.buy_unit, player)

    def test_mage_need_academy(self):
        factory = units.MageFactory()
        self.assertRaises(MyExceptions.HireError, factory.buy_unit, player)


    def test_archer_need_shooting_ground(self):
        factory = units.ArcherFactory()
        self.assertRaises(MyExceptions.HireError, factory.buy_unit, player)

    def test_knight_need_level2(self):
        factory = units.KnightFactory()
        player.buildings.append(buildings.ManBarrack())
        self.assertRaises(MyExceptions.HireError, factory.buy_unit, player)


class MakeElfHireTest(unittest.TestCase):
    def setUp(self):
        global player
        player = main.ElfPlayer(0)
        global start_money
        start_money = constants.start_money
        player.buildings.append(buildings.Palace())
    
    def test_hobbit_hire(self):
        factory = units.HobbitFactory()
        player.buildings.append(buildings.ElfShootingGround())
        peasant = factory.buy_unit(player)
        res_unit = units.Hobbit()
        self.assertEqual(peasant, res_unit)
        self.assertEqual(player.money, start_money - factory.ask_cost())

    def test_elf_hire(self):
        factory = units.ElfArcherFactory()
        player.buildings.append(buildings.ElfShootingGround())
        peasant = factory.buy_unit(player)
        res_unit = units.ElfArcher()
        self.assertEqual(peasant, res_unit)
        self.assertEqual(player.money, start_money - factory.ask_cost())

    def test_archer_master_hire(self):
        factory = units.ArcherMasterFactory()
        player.buildings.append(buildings.ElfShootingGround())
        player.buildings[-1].level += 1
        peasant = factory.buy_unit(player)
        res_unit = units.ArcherMaster()
        self.assertEqual(peasant, res_unit)
        self.assertEqual(player.money, start_money - factory.ask_cost())

    def test_druid_hire(self):
        factory = units.DruidFactory()
        player.buildings.append(buildings.ElfMagicAcademy())
        peasant = factory.buy_unit(player)
        res_unit = units.Druid()
        self.assertEqual(peasant, res_unit)
        self.assertEqual(player.money, start_money - factory.ask_cost())


    def test_elf_swordman_hire(self):
        factory = units.ElfSwordmanFactory()
        player.buildings.append(buildings.ElfBarrack())
        peasant = factory.buy_unit(player)
        res_unit = units.ElfSwordman()
        self.assertEqual(peasant, res_unit)
        self.assertEqual(player.money, start_money - factory.ask_cost())
        
    def test_hobbit_need_shooting_ground(self):
        factory = units.HobbitFactory()
        self.assertRaises(MyExceptions.HireError, factory.buy_unit, player)

    def test_elf_need_shooting_ground(self):
        factory = units.ElfArcherFactory()
        self.assertRaises(MyExceptions.HireError, factory.buy_unit, player)

    def test_archer_master_need_shooting_ground(self):
        factory = units.ArcherMasterFactory()
        self.assertRaises(MyExceptions.HireError, factory.buy_unit, player)

    def test_druid_need_academy(self):
        factory = units.DruidFactory()
        self.assertRaises(MyExceptions.HireError, factory.buy_unit, player)


    def test_elf_swordman_need_barrack(self):
        factory = units.ElfSwordmanFactory()
        self.assertRaises(MyExceptions.HireError, factory.buy_unit, player)

    def test_archer_master_need_level2(self):
        factory = units.ArcherMasterFactory()
        player.buildings.append(buildings.ElfShootingGround())
        self.assertRaises(MyExceptions.HireError, factory.buy_unit, player)


if __name__ == '__main__':
    unittest.main()