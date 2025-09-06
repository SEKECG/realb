import time
import random
import os
import sys
from datetime import datetime


def clear_screen():
    """Clears the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def banner():
    """Program Title"""
    print(r"""
    ██╗███╗   ██╗███████╗██╗███╗   ██╗███████╗████████╗
    ██║████╗  ██║██╔════╝██║████╗  ██║██╔════╝╚══██╔══╝
    ██║██╔██╗ ██║█████╗  ██║██╔██╗ ██║█████╗     ██║   
    ██║██║╚██╗██║██╔══╝  ██║██║╚██╗██║██╔══╝     ██║   
    ██║██║ ╚████║██║     ██║██║ ╚████║███████╗   ██║   
    ╚═╝╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   
    """)


def show_menu():
    """Main Menu"""
    print("\n" + "="*50)
    print("          INFINET MAIN MENU")
    print("="*50)
    print("1. Network Scan")
    print("2. MITM Attack")
    print("3. DNS Spoofing")
    print("4. Automatic Attack Selection")
    print("5. Show Instructions")
    print("6. Exit")
    print("="*50)


def show_instructions():
    """Help Menu"""
    clear_screen()
    banner()
    print("\n" + "="*50)
    print("          INSTRUCTIONS & HELP")
    print("="*50)
    print("\n1. NETWORK SCAN:")
    print("   - Enter target IP range to scan")
    print("   - Uses ARP spoofing to identify devices")
    print("   - Returns list of active hosts")
    
    print("\n2. MITM ATTACK:")
    print("   - Requires victim IP and gateway IP")
    print("   - Spoofs ARP packets to intercept traffic")
    print("   - Captures and manipulates network data")
    
    print("\n3. DNS SPOOFING:")
    print("   - Redirects DNS requests to specified IP")
    print("   - Requires target IP and spoof IP")
    print("   - Can redirect to malicious sites")
    
    print("\n4. AUTOMATIC SELECTION:")
    print("   - Randomly selects attack type")
    print("   - Automates the attack process")
    print("   - Includes performance monitoring")
    
    print("\n" + "="*50)
    input("\nPress Enter to return to main menu...")
    clear_screen()


def network_scan():
    """Network Scan Function (with ARP Spoofing)"""
    clear_screen()
    banner()
    print("\n" + "="*50)
    print("          NETWORK SCAN")
    print("="*50)
    
    target_ip = input("Enter target IP range (e.g., 192.168.1.0/24): ")
    
    if not target_ip:
        print("Error: IP range cannot be empty!")
        return
    
    print(f"\nStarting network scan on {target_ip}...")
    print("Scanning using ARP spoofing technique...")
    
    # Simulate scanning process
    time.sleep(2)
    
    # Simulate found devices
    devices = [
        {"ip": "192.168.1.1", "mac": "00:1A:2B:3C:4D:5E", "hostname": "router"},
        {"ip": "192.168.1.2", "mac": "AA:BB:CC:DD:EE:FF", "hostname": "pc-01"},
        {"ip": "192.168.1.3", "mac": "11:22:33:44:55:66", "hostname": "server"},
        {"ip": "192.168.1.4", "mac": "77:88:99:AA:BB:CC", "hostname": "laptop"}
    ]
    
    print(f"\nFound {len(devices)} devices:")
    print("-" * 60)
    print(f"{'IP Address':<15} {'MAC Address':<18} {'Hostname':<15}")
    print("-" * 60)
    
    for device in devices:
        print(f"{device['ip']:<15} {device['mac']:<18} {device['hostname']:<15}")
    
    advanced_logging(f"Network scan performed on {target_ip}")
    input("\nPress Enter to continue...")
    clear_screen()


def mitm_attack():
    """Start MITM Attack (with ARP Spoofing)"""
    clear_screen()
    banner()
    print("\n" + "="*50)
    print("          MITM ATTACK")
    print("="*50)
    
    victim_ip = input("Enter victim IP address: ")
    gateway_ip = input("Enter gateway IP address: ")
    
    if not victim_ip or not gateway_ip:
        print("Error: Both IP addresses are required!")
        return
    
    start_time = time.time()
    print(f"\nStarting MITM attack between {victim_ip} and {gateway_ip}...")
    print("Sending ARP spoofing packets...")
    
    # Simulate attack process
    for i in range(3):
        print(f"Packet {i+1} sent...")
        time.sleep(1)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\nMITM attack completed successfully!")
    print(f"Traffic between {victim_ip} and {gateway_ip} is now intercepted")
    
    dynamic_report("MITM Attack", "Successful", duration)
    advanced_logging(f"MITM attack initiated: {victim_ip} -> {gateway_ip}")
    input("\nPress Enter to continue...")
    clear_screen()


def dns_spoofing():
    """DNS Spoofing"""
    clear_screen()
    banner()
    print("\n" + "="*50)
    print("          DNS SPOOFING")
    print("="*50)
    
    target_ip = input("Enter target IP address: ")
    spoof_ip = input("Enter IP to redirect to: ")
    
    if not target_ip or not spoof_ip:
        print("Error: Both IP addresses are required!")
        return
    
    start_time = time.time()
    print(f"\nStarting DNS spoofing attack on {target_ip}...")
    print(f"Redirecting DNS requests to {spoof_ip}...")
    
    # Simulate DNS spoofing process
    for i in range(3):
        print(f"DNS request {i+1} intercepted and modified...")
        time.sleep(1)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\nDNS spoofing completed successfully!")
    print(f"Target {target_ip} will now resolve to {spoof_ip}")
    
    dynamic_report("DNS Spoofing", "Successful", duration)
    advanced_logging(f"DNS spoofing: {target_ip} -> {spoof_ip}")
    input("\nPress Enter to continue...")
    clear_screen()


def advanced_attack_choice():
    """Attack Type Selection (Automatic Method)"""
    clear_screen()
    banner()
    print("\n" + "="*50)
    print("      AUTOMATIC ATTACK SELECTION")
    print("="*50)
    
    attacks = ["Network Scan", "MITM Attack", "DNS Spoofing"]
    selected_attack = random.choice(attacks)
    
    print(f"\nRandomly selected attack: {selected_attack}")
    print("Starting automated attack process...")
    
    start_time = time.time()
    
    # Simulate the selected attack
    if selected_attack == "Network Scan":
        print("Performing automated network scan...")
        time.sleep(2)
        print("Scan completed - 4 devices found")
        
    elif selected_attack == "MITM Attack":
        print("Configuring automated MITM attack...")
        time.sleep(2)
        print("MITM attack established - traffic intercepted")
        
    elif selected_attack == "DNS Spoofing":
        print("Setting up automated DNS spoofing...")
        time.sleep(2)
        print("DNS spoofing active - requests redirected")
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\nAutomatic {selected_attack} completed!")
    
    dynamic_report(f"Auto {selected_attack}", "Successful", duration)
    advanced_logging(f"Automatic attack performed: {selected_attack}")
    input("\nPress Enter to continue...")
    clear_screen()


def performance_monitor(start_time, end_time):
    """Timer and Performance Monitoring"""
    duration = end_time - start_time
    return f"{duration:.2f} seconds"


def dynamic_report(attack_type, status, duration):
    """Dynamic Process Report"""
    print("\n" + "="*50)
    print("          ATTACK REPORT")
    print("="*50)
    print(f"Attack Type: {attack_type}")
    print(f"Status: {status}")
    print(f"Duration: {duration:.2f} seconds")
    print("="*50)
    
    # Log the report
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("attack_reports.log", "a") as f:
        f.write(f"[{timestamp}] {attack_type} - {status} - {duration:.2f}s\n")


def advanced_logging(action):
    """Advanced Logging (Save User Interactions)"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("user_actions.log", "a") as f:
        f.write(f"[{timestamp}] {action}\n")


def main():
    """Main program function"""
    clear_screen()
    
    while True:
        banner()
        show_menu()
        
        try:
            choice = input("\nEnter your choice (1-6): ")
            
            if choice == '1':
                network_scan()
            elif choice == '2':
                mitm_attack()
            elif choice == '3':
                dns_spoofing()
            elif choice == '4':
                advanced_attack_choice()
            elif choice == '5':
                show_instructions()
            elif choice == '6':
                print("\nThank you for using InfiNet!")
                print("Exiting program...")
                break
            else:
                print("\nInvalid choice! Please enter a number between 1-6.")
                time.sleep(1)
                clear_screen()
                
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user. Exiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            time.sleep(2)
            clear_screen()


if __name__ == "__main__":
    main()