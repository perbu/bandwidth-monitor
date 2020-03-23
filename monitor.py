#!/usr/bin/env python3

import logging
import time
import sys
import socket
from collections import deque

UDP_IP = "192.168.1.87"
UDP_PORT = 666

# Max bandwidth in bytes per second. Should be measured.
bandwidth = 20280480
pixels = 24
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM)


def get_rx_tx():
    res = []
    for op in ['rx', 'tx']:
        with open(f'/sys/class/net/eth0/statistics/{op}_bytes') as f:
            res.append(int(f.read()))
    return res


def superloop():
    first_run = True
    rx0 = 0
    rx1 = 0
    tx0 = 1
    tx1 = 1
    t0 = 1
    t1 = 1
    smooth_rx = deque(maxlen=3)
    smooth_tx = deque(maxlen=3)

    while True:
        rx0, tx0 = get_rx_tx()
        t0 = time.time()
        if not first_run:
            time_delta = t0 - t1 # float, secs
            rxd = int((rx0 - rx1) / time_delta)
            txd = int((tx0 - tx1) / time_delta)

            rel_rxd = rxd / bandwidth
            rel_txd = txd / bandwidth 
            pix_rxd = int(rel_rxd * pixels)
            pix_txd = int(rel_txd * pixels)
            smooth_rx.append(pix_rxd)
            smooth_tx.append(pix_txd)

            avg_rxd = sum(smooth_rx) // 3
            avg_txd = sum(smooth_tx) // 3
            MESSAGE = f"{avg_rxd} {avg_txd}"
            print(MESSAGE)
            MESSAGE = MESSAGE.encode('ascii')
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

        first_run = False
        rx1 = rx0
        tx1 = tx0
        t1 = t0
        time.sleep(0.1)
        
superloop()
