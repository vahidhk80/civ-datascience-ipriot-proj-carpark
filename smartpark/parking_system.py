from interfaces import CarparkSensorListener
from interfaces import CarparkDataProvider
from config_parser import parse_config
import time

'''
    TODO: 
    - make your own module, or rename this one. Yours won't be a mock-up, so "mocks" is a bad name here.
    - Read your configuration from a file. 
    - Write entries to a log file when something happens.
    - The "display" should update instantly when something happens
    - Make a "Car" class to contain information about cars:
        * License plate number. You can use this as an identifier
        * Entry time
        * Exit time
    - The manager class should record all activity. This includes:
        * Cars arriving
        * Cars departing
        * Temperature measurements.
    - The manager class should provide informtaion to potential customers:
        * The current time (optional)
        * The number of bays available
        * The current temperature
    
'''
class CarparkManager(CarparkSensorListener,CarparkDataProvider):
    #constant, for where to get the configuration data.
    total_in_car = 0
    parking_temp = 32
    CONFIG_FILE = "config.json"
    log_file = 'change_log.txt'
    cars_data = []
    def __init__(self):
        self.configuration = parse_config(CarparkManager.CONFIG_FILE)
        print(self.configuration)

    @property
    def available_spaces(self):
        available_park = self.configuration["total_spaces"] - self.total_in_car
        return available_park
    
    @property
    def temperature(self):
        return self.parking_temp

    @property
    def current_time(self):
        return time.localtime()

    def incoming_car(self,license_plate):
        self.total_in_car += 1
        self.cars_data.append(Car(license_plate))
        self.log_file_prepare()
        print('Car in! ' + license_plate)
        print(self.cars_data[0])

    def outgoing_car(self,license_plate):
        Car(license_plate).set_exit_time
        self.total_in_car -= 1
        self.log_file_prepare()
        print('Car out! ' + license_plate)

    def temperature_reading(self,reading):
        self.parking_temp = int(reading)

#        print(f'temperature is {reading}')
    def log_file_prepare(self):
        with open(self.configuration["log_file"], "r") as src, open(self.log_file, "w") as dst:
            for line in src:
                dst.write(line)
        with open(self.log_file, "a") as log:
            for car in self.cars_data:
                log.write(car.to_log())
class Car:
    def __init__(self,plate=None):
        self.LicensePlate = plate
        self.Entry_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.Exit_time = None
    def set_exit_time(self):
        self.Exit_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(self.Exit_time)
    def to_log(self):
        return (
            f"Plate= {self.LicensePlate},\n"
            f"Entry_time= {self.Entry_time},\n"
            f"Exit_time= {self.Exit_time}\n"
        )
    


