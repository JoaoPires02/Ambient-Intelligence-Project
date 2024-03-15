import RPi.GPIO as GPIO
import command_parser
import threading
import serial
import time

TEMP = 0
LIGHT = 1
PROJ = 2
BUTTON = 2
GET = 3

LIGHT_IO = [18, 23, 24]
PROJ_IO = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(LIGHT_IO[0], GPIO.OUT)
GPIO.setup(LIGHT_IO[1], GPIO.OUT)
GPIO.setup(LIGHT_IO[2], GPIO.OUT)
GPIO.setup(PROJ_IO, GPIO.OUT)

ser = serial.Serial('/dev/ttyACM0')

students = {'99090':'João Pires',
            '99104':'Marco Castro aKa Deus do Técnico',
            '99112':'Miguel Gago',
            '96447':'Matilde Martins',
            '96308':'Ricardo Pinto',
            '99217':'Francesco Pelizzari'}

present_students = [] #Only IDs

def new_student(id):
    if id not in students:
        print('Error: you don\'t belong here')
    else:
        present_students.append(id)

def student_list():
    res = 'List of students:\n'
    for student in students:
        res += student + ': ' + students[student]
        if student in present_students:
            res += ' - Present\n'
        else:
            res += ' - Missing\n'

current_temp = [0, 0]
current_light_level = [0, 0, 0]
student_present = [False, False, False, False]

def get_current_temp():
    return sum(current_temp) / len(current_temp)

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

def get_info(arg):
    if arg == 'temp':
        print('Temp 0: ' + str(current_temp[0]))
        print('Temp 1: ' + str(current_temp[1]))
        print('Average Temp: ' + str(get_current_temp()))

    elif arg == 'light':
        print('Light 0: ' + str(current_light_level[0]))
        print('Light 1: ' + str(current_light_level[1]))
        print('Light 2: ' + str(current_light_level[2]))

def manual_commands():
    while True:
        try:
            command = command_parser.read_command()
            if command[0] == TEMP:
                change_temp(command[1])

            elif command[0] == LIGHT:
                set_light(command[1], command[2])

            elif command[0] == PROJ:
                set_proj(command[1])

            elif command[0] == GET:
                get_info(command[1])

        except Exception as e:
            pass

def sensor_commands():
    while True:
        msg = ser.readline().decode()[1:]
        command = command_parser.read_sensor_info(msg)
        if command != None:
            if command[0] == TEMP:
                current_temp[command[2]] = command[1]
                #print('TEMP' + str(command[2]) + ' = ' + str(current_temp[command[2]]))

            elif command[0] == LIGHT:
                current_light_level[command[2]] = command[1]
                #print('LIGHT' + str(command[2]) + ' = ' + str(current_light_level[command[2]]))

            elif command[0] == BUTTON:
                student_present[command[1]] = not(student_present[command[1]])
                #print('STUDENT' + str(command[1]) + '_PRESENT = ' + str(student_present[command[1]]))


commands_thread = threading.Thread(target=manual_commands, name='Thread 1')
sensors_thread = threading.Thread(target=sensor_commands, name='Thread 2')
commands_thread.start()
sensors_thread.start()

    
