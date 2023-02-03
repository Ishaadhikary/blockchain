import socket
import unittest

class ServerTestCase(unittest.TestCase):
    def test_server_program(self):
        host = socket.gethostname() 
        port = 9500

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        data = b'Test message'
        client_socket.send(data)
        received_data = client_socket.recv(1024)
        self.assertEqual(data, received_data)
        client_socket.close()

if __name__ == '__main__':
    unittest.main()