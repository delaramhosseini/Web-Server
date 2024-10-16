# Web-Server Simulation using Thread Pool

## Introduction
This program simulates a web server that handles client requests using a thread pool. It listens for incoming connections, processes client requests in parallel using a fixed number of worker threads, and responds to the clients with either the content of the requested file or an error message based on the nature of the request. The program handles several scenarios such as valid and invalid requests, non-existent files, full thread pools, and graceful shutdown on receiving a SIGINT signal.

### Thread Pool Overview
A **thread pool** is a design pattern used to manage a collection of pre-initialized threads that can be reused to perform multiple tasks concurrently. The primary purpose of a thread pool is to improve the efficiency of thread management, reduce the overhead associated with thread creation and destruction, and control the number of concurrent threads running in an application.

#### Benefits of Using a Thread Pool:
- **Resource Management**: Limits the number of concurrent threads to prevent resource exhaustion (e.g., CPU and memory usage).
- **Performance**: Reduces the overhead of thread creation by reusing existing threads for multiple tasks, which is especially useful in applications with high request rates, such as web servers.
- **Simplified Programming Model**: Abstracts the complexities of thread management, allowing developers to focus on the core functionality of their applications without worrying about low-level threading details.

<img width="1152" alt="Screenshot 1403-07-25 at 10 31 21" src="https://github.com/user-attachments/assets/13919dc8-5d40-4459-a25e-26a1554b1d8c">


## Program Functionality

### Key Features:
- **Thread Pool Management**: Requests are handled by a pool of worker threads to efficiently manage concurrent client connections.
- **File Handling**: The server returns the contents of a requested file if it exists or a `404 Not Found` error if it doesn't.
- **Error Handling**: The server responds with appropriate HTTP status codes, such as:
  - **400 Bad Request**: If the request is invalid.
  - **404 Not Found**: If the requested file doesn't exist.
  - **503 Service Unavailable**: If the thread pool is full and unable to handle more requests.
- **Graceful Shutdown**: When the program receives a `SIGINT` signal (e.g., by pressing Ctrl+C), it terminates the worker threads and closes the server socket gracefully, ensuring no data loss or abrupt termination.

### Thread Management:
- **`pthread_create` and `pthread_join`**: These functions are used to create and manage a fixed number of worker threads in the thread pool. Each thread waits for a request from the shared queue and processes it.
- **Synchronization**: A shared queue is used to manage incoming requests. Synchronization mechanisms like mutexes and condition variables are used to ensure that access to this queue is thread-safe.

### Socket Communication:
- **`socket`, `listen`, `accept`, `send`, and `recv`**: These functions handle network communication with clients. The server listens for incoming connections, accepts them, and uses `send` and `recv` to exchange data with the client.

### Signal Handling:
- **`signal(SIGINT, handler)`**: The program registers a signal handler for `SIGINT` to allow graceful shutdown. When the signal is received, the server stops accepting new requests, terminates active worker threads, and closes the listening socket.

## Error Scenarios:
- **Valid Requests**: When a client makes a valid request (e.g., requesting an existing file), the worker thread fetches the file content and sends it back to the client.
- **Invalid Requests (400)**: If the client sends a malformed or invalid request, the server responds with a `400 Bad Request` error.
- **File Not Found (404)**: If the requested file does not exist on the server, the worker thread returns a `404 Not Found` error.
- **Thread Pool Full (503)**: If all worker threads are busy and the thread pool is full, the server responds with a `503 Service Unavailable` error, indicating it cannot handle more requests at the moment.
