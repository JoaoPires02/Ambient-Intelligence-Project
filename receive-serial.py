import serial

ser = serial.Serial('/dev/ttyACM0')

while True:
    try:
        msg = ser.readline()
        print(msg)
    except Exception as err:
        print('Error: '.format(err.args))