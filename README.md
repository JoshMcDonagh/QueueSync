# QueueSync

The **QueueSync** is a Python library for coordinating and managing distributed systems. It consists of a **Coordinator** (server) that queues and processes client requests sequentially, and **Worker** (client) instances that send requests to the Coordinator. This library is structured to support multi-machine coordination in a networked environment.

## Features

- **Queue-based Request Management**: The `Coordinator` class queues client requests, handling them one at a time.
- **Threaded Connections**: Supports concurrent connections without blocking operations.
- **Extensible**: Built with abstract base classes, allowing custom implementations of both `Coordinator` and `Worker`.
- **Optional Status Updates**: Display connection status and data transfer updates.

## Directory Structure

The project is organized as follows:

```plaintext
QueueSync/
├── src/
│   ├── __init__.py
│   ├── coordinator.py
│   └── worker.py
├── tests/
│   ├── __init__.py
│   ├── test_coordinator.py
│   └── test_worker.py
├── .gitignore
├── LICENSE
├── README.md
├── setup.py                   
└── pyproject.toml
```

## Installation

Clone the repository and ensure you have Python 3.x installed. Optionally, set up a virtual environment:

```
git clone https://github.com/yourusername/inter-machine-coordinator-library.git
cd inter-machine-coordinator-library
python3 -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```

## Usage

### Coordinator

The `Coordinator class`, located in `src/coordinator.py`, is an abstract class that serves as the server, managing client connections and processing requests from a queue.

#### Key Methods

- `start()`: Initializes and starts the server.
- `queue_client_request(client_socket, client_address)`: Adds client requests to a queue.
- `Process_requests()`: Sequentially processes each queued request.
- `handle_request(client_socket, client_address, received_data)`: Abstract method to be implemented for custom request processing.

### Worker
The `Worker` class, located in `src/worker.py`, is an abstract class representing the client, which connects to the `Coordinator` server, sends requests, and receives responses.

#### Key Methods

- `start()`: Connects the Worker to the Coordinator server.
- `query_coordinator(data)`: Sends data to the server and awaits a response.
- `run_worker()`: Abstract method to be implemented for custom worker logic.

## Customisation

To implement specific request handling and worker functionality, create subclasses of `Coordinator` and `Worker`, then override the `handle_request` and `run_worker` methods, respectively.

Example:

```
from src.coordinator import Coordinator
from src.worker import Worker

class MyCoordinator(Coordinator):
    def handle_request(self, client_socket, client_address, received_data):
        response = b"Custom response data"
        return response

class MyWorker(Worker):
    def run_worker(self):
        data = b"Sample request data"
        response = self.query_coordinator(data)
        print(f"Received response: {response}")
```

## Example

1. **Coordinator**:
    ```
    coordinator = MyCoordinator(host='127.0.0.1', port=12345, max_num_of_clients=5, are_updates_displayed=True)
    coordinator.start()
    ```

2. **Worker**:
    ```
    worker = MyWorker(host='127.0.0.1', port=12345, are_updates_displayed=True)
    worker.start()
    ```

This example demonstrates a simple setup with a `Coordinator` listening on localhost and a custom `Worker` connecting to it.

## License

This library is open-source and available under the Apache License 2.0. See the `LICENSE` file for details.