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
    """
    Manages the state of the car park, including tracking incoming and outgoing
    cars, calculating available spaces, recording temperature readings, and
    providing car park data to the display. This class also logs all car
    movements to a text file.

    Parameters
    ----------
    None

    Attributes
    ----------
    configuration : dict
        Loaded configuration settings from the JSON file.
    total_in_car : int
        Number of cars currently inside the car park.
    parking_temp : int
        Current temperature reading in the car park.
    cars_data : list of Car
        List of Car objects representing all cars that have entered.
    log_file : str
        Path to the output log file. the file that save all the events.
    CONFIG_FILE : str
        Name of the configuration file.
    """
    total_in_car = 0
    parking_temp = 32
    CONFIG_FILE = "config.json"
    log_file = 'change_log.txt'
    cars_data = []
    def __init__(self):
        """
        Initialize the car park manager by loading configuration settings
        """
        self.configuration = parse_config(CarparkManager.CONFIG_FILE)
        print(self.configuration)
#        self.configuration["total_spaces"] = 10

    @property
    def available_spaces(self):
        """
        Calculate the number of available parking spaces.

        Returns
        -------
        available_park : int
            The number of free parking bays (never less than zero).
        """
        available_park = self.configuration["total_spaces"] - self.total_in_car
        if available_park < 0:
            available_park = 0
        return available_park

    
    @property
    def temperature(self):
        """
        Return the current temperature reading for the car park.

        Returns
        -------
        self.parking_temp : int
            The latest temperature value.
        """
        return self.parking_temp

    @property
    def current_time(self):
        """
        Retrieve the current local system time.

        Returns
        -------
        struct_time
            Current timestamp from time.localtime().
        """
        return time.localtime()

    def incoming_car(self,license_plate):
        """
        Register a new incoming car and add it to the internal list.

        Parameters
        ----------
        license_plate : str
            The license plate of the incoming vehicle.
        """
        if license_plate != '':
            self.total_in_car += 1
            car = Car(license_plate)
            car.Entry_temp = self.parking_temp
            self.cars_data.append(car)
            self.log_file_prepare()
#        print('Car in! ' + license_plate)


    def outgoing_car(self,license_plate):
        """
        Register an outgoing car by locating its record, updating exit time,
        and adjusting internal counters.

        Parameters
        ----------
        license_plate : str
            The plate number of the car that is leaving.
        """
        for car in self.cars_data:
            if car.LicensePlate == license_plate:
                car.set_exit_time()
                car.Exit_temp = self.parking_temp
                self.total_in_car -= 1
                if self.total_in_car < 0:
                    self.total_in_car = 0                
                break
        self.log_file_prepare()
#        print('Car out! ' + license_plate)

    def temperature_reading(self,reading):
        """
        Update the stored temperature value.

        Parameters
        ----------
        reading : float or int
            The new temperature reported by the sensor.
        """
        self.parking_temp = int(reading)

#        print(f'temperature is {reading}')
    def log_file_prepare(self):
        """
        Generate and update the parking log file. This copies the header
        from the template log file and appends the latest car records.

        Side Effects
        ------------
        Writes output to the log file defined in configuration.
        """
        with open(self.configuration["log_file"], "r") as src, open(self.log_file, "w") as dst:
            for line in src:
                dst.write(line)
        with open(self.log_file, "a") as log:
            for car in self.cars_data:
                log.write(car.to_log())
class Car:
    """
    Represents a car entering or exiting the car park.

    Parameters:
    ----------
        license_plate (str): The car's number plate.
        
    Attributes
    ----------
    license_plate : str
        Unique identifier for the car.
    entry_time : struct_time
        Time when the car entered the car park.
    exit_time : struct_time or None
        Time when the car exited the car park (None if still inside).
    Entry_temp : float
        Parking temperature at the entry time of the car
    Exit_temp  : float
        Parking temperature at the exit time of the car        
    
    """
    def __init__(self,plate=None):
        self.LicensePlate = plate
        self.Entry_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.Exit_time = None
        self.Entry_temp = None
        self.Exit_temp = None
    def set_exit_time(self):
        """
        Set the time the car exited.

        Parameters:
            exit_time: The exit time from time.localtime().
        """
        self.Exit_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(self.Exit_time)
    def to_log(self):
        """
        Returns a formatted log string for this car.

        Returns
        -------
        str
            A string containing license plate, entry time, exit time, temperature at entry time and temperature at exit time.
        """
        return (
            f"Plate= {self.LicensePlate},\n"
            f"Entry_time= {self.Entry_time},\n"
            f"Exit_time= {self.Exit_time}\n"
            f"Entry Temperature= {self.Entry_temp}\n"
            f"Exit Temperature= {self.Exit_temp}\n"
        )
    


