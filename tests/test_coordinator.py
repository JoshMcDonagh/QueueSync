import unittest
from unittest.mock import MagicMock, patch
import threading
import socket
from src.coordinator import Coordinator


# Mock subclass of Coordinator for testing
class MockCoordinator(Coordinator):
    def handle_request(self, client_socket, client_address, received_data):
        return b"Mock response"


class TestCoordinator(unittest.TestCase):

    def setUp(self):
        # Initialize the mock Coordinator with test settings
        self.coordinator = MockCoordinator("127.0.0.1", 5000, max_num_of_clients=5, are_updates_displayed=True)

    @patch("socket.socket")
    def test_queue_client_request(self, mock_socket):
        client_socket = mock_socket()
        client_address = ("127.0.0.1", 6000)

        # Call the method to test
        self.coordinator.queue_client_request(client_socket, client_address)

        # Check that the request was added to the queue
        queued_client_socket, queued_client_address = self.coordinator.request_queue.get()
        self.assertEqual(queued_client_socket, client_socket)
        self.assertEqual(queued_client_address, client_address)

    @patch("socket.socket")
    def test_process_requests(self, mock_socket):
        client_socket = mock_socket()
        client_address = ("127.0.0.1", 6000)

        # Mock the socket's recv and send methods
        client_socket.recv = MagicMock(return_value=b"Mock data")
        client_socket.send = MagicMock()

        # Add a mock client request to the queue
        self.coordinator.request_queue.put((client_socket, client_address))

        # Start process_requests in a separate thread
        process_thread = threading.Thread(target=self.coordinator.process_requests)
        process_thread.daemon = True  # Ensures thread closes when test ends
        process_thread.start()

        # Allow some time for process_requests to process the request
        process_thread.join(timeout=1)

        # Check that handle_request was called and the response was sent
        client_socket.send.assert_called_once_with(b"Mock response")

    @patch("socket.socket")
    def test_start_stop(self, mock_socket):
        server_socket = mock_socket()
        self.coordinator.running = True

        # Mock accept method to simulate client connection
        server_socket.accept = MagicMock(
            side_effect=[(mock_socket(), ("127.0.0.1", 6000)), socket.error("Test Exception")])

        # Run the start method in a separate thread
        with patch.object(self.coordinator, 'display_update'):
            with patch.object(self.coordinator, 'process_requests'):
                threading.Thread(target=self.coordinator.start).start()

                # Allow some time for the server to start
                self.coordinator.stop()

        self.assertFalse(self.coordinator.running)


if __name__ == "__main__":
    unittest.main()
