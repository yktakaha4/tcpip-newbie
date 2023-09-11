#!/usr/bin/env python

import socket


def main():
    # IPv4/TCP のソケットを用意する
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 'Address already in use' の回避策（必須ではない）
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    # 待ち受けるアドレスとポートを指定する
    # もし任意のアドレスで Listen したいときは '' を使う
    host = 'localhost'
    port = 37654
    serversocket.bind((host, port))

    # クライアントをいくつまでキューイングするか
    serversocket.listen(128)

    while True:
        # クライアントからの接続を待ち受ける（接続されるまでブロックする）
        clientsocket, (client_address, client_port) = serversocket.accept()
        print('New client: {0}:{1}'.format(client_address, client_port))

        while True:
            # クライアントソケットから指定したバッファバイト数だけデータを受け取る
            try:
                message = clientsocket.recv(1024)
                print('Recv: {}'.format(message))
            except OSError:
                break
                
            # 受信したデータの長さが 0 ならクライアントからの切断を表す
            if len(message) == 0:
                break

            # 受信したデータをそのまま送り返す（エコー）
            sent_message = message
            while True:
                # 送信できたバイト数が返ってくる
                sent_len = clientsocket.send(sent_message)
                # 全て遅れたら完了
                if sent_len == len(sent_message):
                    break
                # 送れなかった分をもう一度送る
                sent_message = sent_message[sent_len:]
            print('Send: {}'.format(message))

        # 後始末
        clientsocket.close()
        print('Bye-Bye: {0}:{1}'.format(client_address, client_port))


if __name__ == '__main__':
    main()
