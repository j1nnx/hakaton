from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import Queue, get_db
import requests

app = FastAPI()

# Переменная для хранения заголовка
title = "Текущий заголовок не установлен."
time = 1
number_attractions = 1


# Добавление пользователя в очередь
@app.post("/add_to_queue/")
def add_to_queue(user_id: int, username: str, db: Session = Depends(get_db)):
    # Проверяем, существует ли пользователь в очереди
    existing_user = db.query(Queue).filter(Queue.user_id == user_id).first()

    if existing_user:
        return {"message": f"User {username} already in the queue with position {existing_user.position}."}

    # Определяем позицию для нового пользователя
    position = db.query(Queue).count() + 1

    # Добавляем пользователя в очередь
    new_user = Queue(user_id=user_id, username=username, position=position)
    db.add(new_user)
    db.commit()

    return {"message": f"User {username} added to the queue with position {position}."}


# Получение текущей позиции пользователя в очереди
@app.get("/position/{user_id}")
def get_position(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Queue).filter(Queue.user_id == user_id).first()

    if user:
        return {"position": user.position}
    return {"message": "User not found in queue."}


# Удаление первого пользователя из очереди и уведомление нового первого пользователя
@app.delete("/next/")
def remove_first_from_queue(db: Session = Depends(get_db)):
    global number_attractions  # Используем глобальную переменную number_attractions

    # Получаем первого пользователя в очереди
    first_in_queue = db.query(Queue).order_by(Queue.position.asc()).first()

    if first_in_queue:
        # Сохраняем данные удаляемого пользователя для логов
        removed_user_id = first_in_queue.user_id
        removed_username = first_in_queue.username

        # Удаляем первого пользователя из очереди
        db.delete(first_in_queue)
        db.commit()

        # Пересчитываем позиции для остальных пользователей
        remaining_users = db.query(Queue).filter(Queue.position > first_in_queue.position).all()
        for user in remaining_users:
            user.position -= 1
        db.commit()

        # Пытаемся найти пользователя на позиции number_attractions
        user_to_notify = db.query(Queue).filter(Queue.position == number_attractions).first()

        if user_to_notify:
            # Уведомляем пользователя на позиции number_attractions через Telegram
            send_message_to_user(user_to_notify.user_id, user_to_notify.username)

        return {
            "message": f"User {removed_username} (ID: {removed_user_id}) removed from queue. Remaining positions updated."
        }

    return {"message": "Queue is empty."}


# Удаление пользователя из очереди
@app.delete("/remove_from_queue/{user_id}")
def remove_from_queue(user_id: int, db: Session = Depends(get_db)):
    global number_attractions  # Получаем текущее значение number_attractions

    # Ищем пользователя в базе данных по его user_id
    user = db.query(Queue).filter(Queue.user_id == user_id).first()

    if user:
        user_position = user.position

        # Удаляем пользователя из очереди
        db.delete(user)
        db.commit()

        # Пересчитываем позиции для всех пользователей, которые идут после удаленного
        remaining_users = db.query(Queue).filter(Queue.position > user.position).all()
        for remaining_user in remaining_users:
            remaining_user.position -= 1
        db.commit()

        # Проверяем, если позиция удаляемого пользователя меньше или равна number_attractions
        if user_position <= number_attractions:
            # Пытаемся найти пользователя на позиции number_attractions после пересчета позиций
            user_to_notify = db.query(Queue).filter(Queue.position == number_attractions).first()

            if user_to_notify:
                # Уведомляем пользователя на позиции number_attractions через Telegram
                send_message_to_user(user_to_notify.user_id, user_to_notify.username)

        return {"message": f"Пользователь с ID {user_id} был удален из очереди."}
    else:
        # Если пользователя нет в базе
        return {"message": f"Пользователь с ID {user_id} не найден в очереди."}


# Получение всех участников очереди
@app.get("/all_queue/")
def get_all_queue(db: Session = Depends(get_db)):
    # Получаем всех пользователей, отсортированных по позиции в очереди
    users_in_queue = db.query(Queue).order_by(Queue.position.asc()).all()

    # Если очередь пуста
    if not users_in_queue:
        return {"message": "Queue is empty."}

    # Формируем список участников
    queue_list = [
        {"user_id": user.user_id, "username": user.username, "position": user.position}
        for user in users_in_queue
    ]

    return {"queue": queue_list}


# Получение текущего заголовка
@app.get("/title/")
def get_title():
    return {"title": title}


# Установка нового заголовка
@app.post("/title/")
def set_title(new_title: str):
    global title
    title = new_title
    return {"message": f"Заголовок был изменен на: {title}"}


@app.get("/time/")
def get_time():
    return {"time": time}


@app.post("/time/")
def set_time(new_time: str):
    global time
    time = new_time
    return {"message": f"Максимальное время на человека: {time}"}


@app.get("/attractions/")
def get_number_attractions():
    return {"number_attractions": number_attractions}


@app.post("/attractions/")
def set_number_attractions(attractions: str):
    global number_attractions
    number_attractions = attractions
    return {"message": f"Количество терминалов: {number_attractions}"}


# Функция для отправки уведомления через Telegram
def send_message_to_user(user_id: int, username: str):
    # Укажите токен вашего бота и создайте URL для отправки сообщения
    BOT_TOKEN = '8040546358:AAGP_zFqjFTJu65JylfiacNAQFrjHk2SSiw'  # Замените на реальный токен вашего бота
    TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    # Формируем сообщение для первого пользователя
    message_text = f"Привет, {username}! Вы теперь первый в очереди. Подходите к терминалу."

    # Данные для запроса
    payload = {
        "chat_id": user_id,  # Telegram ID пользователя
        "text": message_text
    }

    # Отправляем запрос на сервер Telegram
    try:
        response = requests.post(TELEGRAM_API_URL, json=payload)
        if response.status_code == 200:
            print(f"Сообщение отправлено пользователю {username} (ID: {user_id})")
        else:
            print(f"Ошибка при отправке сообщения: {response.text}")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")
