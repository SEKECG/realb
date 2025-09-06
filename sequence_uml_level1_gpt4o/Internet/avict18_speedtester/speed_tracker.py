#!/usr/bin/env python3
"""
Speedtester - A command-line tool to monitor and record internet speed at regular intervals.
"""

import csv
import time
from datetime import datetime
import speedtest
import colorama
from colorama import Fore, Style

# Initialize colorama for colored terminal output
colorama.init(autoreset=True)

def run_speed_test(high, low, serial_number, record_file):
    """
    Measure and record internet speed metrics (download, upload, ping) with status evaluation 
    based on predefined thresholds, and save the results to a CSV file.
    
    Args:
        high: High threshold for download speed (Mbps) - above this is "great"
        low: Low threshold for download speed (Mbps) - below this is "bad"
        serial_number: Current test sequence number
        record_file: CSV file path to record results
    """
    try:
        # Create speedtest object
        st = speedtest.Speedtest()
        
        # Get best server
        st.get_best_server()
        
        # Perform speed tests
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000      # Convert to Mbps
        ping = st.results.ping
        
        # Determine status based on thresholds
        if download_speed >= high:
            status = "great"
            status_color = Fore.GREEN
        elif download_speed >= low:
            status = "okay"
            status_color = Fore.YELLOW
        else:
            status = "bad"
            status_color = Fore.RED
        
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Display results with color coding
        print(f"\n{Fore.CYAN}=== Speed Test #{serial_number} ===")
        print(f"{Fore.WHITE}Timestamp: {timestamp}")
        print(f"{Fore.BLUE}Download: {download_speed:.2f} Mbps")
        print(f"{Fore.BLUE}Upload: {upload_speed:.2f} Mbps")
        print(f"{Fore.BLUE}Ping: {ping:.2f} ms")
        print(f"{status_color}Status: {status.upper()}{Style.RESET_ALL}")
        
        # Write results to CSV file
        with open(record_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                serial_number,
                timestamp,
                f"{download_speed:.2f}",
                f"{upload_speed:.2f}",
                f"{ping:.2f}",
                status
            ])
            
    except speedtest.SpeedtestException as e:
        print(f"{Fore.RED}Error during speed test: {e}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")

def main():
    """
    Run periodic internet speed tests, compare results against user-defined thresholds, 
    and record the data in a CSV file.
    """
    print(f"{Fore.GREEN}=== Speedtester - Internet Speed Monitor ==={Style.RESET_ALL}")
    print("Press Ctrl+C to stop the monitoring...")
    
    # Configuration
    HIGH_THRESHOLD = 50.0  # Mbps - above this is "great"
    LOW_THRESHOLD = 10.0   # Mbps - below this is "bad"
    TEST_INTERVAL = 300    # 5 minutes in seconds
    RECORD_FILE = "speed_records.csv"
    
    # Initialize CSV file with headers if it doesn't exist
    try:
        with open(RECORD_FILE, 'x', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Serial', 'Timestamp', 'Download (Mbps)', 'Upload (Mbps)', 'Ping (ms)', 'Status'])
        print(f"{Fore.YELLOW}Created new record file: {RECORD_FILE}{Style.RESET_ALL}")
    except FileExistsError:
        print(f"{Fore.YELLOW}Appending to existing record file: {RECORD_FILE}{Style.RESET_ALL}")
    
    serial_number = 1
    
    try:
        while True:
            run_speed_test(HIGH_THRESHOLD, LOW_THRESHOLD, serial_number, RECORD_FILE)
            
            # Wait for the next test interval
            print(f"{Fore.CYAN}\nNext test in {TEST_INTERVAL//60} minutes...{Style.RESET_ALL}")
            time.sleep(TEST_INTERVAL)
            serial_number += 1
            
    except KeyboardInterrupt:
        print(f"\n{Fore.GREEN}Speed monitoring stopped.{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Results saved to: {RECORD_FILE}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()