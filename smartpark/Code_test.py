
# test_carpark_manager.py

import unittest
from parking_system import CarparkManager, Car

class TestableCarparkManager(CarparkManager):
    """
    A lightweight subclass of CarparkManager for testing purposes.
    It avoids reading/writing real files.
    """
    def __init__(self):
        self.configuration = {
            "total_spaces": 10,
            "log_file": "dummy_template_log.txt",
        }
        self.total_in_car = 0
        self.parking_temp = 32
        self.cars_data = []
        self.log_file = "dummy_log.txt"

    def log_file_prepare(self):
        """Override to do nothing in tests."""
        pass

class TestCarparkManagerEvents(unittest.TestCase):

    def test_incoming_car_adds_car_and_increments_count(self):
        manager = TestableCarparkManager()
        manager.temperature_reading(25)  # set current temperature

        manager.incoming_car("ABC123")

        # total_in_car increased
        self.assertEqual(manager.total_in_car, 1)

        # a car was added to cars_data
        self.assertEqual(len(manager.cars_data), 1)
        car = manager.cars_data[0]

        # car attributes set correctly
        self.assertEqual(car.LicensePlate, "ABC123")
        self.assertEqual(car.Entry_temp, 25)

        # available_spaces decreased from 10 to 9
        self.assertEqual(manager.available_spaces, 9)

        def test_outgoing_car_sets_exit_time_and_decrements_count(self):
            manager = TestableCarparkManager()
            manager.temperature_reading(30)

            # First, car enters
            manager.incoming_car("XYZ999")
            self.assertEqual(manager.total_in_car, 1)

            # Then, car leaves
            manager.outgoing_car("XYZ999")

            # total_in_car decreased
            self.assertEqual(manager.total_in_car, 0)

            # car still in list, but now with exit time and exit temp
            car = manager.cars_data[0]
            self.assertIsNotNone(getattr(car, "Exit_time", None))
            self.assertEqual(car.Exit_temp, 30)

        def test_available_spaces_never_negative(self):
            manager = TestableCarparkManager()
            manager.total_in_car = 20  # more than total_spaces

            self.assertEqual(manager.available_spaces, 0)
        
        def test_available_spaces_not_more_than_total_spaces(self):
            manager = TestableCarparkManager()
            manager.total

            
if __name__ == "__main__":
    unittest.main()