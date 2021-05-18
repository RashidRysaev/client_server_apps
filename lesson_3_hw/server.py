import logging
import pickle
from datetime import datetime
from socket import AF_INET, SOCK_STREAM, socket
import sys
import os
from lesson_6_hw.decs import log

sys.path.append(
    os.path.abspath(
        "/Users/Rashid/Documents/AaP/GeekBrains Cources/12. Клиент-серверные приложения на Python/client_server_apps/lesson_5_hw/log"
    )
)
import server_log_config


""" Server """

logger = logging.getLogger("server_log")

host = "localhost"
port = 7779

s_serv = socket(AF_INET, SOCK_STREAM)
s_serv.bind((host, port))
s_serv.listen(1)

TIME = datetime.now().replace(microsecond=0).isoformat(sep=" ")


@log
def respond_presence_msg(sender):

    """Responding client's presence message"""

    presence_msg_response = {
        "response": 200,
        "alert": f"Hi there, {data['user']}!",
    }
    return sender.send(pickle.dumps(presence_msg_response))


@log
def respond_msg(sender):

    msg_responce = {
        "response": 200,
        "alert": f"I've got your message: '{data['message']}'",
    }

    return sender.send(pickle.dumps(msg_responce))


if __name__ == "__main__":

    while True:
        client, addr = s_serv.accept()

        data = pickle.loads(client.recv(1024))

        if data["action"] == "presence":
            respond_presence_msg(client)
            print(data)
            logger.info()
        elif data["action"] == "msg":
            respond_msg(client)
            print(data)
            logger.info()

        client.close()
