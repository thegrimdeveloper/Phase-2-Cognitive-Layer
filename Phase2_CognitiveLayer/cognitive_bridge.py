import os
import json
import time

# Paths
LOG_PATH = "../Phase1_SystemLaws/Logs/system_log.txt"
CONTEXT_PATH = "context_map.json"


def load_context():
    """Load the context map if valid JSON, or reset it cleanly."""
    try:
        if not os.path.exists(CONTEXT_PATH):
            print("[COGNITIVE_BRIDGE] No context map found — initializing new context.")
            return {}

        with open(CONTEXT_PATH, "r", encoding="utf-8", errors="ignore") as f:
            data = f.read().strip()
            if not data:
                print("[COGNITIVE_BRIDGE] Context map empty — starting fresh.")
                return {}

            obj = json.loads(data)
            if isinstance(obj, list):
                print("[COGNITIVE_BRIDGE] Invalid context format (list). Resetting to dict.")
                return {}
            if not isinstance(obj, dict):
                print("[COGNITIVE_BRIDGE] Unexpected context structure. Resetting.")
                return {}

            return obj
    except Exception as e:
        print(f"[COGNITIVE_BRIDGE] Failed to load context: {e}")
        return {}


def save_context(context):
    """Persist context to disk safely."""
    try:
        with open(CONTEXT_PATH, "w", encoding="utf-8") as f:
            json.dump(context, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[COGNITIVE_BRIDGE] Error saving context: {e}")


def monitor_logs(context):
    """Continuously listen to log file and react to system events."""
    if not os.path.exists(LOG_PATH):
        print("[COGNITIVE_BRIDGE] Log file not found.")
        return

    print("[COGNITIVE_BRIDGE] Active – Listening for new log events...")

    with open(LOG_PATH, "r", encoding="utf-8", errors="ignore") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue

            line = line.strip()
            if not line:
                continue

            if "ALERT" in line:
                print("[COGNITIVE_BRIDGE] ALERT detected – Analyzing context...")
                details = context.get("details", "No contextual data.")
                print(f"    Context summary: {details}")
                context["last_event"] = "ALERT"
                context["last_message"] = line

            elif "RECOVERY" in line:
                print("[COGNITIVE_BRIDGE] RECOVERY detected – Confirming resilience.")
                context["last_event"] = "RECOVERY"
                context["last_message"] = line

            elif "INTEGRITY" in line:
                print("[COGNITIVE_BRIDGE] INTEGRITY verified – System baseline stable.")
                context["last_event"] = "INTEGRITY"
                context["last_message"] = line

            save_context(context)


if __name__ == "__main__":
    context = load_context()
    monitor_logs(context)
