#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import socket
import multiprocessing
import threading


def worker_thread(serversocket, process_number, thread_number):
    """クライアントとの接続を処理するハンドラ（スレッド）"""
    while True:
        # クライアントからの接続を待ち受ける（接続されるまでブロックする）
        # ワーカースレッド同士でクライアントからの接続を奪い合う
        clientsocket, (client_address, client_port) = serversocket.accept()
        print('Thread: {0}, Process: {1}'.format(thread_number, process_number))
        print('New client: {0}:{1}'.format(client_address, client_port))

        while True:
            try:
                sent_message = clientsocket.recv(1024)
                print('Recv: {0} from {1}:{2}'.format(sent_message, client_address, client_port))
            except OSError:
                break

            if len(sent_message) == 0:
                break

            message = sent_message
            while True:
                sent_len = clientsocket.send(message)
                if sent_len == len(message):
                    break
                sent_message = sent_message[sent_len:]
            print('Send: {0} to {1}:{2}'.format(message, client_address, client_port))
        
        clientsocket.close()
        print('Bye-Bye: {0}:{1}'.format(client_address, client_port))


def worker_process(serversocket, process_number):
    """クライアントとの接続を受け付けるハンドラ（プロセス）"""

    # サーバソケットを渡してワーカースレッドを起動する
    NUMBER_OF_THREADS = 10
    for thread_number in range(NUMBER_OF_THREADS):
        thread = threading.Thread(target=worker_thread, args=(serversocket, process_number, thread_number))
        thread.start()
        # ここではワーカーをデーモンスレッドにする必要はない（死ぬときはプロセスごと逝くので）
    
    while True:
        # ワーカープロセスのメインスレッドは遊ばせておく
        time.sleep(1)


def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    host = 'localhost'
    port = 37654

    serversocket.bind((host, port))
    serversocket.listen(128)

    NUMBER_OF_PROCESSES = multiprocessing.cpu_count()
    for process_number in range(NUMBER_OF_PROCESSES):
        process = multiprocessing.Process(target=worker_process, args=(serversocket, process_number))

        process.daemon = True
        process.start()
    
    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
