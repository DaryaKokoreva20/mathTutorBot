import json
import os
import pandas as pd

DATA_FILE = "users.json"

FILES = {
    "schedule": "schedule.xlsx",
    "past_lessons": "past_lessons.xlsx",
    "students": "students.xlsx",
    "parents": "parents.xlsx",
    "homework": "homework.xlsx",
}

TABLE_STRUCTURE = {
    "schedule": ["id", "telegram_id", "name", "day_of_week", "start_time", "duration"],
    "past_lessons": ["id", "telegram_id", "name", "day_of_week", "start_time", "duration", "date", "status"],
    "students": ["telegram_id", "first_name", "last_name", "role", "hourly_rate", "parent_id"],
    "parents": ["telegram_id", "full_name", "child_name", "phone_number"],
    "homework": ["id", "date", "student_name", "status"],
}

def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    else:
        return {"tutor_id": None, "students": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_table(name):
    path = FILES[name]
    if os.path.exists(path):
        return pd.read_excel(path)
    else:
        df = pd.DataFrame(columns=TABLE_STRUCTURE[name])
        df.to_excel(path, index=False)
        return df

def save_table(name, df):
    df.to_excel(FILES[name], index=False)
