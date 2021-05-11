import pickle
import threading
from datetime import datetime
from socket import AF_INET, SOCK_STREAM, socket

""" Client """

host = "localhost"
port = 7779

s_cl = socket(AF_INET, SOCK_STREAM)
s_cl.connect((host, port))

TIME = datetime.now().replace(microsecond=0).isoformat(sep=" ")


def handle_messages():

    while True:
        try:
            data = s_cl.recv(1024)

            if data:
                print(f"Response from server: {pickle.loads(data)}")
            else:
                s_cl.close()
                break

        except Exception as e:
            print(f"Error handling message from server: {e}")
            s_cl.close()
            break


def send_presence_msg():

    """Sending presence message to the server"""

    presence = {
        "action": "presence",
        "time": TIME,
        "type": "status",
        "user": {"accout_name": account_name, "status": "Oi there, I am here!"},
    }

    return s_cl.send(pickle.dumps(presence))


def send_msg():

    """Sending a message to the server"""

    message = {
        "action": "msg",
        "time": TIME,
        "to": "anyone",
        "from": account_name,
        "message": "Workers of the world, unite!",
    }

    return s_cl.send(pickle.dumps(message))


if __name__ == "__main__":

    account_name = input("Enter your name here: ")

    threading.Thread(target=handle_messages).start()

    send_presence_msg()

    send_msg()
