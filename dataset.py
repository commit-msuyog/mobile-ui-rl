import json
from pathlib import Path


DATA_PATH = Path(__file__).parent.parent / "data" / "tasks.json"


def load_tasks(split):
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        tasks = json.load(file)

    return tasks[split]