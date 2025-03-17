# We tried to implement communication between our Raspberry Pi and ESP32 through the same
# nRF24L01+ module, but with various library issues and the SPI pin not being active
# on the same board, we decided to not implement this test code and used Bluetooth Low Energy instead
# Writted and implemented by Anthony Sandi

import lgpio
import time
import spidev
from pyrf24 import RF24, RF24_PA_LOW, RF24_DRIVER

chip = lgpio.gpiochip_open(0)
CE_PIN = 22  
CSN_PIN = 8  
chip = lgpio.gpiochip_open(0)

lgpio.gpio_claim_input(chip, CE_PIN)
lgpio.gpio_claim_input(chip, CSN_PIN)

pipes = [0xe8, 0xe8, 0xf0, 0xf0, 0xe1]
radio = RF24(ce_pin=CE_PIN, csn_pin=CSN_PIN, spi_speed=10000000)
radio.begin(0,0)
radio.setPayloadSize(32)
radio.setChannel(0x77)
radio.setAutoAck(False)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openReadingPipe(1,pipes)
radio.printDetails()
radio.startListening()

if not radio.available(0):
    time.sleep(0.01)
else:
    rcvd = []
    radio.read(rcvd, radio.getDyanmicPayloadSize())
    string = ''
    for n in rcvd:
        if (n >= 32 and n <= 126):
            string+=chr(n)
    print("Recieved.{}".format(string))
    radio.flush_rx()
lgpio.gpiochip_close(h)
