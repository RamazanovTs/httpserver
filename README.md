# Simple HTTP Server

## Overview
This Simple HTTP Server is a basic implementation of an HTTP server using Python's socket programming and threading. It listens for incoming client requests, serves HTML pages from a specified directory, and handles common HTTP status codes.

## Features
- **Multi-threaded**: Handles multiple clients concurrently.
- **Dynamic Routing**: Maps URLs to HTML template files.
- **Custom Error Pages**: Supports custom error pages for 404 errors.
- **Basic HTTP Protocol**: Implements basic GET method handling.

## Class: `Server`

### Constructor
```python
__init__(self, host='localhost', port=8080, tempdir='templates', tempdic=None, err_page=None)
```

#### Parameters
- `host` (str): The hostname or IP address to bind the server to (default: `'localhost'`).
- `port` (int): The port number to listen on (default: `8080`).
- `tempdir` (str): Directory where HTML templates are stored (default: `'templates'`).
- `tempdic` (dict): A dictionary mapping URL paths to template filenames (default: `{"index": "index.html"}`).
- `err_page` (str): Filename for a custom 404 error page (default: `None`).

### Methods

#### `startServer()`
Starts the server, listens for incoming connections, and spawns a new thread for each client.

```python
def startServer(self)
```

#### `handleClient(client_socket, addr)`
Handles the communication with a connected client.

```python
def handleClient(self, client_socket, addr)
```

- **Parameters**:
  - `client_socket`: The socket object for the client connection.
  - `addr`: The address of the connected client.

#### `returnResponse(method, page)`
Processes the HTTP request and returns the appropriate response based on the request method and page.

```python
def returnResponse(self, method, page)
```

- **Parameters**:
  - `method`: The HTTP method of the request (e.g., `GET`).
  - `page`: The requested page (URL path).

- **Returns**: A formatted HTTP response.

#### `buildResponse(status, template_path=None)`
Constructs the HTTP response based on the status code and optional template path.

```python
def buildResponse(self, status, template_path=None)
```

- **Parameters**:
  - `status`: The HTTP status code (e.g., `200`, `404`, `405`).
  - `template_path`: The file path of the HTML template to serve (default: `None` for error pages).

- **Returns**: A formatted HTTP response string.

### Usage Example

To run the server from a separate file (e.g., `app.py`), you can import the `Server` class and instantiate it there. Below is an example of how to set it up:

```python
# app.py
from server import Server

if __name__ == "__main__":
    server = Server("127.0.0.1", 8080, "templates", err_page="404.html")
    server.startServer()
```

### Running the Server
1. Ensure that your directory structure contains the necessary HTML files in the `templates` directory.
2. Run the `app.py` script to start the server:
   ```bash
   python app.py
   ```
3. Open your web browser and navigate to `http://127.0.0.1:8080` to access the server.

### Error Handling
- **404 Not Found**: Serves a custom 404 error page if specified; otherwise, it returns a default message.
- **405 Method Not Allowed**: Returns an error message for unsupported HTTP methods.

### Directory Structure
Ensure the following directory structure exists:
```
.
├── server.py          # Your server code
├── app.py             # Your application entry point
└── templates          # Directory containing HTML files
    ├── index.html    # Default landing page
    └── 404.html      # Custom 404 error page (optional)
```
