from .quantum_comm import QuantumComm

class EntanglementManager:
    """
    Manage quantum communication by establishing, maintaining, and utilizing entangled pairs for message transmission and reception.
    """
    
    def __init__(self):
        """
        Initialize an instance of the class by setting up a quantum communication interface and an empty list to track active communication pairs.
        """
        self.quantum_comm = QuantumComm()
        self.active_pairs = []
    
    def establish_connection(self):
        """
        Establishes a quantum connection by creating entangled pairs.
        """
        pair = self.quantum_comm.create_entangled_pair()
        if pair:
            self.active_pairs.append(pair)
            return len(self.active_pairs) - 1
        return None
    
    def list_active_pairs(self):
        """
        Lists all active entangled pairs.
        """
        return self.active_pairs
    
    def receive_message(self, pair_index):
        """
        Simulates receiving a message by measuring the state of the entangled pair.
        """
        if 0 <= pair_index < len(self.active_pairs):
            return self.quantum_comm.receive_message(pair_index)
        return None
    
    def remove_pair(self, pair_index):
        """
        Removes an entangled pair from the active list.
        """
        if 0 <= pair_index < len(self.active_pairs):
            self.active_pairs.pop(pair_index)
            return True
        return False
    
    def send_message(self, message, pair_index):
        """
        Sends a message using the established quantum connection.
        """
        if 0 <= pair_index < len(self.active_pairs):
            return self.quantum_comm.transmit_message(message, pair_index)
        return False