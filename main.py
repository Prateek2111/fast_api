from fastapi import FastAPI, HTTPException
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data.json"

app = FastAPI(title="Users API")

def load_data():
    if not DATA_PATH.exists():
        return []
    with DATA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.get("/")
def root():
    return {"message": "Users API"}

@app.get("/users")
def get_users():
    return load_data()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    for u in load_data():
        if u.get("id") == user_id:
            return u
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/users")
def create_user(user: dict):
    users = load_data()
    next_id = max((u.get("id", 0) for u in users), default=0) + 1
    user["id"] = next_id
    users.append(user)
    save_data(users)
    return user

@app.put("/users/{user_id}")
def update_user(user_id: int, payload: dict):
    users = load_data()
    for i, u in enumerate(users):
        if u.get("id") == user_id:
            users[i].update(payload)
            users[i]["id"] = user_id
            save_data(users)
            return users[i]
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    users = load_data()
    for i, u in enumerate(users):
        if u.get("id") == user_id:
            removed = users.pop(i)
            save_data(users)
            return {"deleted": removed}
    raise HTTPException(status_code=404, detail="User not found")
