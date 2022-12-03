# Antes de correr el programa ejecutar:
#   sudo modprobe spidev

import board
import digitalio
import busio
from MCP3204 import mcp3204 as MCP
from MCP3204 import analog_in
from time import sleep


#create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)


#Create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

#Create the mcp object 
mcp = MCP.MCP3004(spi, cs)


#Create an analog input channel on pin 0
chan = analog_in.AnalogIn(mcp,MCP.P0)

while True:
            
    print("Raw ADC value: ", chan.value)
    print("ADC voltaje: " + str(chan.voltage) + "V")
    sleep(0.5)
