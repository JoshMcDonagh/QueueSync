import unittest
from unittest.mock import MagicMock, patch
import socket
from src.worker import Worker


# Mock subclass of Worker for testing
class MockWorker(Worker):
    def run_worker(self):
        pass  # No specific functionality needed for this test


class TestWorker(unittest.TestCase):

    def setUp(self):
        # Initialize the mock Worker with test settings
        self.worker = MockWorker("127.0.0.1", 5000, are_updates_displayed=True)

    @patch("socket.socket")
    def test_query_coordinator(self, mock_socket):
        client_socket = mock_socket()

        # Set up the client socket to simulate sending and receiving data
        self.worker.client_socket = client_socket
        client_socket.send = MagicMock()
        client_socket.recv = MagicMock(return_value=b"Mock response")

        # Call the method to test
        response = self.worker.query_coordinator(b"Test data")

        # Check that data was sent and response was received
        client_socket.send.assert_called_once_with(b"Test data")
        self.assertEqual(response, b"Mock response")

    @patch("socket.socket")
    def test_start(self, mock_socket):
        client_socket = mock_socket()

        # Set up the client socket to connect
        client_socket.connect = MagicMock()

        # Run start method
        with patch.object(self.worker, "run_worker") as mock_run_worker:
            self.worker.start()
            mock_run_worker.assert_called_once()

        # Verify that the socket connected to the server
        client_socket.connect.assert_called_once_with(("127.0.0.1", 5000))

    @patch("socket.socket")
    def test_connection_error_handling(self, mock_socket):
        client_socket = mock_socket()

        # Simulate a connection error
        client_socket.connect.side_effect = socket.error("Connection error")

        with patch.object(self.worker, "display_update") as mock_display:
            self.worker.start()
            mock_display.assert_any_call("Connection error: Connection error")


if __name__ == "__main__":
    unittest.main()
