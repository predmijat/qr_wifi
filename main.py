import time

import framebuf
from machine import Pin, SPI

DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9


class Screen(framebuf.FrameBuffer):
    def __init__(self):
        self.column = None
        self.width = 128
        self.height = 64

        self.cs = Pin(CS, Pin.OUT)
        self.rst = Pin(RST, Pin.OUT)

        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1, 2000_000)
        self.spi = SPI(
            1, 20000_000, polarity=0, phase=0, sck=Pin(SCK), mosi=Pin(MOSI), miso=None
        )
        self.dc = Pin(DC, Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width // 8)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_HMSB)
        self.init_display()

        self.white = 0xFFFF
        self.black = 0x0000

    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize display"""
        self.rst(1)
        time.sleep(0.001)
        self.rst(0)
        time.sleep(0.01)
        self.rst(1)

        self.write_cmd(0xAE)  # turn off OLED display

        self.write_cmd(0x00)  # set lower column address
        self.write_cmd(0x10)  # set higher column address

        self.write_cmd(0xB0)  # set page address

        self.write_cmd(0xDC)  # set display start line
        self.write_cmd(0x00)
        self.write_cmd(0x81)  # contract control
        self.write_cmd(0x6F)  # 128
        self.write_cmd(0x21)  # Set Memory addressing mode (0x20/0x21) #

        self.write_cmd(0xA0)  # set segment remap
        self.write_cmd(0xC0)  # Com scan direction
        self.write_cmd(0xA4)  # disable Entire Display On (0xA4/0xA5)

        self.write_cmd(0xA6)  # normal / reverse
        self.write_cmd(0xA8)  # multiplex ratio
        self.write_cmd(0x3F)  # duty = 1/64

        self.write_cmd(0xD3)  # set display offset
        self.write_cmd(0x60)

        self.write_cmd(0xD5)  # set osc division
        self.write_cmd(0x41)

        self.write_cmd(0xD9)  # set pre-charge period
        self.write_cmd(0x22)

        self.write_cmd(0xDB)  # set vcomh
        self.write_cmd(0x35)

        self.write_cmd(0xAD)  # set charge pump enable
        self.write_cmd(0x8A)  # Set DC-DC enable (a=0:disable; a=1:enable)
        self.write_cmd(0xAF)

    def show(self):
        self.write_cmd(0xB0)
        for page in range(0, 64):
            self.column = 63 - page
            self.write_cmd(0x00 + (self.column & 0x0F))
            self.write_cmd(0x10 + (self.column >> 4))
            for num in range(0, 16):
                self.write_data(self.buffer[page * 16 + num])


msg = [
    "##################################################",
    "#                                                #",
    "#                                                #",
    "#                                                #",
    "#                                  ##            #",
    "#     #####  #### ####  # ###    ###### ####     #",
    "#    ##     ##       ## ##  ##     ##  ##  ##    #",
    "#     ####  ##    ##### ##  ##     ##  ##  ##    #",
    "#        ## ##   ##  ## ##  ##     ##  ##  ##    #",
    "#    #####   #### ### # ##  ##      ### ####     #",
    "#                                                #",
    "#                                                #",
    "#                                                #",
    "#                                                #",
    "#      ##           ##                           #",
    "#           ####        # ###             #      #",
    "#      ##  ##  ##  ###  ##  ##            ##     #",
    "#      ##  ##  ##   ##  ##  ##   ############    #",
    "#      ##  ##  ##   ##  ##  ##            ##     #",
    "#      ##   ####   #### ##  ##            #      #",
    "#    ###                                         #",
    "#                                                #",
    "#                                                #",
    "#                                                #",
    "#                                                #",
    "#    ##    ##    ##          ###### ##           #",
    "#    ##    ##                ##                  #",
    "#    ##    ##   ###   ####   ####  ###           #",
    "#    ## ## ##    ##          ##     ##           #",
    "#    ########    ##          ##     ##           #",
    "#    ##    ##   ####         ##    ####          #",
    "#                                                #",
    "#                                                #",
    "#                                                #",
    "#                                                #",
    "##################################################",
    "#                                                #",
    "#                                                #",
    "#                                                #",
    "#                                                #",
    "#    ##### # ###   ####         # ###   #####    #",
    "#   ##     ##  ## ##  ##        ##  ## ##        #",
    "#    ####  ##     ######        ##      ####     #",
    "#       ## ##     ##       ##   ##         ##    #",
    "#   #####  ##      ####    ##   ##     #####     #",
    "#                                                #",
    "#                                                #",
    "#                                                #",
    "#                                                #",
    "##################################################",
]

qr_code = [
# qr_code_start
# qr_code_end
]


if __name__ == "__main__":
    OLED = Screen()
    while True:
        OLED.fill(0x0000)

        y = 7
        for row in msg:
            x = 7
            for ch in row:
                if ch == "#":
                    OLED.pixel(x, y, OLED.white)
                else:
                    OLED.pixel(x, y, OLED.black)
                x += 1
            y += 1

            OLED.show()

        y = 7
        for row in qr_code:
            x = 68
            for ch in row:
                if ch == "#":
                    OLED.pixel(x, y, OLED.white)
                else:
                    OLED.pixel(x, y, OLED.black)
                x += 1
            y += 1

            OLED.show()

        time.sleep(20)

