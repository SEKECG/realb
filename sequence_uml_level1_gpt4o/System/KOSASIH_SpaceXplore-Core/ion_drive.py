import logging
import numpy as np

class IonDrive:
    """
    Simulate the operation of an ion drive, including activation, fuel consumption, acceleration calculation, and status monitoring.
    """
    
    def __init__(self, thrust, fuel_mass, specific_impulse):
        """
        Initialize a rocket engine instance with specified thrust, fuel mass, and specific impulse, and set up logging for the instance.
        :param thrust: Thrust force in newtons
        :param fuel_mass: Initial fuel mass in kilograms
        :param specific_impulse: Specific impulse in seconds
        """
        self.thrust = thrust
        self.fuel_mass = fuel_mass
        self.specific_impulse = specific_impulse
        self.is_active = False
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initialized IonDrive with thrust={thrust}N, fuel_mass={fuel_mass}kg, specific_impulse={specific_impulse}s")
    
    def activate(self):
        """
        Activate the Ion Drive if there is sufficient fuel, otherwise log an error message.
        """
        if self.fuel_mass > 0:
            self.is_active = True
            self.logger.info("Ion Drive activated")
        else:
            self.logger.error("Cannot activate Ion Drive: insufficient fuel")
    
    def deactivate(self):
        """
        Deactivate the Ion Drive by setting its active status to False and log the deactivation event.
        """
        self.is_active = False
        self.logger.info("Ion Drive deactivated")
    
    def consume_fuel(self, time):
        """
        Calculate and update the remaining fuel mass after consuming fuel based on the ion drive's thrust, specific impulse, and given time, while handling inactive state and fuel depletion scenarios.
        :param time: Time duration in seconds
        :return: Fuel consumed in kilograms
        """
        if not self.is_active:
            self.logger.warning("Cannot consume fuel: Ion Drive is not active")
            return 0
        
        if self.fuel_mass <= 0:
            self.logger.warning("No fuel remaining")
            self.deactivate()
            return 0
        
        # Calculate fuel consumption rate (kg/s)
        g0 = 9.81  # Standard gravity (m/s²)
        fuel_consumption_rate = self.thrust / (self.specific_impulse * g0)
        
        # Calculate fuel consumed
        fuel_consumed = fuel_consumption_rate * time
        
        # Ensure we don't consume more fuel than available
        if fuel_consumed > self.fuel_mass:
            fuel_consumed = self.fuel_mass
            self.fuel_mass = 0
            self.logger.warning("Fuel depleted")
            self.deactivate()
        else:
            self.fuel_mass -= fuel_consumed
        
        self.logger.info(f"Consumed {fuel_consumed:.6f} kg of fuel over {time}s")
        return fuel_consumed
    
    def calculate_acceleration(self):
        """
        Calculate the acceleration of an object based on its thrust and fuel mass if it is active, otherwise return 0.
        :return: Acceleration in m/s²
        """
        if not self.is_active:
            return 0
        
        if self.fuel_mass <= 0:
            return 0
        
        # Total mass (assuming constant structural mass for simplicity)
        structural_mass = 100  # kg (example value)
        total_mass = structural_mass + self.fuel_mass
        
        # Calculate acceleration (F = m * a)
        acceleration = self.thrust / total_mass
        
        self.logger.info(f"Calculated acceleration: {acceleration:.6f} m/s²")
        return acceleration
    
    def status(self):
        """
        Retrieve the current operational status of an object, including its active state, thrust level, remaining fuel mass, and calculated acceleration.
        :return: Dictionary containing status information
        """
        acceleration = self.calculate_acceleration()
        
        status_info = {
            "active": self.is_active,
            "thrust": self.thrust,
            "fuel_mass": self.fuel_mass,
            "acceleration": acceleration
        }
        
        self.logger.info(f"Status: {status_info}")
        return status_info
    
    def simulate(self, duration):
        """
        Simulate the operation of an Ion Drive over a specified duration, logging fuel consumption and status at each time step, provided the drive is active.
        :param duration: Total simulation time in seconds
        """
        if not self.is_active:
            self.logger.warning("Cannot simulate: Ion Drive is not active")
            return
        
        time_step = 1  # 1 second time steps
        total_time = 0
        
        self.logger.info(f"Starting simulation for {duration} seconds")
        
        while total_time < duration and self.is_active:
            # Consume fuel for this time step
            self.consume_fuel(time_step)
            
            # Get current status
            current_status = self.status()
            
            self.logger.info(f"Time {total_time}s: {current_status}")
            
            total_time += time_step
            
            # Check if we still have fuel
            if self.fuel_mass <= 0:
                self.logger.info("Simulation ended: fuel depleted")
                break
        
        self.logger.info(f"Simulation completed. Total time: {total_time}s")