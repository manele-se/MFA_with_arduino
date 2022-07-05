from http.server import BaseHTTPRequestHandler, HTTPServer
import time

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
    def do_GET(self):
        path = "./Client" + self.path
        if path.endswith("/"):
            path = path + "index.html"

        self.send_response(200)
        self.send_header("Content-type", get_content_type(path))
        self.end_headers()

        with open(path) as f:
            lines = f.read()

        self.wfile.write(bytes(lines, encoding='utf8'))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
