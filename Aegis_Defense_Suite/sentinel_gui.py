import customtkinter as ctk
import os
import sys
from datetime import datetime

# Path Bootstrapping
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)

from core.monitor_engine import MonitorEngine

class SentinelGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Config
        self.title("AEGIS SENTINEL v2.6 | DEFENSE TRACK")
        self.geometry("1100x650")
        ctk.set_appearance_mode("dark")
        
        self.engine = MonitorEngine()
        self.is_locked = False 

        # Layout Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar Layout ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#0D0D0D")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="AEGIS COMMAND", 
                                 font=ctk.CTkFont(family="Courier", size=22, weight="bold"))
        self.logo.pack(pady=40, padx=20)

        self.scan_btn = ctk.CTkButton(self.sidebar, text="INITIATE SCAN", 
                                      command=self.run_scan, 
                                      fg_color="#1f538d", hover_color="#14375e",
                                      font=ctk.CTkFont(weight="bold"))
        self.scan_btn.pack(pady=10, padx=20)

        self.clear_btn = ctk.CTkButton(self.sidebar, text="CLEAR CONSOLE", 
                                       command=lambda: self.log.delete("1.0", "end"),
                                       fg_color="transparent", border_width=1)
        self.clear_btn.pack(pady=10, padx=20)

        self.exit_btn = ctk.CTkButton(self.sidebar, text="EXIT SYSTEM", fg_color="#5e1914", command=self.quit)
        self.exit_btn.pack(side="bottom", pady=20)

        # --- Main Console Layout ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.status_label = ctk.CTkLabel(self.main_frame, text="SYSTEM STATUS: NOMINAL", 
                                         text_color="#00FF00", 
                                         font=ctk.CTkFont(family="Courier", size=20, weight="bold"))
        self.status_label.pack(pady=(0, 10))

        self.log = ctk.CTkTextbox(self.main_frame, font=("Consolas", 13), 
                                  border_width=2, border_color="#333333",
                                  fg_color="#050505", text_color="#FFFFFF")
        self.log.pack(fill="both", expand=True, padx=10, pady=10)

        # Color Tag Config (Internal Text Widget)
        self.log._textbox.tag_config("tamper", foreground="#FF4444") 
        self.log._textbox.tag_config("secure", foreground="#00FF00")

        self.log_msg("[*] Sentinel Kernel v2.6 Ready.")
        self.log_msg("[*] Active Defense Protocols: ARMED.\n")

    def log_msg(self, message, tag=None):
        timestamp = datetime.now().strftime("%H:%M:%S")
        if tag:
            self.log.insert("end", f"[{timestamp}] {message}\n", tag)
        else:
            self.log.insert("end", f"[{timestamp}] {message}\n")
        self.log.see("end")

    def trigger_ui_lockdown(self):
        self.is_locked = True
        self.status_label.configure(text="!!! TERMINAL LOCKED: SECURITY BREACH !!!", text_color="#FF4444")
        self.scan_btn.configure(state="disabled", fg_color="#333333")
        
        self.log.insert("end", "\n" + "="*60 + "\n", "tamper")
        self.log.insert("end", " SECURITY VIOLATION: NODE EXHAUSTION.\n", "tamper")
        self.log.insert("end", " PHYSICAL FILE LOCKS APPLIED. INTERFACE SHUTDOWN.\n", "tamper")
        self.log.insert("end", "="*60 + "\n", "tamper")
        self.log.configure(state="disabled")

    def run_scan(self):
        if self.is_locked: return
        self.log_msg("--- STARTING INTEGRITY SCAN ---")
        
        targets = ["healthcare.txt", "inventory.txt", "legal.txt"]
        any_tamper = False

        for filename in targets:
            result = self.engine.check_integrity(filename)
            
            if result["status"] == "LOCKED":
                self.log_msg(f"[CRITICAL] {filename.upper()} COMPROMISED. LIMIT EXCEEDED!", "tamper")
                self.trigger_ui_lockdown()
                return 

            elif result["status"] == "WARNING":
                any_tamper = True
                self.log_msg(f"[ALERT] {filename}: Unauthorized Change (Attempt {result['attempts']})", "tamper")
                self.status_label.configure(text="SYSTEM STATUS: BREACH WARNING", text_color="orange")
            
            elif result["status"] == "SECURE":
                self.log_msg(f"[OK] {filename} Verified Secure.", "secure")

        if not any_tamper:
            self.status_label.configure(text="SYSTEM STATUS: NOMINAL", text_color="#00FF00")
        
        self.log.insert("end", "\n")

if __name__ == "__main__":
    app = SentinelGUI()
    app.mainloop()