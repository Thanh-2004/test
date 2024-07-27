import numpy as np
import serial
import os

def collectData(path, time_rec, port):
    if serial.Serial:
        serial.Serial().close()
    # Open the serial port
    s = serial.Serial(port, baudrate=57600)  # COMx in window or /dev/ttyACMx in Ubuntu with x is number of serial port.

    dir_name = os.path.dirname(path)
    
    # Create the directory if it does not exist
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    file = open(path, "w")
    
    x = 0  # iterator of sample
    y = np.array([], dtype=int)  # value

    print("START!")
    while x < (time_rec * 512):
        if x % 512 == 0:
            print(x // 512)
        x += 1
        data = s.readline().decode('utf-8').rstrip("\r\n")
        file.write(str(data))
        file.write('\n')
    # Close the serial port
    print("DONE")
    s.close()
    file.close()
    return 

if __name__ == "__main__":
    collectData("test.txt", 20, "/dev/tty.usbmodem12301")
