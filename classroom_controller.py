import RPi.GPIO as GPIO
from command_parser import read_command

TEMP = 0
LIGHT = 1
PROJ = 2

LIGHT_IO = [18, 23]
PROJ_IO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_IO[0], GPIO.OUT)
GPIO.setup(LIGHT_IO[1], GPIO.OUT)
GPIO.setup(PROJ_IO, GPIO.OUT)

def change_temp(t):
    print('Temperature changed to: ' + str(t))

def set_light(light_n, state):
    print('Light number ' + str(light_n) + ' turned ', end='')
    if state: print('on')
    else: print('off')

    if state: GPIO.output(LIGHT_IO[light_n], GPIO.HIGH)
    else: GPIO.output(LIGHT_IO[light_n], GPIO.LOW)

def set_proj(state):
    print('Projector turned ', end='')
    if state: print('on')
    else: print('off')

    if state: GPIO.output(PROJ_IO, GPIO.HIGH)
    else: GPIO.output(PROJ_IO, GPIO.LOW)

while True:
    try:
        command = read_command()
        if command[0] == TEMP:
            change_temp(command[1])

        elif command[0] == LIGHT:
            set_light(command[1], command[2])

        elif command[0] == PROJ:
            set_proj(command[1])
    except Exception as e:
        pass
