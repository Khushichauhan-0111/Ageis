import customtkinter as ctk
import os
import sys
import threading
import time
from datetime import datetime
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)

from core.monitor_engine import MonitorEngine

class AegisAutoMonitor(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AEGIS v2.0 | AUTONOMOUS IPS")
        self.geometry("1000x650")
        ctk.set_appearance_mode("dark")
        
        self.engine = MonitorEngine()
        self.is_locked = False 
        self.monitoring = True

        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#0A0A0A")
        self.sidebar.place(x=0, y=0, relheight=1)
        
        self.logo = ctk.CTkLabel(self.sidebar, text="AEGIS AUTO", font=("Courier", 24, "bold"), text_color="#00FF00")
        self.logo.pack(pady=40, padx=20)

        self.status_label = ctk.CTkLabel(self, text="STATUS: PROTECTED", text_color="#00FF00", font=("Courier", 22, "bold"))
        self.status_label.place(x=250, y=20)
        self.log = ctk.CTkTextbox(self, 
                                  width=720, 
                                  height=550, 
                                  font=("Consolas", 13), 
                                  border_width=2, 
                                  fg_color="#050505")
        self.log.place(x=250, y=70)
        self.log._textbox.tag_config("tamper", foreground="#FF4444") 
        self.log._textbox.tag_config("secure", foreground="#00FF00")

        self.log_msg("[*] HIDS Watchdog Thread Initialized.")
        self.log_msg("[*] Detection Mode: Real-Time Event-Driven.")

        self.watch_thread = threading.Thread(target=self.run_watchdog, daemon=True)
        self.watch_thread.start()

    def log_msg(self, message, tag=None):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log.insert("end", f"[{ts}] {message}\n", tag)
        self.log.see("end")

    def force_popup(self):
        """Forces window to the top if hidden or minimized."""
        self.attributes("-topmost", True)
        self.deiconify() 
        self.focus_force()

        self.after(2000, lambda: self.attributes("-topmost", False))

    def handle_breach_ui(self, filename, result):
        """Auto-popup and update UI on breach."""
        self.force_popup()
        
        if result["status"] == "LOCKED":
            self.is_locked = True
            self.status_label.configure(text="!!! CRITICAL BREACH: LOCKDOWN !!!", text_color="red")
            self.log_msg(f"FATAL: {filename.upper()} TAMPERED. THRESHOLD EXCEEDED.", "tamper")
            self.log_msg("OS-LEVEL FILE LOCKING ENGAGED. SYSTEM SHUTDOWN.", "tamper")
            self.log.configure(state="disabled")
        else:
            self.log_msg(f"BREACH ALERT: {filename} modified! Attempt: {result['attempts']}", "tamper")
            self.status_label.configure(text="STATUS: UNDER ATTACK", text_color="orange")

    def run_watchdog(self):
        """The Background Eye."""
        targets = ["healthcare.txt", "inventory.txt", "legal.txt"]
        
        while self.monitoring:
            if not self.is_locked:
                for filename in targets:
                    res = self.engine.check_integrity(filename)
                    
                    if res["status"] in ["LOCKED", "WARNING"]:
                        self.after(0, self.handle_breach_ui, filename, res)
                    
                    elif res["status"] == "SECURE":
                        pass
            
            time.sleep(2) 

if __name__ == "__main__":
    app = AegisAutoMonitor()
    app.mainloop()
