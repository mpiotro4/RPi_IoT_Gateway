import serial_wrapper
import bluetoothctl_wrapper
import sys


def switch_on(mac_address, pin, port):
    bt = bluetoothctl_wrapper.Bluetoothctl()
    if(bt.find_and_pair(mac_address, pin)):
        hc05 = serial_wrapper.SerialWrapper(mac_address, port)
        hc05.switch_on()
    else:
        print('Error')

def switch_off(mac_address, pin, port):
    bt = bluetoothctl_wrapper.Bluetoothctl()
    if(bt.find_and_pair(mac_address, pin)):
        hc05 = serial_wrapper.SerialWrapper(mac_address, port)
        hc05.switch_off()
    else:
        print('Error')


mac_address = '00:20:12:08:B6:73'
#mac_address = sys.argv[1]
pin = '1234'
port = 0

if sys.argv[1] == '1':
    switch_on(mac_address, pin, port)
 
if sys.argv[1] == '0':
    switch_off(mac_address, pin, port)