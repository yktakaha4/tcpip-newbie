#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import socket
import threading


def worker_thread(serversocket):
    """クライアントとの接続を処理するハンドラ"""
    while True:
        # クライアントからの接続を待ち受ける（接続されるまでブロックする）
        # ワーカスレッド同士でクライアントからの接続を奪い合う
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


def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    host = 'localhost'
    port = 37654
    serversocket.bind((host, port))

    serversocket.listen(128)

    # サーバソケットを渡してワーカースレッドを起動する
    NUMBER_OF_THREADS = 10
    for _ in range(NUMBER_OF_THREADS):
        thread = threading.Thread(target=worker_thread, args=(serversocket,))
        thread.daemon = True
        thread.start()

    while True:
        # メインスレッドは遊ばせておく（ハンドラを処理させても構わない）
        time.sleep(1)


if __name__ == '__main__':
    main()
