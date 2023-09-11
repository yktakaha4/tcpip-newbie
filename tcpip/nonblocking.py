#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket


def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # ソケットをノンブロッキングモードにする
    serversocket.setblocking(False)

    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    host = 'localhost'
    port = 37654

    serversocket.bind((host, port))
    serversocket.listen(128)

    while True:
        clientsocket, (client_address, client_port) = serversocket.accept()
        print('New client: {0}:{1}'.format(client_address, client_port))

        while True:
            try:
                message = clientsocket.recv(1024)
                print('Recv: {0} from {1}:{2}'.format(message, client_address, client_port))
            except OSError:
                break

            if len(message) == 0:
                break

            sent_message = message
            while True:
                sent_len = clientsocket.send(sent_message)
                if sent_len == len(sent_message):
                    break

                sent_message = sent_message[sent_len:]
            print('Send: {0} to {1}:{2}'.format(message, client_address, client_port))

        clientsocket.close()
        print('Bye-Bye: {0}:{1}'.format(client_address, client_port))


if __name__ == '__main__':
    main()
