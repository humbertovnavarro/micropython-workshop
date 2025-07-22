from machine import Pin, I2C
import time
import framebuf
import neopixel

# SH1106 constants
WIDTH = 128
HEIGHT = 64
I2C_ADDR = 0x3C

# I2C setup
SCL = 35
SDA = 33
i2c = I2C(scl=Pin(SCL), sda=Pin(SDA), freq=400000)

# Allocate framebuffer (1024 bytes for 128x64 monochrome display)
buffer = bytearray(WIDTH * HEIGHT // 8)
fb = framebuf.FrameBuffer(buffer, WIDTH, HEIGHT, framebuf.MONO_VLSB)

# SH1106 low-level commands (since no built-in SH1106 framebuffer driver)
def write_cmd(cmd):
    i2c.writeto(I2C_ADDR, b'\x00' + bytearray([cmd]))

def init_display():
    cmds = [
        0xAE,  # Display off
        0xD5, 0x80,  # Clock divide
        0xA8, 0x3F,  # Multiplex
        0xD3, 0x00,  # Display offset
        0x40,        # Start line
        0xAD, 0x8B,  # Charge pump
        0xA1,        # Segment remap
        0xC8,        # COM scan dec
        0xDA, 0x12,  # COM pins
        0x81, 0xCF,  # Contrast
        0xD9, 0xF1,  # Precharge
        0xDB, 0x40,  # Vcom detect
        0xA4,        # Resume RAM content
        0xA6,        # Normal display
        0xAF         # Display ON
    ]
    for cmd in cmds:
        write_cmd(cmd)

def update_display():
    for page in range(HEIGHT // 8):
        write_cmd(0xB0 + page)       # Set page start
        write_cmd(0x02)              # Set lower column address
        write_cmd(0x10)              # Set higher column address
        i2c.writeto(I2C_ADDR, b'\x40' + buffer[WIDTH * page : WIDTH * (page + 1)])

# Initialize display
init_display()

# Counter logic
num = 0
last_num = -1

while True:
    if num != last_num:
        fb.fill(0)  # Clear framebuffer
        fb.text(str(num), 0, 0, 1)
        update_display()
        last_num = num
    num += 1
