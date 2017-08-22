# coding=utf-8
import socket
from threading import Thread

from app.modules.logging import Loggers

BUFFER_SIZE = 1024


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

    def start_listening(self, ip, port, callback):
        """
        Start listening for data on the specified ip address and port.

        Args:
            ip: The IP-address of the sender of the data. An ip of "0.0.0.0" corresponds to all ip's available op IPv4.
            port: The port on which should be listened
            callback: Called when a new packet is received

        Returns: - (use the parameter callback to retrieve the data contained in the packet)

        """
        if self.thread_listen_run:
            self.logger.warning("Ignored start recording - already recording")
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((ip, port))
            self.thread_listen_run = True
            self.thread_listen = Thread(target=self.listen_for_packets, args=(sock, callback))
            self.thread_listen.start()

    def stop_listening(self):
        if self.thread_listen_run:
            self.thread_listen_run = False
        else:
            self.logger.warning("Ignored stop recording - was not recording")

    def listen_for_packets(self, sock, callback):
        while self.thread_listen_run:
            msg = bytearray(BUFFER_SIZE)
            sock.recv_into(msg)
            self.logger.user_input("Received message: " + str(msg))
            callback(msg)
