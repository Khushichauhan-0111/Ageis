import os
import json
import stat
import platform

if platform.system() == "Windows":
    import winsound

class MonitorEngine:
    def __init__(self):
        self.core_dir = os.path.dirname(os.path.abspath(__file__))
        self.root_dir = os.path.dirname(self.core_dir)
        self.rules_path = os.path.join(self.core_dir, "forensic_rules.json")
        self.data_dir = os.path.join(self.root_dir, "data")
        self.attempts_tracker = {"healthcare.txt": 0, "inventory.txt": 0, "legal.txt": 0}

        with open(self.rules_path, 'r') as f:
            self.rules = json.load(f)

    def play_sound(self, duration):
        if platform.system() == "Windows":
            winsound.Beep(2000, duration) 
        else:
            print('\a')

    def lock_file_on_disk(self, file_path):
        try:
            os.chmod(file_path, stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH)
        except Exception as e:
            print(f"Lock Error: {e}")

    def check_integrity(self, filename):
        file_path = os.path.join(self.data_dir, filename)
        rule = self.rules.get(filename)
        
        current_data = {}
        with open(file_path, 'r') as f:
            for line in f:
                if ":" in line:
                    k, v = line.split(":", 1)
                    current_data[k.strip()] = v.strip()

        tampered_fields = []
        for field, expected in rule['baseline'].items():
            actual = current_data.get(field)
            if str(actual).strip() != str(expected).strip():
                tampered_fields.append(field)

        if tampered_fields:
            self.attempts_tracker[filename] += 1
            
            if self.attempts_tracker[filename] >= rule['max_attempts']:
                self.play_sound(1500)
                self.lock_file_on_disk(file_path)
                return {"status": "LOCKED", "attempts": self.attempts_tracker[filename]}
            
            self.play_sound(200) 
            return {"status": "WARNING", "attempts": self.attempts_tracker[filename]}
        
        return {"status": "SECURE"}
