"""Программа-клиент"""

import sys
import json
import socket
import time
import argparse
import logging
import threading
from common.variables import (
    DEFAULT_PORT,
    DEFAULT_IP_ADDRESS,
    ACTION,
    TIME,
    USER,
    ACCOUNT_NAME,
    SENDER,
    PRESENCE,
    RESPONSE,
    ERROR,
    MESSAGE,
    MESSAGE_TEXT,
    DESTINATION,
    EXIT,
)
from common.utils import get_message, send_message
from errors import IncorrectDataRecivedError, ReqFieldMissingError, ServerError


def create_exit_message(account_name):
    """Функция создаёт словарь с сообщением о выходе"""
    return {ACTION: EXIT, TIME: time.time(), ACCOUNT_NAME: account_name}


def message_from_server(sock, my_username):
    """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
    while True:
        try:
            message = get_message(sock)
            if (
                ACTION in message
                and message[ACTION] == MESSAGE
                and SENDER in message
                and DESTINATION in message
                and MESSAGE_TEXT in message
                and message[DESTINATION] == my_username
            ):
                print(
                    f"\nПолучено сообщение от пользователя {message[SENDER]}:"
                    f"\n{message[MESSAGE_TEXT]}"
                )
                print(
                    f"Получено сообщение от пользователя {message[SENDER]}:"
                    f"\n{message[MESSAGE_TEXT]}"
                )
            else:
                print(f"Получено некорректное сообщение с сервера: {message}")
        except IncorrectDataRecivedError:
            print(f"Не удалось декодировать полученное сообщение.")
        except (
            OSError,
            ConnectionError,
            ConnectionAbortedError,
            ConnectionResetError,
            json.JSONDecodeError,
        ):
            print(f"Потеряно соединение с сервером.")
            break


def create_message(sock, account_name="Guest"):
    """
    Функция запрашивает кому отправить сообщение и само сообщение,
    и отправляет полученные данные на сервер
    :param sock:
    :param account_name:
    :return:
    """
    to_user = input("Введите получателя сообщения: ")
    message = input("Введите сообщение для отправки: ")
    message_dict = {
        ACTION: MESSAGE,
        SENDER: account_name,
        DESTINATION: to_user,
        TIME: time.time(),
        MESSAGE_TEXT: message,
    }
    print(f"Сформирован словарь сообщения: {message_dict}")
    try:
        send_message(sock, message_dict)
        print(f"Отправлено сообщение для пользователя {to_user}")
    except:
        print("Потеряно соединение с сервером.")
        sys.exit(1)


def user_interactive(sock, username):
    """Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения"""
    print_help()
    while True:
        command = input("Введите команду: ")
        if command == "message":
            create_message(sock, username)
        elif command == "help":
            print_help()
        elif command == "exit":
            send_message(sock, create_exit_message(username))
            print("Завершение соединения.")
            print("Завершение работы по команде пользователя.")
            break
        else:
            print(
                "Команда не распознана, попробойте снова. help - вывести поддерживаемые команды."
            )


def create_presence(account_name):
    """Функция генерирует запрос о присутствии клиента"""
    out = {ACTION: PRESENCE, TIME: time.time(), USER: {ACCOUNT_NAME: account_name}}
    print(f"Сформировано {PRESENCE} сообщение для пользователя {account_name}")
    return out


def print_help():
    """Функция выводящяя справку по использованию"""
    print("Поддерживаемые команды:")
    print("message - отправить сообщение. Кому и текст будет запрошены отдельно.")
    print("help - вывести подсказки по командам")
    print("exit - выход из программы")


def process_response_ans(message):
    """
    Функция разбирает ответ сервера на сообщение о присутствии,
    возращает 200 если все ОК или генерирует исключение при ошибке
    :param message:
    :return:
    """
    print(f"Разбор приветственного сообщения от сервера: {message}")
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return "200 : OK"
        elif message[RESPONSE] == 400:
            raise ServerError(f"400 : {message[ERROR]}")
    raise ReqFieldMissingError(RESPONSE)


def arg_parser():
    """Парсер аргументов коммандной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument("addr", default=DEFAULT_IP_ADDRESS, nargs="?")
    parser.add_argument("port", default=DEFAULT_PORT, type=int, nargs="?")
    parser.add_argument("-n", "--name", default=None, nargs="?")
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name

    return server_address, server_port, client_name


def main():
    """Сообщаем о запуске"""
    print("Консольный месседжер. Клиентский модуль.")

    # Загружаем параметы коммандной строки
    server_address, server_port, client_name = arg_parser()

    # Если имя пользователя не было задано, необходимо запросить пользователя.
    if not client_name:
        client_name = input("Введите имя пользователя: ")

    print(
        f"Запущен клиент с парамертами: адрес сервера: {server_address}, "
        f"порт: {server_port}, имя пользователя: {client_name}"
    )

    # Инициализация сокета и сообщение серверу о нашем появлении
    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence(client_name))
        answer = process_response_ans(get_message(transport))
        print(f"Установлено соединение с сервером. Ответ сервера: {answer}")
        print(f"Установлено соединение с сервером.")
    except json.JSONDecodeError:
        sys.exit(1)
    except ServerError as error:
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        print(
            f"В ответе сервера отсутствует необходимое поле {missing_error.missing_field}"
        )
        sys.exit(1)
    except (ConnectionRefusedError, ConnectionError):
        print(
            f"Не удалось подключиться к серверу {server_address}:{server_port}, "
            f"конечный компьютер отверг запрос на подключение."
        )
        sys.exit(1)
    else:
        receiver = threading.Thread(
            target=message_from_server, args=(transport, client_name)
        )
        receiver.daemon = True
        receiver.start()

        user_interface = threading.Thread(
            target=user_interactive, args=(transport, client_name)
        )
        user_interface.daemon = True
        user_interface.start()

        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break


if __name__ == "__main__":
    main()
