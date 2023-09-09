#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from typing import Optional


class EchoServer(asyncio.Protocol):
    def connection_made(self, transport: asyncio.Transport) -> None:
        """クライアントからの接続があったときに呼ばれるイベントハンドラ"""
        # 接続をインスタンス変数として保存する
        self.transport = transport

        # 接続元の情報を出力する
        client_address, client_port = self.transport.get_extra_info('peername')
        print('New client: {0}:{1}'.format(client_address, client_port))

    def data_received(self, data: bytes) -> None:
        """クライアントからデータを受信したときに呼ばれるイベントハンドラ"""
        # 受信した内容を出力する
        client_address, client_port = self.transport.get_extra_info('peername')
        print('Data received from {0}:{1}: {2}'.format(client_address, client_port, data))

        # 受信したのと同じ内容を返信する
        self.transport.write(data)
        print('Send: {0} to {1}:{2}'.format(data, client_address, client_port))

    def connection_lost(self, exc: Optional[Exception]) -> None:
        """クライアントとの接続が切れたときに呼ばれるイベントハンドラ"""
        # 接続が切れたら後始末をする
        client_address, client_port = self.transport.get_extra_info('peername')
        print('Bye-Bye: {0}:{1}'.format(client_address, client_port))
        self.transport.close()


def main():
    host = 'localhost'
    port = 37654

    # イベントループを用意する
    ev_loop = asyncio.get_event_loop()

    # 指定したアドレスとポートでサーバを作る
    factory = ev_loop.create_server(EchoServer, host, port)
    # サーバを起動する
    server = ev_loop.run_until_complete(factory)

    try:
        # イベントループを起動する
        ev_loop.run_forever()
    finally:
        # 後始末
        server.close()


if __name__ == '__main__':
    main()
