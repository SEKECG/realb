from datetime import datetime
from typing import List
from .sigmod_metrics import Metrics


class SessionMetrics:
    """
    To collect, store, and summarize signal strength and bitrate metrics over a session duration.
    """
    
    def __init__(self) -> None:
        """
        Initialize an instance with empty lists for signal and bitrate readings, and record the current datetime as the start time.
        """
        self.signal_readings: List[float] = []
        self.bitrate_readings: List[float] = []
        self.start_time: datetime = datetime.now()

    def add_metrics(self, metrics: Metrics) -> None:
        """
        Append valid signal strength and bitrate values from a Metrics object to respective reading lists, handling potential invalid values with a warning.
        """
        if metrics.signal_strength is not None:
            try:
                signal_strength = float(metrics.signal_strength)
                if signal_strength > 0:
                    signal_strength = -signal_strength
                self.signal_readings.append(signal_strength)
            except (ValueError, TypeError):
                print(f"Warning: Invalid signal strength value: {metrics.signal_strength}")
        
        if metrics.bitrate is not None:
            try:
                bitrate = float(metrics.bitrate)
                self.bitrate_readings.append(bitrate)
            except (ValueError, TypeError):
                print(f"Warning: Invalid bitrate value: {metrics.bitrate}")

    def get_session_summary(self) -> str:
        """
        Generate a summary of a session including average signal strength, average bitrate, duration, and the number of samples collected.
        """
        duration = datetime.now() - self.start_time
        hours, remainder = divmod(duration.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        signal_samples = len(self.signal_readings)
        bitrate_samples = len(self.bitrate_readings)
        
        avg_signal = sum(self.signal_readings) / signal_samples if signal_samples > 0 else 0
        avg_bitrate = sum(self.bitrate_readings) / bitrate_samples if bitrate_samples > 0 else 0
        
        summary = f"""
Session Summary:
----------------
Duration: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}
Signal Samples: {signal_samples}
Bitrate Samples: {bitrate_samples}
Average Signal Strength: {avg_signal:.1f} dBm
Average Bitrate: {avg_bitrate:.1f} Mb/s
"""
        return summary