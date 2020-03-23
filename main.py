from machine import Pin
import neopixel
import time
import socket

# UDP Port to listen on.
port = 666
pixel_pin = 14
num_pixels = 48

rainbow_offset = 40

# HSV Color wheel.
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    # Shift the phase a bit to make the red bit match the end.
    pos = (pos + rainbow_offset) % 256
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

def blank(strip):
    for i in range(num_pixels):
        strip[i] = (0,0,0)


def set_rainbow(strip, setpixels, start):
    if setpixels > (num_pixels // 2):
        return
    for i in range(start, start + setpixels, 1):
        val = wheel((i - start) * 255 // (num_pixels // 2))
        strip[i] = val


def superloop(strip, s):
    while True:
        rx, tx= 0,0
        blank(pixels)
        data,addr = s.recvfrom(1024)
        data = data.decode('ascii')
        rx, tx = data.split(' ', 2)
        rx = int(rx)
        tx = int(tx)
        set_rainbow(pixels, rx, 0)
        set_rainbow(pixels, tx, (num_pixels//2))
        pixels.write()


pin = Pin(pixel_pin, Pin.OUT)
pixels = neopixel.NeoPixel(pin, num_pixels)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0',port))
print('Listening for UDP packets on port ', port)
superloop(pixels, sock)




