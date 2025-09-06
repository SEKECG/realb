import numpy as np
import logging

class ErrorCorrection:
    """
    Implement Hamming (7,4) error correction code to encode 4-bit data into 7-bit codewords 
    and detect/correct single-bit errors in received 7-bit data.
    """
    
    def __init__(self):
        """Initialize the ErrorCorrection class with logging configuration."""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def hamming_code(self, data):
        """
        Encodes 4 bits of data using Hamming (7,4) code.
        :param data: A string of 4 bits (e.g., '1011').
        :return: A numpy array of encoded data (7 bits).
        """
        if len(data) != 4:
            raise ValueError("Input data must be exactly 4 bits")
        
        # Convert string to integers
        d = [int(bit) for bit in data]
        
        # Calculate parity bits
        p1 = d[0] ^ d[1] ^ d[3]
        p2 = d[0] ^ d[2] ^ d[3]
        p3 = d[1] ^ d[2] ^ d[3]
        
        # Construct the 7-bit codeword
        codeword = np.array([p1, p2, d[0], p3, d[1], d[2], d[3]])
        
        self.logger.info(f"Encoded data '{data}' to Hamming code: {codeword}")
        return codeword
    
    def detect_and_correct(self, received_data):
        """
        Detects and corrects a single-bit error in the received data using Hamming (7,4) code.
        :param received_data: A numpy array of received data (7 bits).
        :return: A numpy array of corrected data (4 bits).
        """
        if len(received_data) != 7:
            raise ValueError("Received data must be exactly 7 bits")
        
        # Calculate syndrome bits
        s1 = received_data[0] ^ received_data[2] ^ received_data[4] ^ received_data[6]
        s2 = received_data[1] ^ received_data[2] ^ received_data[5] ^ received_data[6]
        s3 = received_data[3] ^ received_data[4] ^ received_data[5] ^ received_data[6]
        
        error_position = s1 + 2*s2 + 4*s3 - 1
        
        corrected_data = received_data.copy()
        
        if error_position >= 0:
            # Correct the error
            corrected_data[error_position] = 1 - corrected_data[error_position]
            self.logger.info(f"Detected and corrected error at position {error_position + 1}")
        
        # Extract the original 4 data bits
        original_data = np.array([corrected_data[2], corrected_data[4], corrected_data[5], corrected_data[6]])
        
        self.logger.info(f"Corrected data: {original_data}")
        return original_data