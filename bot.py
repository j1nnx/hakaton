import logging
import requests
import telebot

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Настройки для бота
BOT_TOKEN = '7833886320:AAE1Z9OQqA-YePBJ5EH9BQ6mo4qQhleLbBo'
API_URL = "http://localhost:8000"  # URL FastAPI

bot = telebot.TeleBot(BOT_TOKEN)


# Обработчик команды /start — регистрация пользователя в очереди
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username

    logging.info(f"Добавление пользователя в очередь: {username} (ID: {user_id})")

    # Отправляем запрос к FastAPI для добавления пользователя в очередь
    try:
        # Исправленный запрос с параметрами в query строке
        response = requests.post(f"{API_URL}/add_to_queue/?user_id={user_id}&username={username}")

        logging.info(f"Ответ от FastAPI: {response.status_code} - {response.text}")

        if response.status_code == 200:
            bot.send_message(message.chat.id, response.json()["message"])
        else:
            bot.send_message(message.chat.id, "Что-то пошло не так!")
            # Дополнительная информация об ошибке
            print(f"Failed request with status code {response.status_code}")
            print(f"Response text: {response.text}")

    except Exception as e:
        logging.error(f"Ошибка при отправке запроса: {e}")
        bot.send_message(message.chat.id, "Не удалось добавить вас в очередь. Попробуйте позже.")


# Обработчик команды /status — проверка текущего статуса пользователя в очереди
@bot.message_handler(commands=['status'])
def status(message):
    user_id = message.from_user.id
    logging.info(f"Проверка статуса для пользователя с ID: {user_id}")

    # Отправляем запрос к FastAPI для получения позиции пользователя в очереди
    try:
        # Теперь передаем user_id как часть пути
        response = requests.get(f"{API_URL}/position/{user_id}")

        logging.info(f"Ответ от FastAPI: {response.status_code} - {response.text}")

        if response.status_code == 200:
            data = response.json()
            bot.send_message(message.chat.id, f"Ваша позиция в очереди: {data['position']}")
        else:
            bot.send_message(message.chat.id, "Вы не в очереди.")
            print(f"Failed request with status code {response.status_code}")
            print(f"Response text: {response.text}")

    except Exception as e:
        logging.error(f"Ошибка при отправке запроса: {e}")
        bot.send_message(message.chat.id, "Не удалось получить ваш статус. Попробуйте позже.")


@bot.message_handler(commands=['quit'])
def remove_from_queue(message):
    user_id = message.from_user.id
    logging.info(f"Удаление пользователя с ID: {user_id} из очереди")

    # Отправляем запрос к FastAPI для удаления пользователя из очереди
    try:
        # Отправляем DELETE запрос к FastAPI для удаления пользователя
        response = requests.delete(f"{API_URL}/remove_from_queue/{user_id}")

        logging.info(f"Ответ от FastAPI: {response.status_code} - {response.text}")

        if response.status_code == 200:
            data = response.json()
            bot.send_message(message.chat.id, f"Статус: {data['message']}")
        else:
            bot.send_message(message.chat.id, "Не удалось удалить пользователя из очереди.")
            print(f"Failed request with status code {response.status_code}")
            print(f"Response text: {response.text}")

    except Exception as e:
        logging.error(f"Ошибка при отправке запроса: {e}")
        bot.send_message(message.chat.id, "Не удалось удалить пользователя из очереди. Попробуйте позже.")


# Обработчик команды /next — удаление первого пользователя из очереди
@bot.message_handler(commands=['next'])
def next_user(message):
    try:
        # Отправляем запрос к FastAPI для удаления первого пользователя из очереди
        response = requests.delete(f"{API_URL}/next/")

        logging.info(f"Ответ от FastAPI: {response.status_code} - {response.text}")

        if response.status_code == 200:
            bot.send_message(message.chat.id, response.json()["message"])
        else:
            bot.send_message(message.chat.id, "Очередь пуста или что-то пошло не так!")
            print(f"Failed request with status code {response.status_code}")
            print(f"Response text: {response.text}")

    except Exception as e:
        logging.error(f"Ошибка при отправке запроса: {e}")
        bot.send_message(message.chat.id, "Не удалось удалить пользователя из очереди. Попробуйте позже.")


# Основной цикл для запуска бота
if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
