import logging
import numpy as np

class AutonomousNavigation:
    """
    The AutonomousNavigation class is designed to simulate the movement of a probe from an initial position to a specified destination, calculating direction and moving incrementally until the destination is reached.
    """
    
    def __init__(self, initial_position, destination, speed=1.0):
        """
        Initialize a probe with its starting position, destination, speed, and logging configuration.
        :param initial_position: Initial position as a numpy array [x, y, z]
        :param destination: Destination position as a numpy array [x, y, z]
        :param speed: Movement speed in units per step (default: 1.0)
        """
        self.position = np.array(initial_position, dtype=float)
        self.destination = np.array(destination, dtype=float)
        self.speed = speed
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initialized AutonomousNavigation with position={self.position}, destination={self.destination}, speed={self.speed}")
    
    def calculate_direction(self):
        """
        Calculate the normalized direction vector from the current position to the destination.
        :return: Normalized direction vector as numpy array
        """
        direction = self.destination - self.position
        distance = np.linalg.norm(direction)
        
        if distance < 1e-10:  # Avoid division by zero
            return np.zeros_like(direction)
        
        normalized_direction = direction / distance
        self.logger.info(f"Calculated direction: {normalized_direction}")
        return normalized_direction
    
    def has_reached_destination(self):
        """
        Check if the current position has reached the destination within a small tolerance using numerical comparison.
        :return: Boolean indicating if destination is reached
        """
        distance = np.linalg.norm(self.destination - self.position)
        reached = distance < 1e-6
        
        if reached:
            self.logger.info("Destination reached!")
        else:
            self.logger.info(f"Distance to destination: {distance:.6f}")
        
        return reached
    
    def move(self):
        """
        Move the object in a calculated direction at a defined speed and update its position, logging the new position.
        """
        if self.has_reached_destination():
            return
        
        direction = self.calculate_direction()
        movement = direction * self.speed
        
        # Update position
        self.position += movement
        
        self.logger.info(f"Moved to new position: {self.position}")
    
    def navigate(self):
        """
        Continuously move the object until it reaches its destination, then log a message indicating the destination has been reached.
        """
        self.logger.info("Starting navigation to destination")
        
        step_count = 0
        max_steps = 1000  # Safety limit to prevent infinite loops
        
        while not self.has_reached_destination() and step_count < max_steps:
            self.move()
            step_count += 1
        
        if step_count >= max_steps:
            self.logger.warning("Navigation stopped: maximum steps reached without reaching destination")
        else:
            self.logger.info("Navigation completed successfully")