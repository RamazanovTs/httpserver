# Simple HTTP Server

## Overview
This Simple HTTP Server is a basic implementation using Python's `socket` and `threading` libraries. It listens for incoming client requests, serves HTML pages from a specified templates directory, and handles static files (like CSS) from a designated static directory.

## Features
- **Multi-threaded**: Handles multiple clients concurrently using threading.
- **Dynamic Routing**: Maps URLs to corresponding HTML templates for easy access.
- **Static File Serving**: Serves CSS files and other static assets from a static directory.
- **Custom Error Pages**: Supports customizable 404 error pages.
- **Basic HTTP Protocol**: Implements basic HTTP GET request handling.

## Class: `Server`

### Constructor
```python
__init__(self, host='localhost', port=8080, tempdir='templates', static_dir=None, tempdic=None, err_page=None)
```

#### Parameters
- `host` (str): The hostname or IP address to bind the server to (default: `'localhost'`).
- `port` (int): The port number to listen on (default: `8080`).
- `tempdir` (str): Directory where HTML templates are stored (default: `'templates'`).
- `static_dir` (str): Directory where static files are stored (default: `None`).
- `tempdic` (dict): A dictionary mapping URL paths to template filenames (default: `{"index": "index.html"}`).
- `err_page` (str): Filename for a custom 404 error page (default: `None`).

### Methods

#### `startServer()`
Starts the server, listens for incoming connections, and spawns a new thread for each client.
```python
def startServer(self)
```

#### `handleClient(client_socket, addr)`
Handles communication with the connected client.
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

#### `buildResponse(status, template_path=None, content_type="text/html")`
Constructs the HTTP response based on the status code and optional template path.
```python
def buildResponse(self, status, template_path=None, content_type="text/html")
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

app = Server(
    host="127.0.0.1",
    port=8080,
    tempdir="templates",
    static_dir="static",
    tempdic={
        "index": "index.html",
        "about": "about.html",
        "contact": "contact.html",
    },
    err_page="404.html"
)

if __name__ == "__main__":
    app.startServer()
```

### Running the Server
1. Ensure that your directory structure contains the necessary HTML files in the `templates` directory and any static files in the `static` directory.
2. Run the `app.py` script to start the server:
   ```bash
   python app.py
   ```
3. Open your web browser and navigate to `http://127.0.0.1:8080` to access the server.

### Serving Static Files
Static files like CSS can be served from the static directory. For example, if you have a `styles.css` file in the `static` directory, it will be accessible at `http://127.0.0.1:8080/styles.css`.

### Error Handling
- **404 Not Found**: Serves a custom 404 error page if specified; otherwise, it returns a default message.
- **405 Method Not Allowed**: Returns an error message for unsupported HTTP methods.

### Directory Structure
Ensure the following directory structure exists:
```
.
├── server.py          # Your server code
├── app.py             # Your application entry point
├── templates          # Directory containing HTML files
│   ├── index.html    # Default landing page
│   ├── about.html    # About page
│   ├── contact.html   # Contact page
│   └── 404.html      # Custom 404 error page (optional)
└── static            # Directory containing static files
    └── styles.css    # CSS file for styling (optional)
```