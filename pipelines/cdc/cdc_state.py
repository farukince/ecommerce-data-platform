import json
from datetime import datetime
from pathlib import Path

STATE_PATH = Path("data_lake/raw/cdc_state/state.json")


def get_default_state() -> dict:
    return {
        "last_run_at": "1970-01-01T00:00:00",
    }


def load_state() -> dict:
    if not STATE_PATH.exists():
        return get_default_state()

    with STATE_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_state(last_run_at: datetime) -> Path:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)

    state = {
        "last_run_at": last_run_at.isoformat(),
    }

    with STATE_PATH.open("w", encoding="utf-8") as file:
        json.dump(state, file, ensure_ascii=False, indent=2)

    return STATE_PATH
