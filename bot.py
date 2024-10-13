import logging
import requests
import telebot

# Логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Настройки для бота
BOT_TOKEN = '8040546358:AAGP_zFqjFTJu65JylfiacNAQFrjHk2SSiw'
API_URL = "http://localhost:8000"  # URL FastAPI

bot = telebot.TeleBot(BOT_TOKEN)

title = "Текущее заголовок не установлен."


# Обработчик команды /help — инструкция по использованию команд
@bot.message_handler(commands=['help'])
def help_message(message):
    help_text = """
    Список команд бота:
/join - Добавить вас в очередь.
/status - Проверить ваш текущий статус в очереди.
/quit - Удалить вас из очереди.
    """
    bot.send_message(message.chat.id, help_text)


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username

    logging.info(f"Приветствие пользователя с ID: {user_id}, Username: {username}")

    # Приветственное сообщение с информацией о пользователе
    bot.send_message(
        message.chat.id,
        f"Привет, {username}!\n\nВаш ID: {user_id}\nВы можете использовать команды: "
        f"\n/join-встать в очередь\n"
        f"/status - посмотреть место в очереди\n"
        f"/quit - выйти из очереди\n"
        f"/help - посмотреть список команд"
    )


# Обработчик команды /start — регистрация пользователя в очереди
@bot.message_handler(commands=['join'])
def join(message):
    user_id = message.from_user.id
    username = message.from_user.username

    logging.info(f"Проверка и добавление пользователя в очередь: {username} (ID: {user_id})")

    try:
        # Сначала проверяем, есть ли пользователь уже в очереди
        position_response = requests.get(f"{API_URL}/position/{user_id}")

        if position_response.status_code == 200:
            # Пользователь уже в очереди, получаем его позицию
            position_data = position_response.json()
            user_position = position_data.get("position")

            if user_position is not None:
                bot.send_message(message.chat.id, f"Вы уже находитесь в очереди, ваша позиция: {user_position}")
                return  # Прерываем выполнение, если пользователь уже в очереди

        # Если пользователь не в очереди, добавляем его
        response = requests.post(f"{API_URL}/add_to_queue/?user_id={user_id}&username={username}")

        logging.info(f"Ответ от FastAPI: {response.status_code} - {response.text}")

        if response.status_code == 200:
            # Получаем текущую позицию пользователя в очереди
            position_response = requests.get(f"{API_URL}/position/{user_id}")
            position_data = position_response.json()
            user_position = position_data.get("position")

            # Получаем данные о времени и количестве касс
            time_response = requests.get(f"{API_URL}/time/")
            attractions_response = requests.get(f"{API_URL}/attractions/")

            time_per_person = time_response.json().get("time", 2)  # Время на одного человека
            number_of_attractions = attractions_response.json().get("number_attractions", 2)  # Количество терминалов

            # Рассчитываем ожидаемое время
            if user_position > 1:
                wait_time = ((user_position - 1) * int(time_per_person)) / int(number_of_attractions)
            else:
                wait_time = 0

            # Если время ожидания равно 0, говорим пользователю подходить к терминалу
            if wait_time == 0:
                bot.send_message(message.chat.id, f"Вы вошли в очередь!\n"
                                                  f"Ваша позиция: {user_position}\n"
                                                  f"Подходите к терминалу!")
            else:
                # Отправляем сообщение пользователю с его позицией и временем ожидания
                bot.send_message(message.chat.id, f"Вы вошли в очередь!\n"
                                                  f"Ваша позиция: {user_position}\n"
                                                  f"Примерное время ожидания: {int(wait_time)} минут.")
        else:
            bot.send_message(message.chat.id, "Что-то пошло не так!")
            logging.error(f"Failed request with status code {response.status_code}")
            logging.error(f"Response text: {response.text}")

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
        response = requests.get(f"{API_URL}/position/{user_id}")

        logging.info(f"Ответ от FastAPI: {response.status_code} - {response.text}")

        if response.status_code == 200:
            data = response.json()
            user_position = data.get('position')

            if user_position is not None:
                # Получаем данные о времени и количестве касс
                time_response = requests.get(f"{API_URL}/time/")
                attractions_response = requests.get(f"{API_URL}/attractions/")

                time_per_person = time_response.json().get("time", 2)  # Время на одного человека
                number_of_attractions = attractions_response.json().get("number_attractions",
                                                                        2)  # Количество терминалов

                # Рассчитываем примерное время ожидания
                if user_position > 1:
                    wait_time = ((user_position - 1) * int(time_per_person)) / int(number_of_attractions)
                else:
                    wait_time = 0

                # Отправляем сообщение с текущей позицией и временем ожидания
                bot.send_message(message.chat.id, f"Ваша позиция в очереди: {user_position}\n"
                                                  f"Примерное время ожидания: {int(wait_time)} минут.")
            else:
                bot.send_message(message.chat.id, "Вы не в очереди.")
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
    username = message.from_user.username  # Получаем username

    # Логируем ID пользователя и его имя (или None, если его нет)
    logging.info(f"Удаление пользователя с ID: {user_id}, Username: {username} из очереди")

    # Отправляем запрос к FastAPI для удаления пользователя из очереди
    try:
        # Отправляем DELETE запрос к FastAPI для удаления пользователя
        response = requests.delete(f"{API_URL}/remove_from_queue/{user_id}")

        logging.info(f"Ответ от FastAPI: {response.status_code} - {response.text}")

        # Проверяем, успешно ли удален пользователь
        if response.status_code == 200:
            data = response.json()

            # Проверяем, есть ли username, если нет - выводим user_id
            display_name = username if username else user_id
            bot.send_message(message.chat.id, f"{display_name}, вы были удалены из очереди.\nСтатус: {data['message']}")
        else:
            bot.send_message(message.chat.id, "Не удалось удалить пользователя из очереди.")
            print(f"Failed request with status code {response.status_code}")
            print(f"Response text: {response.text}")

    except Exception as e:
        logging.error(f"Ошибка при отправке запроса: {e}")
        bot.send_message(message.chat.id, "Не удалось удалить пользователя из очереди. Попробуйте позже.")


# Обработчик команды /next — удаление первого пользователя из очереди
# @bot.message_handler(commands=['next'])
# def next_user(message):
#     try:
#         # Отправляем запрос к FastAPI для удаления первого пользователя из очереди
#         response = requests.delete(f"{API_URL}/next/")
#
#         logging.info(f"Ответ от FastAPI: {response.status_code} - {response.text}")
#
#         if response.status_code == 200:
#             bot.send_message(message.chat.id, response.json()["message"])
#         else:
#             bot.send_message(message.chat.id, "Очередь пуста или что-то пошло не так!")
#             print(f"Failed request with status code {response.status_code}")
#             print(f"Response text: {response.text}")
#
#     except Exception as e:
#         logging.error(f"Ошибка при отправке запроса: {e}")
#         bot.send_message(message.chat.id, "Не удалось удалить пользователя из очереди. Попробуйте позже.")


# Основной цикл для запуска бота
if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
