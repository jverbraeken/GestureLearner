# coding=utf-8
import socket
from threading import Thread

from app.modules.logging import Loggers

BUFFER_SIZE = 12


def register(service_locator):
    UDPScanner.service_locator = service_locator
    service_locator.udp_scanner = UDPScanner(service_locator)





class UDPScanner:
    service_locator = None
    thread_listen = None
    thread_listen_run = False
    logger = None

    def __init__(self, service_locator):
        self.service_locator = service_locator
        self.logger = self.service_locator.logger_factory.get_logger(Loggers.udp_scanner)

    def start_listening(self, ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((ip, port))
        self.thread_listen_run = True
        self.thread_listen = Thread(target=self.listen_for_packets, args=(sock,))
        self.thread_listen.start()

    def stop_listening(self):
        self.thread_listen_run = False

    def listen_for_packets(self, sock):
        while self.thread_listen_run:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            self.logger.user_input("received message: " + str(data))
