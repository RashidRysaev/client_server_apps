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
import client


class TestClient(unittest.TestCase):

    # ConnectionRefusedError: [Errno 61] Connection refused -- ничего не могу с ней поделать.

    def setUp(self):
        self.s_cl = socket(AF_INET, SOCK_STREAM)
        self.s_cl.connect(("localhost", 7779))

    def tearDown(self):
        self.s_cl.close()

    def test_handle_message(self):
        data = self.s_cl.recv(1024)
        self.assertEqual(data, pickle.loads(data))

    def test_send_presence_msg(self):
        presence_msg = self.s_cl.send(pickle.dumps({"test": "test"}))
        data = self.s_cl.recv(1024)
        self.assertEqual(presence_msg, data)

    def test_send_presence_msg(self):
        msg = self.s_cl.send(pickle.dumps({"test": "test"}))
        data = self.s_cl.recv(1024)
        self.assertEqual(msg, data)


if __name__ == "__main__":
    unittest.main()
