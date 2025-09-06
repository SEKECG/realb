import sys
import time
import logging
import hashlib
import hmac
import threading
import random
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableWidget, QTableWidgetItem, 
                             QPushButton, QVBoxLayout, QWidget, QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QEvent
from PyQt5.QtGui import QColor

# Global variables
SECRET_KEY = b'secret_key_123456'  # Shared secret key for MAC generation
can_bus = []  # Simulated CAN bus as a shared list
freshness_manager = {}  # Dictionary to track freshness values per message ID
stop_event = threading.Event()  # Event to signal threads to stop

# Logging setup
def setup_logging():
    """Logging setup"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('secoc_simulation.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def generate_mac(message, freshness, key):
    """Generate a MAC for a given message and freshness (timestamp)."""
    data = f"{message}{freshness}".encode('utf-8')
    mac = hmac.new(key, data, hashlib.sha256).hexdigest()
    return mac

def verify_mac(message, freshness, received_mac, key):
    """Verify the MAC for a given message and freshness (timestamp)."""
    expected_mac = generate_mac(message, freshness, key)
    return hmac.compare_digest(expected_mac, received_mac)

class SenderThread(QThread):
    new_message_signal = pyqtSignal(list, bool, str)
    
    def __init__(self):
        super().__init__()
        self.last_sent_freshness = {}

    def run(self):
        """Simulate a sender ECU."""
        logging.info("Sender thread started")
        message_counter = 0
        
        while not stop_event.is_set():
            try:
                # Generate message data
                message_id = random.randint(0x100, 0x7FF)  # Standard CAN ID range
                data_length = random.randint(1, 8)
                message_data = ''.join([f"{random.randint(0, 255):02X}" for _ in range(data_length)])
                
                # Generate freshness value (timestamp)
                current_time = int(time.time() * 1000)  # Milliseconds
                self.last_sent_freshness[message_id] = current_time
                
                # Generate MAC
                mac = generate_mac(message_data, current_time, SECRET_KEY)
                
                # Format CAN message
                can_message = f"{message_id:03X}#{message_data}#{current_time}#{mac}"
                
                # Add to CAN bus
                can_bus.append(can_message)
                
                # Emit signal for UI update
                message_parts = [
                    datetime.now().strftime("%H:%M:%S.%f")[:-3],
                    message_data,
                    f"{message_id:03X}",
                    str(data_length),
                    str(current_time),
                    mac,
                    "Sent"
                ]
                self.new_message_signal.emit(message_parts, False, "sent")
                
                message_counter += 1
                logging.info(f"Sent message {message_counter}: {can_message}")
                
                # Wait before sending next message
                time.sleep(random.uniform(0.5, 2.0))
                
            except Exception as e:
                logging.error(f"Error in sender thread: {e}")
                break

class ReceiverThread(QThread):
    new_message_signal = pyqtSignal(list, bool, str)
    
    def __init__(self):
        super().__init__()
        self.replay_attack_triggered = False

    def run(self):
        """Simulate a receiver ECU."""
        logging.info("Receiver thread started")
        processed_messages = set()
        
        while not stop_event.is_set():
            try:
                if can_bus:
                    # Get the oldest message from CAN bus
                    can_message = can_bus.pop(0)
                    
                    # Parse CAN message
                    try:
                        message_id_str, message_data, freshness_str, received_mac = can_message.split('#')
                        message_id = int(message_id_str, 16)
                        freshness = int(freshness_str)
                    except ValueError:
                        logging.warning(f"Invalid message format: {can_message}")
                        continue
                    
                    # Check for replay attack
                    is_replay = False
                    message_signature = f"{message_id}_{freshness}_{received_mac}"
                    
                    if message_signature in processed_messages:
                        is_replay = True
                        self.replay_attack_triggered = True
                        logging.warning(f"Replay attack detected! Message: {can_message}")
                    else:
                        processed_messages.add(message_signature)
                    
                    # Verify MAC
                    mac_valid = verify_mac(message_data, freshness, received_mac, SECRET_KEY)
                    
                    if not mac_valid:
                        logging.warning(f"MAC verification failed for message: {can_message}")
                        continue
                    
                    # Update freshness value for this message ID
                    if message_id not in freshness_manager or freshness > freshness_manager[message_id]:
                        freshness_manager[message_id] = freshness
                    
                    # Emit signal for UI update
                    message_parts = [
                        datetime.now().strftime("%H:%M:%S.%f")[:-3],
                        message_data,
                        message_id_str,
                        str(len(message_data) // 2),  # DLC
                        freshness_str,
                        received_mac,
                        "Received"
                    ]
                    self.new_message_signal.emit(message_parts, is_replay, "received")
                    
                    logging.info(f"Received valid message: {can_message}")
                
                time.sleep(0.1)  # Small delay to prevent busy waiting
                
            except Exception as e:
                logging.error(f"Error in receiver thread: {e}")
                break

class MainWindow(QMainWindow):
    def __init__(self):
        """Initialize the main window for a CAN Message Simulation application, setting up the UI components (table, buttons), layout, and background threads for message handling."""
        super().__init__()
        
        self.sender_thread = None
        self.receiver_thread = None
        self.replay_attack_triggered = False
        
        self.setWindowTitle("SecOC Simulation - CAN Message Monitor")
        self.setGeometry(100, 100, 1200, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create table widget
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels([
            "Timestamp", "Message", "ID", "DLC", "Freshness", "MAC", "Type"
        ])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tableWidget)
        
        # Create buttons
        button_layout = QVBoxLayout()
        
        self.start_stop_button = QPushButton("Start Simulation")
        self.start_stop_button.clicked.connect(self.toggle_simulation)
        button_layout.addWidget(self.start_stop_button)
        
        self.replay_button = QPushButton("Trigger Replay Attack")
        self.replay_button.clicked.connect(self.trigger_replay_attack)
        self.replay_button.setEnabled(False)
        button_layout.addWidget(self.replay_button)
        
        self.clear_button = QPushButton("Clear Table")
        self.clear_button.clicked.connect(self.clear_simulation)
        button_layout.addWidget(self.clear_button)
        
        layout.addLayout(button_layout)
        
        # Setup logging
        setup_logging()

    def toggle_simulation(self):
        """Start or stop the simulation."""
        if self.sender_thread and self.sender_thread.isRunning():
            # Stop simulation
            stop_event.set()
            self.sender_thread.wait()
            self.receiver_thread.wait()
            self.start_stop_button.setText("Start Simulation")
            self.replay_button.setEnabled(False)
            logging.info("Simulation stopped")
        else:
            # Start simulation
            stop_event.clear()
            global can_bus, freshness_manager
            can_bus.clear()
            freshness_manager.clear()
            
            self.sender_thread = SenderThread()
            self.receiver_thread = ReceiverThread()
            
            self.sender_thread.new_message_signal.connect(self.update_table)
            self.receiver_thread.new_message_signal.connect(self.update_table)
            
            self.sender_thread.start()
            self.receiver_thread.start()
            
            self.start_stop_button.setText("Stop Simulation")
            self.replay_button.setEnabled(True)
            logging.info("Simulation started")

    def trigger_replay_attack(self):
        """Trigger the replay attack when the button is clicked."""
        if self.sender_thread and hasattr(self.sender_thread, 'last_sent_freshness'):
            # Replay the last sent message for each ID
            for msg_id, freshness in self.sender_thread.last_sent_freshness.items():
                # Create a fake message with the same freshness and MAC
                data_length = random.randint(1, 8)
                message_data = ''.join([f"{random.randint(0, 255):02X}" for _ in range(data_length)])
                mac = generate_mac(message_data, freshness, SECRET_KEY)
                
                can_message = f"{msg_id:03X}#{message_data}#{freshness}#{mac}"
                can_bus.append(can_message)
                
                logging.warning(f"Replay attack triggered for message ID {msg_id:03X}")
            
            self.replay_attack_triggered = True

    def clear_simulation(self):
        """Clear the simulation window for easier analysis
        self.tableWidget.clearContents()"""
        self.tableWidget.setRowCount(0)

    def update_table(self, message_parts, is_replay_attack, message_type):
        """Update a table widget with message details including timestamp, message content, ID, DLC, freshness value, MAC, and message type, highlighting rows in red if a replay attack is detected."""
        row_position = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row_position)
        
        for col, part in enumerate(message_parts):
            item = QTableWidgetItem(part)
            self.tableWidget.setItem(row_position, col, item)
        
        # Highlight replay attacks in red
        if is_replay_attack:
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row_position, col)
                if item:
                    item.setBackground(QColor(255, 200, 200))  # Light red
        
        # Auto-scroll to the bottom
        self.tableWidget.scrollToBottom()

    def closeEvent(self, event):
        """Handle closing of the application."""
        stop_event.set()
        
        if self.sender_thread and self.sender_thread.isRunning():
            self.sender_thread.wait()
        if self.receiver_thread and self.receiver_thread.isRunning():
            self.receiver_thread.wait()
        
        event.accept()

def main():
    """Main function to run the SecOC simulation application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()