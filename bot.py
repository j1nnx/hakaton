import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

    # Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Настройки для бота
BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
API_URL = "http://localhost:8000"  # URL FastAPI

    # Команда /start — регистрация пользователя в очереди
def start(update: Update, context: CallbackContext):
        user = update.effective_user
        user_id = user.id
        username = user.username

        # Отправляем запрос к FastAPI для добавления пользователя в очередь
        response = requests.post(f"{API_URL}/add_to_queue/", json={"user_id": user_id, "username": username})

        if response.status_code == 200:
            update.message.reply_text(response.json()["message"])
        else:
            update.message.reply_text("Something went wrong!")

    # Команда /status — проверка текущего статуса в очереди
def status(update: Update, context: CallbackContext):
        user = update.effective_user
        user_id = user.id

        # Отправляем запрос к FastAPI для получения позиции пользователя в очереди
        response = requests.get(f"{API_URL}/position/{user_id}")

        if response.status_code == 200:
            data = response.json()
            update.message.reply_text(f"Your position in the queue is: {data['position']}")
        else:
            update.message.reply_text("You are not in the queue.")

    # Команда /next — продвижение по очереди (удаляет первого пользователя)
def next(update: Update, context: CallbackContext):
        # Отправляем запрос к FastAPI для удаления первого пользователя из очереди
        response = requests.delete(f"{API_URL}/next/")

        if response.status_code == 200:
            update.message.reply_text(response.json()["message"])
        else:
            update.message.reply_text("Queue is empty or something went wrong!")

    # Основной блок для запуска бота
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

        # Обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("status", status))
    dispatcher.add_handler(CommandHandler("next", next))

        # Запуск бота
    updater.start_polling()
    updater.idle()

    if __name__ == '__main__':
        main()
