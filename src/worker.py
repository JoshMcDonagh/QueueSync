import socket
from abc import ABC, abstractmethod

class Worker(ABC):
    def __init__(self, host: str, port: int, are_updates_displayed: bool = False) -> None:
        """
        Initializes the Worker client with the server's host, port, and optional display settings.

        Args:
            host (str): The server's hostname or IP address.
            port (int): The port number for the server.
            are_updates_displayed (bool): Whether to display connection and data transfer updates.
        """
        self.host = host
        self.port = port
        self.are_updates_displayed = are_updates_displayed
        self.client_socket = None  # Will hold the socket connection

    def display_update(self, message: str) -> None:
        """
        Prints updates if the are_updates_displayed flag is set.

        Args:
            message (str): The message to display.
        """
        if self.are_updates_displayed:
            print(message)

    def query_coordinator(self, data: bytes) -> bytes:
        """
        Sends a query to the server and waits for a response.

        Args:
            data (bytes): The data to send to the server.

        Returns:
            bytes: The response received from the server.
        """
        try:
            self.display_update("Querying the coordinator...")
            self.client_socket.send(data)
            self.display_update("Waiting for response...")

            # Receive the response (you could adjust the buffer size if needed)
            response = self.client_socket.recv(1024)
            self.display_update("Response received...")
            return response

        except socket.error as e:
            self.display_update(f"Error during communication: {e}")
            return b''  # Return empty bytes on error

    def start(self) -> None:
        """
        Starts the client, connects to the server, and runs the worker logic.
        """
        try:
            self.client_socket = socket.socket()
            self.client_socket.connect((self.host, self.port))
            self.display_update(f"Connected to server at {self.host}:{self.port}")
            self.run_worker()  # Call the worker's main function

        except socket.error as e:
            self.display_update(f"Connection error: {e}")

        finally:
            if self.client_socket:
                self.client_socket.close()
                self.client_socket = None
                self.display_update("Connection closed.")

    @abstractmethod
    def run_worker(self) -> None:
        """
        Defines the main functionality of the client worker. Must be implemented by subclasses.
        """
        pass
