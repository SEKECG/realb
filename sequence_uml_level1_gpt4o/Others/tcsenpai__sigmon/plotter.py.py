import subprocess
import re
from typing import Optional
from .sigmod_metrics import Metrics


def get_active_interface() -> Optional[str]:
    """
    Get the active interface name
    """
    try:
        # Get list of network interfaces
        result = subprocess.run(['iwconfig'], capture_output=True, text=True, check=True)
        
        # Look for interfaces that aren't loopback and have wireless extensions
        lines = result.stdout.split('\n')
        for line in lines:
            if 'IEEE 802.11' in line and 'no wireless extensions' not in line:
                # Extract interface name (first word before space)
                interface_match = re.match(r'^(\w+)\s+', line)
                if interface_match:
                    return interface_match.group(1)
        
        return None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_metrics(adapter_name) -> Metrics:
    """
    Get the metrics of the network adapter

    Execute iwconfig command and return the output
    """
    try:
        # Run iwconfig for the specific adapter
        result = subprocess.run(['iwconfig', adapter_name], capture_output=True, text=True, check=True)
        output = result.stdout
        
        # Parse signal strength
        signal_match = re.search(r'Signal level=(-?\d+) dBm', output)
        signal_strength = float(signal_match.group(1)) if signal_match else None
        
        # Parse bitrate
        bitrate_match = re.search(r'Bit Rate=([\d.]+) Mb/s', output)
        bitrate = float(bitrate_match.group(1)) if bitrate_match else None
        
        # Parse power management
        power_match = re.search(r'Power Management:(\w+)', output)
        is_power_save_enabled = power_match.group(1).lower() == 'on' if power_match else False
        
        return Metrics(signal_strength, bitrate, is_power_save_enabled)
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Return empty metrics if command fails
        return Metrics(None, None, False)