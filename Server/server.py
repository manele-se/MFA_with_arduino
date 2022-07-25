
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from urllib.parse import parse_qs
from random import randrange
import asyncio
from bleak import BleakClient
import threading
from hashlib import sha256

hostName = "localhost"
serverPort = 8080
address="A4:06:E9:79:ED:16"
sema= threading.Semaphore(0)
id= 0x5b
vcode=None 
stop=True
is_locked = False
pressed = 0



#channel to write to 
CUSTOM_DATA_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"



class BluetoothClient:
    async def send_signal(self,ble):
        global vcode, stop
        if stop:
            vcode=0
        else:
            vcode = self.random_number()
        # send code to bluetooth
        await ble.write_gatt_char(CUSTOM_DATA_UUID, bytes([id, vcode, (id ^ vcode)]))

    def random_number(self):
        return randrange(1, 15)

    
    async def bluetooth_main(self,address):
        async with BleakClient(address) as client:
            while True:
                sema.acquire()
                await self.send_signal(client)
              


class MyServer(BaseHTTPRequestHandler):
    def http_response(self, path):
        self.send_response(200)
        self.send_header("Content-type", self.get_content_type(path))
        self.end_headers()

        with open(path, "rb") as f:
            file_contents = f.read()

        self.wfile.write(file_contents)



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
        global is_locked
        path = "./Client" + self.path
        if path.endswith("/"):
            path = path + "index.html"
        if is_locked and path.endswith("html"): 
            self.http_response("./Client/logged_out.html")
        else:
            self.http_response(path)


    def start_timer():   
        global is_locked
        time.sleep(60)
        is_locked = False 


    def send_mfa_code(self):
        global stop
        self.http_response("./Client/MFA.html")
        stop=False
        sema.release()
      

    def log_in (self,postvars):
        if(bytes('username', encoding='utf8')in postvars ): 
            username = postvars[bytes('username', encoding='utf8')]
            password = postvars[bytes('password', encoding='utf8')]
            password = password[0]
            username = username[0].decode("utf-8")
            hash = sha256(password).hexdigest()
            username_and_password = username + " " + hash

            f = open("./Database/db.txt", "r")
            for line in f:
                if line.strip() == username_and_password:
                    self.send_mfa_code()
                    return
                  
            self.http_response("./Client/index.html")


    def check_verification_code(self, postvars):
        global stop
        if bytes('code', encoding='utf8')in postvars and not bytes('new_code', encoding='utf8')in postvars:
            code = postvars[bytes('code', encoding='utf8')]
            code = code[0].decode("utf-8")
            if code == str(vcode):
                self.http_response("./Client/welcome.html")
                #stop blinking
                stop= True
                sema.release()

            else: 
                self.http_response("./Client/MFA failed.html")



    def new_code(self, postvars):
        global is_locked, pressed
        if bytes('new_code', encoding='utf8')in postvars:
            if pressed < 2: 
               pressed= pressed+1
               self.send_mfa_code() 
            else: 
                 self.http_response("./Client/logged_out.html")
                 is_locked= True
                 threading.Thread(target=MyServer.start_timer).start()


    def do_POST(self):
        global is_locked
        if not is_locked: 
            length = int(self.headers['content-length'])
            postvars = parse_qs(self.rfile.read(length),
                                keep_blank_values=1)
            self.log_in(postvars)                    
            self.check_verification_code( postvars)
            self.new_code(postvars)
        else:
            self.http_response("./Client/logged_out.html")


    #create a thread for the web server
    def web_server_main():
        webServer = HTTPServer((hostName, serverPort), MyServer)
        print("Server started http://%s:%s" % (hostName, serverPort))

        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()
        sema.release()


            
threading.Thread(target=MyServer.web_server_main).start()
bluetooth= BluetoothClient()
asyncio.run(bluetooth.bluetooth_main(address))




## TODO: write fuzz test 
## the test should include a brute force against the code. 

