import logging
import random

class SensorIntegration:
    """
    The SensorIntegration class is designed to simulate and manage the collection of data from various sensors (temperature, humidity, pressure, and biosensor) and provide a unified interface for accessing the sensor readings.
    """
    
    def __init__(self):
        """
        Initialize the object with a dictionary of sensor reading methods and configure basic logging settings.
        """
        self.sensors = {
            "temperature": self.read_temperature,
            "humidity": self.read_humidity,
            "pressure": self.read_pressure,
            "biosensor": self.read_biosensor
        }
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initialized SensorIntegration with temperature, humidity, pressure, and biosensor")
    
    def read_temperature(self):
        """
        Simulate reading a random temperature value between -50 and 50 degrees Celsius and log the result.
        Simulate reading temperature
        :return: Temperature in degrees Celsius
        """
        temperature = random.uniform(-50, 50)
        self.logger.info(f"Temperature reading: {temperature:.2f}°C")
        return temperature
    
    def read_humidity(self):
        """
        Simulate reading and returning a random humidity percentage between 0% and 100%, and log the value.
        Simulate reading humidity
        :return: Humidity percentage
        """
        humidity = random.uniform(0, 100)
        self.logger.info(f"Humidity reading: {humidity:.2f}%")
        return humidity
    
    def read_pressure(self):
        """
        Simulate reading and logging atmospheric pressure in hectopascals (hPa) within a range of 900 to 1100 hPa.
        Simulate reading pressure
        :return: Pressure in hPa
        """
        pressure = random.uniform(900, 1100)
        self.logger.info(f"Pressure reading: {pressure:.2f} hPa")
        return pressure
    
    def read_biosensor(self):
        """
        Simulate reading biosensor data by randomly generating a biosignal (True or False) and log the detection result.
        Simulate reading biosensor data
        :return: Boolean indicating biosignal detection
        """
        biosignal = random.choice([True, False])
        if biosignal:
            self.logger.info("Biosensor reading: Biosignal detected")
        else:
            self.logger.info("Biosensor reading: No biosignal detected")
        return biosignal
    
    def collect_data(self):
        """
        Collect data from multiple sensors by executing their associated functions and return the results in a dictionary where keys are sensor names and values are the corresponding sensor readings.
        :return: Dictionary containing sensor readings
        """
        self.logger.info("Starting data collection from all sensors")
        
        sensor_data = {}
        for sensor_name, sensor_function in self.sensors.items():
            sensor_data[sensor_name] = sensor_function()
        
        self.logger.info(f"Collected sensor data: {sensor_data}")
        return sensor_data