import socket
from multiprocessing import Process
import time




class Client:

    def __init__(self, host, port):
        self.k = Process(target=self.process_killer(), name='resv')
        self.p = Process(target=self.ansver(), name='resv')
        self.host = host
        self.port = port
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = None

    def connect_serv(self):
        self.tcp_socket.connect((self.host, self.port))

    def disconnect_serv(self):
        self.tcp_socket.close()

    def send(self, send):
        self.tcp_socket.send(send.encode("ascii"))

    def ansver(self):
        socket.setdefaulttimeout(5) # в документации я не нашел как именно прекращается процесс
                                    # выполнения ошибкой или нулём по идее это время ожидания ответа
        try:
            ans = self.tcp_socket.recv(1024)
            if not ans:
                self.status = 0
            self.status = ans
            self.process_killer()
        except:
            self.status = 0

    def thread_send_ansver(self, send):      #если setdefaulttimeout работает то можно обойтись без потоков
        self.send(send)
        self.p.start()
        self.k.start()
        return self.status_now()

    def process_killer_timer(self): # для уничтожение потоков в потоке в качестве таймера
        time.sleep(5)
        self.p.terminate()
        self.k.terminate()

    def process_killer(self): # уничтожение потоков в основной программе при успешном ответе
        self.p.terminate()
        self.k.terminate()

    def rewrite_status(self, new_st):   # изменение статуса ответа или не ответа
        self.status = new_st

    def status_now(self):
        return self.status



def main():
    client = Client(input(), input()) # я не уверен как будет передаваться хост и порт
    ans1 = client.thread_send_ansver('INIT_CIRC')



if __name__ == '__main__':
    main()