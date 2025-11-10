import json
import time

CONTEXT_MAP = "context_map.json"

def load_context():
    context = []
    try:
        with open(CONTEXT_MAP, "r", encoding="utf-8") as f:
            for line in f:
                context.append(json.loads(line))
    except FileNotFoundError:
        print("[INTERPRETER] No context file found, starting fresh.")
    return context

def interpret(event):
    event_type = event["event_type"]
    details = event["details"]
    if event_type == "alert":
        print(f"[INTERPRETER] ALERT — Investigating abnormal condition: {details}")
    elif event_type == "error":
        print(f"[INTERPRETER] ERROR — Flagging system instability: {details}")
    elif event_type == "recovery":
        print(f"[INTERPRETER] RECOVERY — System resilience confirmed: {details}")
    else:
        print(f"[INTERPRETER] Unrecognized event type: {event_type}")

def run_interpreter():
    print("[INTERPRETER] Active — Reading context map for cognitive analysis...")
    known = set()
    while True:
        context = load_context()
        for event in context:
            key = (event["timestamp"], event["event_type"])
            if key not in known:
                known.add(key)
                interpret(event)
        time.sleep(3)

if __name__ == "__main__":
    run_interpreter()
