import unittest
import buildings
import main
import constants
import MyExceptions
import units
import creating_armies

class MakeUnitBuildTest(unittest.TestCase):
    def setUp(self):
        global player
        player = main.ManPlayer(0)
        player.armies.append(main.Army(0))
        global start_money
        start_money = constants.start_money
        player.buildings.append(buildings.Palace())
        global army_builder
        army_builder = creating_armies.ArmyBuilder(player, player.armies[0])
        global peasant_factory, swordman_factory, mage_factory, archer_factory
        peasant_factory = units.PeasantFactory()
        swordman_factory = units.SwordmanFactory()
        mage_factory = units.MageFactory()
        archer_factory = units.ArcherFactory()
    
    def test_successful_hire(self):
        #peasant_factory = units.PeasantFactory()
        #swordman_factory = units.SwordmanFactory()
        #mage_factory = units.MageFactory()
        #archer_factory = units.ArcherFactory()
        player.buildings.append(buildings.ManBarrack())
        player.buildings.append(buildings.ManMagicAcademy())
        player.buildings.append(buildings.ManShootingGround())
        rest_money = start_money
        army = main.Army(0)
        for i in range(5):
            army_builder.buy_unit(swordman_factory)
            rest_money -= swordman_factory.ask_cost()
        for i in range(5):
            army_builder.buy_unit(mage_factory)
            rest_money -= mage_factory.ask_cost()
        for i in range(50):
            army_builder.buy_unit(peasant_factory)
            rest_money -= peasant_factory.ask_cost()
        for i in range(5):
            army_builder.buy_unit(archer_factory)
            rest_money -= archer_factory.ask_cost()
        army.units.append(units.Swordman())
        army.units[0].amount = 5
        army.units.append(units.Mage())
        army.units[1].amount = 5
        army.units.append(units.Peasant())
        army.units[2].amount = 50
        army.units.append(units.Archer())
        army.units[3].amount = 5
        self.assertEqual(player.money, rest_money)
        self.assertEqual(player.armies[0], army)


    def test_no_money_hire(self):
        #peasant_factory = units.PeasantFactory()
        #swordman_factory = units.SwordmanFactory()
        #mage_factory = units.MageFactory()
        #archer_factory = units.ArcherFactory()
        player.buildings.append(buildings.ManBarrack())
        player.buildings.append(buildings.ManMagicAcademy())
        player.buildings.append(buildings.ManShootingGround())
        rest_money = start_money
        army = main.Army(0)
        for i in range(5):
            army_builder.buy_unit(swordman_factory)
            rest_money -= swordman_factory.ask_cost()
        for i in range(5):
            army_builder.buy_unit(mage_factory)
            rest_money -= mage_factory.ask_cost()
        for i in range(50):
            army_builder.buy_unit(peasant_factory)
            rest_money -= peasant_factory.ask_cost()
        for i in range(5):
            army_builder.buy_unit(archer_factory)
            rest_money -= archer_factory.ask_cost()
        army.units.append(units.Swordman())
        army.units[0].amount = 5
        army.units.append(units.Mage())
        army.units[1].amount = 5
        army.units.append(units.Peasant())
        army.units[2].amount = 50
        army.units.append(units.Archer())
        army.units[3].amount = 5
        while rest_money >= peasant_factory.ask_cost():
            army_builder.buy_unit(peasant_factory)
            rest_money -= peasant_factory.ask_cost()
            army.units[2].amount += 1
        self.assertEqual(player.money, rest_money)
        self.assertEqual(player.armies[0], army)
        self.assertRaises(MyExceptions.HireError, army_builder.buy_unit, peasant_factory)        


    def test_no_building_hire(self):
        #peasant_factory = units.PeasantFactory()
        #swordman_factory = units.SwordmanFactory()
        #mage_factory = units.MageFactory()
        #archer_factory = units.ArcherFactory()
        player.buildings.append(buildings.ManBarrack())
        player.buildings.append(buildings.ManShootingGround())
        rest_money = start_money
        army = main.Army(0)
        for i in range(5):
            army_builder.buy_unit(swordman_factory)
            rest_money -= swordman_factory.ask_cost()
        for i in range(50):
            army_builder.buy_unit(peasant_factory)
            rest_money -= peasant_factory.ask_cost()
        for i in range(5):
            army_builder.buy_unit(archer_factory)
            rest_money -= archer_factory.ask_cost()
        army.units.append(units.Swordman())
        army.units[0].amount = 5
        army.units.append(units.Peasant())
        army.units[1].amount = 50
        army.units.append(units.Archer())
        army.units[2].amount = 5
        self.assertEqual(player.money, rest_money)
        self.assertEqual(player.armies[0], army)
        self.assertRaises(MyExceptions.HireError, army_builder.buy_unit, mage_factory)        


if __name__ == '__main__':
    unittest.main()
