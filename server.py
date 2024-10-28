import socket
import threading
import os

class Server:
    def __init__(self, host='localhost', port=8080, tempdir='templates',static_dir=None, tempdic=None,err_page=None):
        if tempdic is None:
            tempdic = {"index": "index.html"}
        self.host = host
        self.port = port
        self.template_dir = tempdir 
        self.template_dic = tempdic
        self.error_page=err_page
        self.static_dir=static_dir


        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))

    def startServer(self):
        self.server_socket.listen(5)
        print(f"Listening to {self.host}:{self.port}")
        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                print(f"Client {addr[0]}:{addr[1]} joined!")
                threading.Thread(target=self.handleClient, args=(client_socket, addr)).start()
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            self.server_socket.close()

    def handleClient(self, client_socket, addr):
        try:
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                return

            request_line = request.split('\r\n')[0]
            method, page, _ = request_line.split()

            response = self.returnResponse(method, page)
            client_socket.sendall(response.encode('utf-8'))
        finally:
            client_socket.close()

    def returnResponse(self, method, page):
        if page == "/":
            page = 'index'
        else:
            page = page[1:]

        if page.endswith(".html"):
            page = page[:-5]

        if method == 'GET':
            if page in self.template_dic:
                template_path = os.path.join(self.template_dir, self.template_dic[page])
                return self.buildResponse(200, template_path)
            elif page.endswith(".css"):
                static_path = os.path.join(self.static_dir, page)
                return self.buildResponse(200, static_path, "text/css")
            else:
                return self.buildResponse(404)
        else:
            return self.buildResponse(405)

    def buildResponse(self, status, template_path=None,content_type="text/html"):
        response = ""
        if status == 200:
            try:
                with open(template_path, "r") as f:
                    content = f.read()
                response += "HTTP/1.1 200 OK\r\n"
                response += f"Content-Type: {content_type}; charset=utf-8\r\n"
                response += "Content-Length: {}\r\n".format(len(content))
                response += "Connection: close\r\n"
                response += "\r\n"
                response += content
            except FileNotFoundError:
                return self.buildResponse(404) 
        elif status == 404:
            if self.error_page:
                with open(self.template_dir+f"/{self.error_page}","r") as f:
                    content = f.read()
                response+="HTTP/1.1 404 Not Found\r\n\r\n"
                response+=content
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\n<h1>404 Not Found</h1>"
        elif status == 405:
            response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n<h1>405 Method Not Allowed</h1>"
        
        return response

