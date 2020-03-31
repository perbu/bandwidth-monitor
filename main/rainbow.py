from machine import Pin, I2C
import ssd1306
import neopixel
import socket


class RainbowMonitor():
    def __init__(self,pin=26,
                 num_pixels=48, rainbow_offset=40):
        # UDP Port to listen on.
        self.num_pixels = num_pixels
        self.rainbow_offset = rainbow_offset
        p = Pin(pin, Pin.OUT)
        self.pixels = neopixel.NeoPixel(p, num_pixels)
        i2c = I2C(1, scl=Pin(22), sda=Pin(21))
        self.oled = ssd1306.SSD1306_I2C(128, 32, i2c)


    def listen(self,port=666):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', port))

# HSV Color wheel.

    def wheel(self,pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            return (0, 0, 0)
        # Shift the phase a bit to make the red bit match the end.
        pos = (pos + self.rainbow_offset) % 256
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        if pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

    def blank(self):
        for i in range(self.num_pixels):
            self.pixels[i] = (0, 0, 0)

    def set_rainbow(self, setpixels, start):
        if setpixels > (self.num_pixels // 2):
            return
        for i in range(start, start + setpixels, 1):
            val = self.wheel((i - start) * 255 // (self.num_pixels // 2))
            self.pixels[i] = val

    def superloop(self):
        # Internal led
        led = Pin(25, Pin.OUT)
        ledstate = True
        while True:
            led.value(ledstate)
            ledstate = not ledstate
            rx, tx = 0, 0
            try:
                data, addr = self.sock.recvfrom(1024)
            except Exception as e:
                print('Network error', e)
            try:
                data = data.decode('ascii')
                rx, tx, relrx, reltx = data.split(' ', 4)
                relrx = float(relrx)
                reltx = float(reltx)
                rx = int(rx)
                tx = int(tx)
            except Exception as e:
                print('Parser error', e) 


            self.oled.fill(0)
            if (relrx > 5 or reltx > 5):
                self.oled.text('RX: {:5.2f}%'.format(relrx),0,0)
                self.oled.text('TX: {:5.2f}%'.format(reltx),0,10)
            
            self.oled.show()
            self.blank()
            self.set_rainbow(rx, 0)
            self.set_rainbow(tx, (self.num_pixels // 2))
            self.pixels.write()
