from concurrent.futures import thread
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from urllib.parse import parse_qs
from random import randrange
import asyncio
from bleak import BleakScanner, BleakClient
import threading

hostName = "localhost"
serverPort = 8080
address="A4:06:E9:79:ED:16"
mutex= threading.Lock()
id= 0x5b


#channel to write to 
CUSTOM_DATA_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"



class BluetoothClient:
    async def send_signal(self,ble):
        code = self.random_number()
        # send code to bluetooth
        await ble.write_gatt_char(CUSTOM_DATA_UUID, bytes([id,code, (id ^ code)]))

    def random_number(self):
        return randrange(1, 15)

    
    async def bluetooth_main(self,address):
        async with BleakClient(address) as client:
            while True:
                mutex.acquire()    
                print("sending to ble")
                await self.send_signal(client)
                mutex.release()
                print("release")


class MyServer(BaseHTTPRequestHandler):
    def http_response(self, path):
        self.send_response(200)
        self.send_header("Content-type", self.get_content_type(path))
        self.end_headers()

        with open(path) as f:
            lines = f.read()

        self.wfile.write(bytes(lines, encoding='utf8'))



    def get_content_type(self, filename):
        if filename.endswith("html"):
            return "text/html"
        if filename.endswith("js"):
            return "text/javascript"
        if filename.endswith("css"):
            return "text/css"
        if filename.endswith("ico"):
            return "image/x-icon"    

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
                mutex.release()
                print("server release")
                mutex.acquire()
                print("server acquire")
                return
        self.http_response("./Client/index.html")


    #create a thread for the web server
    def web_server_main():
        mutex.acquire()
        webServer = HTTPServer((hostName, serverPort), MyServer)
        print("Server started http://%s:%s" % (hostName, serverPort))

        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()
        print("Server stopped.")
        mutex.release()


            
threading.Thread(target=MyServer.web_server_main).start()
bluetooth= BluetoothClient()
asyncio.run(bluetooth.bluetooth_main(address))
    