import unittest
import test_buildings
import test_units
import test_unit_builder
import test_building_builder

buildings_test_suite = unittest.TestSuite()
buildings_test_suite.addTest(unittest.makeSuite(test_buildings.MakeManBuildingTest))
buildings_test_suite.addTest(unittest.makeSuite(test_buildings.MakeElfBuildingTest))
hire_test_suite = unittest.TestSuite()
hire_test_suite.addTest(unittest.makeSuite(test_units.MakeManHireTest))
hire_test_suite.addTest(unittest.makeSuite(test_units.MakeElfHireTest))
builder_test_suite = unittest.TestSuite()
builder_test_suite.addTest(unittest.makeSuite(test_unit_builder.MakeUnitBuildTest))
builder_test_suite.addTest(unittest.makeSuite(test_building_builder.MakeBuildingBuildTest))
all_test_suite = unittest.TestSuite()
all_test_suite.addTest(buildings_test_suite)
all_test_suite.addTest(hire_test_suite)
all_test_suite.addTest(builder_test_suite)

runner = unittest.TextTestRunner(verbosity=2)
runner.run(all_test_suite)