from colorama import init, Fore, Style
import sys, json, socket

class Socket:
    def __init__(self):
        self.log = NatsumeLogger("Socket")
        self.host = "api.vndb.org"
        self.port = 19534
        self.ADDR = (self.host, self.port)
        self.end = b'\x04'
        self.client : socket.socket = None

    def connect(self):
        if not self.client:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(self.ADDR)

            self.log.info("Client Connected!")

    def disconnect(self):
        if self.client:
            self.client.close()
            self.client = None
            self.log.warning("Client isn't connected anymore!")

    def login(self):
        cred = {
            "protocol": 1,
            "client": "natsume-vndb",
            "clientver": "0.1-alpha"
        }
        
        self.communicate(f"login {json.dumps(cred)}")

    def send(self, message):
        msg = message.encode()
        msg += self.end
        self.log.info(message)
        msgLength = 0
        while msgLength < len(message):
            sent = self.client.send(msg)
            if sent == 0:
                self.log.error("Message failed to sent!")
                return
            msgLength += sent

    def receive(self):
        chunks = []
        while True:
            chunk = self.client.recv(1024)
            self.log.info("Receiving data...")
            if chunk.endswith(self.end):
                chunk = chunk.rstrip(self.end)
                chunks.append(chunk)
                break
            chunks.append(chunk)
        response = b"".join(chunks)
        self.log.info(f"Response: {response.decode()}")
        return response

    def communicate(self, message):
        self.send(message)
        return self.receive()

class NatsumeLogger:
    def __init__(self, host):
        self.name = "Natsume Logger"
        self.ver = "1.0"
        self.utils = NatsumeUtils()
        self.host = host or "Module"

    def info(self, msg):
        sys.stdout.write(f"{self.utils.MAGENTA}[{self.host}]{self.utils.BLUE} {msg}{self.utils.CLR}\n")        

    def error(self, msg):
        sys.stdout.write(f"{self.utils.MAGENTA}[{self.host}]{self.utils.RED} {msg}{self.utils.CLR}\n")        

    def warning(self, msg):
        sys.stdout.write(f"{self.utils.MAGENTA}[{self.host}]{self.utils.GREEN} {msg}{self.utils.CLR}\n")        

class NatsumeUtils:
    def __init__(self):
        self.name = "Natsume Utils"
        self.ver = "1.0"

        self.RED = Fore.RED
        self.BLUE = Fore.BLUE
        self.GREEN = Fore.GREEN
        self.MAGENTA = Fore.MAGENTA
        self.CLR = Style.RESET_ALL

    def printInfo(self, msg):
        sys.stdout.write(f"{self.MAGENTA}[INFO]{self.BLUE} {msg}{self.CLR}\n")     

       
