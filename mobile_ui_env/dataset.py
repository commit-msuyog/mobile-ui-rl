import json
from pathlib import Path


# Keep the dataset path relative to the project.
DATA_PATH = Path(__file__).parent.parent / "data" / "tasks.json"


def load_tasks(split):
    # Load either the train or eval tasks. (load_tasks(train) or load_taks(eval))
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        tasks = json.load(file)

    return tasks[split]