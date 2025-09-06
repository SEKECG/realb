import logging

class RelayNetwork:
    """
    Manage and transmit data through a network of relay nodes, allowing addition of relays and ensuring data transmission via available relays.
    """
    
    def __init__(self):
        """
        Initialize an instance of the class by setting up an empty list for relay nodes and configuring basic logging at the INFO level.
        """
        self.relays = []
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initialized RelayNetwork with empty relay list")
    
    def add_relay(self, relay_id):
        """
        Add a relay ID to the network and log the addition.
        :param relay_id: ID of the relay to add
        """
        self.relays.append(relay_id)
        self.logger.info(f"Added relay with ID: {relay_id}")
    
    def transmit_via_relays(self, data):
        """
        Transmit data through all available relays in the network and log the transmission process. Returns True if successful, False if no relays are available.
        :param data: Data to be transmitted
        :return: Boolean indicating transmission success
        """
        if not self.relays:
            self.logger.warning("No relays available for transmission")
            return False
        
        self.logger.info(f"Starting transmission of data: {data}")
        
        for relay_id in self.relays:
            self.logger.info(f"Transmitting via relay {relay_id}: {data}")
        
        self.logger.info(f"Successfully transmitted data through {len(self.relays)} relays")
        return True