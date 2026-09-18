import redis

redis_client = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

tasks_db = [
   {"id": 1, "title": "Task 1", "description": "First task"},
   {"id": 2, "title": "Task 2", "description": "Second task"},
]


from fastapi import FastAPI, BackgroundTasks
import json

from app.models import Task
from app.tasks import send_notification

app = FastAPI()

CACHE_KEY = "tasks_cache"

@app.get("/tasks")
def get_tasks():
    cached_tasks = redis_client.get(CACHE_KEY)
    if cached_tasks:
        result = {
        "data":json.loads(cached_tasks),
        "cached_result":True
        }
        # Если данные есть в кеше, возвращаем их
        return result

    # Если нет в кеше — используем "базу"
    redis_client.set(CACHE_KEY, json.dumps(tasks_db), ex=60)  # ex=60 — TTL 60 секунд
    result = {
    "data":tasks_db,
    "cached_result":False
    }
    return result
  

@app.post("/tasks")
def create_task(task: Task, background_tasks: BackgroundTasks):
    tasks_db.append(task.dict())

    # Очистка кеша, чтобы новые данные не терялись
    redis_client.delete(CACHE_KEY)

    # Регистрируем фоновую задачу
    background_tasks.add_task(send_notification, task.id, task.title)

    return {"message": "Task created", "task": task}