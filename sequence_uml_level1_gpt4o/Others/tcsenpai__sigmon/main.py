import time
import os
import plotext as plt
from typing import List, Optional, Callable
from datetime import datetime

# Import from other modules in the project
from .session import SessionMetrics
from .sigmod_metrics import Metrics


def plot_metrics_live(get_metrics_func, adapter_name, interval) -> None:
    """
    Continuously plot metrics in real-time

    Args:
        get_metrics_func: Function to get metrics
        adapter_name: Name of the network adapter
        interval: Update interval in seconds
    """
    plotter = MetricsPlotter()
    
    try:
        while True:
            metrics = get_metrics_func(adapter_name)
            plotter.update_plot(metrics)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
        plotter.save_plot()


class MetricsPlotter:
    """
    The MetricsPlotter class is designed to monitor, visualize, and save WiFi signal strength metrics over time, 
    including dynamic plotting, real-time updates, and session summary statistics.
    """
    
    def __init__(self, max_points=100) -> None:
        """
        Initialize an instance with default or specified maximum points, setting up lists for signal strengths 
        and timestamps, initializing min/max seen values, creating a session metrics object, and ensuring a plots directory exists.
        """
        self.max_points = max_points
        self.signal_strengths: List[float] = []
        self.timestamps: List[str] = []
        self.max_seen: Optional[float] = None
        self.min_seen: Optional[float] = None
        self.session = SessionMetrics()
        
        # Ensure plots directory exists
        os.makedirs("plots", exist_ok=True)

    def update_plot(self, metrics: Metrics) -> None:
        """
        Convert signal strength to float and ensure it's negative
        """
        # Add metrics to session
        self.session.add_metrics(metrics)
        
        # Process signal strength
        if metrics.signal_strength:
            try:
                signal_strength = float(metrics.signal_strength)
                # Ensure signal strength is negative (dBm values are negative)
                if signal_strength > 0:
                    signal_strength = -signal_strength
                
                # Update min/max seen values
                if self.max_seen is None or signal_strength > self.max_seen:
                    self.max_seen = signal_strength
                if self.min_seen is None or signal_strength < self.min_seen:
                    self.min_seen = signal_strength
                
                # Add to data lists
                self.signal_strengths.append(signal_strength)
                self.timestamps.append(datetime.now().strftime("%H:%M:%S"))
                
                # Trim lists to max_points
                if len(self.signal_strengths) > self.max_points:
                    self.signal_strengths = self.signal_strengths[-self.max_points:]
                    self.timestamps = self.timestamps[-self.max_points:]
                
                # Clear previous plot
                plt.clear_figure()
                plt.clear_terminal()
                
                # Plot signal strength
                plt.plot(self.signal_strengths, label="Signal Strength (dBm)")
                plt.title("WiFi Signal Strength Monitor")
                plt.xlabel("Time")
                plt.ylabel("Signal Strength (dBm)")
                plt.ylim(self.min_seen - 5, self.max_seen + 5) if self.min_seen is not None and self.max_seen is not None else None
                
                # Add current value annotation
                plt.text(f"Current: {signal_strength:.1f} dBm", x=len(self.signal_strengths)-1, y=signal_strength)
                
                # Show plot
                plt.show()
                
                # Print session summary
                print(self.session.get_session_summary())
                
            except ValueError:
                print(f"Invalid signal strength value: {metrics.signal_strength}")

    def save_plot(self) -> None:
        """
        Save the current plot with averages
        """
        if not self.signal_strengths:
            print("No data to save")
            return
            
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"plots/signal_strength_{timestamp}.png"
        
        # Recreate plot for saving
        plt.clear_figure()
        plt.plot(self.signal_strengths, label="Signal Strength (dBm)")
        plt.title("WiFi Signal Strength History")
        plt.xlabel("Time")
        plt.ylabel("Signal Strength (dBm)")
        
        # Add average line if we have data
        if self.signal_strengths:
            avg_strength = sum(self.signal_strengths) / len(self.signal_strengths)
            plt.hline(avg_strength, color="red", label=f"Average: {avg_strength:.1f} dBm")
        
        # Save the plot
        plt.save_fig(filename)
        print(f"Plot saved as {filename}")
        
        # Print final session summary
        print("\nFinal Session Summary:")
        print(self.session.get_session_summary())