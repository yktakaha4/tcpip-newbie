#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time


def loop():
    """書くスレッドは特に何もしない"""
    while True:
        time.sleep(1)


def main():
    # ネイティブスレッドをたくさん起動してみる
    for _ in range(10000):
        t = threading.Thread(target=loop)
        t.daemon = True
        t.start()
        # 動作中のスレッド数を出力する
        print(threading.active_count())


if __name__ == '__main__':
    main()
