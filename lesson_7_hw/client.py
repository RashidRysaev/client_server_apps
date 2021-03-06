import sys
import json
import socket
import time
import argparse
from utils.constants import (
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
)
from utils.msg_funcs import get_message, send_message


def message_from_server(message):
    if (
        ACTION in message
        and message[ACTION] == MESSAGE
        and SENDER in message
        and MESSAGE_TEXT in message
    ):
        print(
            f"Получено сообщение от пользователя "
            f"{message[SENDER]}:\n{message[MESSAGE_TEXT]}"
        )


def create_message(sock, account_name="User"):
    message = input("Введите сообщение для отправки или 'exit' для завершения работы: ")
    if message == "exit":
        sock.close()
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message,
    }
    return message_dict


def create_presence(account_name="User"):
    out = {ACTION: PRESENCE, TIME: time.time(), USER: {ACCOUNT_NAME: account_name}}
    return out


def process_response_ans(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return "200 : OK"
        elif message[RESPONSE] == 400:
            return "400: NO RESPONSE"


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("addr", default=DEFAULT_IP_ADDRESS, nargs="?")
    parser.add_argument("port", default=DEFAULT_PORT, type=int, nargs="?")
    parser.add_argument("-m", "--mode", default="listen", nargs="?")
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    return server_address, server_port, client_mode


def main():
    server_address, server_port, client_mode = arg_parser()

    try:
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))
        send_message(transport, create_presence())
        answer = process_response_ans(get_message(transport))
        print(f"Установлено соединение с сервером. Ответ сервера: {answer}")
    except json.JSONDecodeError:
        print("Не удалось декодировать полученную Json строку.")
        sys.exit(1)
    except ConnectionRefusedError:
        print(
            f"Не удалось подключиться к серверу {server_address}:{server_port}, "
            f"конечный компьютер отверг запрос на подключение."
        )
        sys.exit(1)
    else:
        if client_mode == "send":
            print("Режим работы - отправка сообщений.")
        else:
            print("Режим работы - приём сообщений.")
        while True:
            if client_mode == "send":
                try:
                    send_message(transport, create_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    print(f"Соединение с сервером {server_address} было потеряно.")
                    sys.exit(1)

            if client_mode == "listen":
                try:
                    message_from_server(get_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    print(f"Соединение с сервером {server_address} было потеряно.")
                    sys.exit(1)


if __name__ == "__main__":
    main()
