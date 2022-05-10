from libs.lib_nrf24 import NRF24
# noinspection PyUnresolvedReferences
import RPi.GPIO as GPIO
# noinspection PyUnresolvedReferences
import spidev
from time import sleep


class Receiver:
    def __init__(self):
        # Initialize radio
        self.pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]
        GPIO.setmode(GPIO.BCM)
        self.radio = NRF24(GPIO, spidev.SpiDev())
        self.radio.begin(0, 17)
        self.radio.setPayloadSize(32)
        self.radio.setChannel(0x66)
        self.radio.setDataRate(NRF24.BR_250KBPS)
        self.radio.setPALevel(NRF24.PA_LOW)

        self.radio.setAutoAck(True)
        self.radio.enableDynamicPayloads()
        self.radio.enableAckPayload()
        self.radio.openWritingPipe(self.pipes[0])
        self.radio.openReadingPipe(1, self.pipes[1])
        self.radio.printDetails()
        # enable listening
        self.radio.startListening()

    def read(self) -> dict:
        senzor = []
        # 0: teplota
        # 1: čírosť
        # 2: PH
        # [3, 4]: ORP
        # 5: O2
        self.radio.read(senzor, self.radio.getDynamicPayloadSize())
        ORP = senzor[3]*100 + senzor[4]
        # Some magic required to ORP encoding
        if ORP > 10000:
            ORP -= 10000
            ORP *= -1

        return {
            "temperature": int(senzor[0]),
            "clarity":  int(senzor[1]) / 2,
            "PH": int(senzor[2]) / 10,
            "ORP": ORP,
            "O2": int(senzor[5]) / 10
        }

    def read_blocking(self) -> dict:
        while not self.radio.available(0):
            sleep(1 / 100)
        return self.read()
