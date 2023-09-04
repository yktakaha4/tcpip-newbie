#!/usr/bin/env python3

"""ソケットを使って ADD プロトコルを実装したクライアントのスクリプト"""

import socket
import struct


def send_msg(sock, msg):
    """ソケットに指定したバイト列を書き込む関数"""
    # これまでに送信できたバイト数
    total_sent_len = 0
    # 送信したいバイト数
    total_msg_len = len(msg)
    # まだ送信したいデータが残っているか判定する
    while total_sent_len < total_msg_len:
        # ソケットにバイト列を書き込んで、書き込めたバイト数を得る
        sent_len = sock.send(msg[total_sent_len:])
        # まったく書き込めなかったらソケットの接続が終了している
        if sent_len == 0:
            raise RuntimeError('socket connection broken')
        # 書き込めた分を加算する
        total_sent_len += sent_len


def recv_msg(sock, total_msg_size):
    """ソケットから特定のバイト数を読み込む関数"""
    # これまでに受信できたバイト数
    total_recv_size = 0
    # 指定したバイト数を受信できたか判定する
    while total_recv_size < total_msg_size:
        # 残りのバイト列を受信する
        received_chunk = sock.recv(total_msg_size - total_recv_size)
        # 1 バイトも読めなかったときはソケットの接続が終了している
        if len(received_chunk) == 0:
            raise RuntimeError('socket connection broken')
        # 受信したバイト列を返す
        yield received_chunk
        # 受信できたバイト数を加算する
        total_recv_size += len(received_chunk)


def main():
    """スクリプトとして実行されたときに呼び出されるメイン関数"""
    # IPv4 / TCP で通信するソケットを用意する
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ループバックアドレスの TCP/54321 ポートに接続する
    client_socket.connect(('127.0.0.1', 54321))
    # 足し算したい値を用意する
    operand1, operand2 = 1000, 2000
    # 送信する値を確認する
    print(f'operand1: {operand1}, operand2: {operand2}')
    # ネットワークバイトオーダーのバイト列に変換する
    request_msg = struct.pack('!ii', operand1, operand2)
    # ソケットにバイト列を書き込む
    send_msg(client_socket, request_msg)
    # 書き込んだバイト列を表示する
    print(f'sent: {request_msg}')
    # ソケットからバイト列を読み込む
    received_msg = b''.join(recv_msg(client_socket, total_msg_size=8))
    # 読み込んだバイト列を表示する
    print(f'received: {received_msg}')
    # 64 ビットの整数として解釈する
    (added_value, ) = struct.unpack('!q', received_msg)
    # 解釈した値を表示する
    print(f'result: {added_value}')
    # ソケットを閉じる
    client_socket.close()


if __name__ == '__main__':
    """スクリプトのエントリーポイントとしてメイン関数を実行する"""
    main()
