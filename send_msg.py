__author__ = 'InfSub'
__contact__ = 'ADmin@TkYD.ru'
__copyright__ = 'Copyright (C) 2024, [LegioNTeaM] InfSub'
__date__ = '2024/11/09'
__deprecated__ = False
__email__ = 'ADmin@TkYD.ru'
__maintainer__ = 'InfSub'
__status__ = 'Production'  # 'Production / Development'
__version__ = '1.0.1'


from os import getenv
from aiohttp import ClientSession as aio_ClientSession
from dotenv import load_dotenv

from logger import configure_logging

# Загрузка логгера с настройками
logging = configure_logging()


# Загрузка переменных из .env файла
load_dotenv()

TELEGRAM_TOKEN = getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = getenv('TELEGRAM_CHAT_ID')


async def send_telegram_message(message: str) -> dict:
    """
    Sends a message to the specified Telegram chat using the API.

    :param message: The text of the message to be sent.
    :return: The response from the Telegram API as a dictionary (JSON) or an empty dictionary in case of an error.
    --
    Отправляет сообщение в указанный чат Телеграм с использованием API.

    :param message: Строка с текстом сообщения, которое нужно отправить.
    :return: Ответ от Telegram API в виде словаря (JSON) или пустой словарь в случае ошибки.
    """
    logging.info('Preparing to send a message to Telegram.')

    # URL for sending a message via the Telegram Bot API
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'

    # Split TELEGRAM_CHAT_ID into chat_id and message_thread_id if necessary
    parts = TELEGRAM_CHAT_ID.split('/')
    chat_id = parts[0]
    message_thread_id = parts[1] if len(parts) > 1 else None

    # Prepare the payload for the POST request
    payload = {
        'chat_id': chat_id,  # The ID of the chat to which the message will be sent
        'text': message  # The text of the message
    }

    # Add message_thread_id to the payload if specified
    if message_thread_id:
        payload['message_thread_id'] = message_thread_id

    logging.debug(f'Payload for Telegram: {payload}')

    # Create an HTTP client session
    async with aio_ClientSession() as session:
        try:
            # Send the POST request
            async with session.post(url, data=payload) as response:
                # Check the response status
                if response.status == 200:
                    logging.info('Message successfully sent to Telegram.')
                    # Return the response in JSON format
                    return await response.json()
                else:
                    # Handle the error in case of an unsuccessful request
                    error_text = await response.text()
                    logging.error(f'Error sending message: {error_text}')
                    return {}  # Return an empty dictionary in case of an error
        except Exception as e:
            # Conditional logging of stack trace
            # Условное логирование трассировки стека
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logging.exception('Exception occurred while trying to send a message to Telegram.')
            else:
                logging.error(f'Error sending message: {e}')
            return {}  # Return an empty dictionary in case of an error


# Пример вызова функции
# asyncio.run(send_telegram_message('Ваше сообщение'))
