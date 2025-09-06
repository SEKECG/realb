import json
import os
import re
import threading
import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk

import customtkinter as ctk
import pyperclip
from cryptography.fernet import Fernet, InvalidToken

# Constants
PACKAGE_FOLDER = os.path.dirname(os.path.abspath(__file__))
KEY_FILE = os.path.join(PACKAGE_FOLDER, "key.key")
SAVE_FILE = os.path.join(PACKAGE_FOLDER, "clips.json")
SETTINGS_FILE = os.path.join(PACKAGE_FOLDER, "settings.json")

# Global variables
cryptKey = None
clipsObj = []
lastClip = ""
autosave = False
darkmode = False
selected_color = "blue"
selected_type_filter = "All"

def generate_key():
    global cryptKey
    cryptKey = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(cryptKey)

def load_key():
    global cryptKey
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as key_file:
            cryptKey = key_file.read()
    else:
        generate_key()

def encrypt_clip(clip):
    fernet = Fernet(cryptKey)
    encrypted_clip = fernet.encrypt(clip.encode())
    return encrypted_clip.decode()

def decrypt_clip(encrypted_clip):
    fernet = Fernet(cryptKey)
    decrypted_clip = fernet.decrypt(encrypted_clip.encode())
    return decrypted_clip.decode()

def determine_content_type(current_clip):
    url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\.-]*\??[/\w\.-=&]*'
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    ipv6_pattern = r'([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}'
    credit_card_pattern = r'\b(?:\d{4}[- ]?){3}\d{4}\b'
    
    if re.match(url_pattern, current_clip):
        return "URL"
    elif re.match(email_pattern, current_clip):
        return "Email"
    elif re.match(ipv4_pattern, current_clip):
        return "IPv4"
    elif re.match(ipv6_pattern, current_clip):
        return "IPv6"
    elif re.match(credit_card_pattern, current_clip):
        return "Credit Card"
    else:
        return "Text"

def load_clips():
    global clipsObj
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as file:
                encrypted_clips = json.load(file)
                clipsObj = []
                for clip in encrypted_clips:
                    try:
                        decrypted_content = decrypt_clip(clip["content"])
                        clipsObj.append({
                            "date": clip["date"],
                            "content": decrypted_content,
                            "type": clip["type"]
                        })
                    except InvalidToken:
                        continue
        except (json.JSONDecodeError, FileNotFoundError):
            clipsObj = []
    else:
        clipsObj = []

def save_clips():
    encrypted_clips = []
    for clip in clipsObj:
        encrypted_content = encrypt_clip(clip["content"])
        encrypted_clips.append({
            "date": clip["date"],
            "content": encrypted_content,
            "type": clip["type"]
        })
    with open(SAVE_FILE, "w") as file:
        json.dump(encrypted_clips, file)

def load_settings():
    global autosave, darkmode, selected_color
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as file:
                settings = json.load(file)
                autosave = settings.get("autosave", False)
                darkmode = settings.get("darkmode", False)
                selected_color = settings.get("color", "blue")
        except (json.JSONDecodeError, FileNotFoundError):
            autosave = False
            darkmode = False
            selected_color = "blue"

def save_settings():
    settings = {
        "autosave": autosave,
        "darkmode": darkmode,
        "color": selected_color
    }
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file)

def monitor_clipboard():
    global lastClip
    while True:
        try:
            current_clip = pyperclip.paste()
            if current_clip != lastClip and current_clip.strip():
                lastClip = current_clip
                if autosave:
                    save_clip()
            time.sleep(1)
        except Exception:
            time.sleep(1)

def save_clip():
    current_clip = pyperclip.paste()
    if current_clip.strip():
        content_type = determine_content_type(current_clip)
        clipsObj.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "content": current_clip,
            "type": content_type
        })
        save_clips()

def delete_clip_from_ui(index):
    if 0 <= index < len(clipsObj):
        clipsObj.pop(index)
        save_clips()

def delete_all_clips():
    global clipsObj
    clipsObj = []
    save_clips()

def delete_key():
    if messagebox.askyesno("Confirm", "This will delete all saved clips and require a restart. Continue?"):
        global cryptKey, clipsObj
        cryptKey = None
        clipsObj = []
        if os.path.exists(KEY_FILE):
            os.remove(KEY_FILE)
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
        messagebox.showinfo("Info", "Encryption key deleted. Please restart the application.")

def toggle_autosave():
    global autosave
    autosave = not autosave
    save_settings()

def toggle_darkmode():
    global darkmode
    darkmode = not darkmode
    save_settings()

def apply_color(choice):
    global selected_color
    selected_color = choice
    save_settings()
    messagebox.showinfo("Info", "Color theme will be applied after restart.")

def apply_filter(choice):
    global selected_type_filter
    selected_type_filter = choice

def search_clips(event=None):
    pass

def populate_clips_table(frame, clips_to_display):
    for widget in frame.winfo_children():
        widget.destroy()
    
    if not clips_to_display:
        label = ctk.CTkLabel(frame, text="No clips found")
        label.pack(pady=20)
        return
    
    for i, clip in enumerate(clips_to_display):
        clip_frame = ctk.CTkFrame(frame)
        clip_frame.pack(fill="x", padx=5, pady=2)
        
        date_label = ctk.CTkLabel(clip_frame, text=clip["date"], width=150)
        date_label.pack(side="left", padx=5)
        
        type_label = ctk.CTkLabel(clip_frame, text=clip["type"], width=80)
        type_label.pack(side="left", padx=5)
        
        content_preview = clip["content"][:50] + "..." if len(clip["content"]) > 50 else clip["content"]
        content_label = ctk.CTkLabel(clip_frame, text=content_preview, width=200)
        content_label.pack(side="left", padx=5, expand=True, fill="x")
        
        copy_btn = ctk.CTkButton(clip_frame, text="Copy", width=60, command=lambda c=clip["content"]: pyperclip.copy(c))
        copy_btn.pack(side="right", padx=2)
        
        delete_btn = ctk.CTkButton(clip_frame, text="Delete", width=60, command=lambda idx=i: delete_clip_from_ui(idx))
        delete_btn.pack(side="right", padx=2)

def refresh_ui(component):
    ctk.set_appearance_mode("dark" if darkmode else "light")
    ctk.set_default_color_theme(selected_color)

def settings_UI():
    settings_window = ctk.CTkToplevel()
    settings_window.title("Settings")
    settings_window.geometry("400x300")
    
    tabview = ctk.CTkTabview(settings_window)
    tabview.pack(fill="both", expand=True, padx=10, pady=10)
    
    appearance_tab = tabview.add("Appearance")
    danger_tab = tabview.add("Danger Zone")
    
    # Appearance tab
    darkmode_var = ctk.BooleanVar(value=darkmode)
    darkmode_switch = ctk.CTkSwitch(appearance_tab, text="Dark Mode", variable=darkmode_var, command=toggle_darkmode)
    darkmode_switch.pack(pady=10)
    
    color_label = ctk.CTkLabel(appearance_tab, text="Color Theme:")
    color_label.pack(pady=5)
    
    color_options = ["blue", "green", "dark-blue"]
    color_dropdown = ctk.CTkOptionMenu(appearance_tab, values=color_options, command=apply_color)
    color_dropdown.set(selected_color)
    color_dropdown.pack(pady=5)
    
    # Danger tab
    delete_key_btn = ctk.CTkButton(danger_tab, text="Reset Encryption Key", command=delete_key, fg_color="red", hover_color="darkred")
    delete_key_btn.pack(pady=20)
    
    delete_all_btn = ctk.CTkButton(danger_tab, text="Delete All Clips", command=delete_all_clips, fg_color="orange", hover_color="darkorange")
    delete_all_btn.pack(pady=10)

def UI():
    global autosave, darkmode, selected_color
    
    root = ctk.CTk()
    root.title("Clipboardy")
    root.geometry("800x600")
    
    refresh_ui(root)
    
    # Header frame
    header_frame = ctk.CTkFrame(root)
    header_frame.pack(fill="x", padx=10, pady=10)
    
    title_label = ctk.CTkLabel(header_frame, text="Clipboardy", font=ctk.CTkFont(size=20, weight="bold"))
    title_label.pack(side="left", padx=10)
    
    settings_btn = ctk.CTkButton(header_frame, text="Settings", command=settings_UI)
    settings_btn.pack(side="right", padx=10)
    
    # Search and filter frame
    search_frame = ctk.CTkFrame(root)
    search_frame.pack(fill="x", padx=10, pady=5)
    
    search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search clips...")
    search_entry.pack(side="left", padx=5, pady=5, fill="x", expand=True)
    search_entry.bind("<KeyRelease>", search_clips)
    
    filter_options = ["All", "URL", "Email", "IPv4", "IPv6", "Credit Card", "Text"]
    filter_dropdown = ctk.CTkOptionMenu(search_frame, values=filter_options, command=apply_filter)
    filter_dropdown.set("All")
    filter_dropdown.pack(side="right", padx=5, pady=5)
    
    # Controls frame
    controls_frame = ctk.CTkFrame(root)
    controls_frame.pack(fill="x", padx=10, pady=5)
    
    save_btn = ctk.CTkButton(controls_frame, text="Save Current Clip", command=save_clip)
    save_btn.pack(side="left", padx=5)
    
    autosave_var = ctk.BooleanVar(value=autosave)
    autosave_switch = ctk.CTkSwitch(controls_frame, text="Auto Save", variable=autosave_var, command=toggle_autosave)
    autosave_switch.pack(side="left", padx=20)
    
    # Clips table frame
    table_frame = ctk.CTkFrame(root)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Table headers
    headers_frame = ctk.CTkFrame(table_frame)
    headers_frame.pack(fill="x")
    
    date_header = ctk.CTkLabel(headers_frame, text="Date", width=150, font=ctk.CTkFont(weight="bold"))
    date_header.pack(side="left", padx=5)
    
    type_header = ctk.CTkLabel(headers_frame, text="Type", width=80, font=ctk.CTkFont(weight="bold"))
    type_header.pack(side="left", padx=5)
    
    content_header = ctk.CTkLabel(headers_frame, text="Content", width=200, font=ctk.CTkFont(weight="bold"))
    content_header.pack(side="left", padx=5, expand=True, fill="x")
    
    actions_header = ctk.CTkLabel(headers_frame, text="Actions", width=130, font=ctk.CTkFont(weight="bold"))
    actions_header.pack(side="right", padx=5)
    
    # Scrollable clips area
    scrollable_frame = ctk.CTkScrollableFrame(table_frame)
    scrollable_frame.pack(fill="both", expand=True)
    
    # Initial population
    filtered_clips = [clip for clip in clipsObj if selected_type_filter == "All" or clip["type"] == selected_type_filter]
    populate_clips_table(scrollable_frame, filtered_clips)
    
    root.mainloop()

def main():
    load_key()
    load_clips()
    load_settings()
    
    # Start clipboard monitoring in a separate thread
    monitor_thread = threading.Thread(target=monitor_clipboard, daemon=True)
    monitor_thread.start()
    
    UI()

if __name__ == "__main__":
    main()