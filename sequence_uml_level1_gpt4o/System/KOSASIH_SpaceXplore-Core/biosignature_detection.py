import logging
import numpy as np

class BiosignatureDetection:
    """
    Detect biosignatures in biosensor data by analyzing detection scores against a configurable threshold.
    """
    
    def __init__(self, threshold=0.7):
        """
        Initialize an instance with a configurable threshold for biosignature detection and set up basic logging configuration.
        :param threshold: Detection threshold (default: 0.7)
        """
        self.threshold = threshold
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initialized BiosignatureDetection with threshold={threshold}")
    
    def analyze_data(self, biosensor_data):
        """
        Analyze biosensor data to detect biosignatures by generating a random detection score and determining if it meets or exceeds a predefined threshold.
        Analyze biosensor data to detect biosignatures
        :param biosensor_data: Biosensor data to analyze
        :return: Detection score
        """
        # Generate a random detection score between 0 and 1
        detection_score = np.random.random()
        
        self.logger.info(f"Analyzed biosensor data. Detection score: {detection_score:.4f}")
        return detection_score
    
    def detect_biosignature(self, biosensor_data):
        """
        Analyze biosensor data to detect the presence of a biosignature and log the result.
        :param biosensor_data: Biosensor data to analyze
        :return: Boolean indicating if biosignature was detected
        """
        detection_score = self.analyze_data(biosensor_data)
        
        if detection_score >= self.threshold:
            self.logger.info(f"Biosignature detected! Score: {detection_score:.4f} (threshold: {self.threshold})")
            return True
        else:
            self.logger.info(f"No biosignature detected. Score: {detection_score:.4f} (threshold: {self.threshold})")
            return False