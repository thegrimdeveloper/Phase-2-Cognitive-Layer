import time
import os

LOG_PATH = "../Phase1_SystemLaws/Logs/system_log.txt"
BRIDGE_PATH = "context_map.json"

def tail_log():
    with open(LOG_PATH, "r", encoding="utf-8", errors="ignore") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            process_line(line)

def process_line(line):
    if "ALERT" in line:
        print("[BRIDGE] Alert detected, updating context map.")
        update_context("alert", line)
    elif "ERROR" in line:
        print("[BRIDGE] Error detected, flagging anomaly.")
        update_context("error", line)
    elif "RECOVERY" in line:
        print("[BRIDGE] Recovery event logged.")
        update_context("recovery", line)

def update_context(event_type, details):
    import json
    data = {"timestamp": time.time(), "event_type": event_type, "details": details.strip()}
    with open(BRIDGE_PATH, "a", encoding="utf-8") as out:
        json.dump(data, out)
        out.write("\n")

if __name__ == "__main__":
    print("[BRIDGE] Active — monitoring system_log.txt for updates...")
    tail_log()
