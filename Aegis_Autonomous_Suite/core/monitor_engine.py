import os
import json
import stat
import platform
import hashlib

if platform.system() == "Windows":
    import winsound

class MonitorEngine:
    def __init__(self):
        self.core_dir = os.path.dirname(os.path.abspath(__file__))
        self.root_dir = os.path.dirname(self.core_dir)
        self.rules_path = os.path.join(self.core_dir, "forensic_rules.json")
        self.data_dir = os.path.join(self.root_dir, "data")
        self.attempts_tracker = {"healthcare.txt": 0, "inventory.txt": 0, "legal.txt": 0}
        self.last_seen_hashes = {"healthcare.txt": None, "inventory.txt": None, "legal.txt": None}

        with open(self.rules_path, 'r') as f:
            self.rules = json.load(f)

    def get_file_hash(self, file_path):
        """Generates a fingerprint of the file to detect NEW changes."""
        try:
            with open(file_path, "rb") as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None

    def play_alarm(self, duration):
        if platform.system() == "Windows":
            winsound.Beep(2000, duration) 

    def lock_file_on_disk(self, file_path):
        try:
            os.chmod(file_path, stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH)
        except:
            pass

    def check_integrity(self, filename):
        file_path = os.path.join(self.data_dir, filename)
        rule = self.rules.get(filename)
        
        if not os.path.exists(file_path): return {"status": "SECURE"}

        current_hash = self.get_file_hash(file_path)
        
        current_data = {}
        with open(file_path, 'r') as f:
            for line in f:
                if ":" in line:
                    k, v = line.split(":", 1)
                    current_data[k.strip()] = v.strip()

        tampered = False
        for field, expected in rule['baseline'].items():
            if str(current_data.get(field)).strip() != str(expected).strip():
                tampered = True
                break

        if tampered:
           
            if current_hash != self.last_seen_hashes[filename]:
                self.last_seen_hashes[filename] = current_hash
                self.attempts_tracker[filename] += 1
                
                if self.attempts_tracker[filename] >= rule['max_attempts']:
                    self.play_alarm(1500)
                    self.lock_file_on_disk(file_path)
                    return {"status": "LOCKED", "attempts": self.attempts_tracker[filename]}
                
                self.play_alarm(200)
                return {"status": "WARNING", "attempts": self.attempts_tracker[filename]}
            else:
                return {"status": "STALE"} 
        
        
        self.last_seen_hashes[filename] = current_hash
        return {"status": "SECURE"}
