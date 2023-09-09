#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 標準ライブラリにモンキーパッチを当てる
# ブロッキング I/O を使った操作が裏側で全てノンブロッキング I/O を使うように書き換えられる
import os
import eventlet
if not os.environ.get('EVENTLET_DISABLED'):
    eventlet.monkey_patch()

import socket
import threading
import time


def client_handler(clientsocket, client_address, client_port):
    """クライアントとの接続を処理するハンドラ"""
    while True:
        try:
            message = clientsocket.recv(1024)
            print('Recv: {0} from {1}:{2}'.format(message,
                                                  client_address,
                                                  client_port))
        except OSError:
            break

        if len(message) == 0:
            break

        time.sleep(10)

        sent_message = message
        while True:
            sent_len = clientsocket.send(sent_message)
            if sent_len == len(sent_message):
                break
            sent_message = sent_message[sent_len:]
        print('Send: {0} to {1}:{2}'.format(message,
                                            client_address,
                                            client_port))

    clientsocket.close()
    print('Bye-Bye: {0}:{1}'.format(client_address, client_port))


def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    host = 'localhost'
    port = 37564
    serversocket.bind((host, port))

    serversocket.listen(128)

    while True:
        clientsocket, (client_address, client_port) = serversocket.accept()
        print('New client: {0}:{1}'.format(client_address, client_port))

        client_thread = threading.Thread(target=client_handler,
                                         args=(clientsocket,
                                               client_address,
                                               client_port))
        client_thread.daemon = True
        client_thread.start()


if __name__ == '__main__':
    main()
