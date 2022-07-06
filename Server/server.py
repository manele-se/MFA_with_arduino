from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from urllib.parse import parse_qs


hostName = "localhost"
serverPort = 8080


def get_content_type(filename):
    if filename.endswith("html"):
        return "text/html"
    if filename.endswith("js"):
        return "text/javascript"
    if filename.endswith("css"):
        return "text/css"
    if filename.endswith("ico"):
        return "image/x-icon"


class MyServer(BaseHTTPRequestHandler):
    def http_response(self, path):
        self.send_response(200)
        self.send_header("Content-type", get_content_type(path))
        self.end_headers()

        with open(path) as f:
            lines = f.read()

        self.wfile.write(bytes(lines, encoding='utf8'))

    def do_GET(self):
        path = "./Client" + self.path
        if path.endswith("/"):
            path = path + "index.html"
        self.http_response(path)

    def do_POST(self):
        length = int(self.headers['content-length'])
        postvars = parse_qs(self.rfile.read(length),
                            keep_blank_values=1)

        username = postvars[bytes('username', encoding='utf8')]
        password = postvars[bytes('password', encoding='utf8')]
        password = password[0].decode("utf-8")
        username = username[0].decode("utf-8")
        username_and_password = username + " " + password

        f = open("./Database/db.txt", "r")
        for line in f:
            if line.strip() == username_and_password:

                self.http_response("./Client/MFA.html")
                # communication with Arduino
                return
        self.http_response("./Client/index.html")


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
