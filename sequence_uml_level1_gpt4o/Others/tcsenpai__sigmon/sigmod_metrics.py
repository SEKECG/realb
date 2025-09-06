class Metrics:
    """
    Class to store the metrics of the network adapter
    """
    
    def __init__(self, signal_strength, bitrate, is_power_save_enabled):
        """
        Initialize Metrics instance with network adapter metrics
        
        Args:
            signal_strength: Signal strength in dBm
            bitrate: Bitrate in Mb/s
            is_power_save_enabled: Whether power save mode is enabled
        """
        self.signal_strength = signal_strength
        self.bitrate = bitrate
        self.is_power_save_enabled = is_power_save_enabled
    
    def __str__(self):
        """
        Return a human-readable string representation of the object's attributes, 
        including signal strength, bitrate, and power save status.
        """
        signal_str = f"{self.signal_strength} dBm" if self.signal_strength is not None else "N/A"
        bitrate_str = f"{self.bitrate} Mb/s" if self.bitrate is not None else "N/A"
        power_save_str = "Enabled" if self.is_power_save_enabled else "Disabled"
        
        return f"Signal Strength: {signal_str}, Bitrate: {bitrate_str}, Power Save: {power_save_str}"