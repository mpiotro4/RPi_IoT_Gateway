import serial_wrapper
import bluetoothctl_wrapper
import sys


def get_measurement(mac_address, pin, port):
    bt = bluetoothctl_wrapper.Bluetoothctl()
    if(bt.find_and_pair(mac_address, pin)):
        hc05 = serial_wrapper.SerialWrapper(mac_address, port)
        print(f"{hc05.readline()}")
    else:
        print('Error')


#mac_address = '00:20:12:08:B6:73'
mac_address = sys.argv[1]
pin = '1234'
port = 0
get_measurement(mac_address, pin, port)