# Bandwidth monitor

Silly little toy that consists of two components. One runs on a MicroPython MCU with a WS2812b lightstrip (or ring) attached. This is main.py.

The other runs on your router, monitor.py. It monitors /sys/class/net/eth0/statistics/(rx|tx)_bytes about ten times per second, smooths it out a bit and then constructs the UDP packet that is sent to the MCU.

This code isn't beutiful. I might clean it up if I get to give a talk about MicroPython.

[![Micropython bandwidth monitor demo](http://img.youtube.com/vi/d9chaeEB2X0/0.jpg)](http://www.youtube.com/watch?v=d9chaeEB2X0 "Micropython bandwidth monitor")