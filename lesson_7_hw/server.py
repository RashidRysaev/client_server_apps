import socket
import sys
import argparse
import select
import time
from utils.constants import (
    DEFAULT_PORT,
    MAX_CONNECTIONS,
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


def process_client_message(message, messages_list, client):

    if (
        ACTION in message
        and message[ACTION] == PRESENCE
        and TIME in message
        and USER in message
        and message[USER][ACCOUNT_NAME] == "User"
    ):
        send_message(client, {RESPONSE: 200})
        return
    elif (
        ACTION in message
        and message[ACTION] == MESSAGE
        and TIME in message
        and MESSAGE_TEXT in message
    ):
        messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    else:
        send_message(client, {RESPONSE: 400, ERROR: "Bad Request"})
        return


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", default=DEFAULT_PORT, type=int, nargs="?")
    parser.add_argument("-a", default="", nargs="?")
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    return listen_address, listen_port


def main():
    listen_address, listen_port = arg_parser()

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.settimeout(0.5)

    clients = []
    messages = []

    transport.listen(MAX_CONNECTIONS)
    while True:
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            clients.append(client)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []
        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(
                    clients, clients, [], 0
                )
        except OSError:
            pass

        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    process_client_message(
                        get_message(client_with_message), messages, client_with_message
                    )
                except:
                    clients.remove(client_with_message)

        if messages and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1],
            }
            del messages[0]
            for waiting_client in send_data_lst:
                try:
                    send_message(waiting_client, message)
                except:
                    clients.remove(waiting_client)


if __name__ == "__main__":
    main()
