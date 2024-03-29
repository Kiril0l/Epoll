import socket
import select
import argparse
import random


SERVER_HOST = "127.0.0.1"
EOL1 = b"\n\n"
EOL2 = b"\n\r\n"
SERVER_RESPONSE = [
    "http://actravel.ru/country_codes.html",
    "https://github.com/Kiril0l?tab=repositories",
    "https://openweathermap.org/current"
]

class EpollServer(object):
    def __init__ (self, host=SERVER_HOST, port=0):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((host,port))
        self.sock.listen(1)
        self.sock.setblocking(0)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        print("Started Epoll Server")
        self.epoll =select.epoll()
        self.epoll.register(self.sock.fileno(), select.EPOLLIN)


    def visit():
        pass

    def run(self):
        connections = {};
        requests = {};
        responses = {}
        events = self.epoll.poll(1)
        data = requests.get(SERVER_RESPONSE[random.randint(0, 2)])
        for key, value in data.headers.items():
            lines.append(f"{key} {value}")
        header = "\r\n".join(lines + ["\r\n\r\n"])
        html = data.text
        self.response = f"{header}{html}".encode("utf-8")
        try:
            while True:
                events = self.epoll.poll(1)
                for fileno, event in events:
                    if fileno == self.sock.fileno():
                        connection, address = self.sock.accept()
                        connection.setblocking(0)
                        self.epoll.register(
                            connection.fileno(),
                            select.EPOLLIN
                        )
                        connections[connection.fileno()] = connection
                        requests[connection.fileno()] = b''
                    elif event & select.EPOLLIN:
                        requests[fileno] += connections[fileno].recv(1024)
                        if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
                            self.epoll.modify(fileno, select.EPOLLOUT)
                            print('-'*40, '\n', requests[fileno].decode()[:-2], sep="")
                    elif event & select.EPOLLOUT:
                        byteswritten = connections[fileno].send(responses[fileno])
                        responses[fileno] = responses[fileno][byteswritten:]
                        if len(responses[fileno]) == 0:
                            self.epoll.modify(fileno, 0)
                            connections[fileno].shutdown(socket.SHUT_RDWR)
                    elif event & select.EPOLLHUP:
                        self.epoll.unregister(fileno)
                        connections[fileno].close()
                        del connections[fileno]
        finally:
            self.epoll.unregister(self.sock.fileno())
            self.epoll.close()
            self.sock.close()

if __name__ == '__main__':
    parser=argparse.ArgumentParser(
        description='Spcket Server Example with Epoll'
    )
    parser.add_argument(
        '--port',
        action="store",
        dest="port",
        type=int,
        required=True
    )
    given_args = parser.parse_args()
    port = given_args.port
    server = EpollServer(host=SERVER_HOST, port=port)
    server.run()

# ключ хост он не обязательный
# метод, который будет хранить 4 ссылки/ делаем метод, который идет на сайт и приносит ответ в респонсис
