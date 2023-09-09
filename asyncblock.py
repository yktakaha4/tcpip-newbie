#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import time
from typing import Optional


class EchoServer(asyncio.Protocol):
    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        self.transport = transport

        client_address, client_port = self.transport.get_extra_info('peername')
        print('New client: {0}:{1}'.format(client_address, client_port))

    def data_received(self, data: bytes) -> None:
        client_address, client_port = self.transport.get_extra_info('peername')
        print('Recv: {0} to {1}:{2}'.format(data, client_address, client_port))

        # 何らかの処理で、イベントループのスレッドがブロックしてしまった！
        print('Go to sleep...')
        time.sleep(20)

        self.transport.write(data)
        print('Send: {0} to {1}:{2}'.format(data, client_address, client_port))

    def connection_lost(self, exc: Optional[Exception]) -> None:
        client_address, client_port = self.transport.get_extra_info('peername')
        print('Bye-Bye: {0}:{1}'.format(client_address, client_port))
        self.transport.close()


def main():
    host = 'localhost'
    port = 37654

    ev_loop = asyncio.get_event_loop()
    factory = ev_loop.create_server(EchoServer, host, port)
    server = ev_loop.run_until_complete(factory)

    try:
        ev_loop.run_forever()
    finally:
        server.close()
        ev_loop.run_until_complete(server.wait_closed())
        ev_loop.close()


if __name__ == '__main__':
    main()
