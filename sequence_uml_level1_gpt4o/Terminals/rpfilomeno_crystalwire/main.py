#!/usr/bin/env python3

import time
import threading
from collections import defaultdict
import psutil
from scapy.all import sniff, IP, TCP, UDP
import pandas as pd
from plotille import Figure
import os

# Global variables
connection2pid = {}
pid2traffic = defaultdict(lambda: [0, 0])
global_df = None
global_graph_data = defaultdict(list)
is_program_running = True
all_macs = {iface.mac for iface in psutil.net_if_addrs().values()}

def get_connections():
    """A function that keeps listening for connections on this machine
    and adds them to `connection2pid` global variable"""
    global connection2pid
    while is_program_running:
        try:
            connections = psutil.net_connections(kind='inet')
            for connection in connections:
                if connection.laddr and connection.raddr and connection.pid:
                    # local address, remote address, and PID are available
                    local_ip, local_port = connection.laddr
                    remote_ip, remote_port = connection.raddr
                    connection_key = (local_ip, local_port, remote_ip, remote_port)
                    connection2pid[connection_key] = connection.pid
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Process might have terminated, skip it
            pass
        time.sleep(1)

def get_size(bytes):
    """Returns size of bytes in a nice format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024

def process_packet(packet):
    """Track and accumulate network traffic (upload and download) per process ID (PID) 
    based on packet source and destination information."""
    global pid2traffic
    
    if IP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        
        # Determine protocol and ports
        src_port = None
        dst_port = None
        if TCP in packet:
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
        elif UDP in packet:
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport
        
        if src_port and dst_port:
            # Try to find the connection in our mapping
            pid = None
            try:
                # Check if this is an outgoing packet (from our machine)
                if src_ip in all_macs or any(iface for iface in psutil.net_if_addrs().values() if iface.address == src_ip):
                    connection_key = (src_ip, src_port, dst_ip, dst_port)
                    pid = connection2pid.get(connection_key)
                    if pid:
                        # This is upload (outgoing) traffic
                        pid2traffic[pid][0] += len(packet)
                # Check if this is an incoming packet (to our machine)
                elif dst_ip in all_macs or any(iface for iface in psutil.net_if_addrs().values() if iface.address == dst_ip):
                    connection_key = (dst_ip, dst_port, src_ip, src_port)
                    pid = connection2pid.get(connection_key)
                    if pid:
                        # This is download (incoming) traffic
                        pid2traffic[pid][1] += len(packet)
            except (KeyError, AttributeError):
                pass

def print_stats():
    """Simple function that keeps printing the stats"""
    global global_df
    while is_program_running:
        time.sleep(1)
        print_pid2traffic()

def print_pid2traffic():
    """Monitor and display network traffic statistics (upload/download speeds and totals) 
    per process ID (PID), including real-time speed calculations and visualization of top processes."""
    global global_df, pid2traffic, global_graph_data
    
    # Create a copy of current traffic data
    current_traffic = dict(pid2traffic)
    
    # Create DataFrame for current stats
    processes = []
    for pid, traffic in current_traffic.items():
        try:
            process = psutil.Process(pid)
            processes.append({
                'pid': pid,
                'name': process.name(),
                'upload': traffic[0],
                'download': traffic[1]
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # Process might have terminated, skip it
            continue
    
    if not processes:
        return
    
    df = pd.DataFrame(processes)
    
    # Calculate speeds if we have previous data
    if global_df is not None:
        # Merge with previous data to calculate speeds
        merged = df.merge(global_df, on=['pid', 'name'], suffixes=('_current', '_previous'))
        merged['upload_speed'] = (merged['upload_current'] - merged['upload_previous']) / 1024  # KB/s
        merged['download_speed'] = (merged['download_current'] - merged['download_previous']) / 1024  # KB/s
        
        # Update graph data
        for _, row in merged.iterrows():
            global_graph_data[row['name']].append(row['upload_speed'] + row['download_speed'])
            # Keep only last 60 seconds of data
            if len(global_graph_data[row['name']]) > 60:
                global_graph_data[row['name']].pop(0)
        
        # Display the stats
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Network Traffic Monitor - Real-time Statistics")
        print("=" * 80)
        
        # Sort by total speed and get top 10
        merged['total_speed'] = merged['upload_speed'] + merged['download_speed']
        top_processes = merged.nlargest(10, 'total_speed')
        
        print(f"{'PID':<8} {'Process':<20} {'Upload':<12} {'Download':<12} {'Up Speed':<12} {'Down Speed':<12}")
        print("-" * 80)
        
        for _, row in top_processes.iterrows():
            print(f"{row['pid']:<8} {row['name'][:19]:<20} "
                  f"{get_size(row['upload_current']):<12} {get_size(row['download_current']):<12} "
                  f"{row['upload_speed']:.2f} KB/s {row['download_speed']:.2f} KB/s")
        
        # Plot the graph
        plot(top_processes)
    
    # Update global DataFrame for next iteration
    global_df = df[['pid', 'name', 'upload', 'download']].copy()

def plot(df):
    """Visualize time-series data of network bandwidth usage (in Kb/s) over a 60-second period 
    for multiple series, using a terminal-based plot with distinct colors for each series."""
    global global_graph_data
    
    if not global_graph_data:
        return
    
    fig = Figure()
    fig.width = 80
    fig.height = 20
    fig.color_mode = 'byte'
    fig.set_x_limits(min_=0, max_=60)
    
    # Find max y value for scaling
    max_y = max(max(data) for data in global_graph_data.values() if data) or 100
    
    fig.set_y_limits(min_=0, max_=max_y * 1.1)
    fig.xlabel = 'Time (seconds ago)'
    fig.ylabel = 'Bandwidth (KB/s)'
    
    colors = ['red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'white']
    
    for i, (process_name, data) in enumerate(global_graph_data.items()):
        if data:
            x_values = list(range(len(data) - 1, -1, -1))
            fig.plot(x_values, data, lc=colors[i % len(colors)], label=process_name[:15])
    
    print("\nBandwidth Usage Over Time:")
    print(fig.show(legend=True))
    print("\n" + "=" * 80)

def stat(df):
    """Display the first few lines of a pandas DataFrame with specific lines 
    highlighted in different colors for enhanced visibility."""
    # This function seems to be a placeholder or alternative display method
    # For now, we'll use the main display in print_pid2traffic
    pass

def main():
    global connections_thread, printing_thread, is_program_running
    
    print("Starting Network Traffic Monitor...")
    print("Press Ctrl+C to stop\n")
    
    # Start the connections thread
    connections_thread = threading.Thread(target=get_connections)
    connections_thread.daemon = True
    connections_thread.start()
    
    # Start the printing thread
    printing_thread = threading.Thread(target=print_stats)
    printing_thread.daemon = True
    printing_thread.start()
    
    # Start sniffing packets
    try:
        sniff(prn=process_packet, store=False)
    except KeyboardInterrupt:
        print("\nStopping Network Traffic Monitor...")
        is_program_running = False
        connections_thread.join(timeout=1)
        printing_thread.join(timeout=1)
        print("Monitor stopped.")

if __name__ == "__main__":
    main()