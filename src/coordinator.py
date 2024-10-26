import queue
import socket
import threading
from abc import ABC, abstractmethod
from typing import Tuple


class Coordinator(ABC):
    """
    Abstract base class for a server that coordinates client connections, handles
    client requests sequentially using a queue, and processes each request in turn.

    Attributes:
        host (str): The server's hostname or IP address.
        port (int): The port number the server listens on.
        max_num_of_clients (int): Maximum number of simultaneous client connections.
        are_updates_displayed (bool): If True, displays status updates for connections.
        request_queue (queue.Queue): Queue to hold client requests for sequential processing.
    """

    def __init__(self, host: str, port: int, max_num_of_clients: int, are_updates_displayed: bool = False) -> None:
        """
        Initializes the Coordinator server with host, port, and client queue settings.

        Args:
            host (str): The server's hostname or IP address.
            port (int): The port number for the server.
            max_num_of_clients (int): Maximum number of concurrent connections.
            are_updates_displayed (bool): Whether to display updates about client connections.
        """
        self.host = host
        self.port = port
        self.max_num_of_clients = max_num_of_clients
        self.are_updates_displayed = are_updates_displayed

        # Queue to store client requests
        self.request_queue = queue.Queue()

    def display_update(self, message: str) -> None:
        """
        Prints updates if the are_updates_displayed flag is set.

        Args:
            message (str): The message to display.
        """
        if self.are_updates_displayed:
            print(message)

    def queue_client_request(self, client_socket: socket.socket, client_address: Tuple[str, int]) -> None:
        """
        Enqueues the client request (socket and address) into the request queue.

        Args:
            client_socket (socket.socket): The client socket object.
            client_address (tuple): The client's address as a (host, port) tuple.
        """
        self.request_queue.put((client_socket, client_address))
        self.display_update(f"Request from {client_address} added to the request queue.")

    def process_requests(self) -> None:
        """
        Processes client requests sequentially from the queue.
        Each request is dequeued, processed by `handle_request`, and the result is
        sent back to the client.
        """
        while True:
            # Retrieve the next client request from the queue
            client_socket, client_address = self.request_queue.get()
            self.display_update(f"Processing request from {client_address}.")

            try:
                # Call handle_request to get the response data
                received_data = client_socket.recv(1024)  # Receive data from client
                response = self.handle_request(client_socket, client_address, received_data)

                # Send the response back to the client
                client_socket.send(response)

            finally:
                # Close the client socket after processing
                client_socket.close()
                self.display_update(f"Closed connection with {client_address}.")
                self.request_queue.task_done()  # Mark the task as done in the queue

    def start(self) -> None:
        """
        Starts the server, listens for incoming connections, and handles them
        by queueing each client request. A separate thread processes requests from the queue.
        """
        # Initialize server socket
        server_socket = socket.socket()
        server_socket.bind((self.host, self.port))
        server_socket.listen(self.max_num_of_clients)
        self.display_update(f"Coordinator server listening on {self.host}:{self.port}")

        # Start a thread to process client requests from the queue
        threading.Thread(target=self.process_requests, daemon=True).start()

        # Main loop to accept and enqueue client connections
        while True:
            # Accept a client connection
            client_socket, client_address = server_socket.accept()
            self.display_update(f"Accepted connection from {client_address}.")

            # Queue the client's request in a separate thread
            threading.Thread(target=self.queue_client_request, args=(client_socket, client_address)).start()

    @abstractmethod
    def handle_request(self, client_socket: socket.socket, client_address: Tuple[str,int], received_data: bytes) -> bytes:
        """
        Abstract method to handle the client's request. Must be implemented in a subclass.

        Args:
            client_socket (socket.socket): The client socket.
            client_address (tuple): The client's address.
            received_data (bytes): The data received from the client.

        Returns:
            bytes: The response to send back to the client.
        """
        pass
