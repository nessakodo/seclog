from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import re
import json
import os
# import pyfiglet
# import random 



# Load suspicious patterns
with open('backend/rules.json', 'r') as f:
    rules = json.load(f)

# Ensure detected_events.json exists
if not os.path.exists('backend/detected_events.json'):
    with open('backend/detected_events.json', 'w') as f:
        json.dump([], f)

class LogHandler(FileSystemEventHandler):
    def __init__(self):
        self.file_positions = {}

    def on_modified(self, event):
        if event.is_directory:
            return

        if event.src_path not in self.file_positions:
            self.file_positions[event.src_path] = 0

        try:
            with open(event.src_path, 'r') as file:
                file.seek(self.file_positions[event.src_path])
                new_lines = file.readlines()
                self.file_positions[event.src_path] = file.tell()

                for line in new_lines:
                    for pattern in rules["patterns"]:
                        if re.search(pattern, line, re.IGNORECASE):
                            self.alert(event.src_path, line.strip())
        except Exception as e:
            print(f"[ERROR] Failed to process file: {event.src_path} Reason: {e}")

    def alert(self, filepath, content):
        print(f"\033[91m[ALERT]\033[0m File: {filepath} | {content}")
        self.save_event(filepath, content)

    def save_event(self, filepath, content):
        try:
            with open('backend/detected_events.json', 'r+') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
                event = {
                    "filepath": filepath,
                    "content": content,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                data.append(event)
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
        except Exception as e:
            print(f"[ERROR] Failed to save event: {e}")


    def save_event(self, filepath, content):
        with open('backend/detected_events.json', 'r+') as f:
            data = json.load(f)
            event = {
                "filepath": filepath,
                "content": content,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            data.append(event)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

if __name__ == "__main__":
    path = "backend/logs"  # Folder to monitor
    event_handler = LogHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
        
    print("\033[32m" + """
    ███████╗███████╗ ██████╗██╗      ██████╗  ██████╗ 
    ██╔════╝██╔════╝██╔════╝██║     ██╔═══██╗██╔════╝ 
    ███████╗█████╗  ██║     ██║     ██║   ██║██║  ███╗
    ╚════██║██╔══╝  ██║     ██║     ██║   ██║██║   ██║
    ███████║███████╗╚██████╗███████╗╚██████╔╝╚██████╔╝
    ╚══════╝╚══════╝ ╚═════╝╚══════╝ ╚═════╝  ╚═════╝ 
    
    SecLog Watch - Monitoring Active

    """ + "\033[0m")
    # banner = pyfiglet.figlet_format("SECLOG", font="slant")
    # print(f"\033[36m{banner}\033[0m")  # purple-pink neon glow

    # print("SecLog Watch - Monitoring Active\n")
    print(f"Monitoring {path} for suspicious activity... Press CTRL+C to stop.")

    observer.start()
    # print(f"Monitoring {path} for suspicious activity... Press CTRL+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
