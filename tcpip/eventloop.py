#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket 
import select


# 読み取りが可能になるまで待っているソケットと、可能になったときに呼び出されるハンドラ・引数の対応を持つ
read_waiters = {}
# 書き込みが可能になるまで待っているソケットと、可能になったときに呼び出されるハンドラ・引数の対応を持つ
write_waiters = {}
# 接続してきたクライアントとの接続情報を格納する
connections = {}


def accept_handler(serversocket):
    """サーバソケットが読み取り可能になったとき呼ばれるハンドラ"""
    # 準備ができているので、すぐに accept() できる
    clientsocket, (client_address, client_port) = serversocket.accept()

    # クライアントソケットもノンブロックモードにする
    clientsocket.setblocking(False)

    # 接続してきたクライアントの情報を出力する
    # ただし、厳密に言えば print() もブロッキング I/O なので避けるべき
    print('New client: {0}:{1}'.format(client_address, client_port))

    # ひとまずクライアントの一覧に入れておく
    connections[clientsocket.fileno()] = (clientsocket, client_address, client_port)

    # 次はクライアントのソケットが読み取り可能になるまでまつ
    read_waiters[clientsocket.fileno()] = (recv_handler, (clientsocket.fileno(), ))

    # 次のクライアントからの接続を待ち受ける
    read_waiters[serversocket.fileno()] = (accept_handler, (serversocket, ))


def recv_handler(fileno):
    """クライアントソケットが読み取り可能になったとき呼ばれるハンドラ"""
    def terminate():
        """クライアントとの接続が切れた時の後始末"""
        # クライアント一覧から取り除く
        del connections[clientsocket.fileno()]
        # ソケットを閉じる
        print('Bye-Bye: {0}:{1}'.format(client_address, client_port))

    # クライアントとの接続情報を取り出す
    clientsocket, client_address, client_port = connections[fileno]

    try:
        # 準備ができているので、すぐに recv() できる
        message = clientsocket.recv(1024)
    except OSError:
        terminate()
        return
    
    if len(message) == 0 :
        terminate()
        return

    print('Recv: {0} to {1}:{2}'.format(message, client_address, client_port))

    # 次はクライアントのソケットが書き込み可能になるまで待つ
    write_waiters[fileno] = (send_handler, (fileno, message))


def send_handler(fileno, message):
    """クライアントソケットが書き込み可能になったとき呼ばれるハンドラ"""
    # クライアントとの接続情報を取り出す
    clientsocket, client_address, client_port = connections[fileno]

    # 準備ができているので、すぐに send() できる
    sent_len = clientsocket.send(message)
    print('Send: {0} to {1}:{2}'.format(message, client_address, client_port))

    if sent_len == len(message):
        # 全て送ることができたら、次はまたソケットが読み取れるようになるのを待つ
        read_waiters[clientsocket.fileno()] = (recv_handler, (clientsocket.fileno(), ))
    
    else:
        # 送り残している内容があったら、再度ソケットが書き込み可能になるまで待つ
        write_waiters[fileno] = (send_handler, (fileno, message[sent_len:]))
    

def main():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # ソケットをノンブロックモードにする
    serversocket.setblocking(False)

    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    host = 'localhost'
    port = 37654
    serversocket.bind((host, port))

    serversocket.listen(128)

    # クライアントからの接続がくるまで待つ
    read_waiters[serversocket.fileno()] = (accept_handler, (serversocket, ))

    while True:
        # ソケットが読み取り・書き込み可能になるまで待つ
        # https://docs.python.org/ja/3/library/select.html#select.select
        rlist, wlist, _ = select.select(read_waiters.keys(), write_waiters.keys(), [], 60)

        # 読み取り可能になったソケット（のファイル番号）の一覧
        for r_fileno in rlist:
            # 読み取り可能になったときに呼んでほしいハンドラを取り出す
            handler, args = read_waiters.pop(r_fileno)
            # ハンドラを実行する
            handler(*args)

        # 書き込み可能になったソケット（のファイル番号）の一覧
        for w_fileno in wlist:
            # 書き込み可能になったときに呼んでほしいハンドラを取り出す
            handler, args = write_waiters.pop(w_fileno)
            # ハンドラを実行する
            handler(*args)


if __name__ == '__main__':
    main()
