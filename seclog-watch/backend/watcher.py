from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import re
import json
import os

# Load suspicious patterns
with open('backend/rules.json', 'r') as f:
    rules = json.load(f)

# Ensure detected_events.json exists
if not os.path.exists('backend/detected_events.json'):
    with open('backend/detected_events.json', 'w') as f:
        json.dump([], f)

class LogHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return

        with open(event.src_path, 'r') as file:
            lines = file.readlines()
            for line in lines[-10:]:  # Only scan last few lines
                for pattern in rules["patterns"]:
                    if re.search(pattern, line, re.IGNORECASE):
                        print(f"[ALERT] Suspicious log entry detected: {line.strip()}")
                        self.save_event(event.src_path, line.strip())

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
    observer.start()
    print(f"Monitoring {path} for suspicious activity... Press CTRL+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
