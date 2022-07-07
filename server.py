import network
import socket
from machine import I2C, SoftI2C, Pin, ADC, PWM
from time import sleep_ms, sleep
import struct
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

def onClick(blogerNumber : int):
    global sock
    global lcd
    global blogers
    global button
    global client
    try:
        print('Client connected:' + str(address))
        sleep(1)
        while True:
            client.sendall('subs ' + str(blogerNumber))
            sleep_ms(300)

            btn_val = button.value()
            if btn_val == False:
                choosing()
            data = client.recv(256)
            if data:
                lcd.clear()
                lcd.putstr(blogers[blogerNumber] + ' subs:' + str(data.decode()))
    except Exception as e:
        print(e)
    finally:
        client.close()
        sock.close()
        lcd.clear()

def choosing():
    global blogers
    global jx
    global button
    global lcd
    global client
    cur = 0
    lenBlogers = len(blogers) #4
    lcd.clear()
    lcd.putstr(blogers[cur] + ' ' * (16-len(blogers[cur])))
    sleep(1)
    while True:
        sleep_ms(300)
        jx_val = jx.read()
        print(jx_val)
        btn_val = button.value()
        if btn_val == False:
            lcd.clear()
            onClick(cur)
            return
        if(jx_val < 2400 and jx_val > 1700):
            continue
        #mid is 2100
        if(jx_val<1700):
            if cur != 0:
                lcd.clear()
                cur-=1
                lcd.putstr(blogers[cur] + ' ' * (16-len(blogers[cur])))
        else:
            if cur != lenBlogers-1:
                lcd.clear()
                cur+=1
                lcd.putstr(blogers[cur] + ' ' * (16-len(blogers[cur])))


wlan = network.WLAN(network.STA_IF) # create station interface
print(wlan.active(True))       # activate the interface
print(wlan.scan())             # scan for access points
wlan.connect('Owl', 'fuckyourself') # connect to an AP

while True:
    if wlan.isconnected():
        print('connected')
        break
    else:
        print('ne connected')
        sleep_ms(250)
print(wlan.ifconfig())      # get the interface's IP/netmask/gw/DNS addresses
#wlan.ifconfig(('192.168.0.4', '255.255.255.0', '192.168.0.1', '8.8.8.8')) # set config of network

#Creating a socket
host, port = '192.168.43.20',9900
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port))
sock.listen(3)
client, address = sock.accept()
#Setting up the joystick
x_pin = 34
jx = ADC(Pin(x_pin))
button = Pin(4, Pin.IN, Pin.PULL_UP)
jx.width(ADC.WIDTH_12BIT)
jx.atten(ADC.ATTN_11DB)

#Setting up the panel
i2c = SoftI2C(scl = Pin(32), sda = Pin(33), freq = 10000)
I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

blogers = ['Mr.Max', 'PewDiePie', 'Toples', 'Lololoshka']

#Start of the code
lcd.putstr('Choose your bloger')
sleep(2)
choosing()
