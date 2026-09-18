import time

def send_notification(task_id: int, task_title: str):
   # Имитируем отправку уведомления (например, пишем в файл)
   with open("notifications.log", "a") as f:
       f.write(f"Notification: Task {task_id} - {task_title} created\n")
   # Можно имитировать задержку
   time.sleep(2)