import socket
import threading
import os

class Server:
    def __init__(self, host='localhost', port=8080, template_dir='templates', static_dir=None, error_page='404.html'):
        self.host = host
        self.port = port
        self.template_dir = template_dir
        self.static_dir = static_dir
        self.error_page = error_page
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
    
    def start_server(self):
        self.server_socket.listen(5)
        print(f"Listening on {self.host}:{self.port}")
        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                print(f"Client {addr[0]}:{addr[1]} connected!")
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket):
        try:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                return

            method, path, _ = request.split('\r\n')[0].split()
            response = self.return_response(method, path)
            client_socket.sendall(response.encode('utf-8'))
        finally:
            client_socket.close()

    def return_response(self, method, path):
        if path == "/":
            path = '/index.html'
        
        if method == 'GET':
            if path.endswith(".html") or path == '/index.html':
                return self.build_response(200, os.path.join(self.template_dir, path[1:]))
            elif path.endswith(".css") and self.static_dir:
                return self.build_response(200, os.path.join(self.static_dir, path[1:]), "text/css")
            else:
                return self.build_response(404)
        else:
            return self.build_response(405)

    def build_response(self, status, file_path=None, content_type="text/html"):
        if status == 200:
            try:
                with open(file_path, "r") as f:
                    content = f.read()
                response = "HTTP/1.1 200 OK\r\n"
                response += f"Content-Type: {content_type}; charset=utf-8\r\n"
                response += f"Content-Length: {len(content)}\r\n"
                response += "Connection: close\r\n\r\n"
                response += content
            except FileNotFoundError:
                return self.build_response(404)
        elif status == 404:
            return self.build_error_response(self.error_page)
        elif status == 405:
            return "HTTP/1.1 405 Method Not Allowed\r\n\r\n<h1>405 Method Not Allowed</h1>"
        
        return response

    def build_error_response(self, error_page):
        try:
            with open(os.path.join(self.template_dir, error_page), "r") as f:
                content = f.read()
            return "HTTP/1.1 404 Not Found\r\n\r\n" + content
        except FileNotFoundError:
            return "HTTP/1.1 404 Not Found\r\n\r\n<h1>404 Not Found</h1>"
