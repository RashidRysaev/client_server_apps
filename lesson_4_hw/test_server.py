import os
import pickle
import sys
import unittest
from socket import AF_INET, SOCK_STREAM, socket

sys.path.append(
    os.path.abspath(
        "/Users/Rashid/Documents/AaP/GeekBrains Cources/12. Клиент-серверные приложения на Python/client_server_apps/lesson_3_hw"
    )
)
import server


class TestServer(unittest.TestCase):
    def setUp(self):
        self.s_serv = socket(AF_INET, SOCK_STREAM)
        self.s_serv.bind(("localhost", 7777))
        self.s_serv.listen(10)

    def tearDown(self):
        self.s_serv.close()

    def test_respond_presence_msg(self, client):
        # не видит client'а вообще, но __init__ - то я не могу сюда поставиь...
        self.client = self.s_serv.accept()
        self.client.send(pickle.dumps({"test": "test"}))
        respond = self.client.recv(1024)
        self.assertEqual({"test": "test"}, respond)

    def test_respond_msg(self, client):
        self.client.send(pickle.dumps({"test": "test"}))
        respond = self.client.recv(1024)
        self.assertEqual({"test": "test"}, respond)


if __name__ == "__main__":
    unittest.main()
