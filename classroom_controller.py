import RPi.GPIO as GPIO
import command_parser
import lcd_commands as lcd
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
led0 = GPIO.PWM(LIGHT_IO[0], 1000)
led1 = GPIO.PWM(LIGHT_IO[1], 1000)
led2 = GPIO.PWM(LIGHT_IO[2], 1000)
leds = [led0, led1, led2]

ser = serial.Serial('/dev/ttyACM0')

students = {'99090':'João Pires',
            '99104':'Marco Castro',
            '99112':'Miguel Gago',
            '99217':'Francesco Pelizzari'}

student_present = [False, False, False, False] #Only IDs

sim_temp = 20
ideal_temp = 22
current_temp = [0, 0]
current_light_level = [0, 0, 0]
student_seated = [False, False, False, False]

automatic_lights = True
light_on = [False, False, True]
button_pressed = False

web_command = ''
new_web_command = False

def get_light_intensity(n):
    brightness = current_light_level[n]
    if brightness < 200:
        return 100
    elif brightness >= 200 and brightness < 300:
        return 80
    elif brightness >= 300 and brightness < 400:
        return 50
    elif brightness >= 400 and brightness < 500:
        return 30
    else:
        return 0

def get_current_temp():
    return sum(current_temp) / len(current_temp)

def change_temp(t):
    global ideal_temp
    global automatic_lights
    ideal_temp = float(format(t, '.1f'))

def set_light(light_n, state):
    global automatic_lights

    if light_n == 9: # Number reserved to switch between manual and auto mode
        automatic_lights = state

    else:
        print('Light number ' + str(light_n) + ' turned ', end='')
        if state: print('on')
        else: print('off')

        global leds
        automatic_lights = False
        if state: leds[light_n].start(100)
        else: leds[light_n].start(0)

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

def web_commands():
    global new_web_command
    global web_command
    while True:
        if new_web_command:
            new_web_command = False
            try:
                command = command_parser.read_web_command(web_command)
                if command[0] == TEMP:
                    change_temp(command[1])

                elif command[0] == LIGHT:
                    set_light(command[1], command[2])

                elif command[0] == PROJ:
                    set_proj(command[1])

                elif command[0] == GET:
                    get_info(command[1])

            except Exception as e:
                print('Web Command Error')
        
        else:
            time.sleep(0.02)
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
                student_seated[command[1]] = not(student_seated[command[1]])
                #print('STUDENT' + str(command[1]) + '_PRESENT = ' + str(student_seated[command[1]]))
                global button_pressed
                button_pressed = True

def update_sim_temp():
    while True:
        global ideal_temp
        global sim_temp

        if sim_temp < ideal_temp:
            sim_temp += 0.1
        elif sim_temp > ideal_temp:
            sim_temp -= 0.1
        sim_temp = float(format(sim_temp, '.1f'))
        time.sleep(1)

def lcd_manager():
    lcd.clear()
    try:
        lcd.init_lcd()
        time.sleep(1)
        while True:
            lcd.update_lcd(get_current_temp(), ideal_temp, sim_temp)
    
    except KeyboardInterrupt:
        pass
    finally:
        lcd.close_lcd()

def light_control():
    global button_pressed
    global light_on
    prev_light_intensities = [0, 0, 0]
    while True:
        if automatic_lights:
            light_intensities = [get_light_intensity(0), get_light_intensity(1), get_light_intensity(2)]
            if button_pressed:
                button_pressed = False
                if student_seated[0] or student_seated[1]:
                    led0.start(light_intensities[0])
                    light_on[0] = True
                else:
                    led0.start(0)
                    light_on[0] = False

                if student_seated[2] or student_seated[3]:
                    led1.start(light_intensities[1])
                    light_on[1] = True
                else:
                    led1.start(0)
                    light_on[1] = False
                
            if light_intensities != prev_light_intensities:
                if light_on[0]:
                    led0.start(light_intensities[0])
                if light_on[1]:
                    led1.start(light_intensities[1])
                if light_on[2]:
                    led2.start(light_intensities[2])
            prev_light_intensities = light_intensities
        
        else:
            pass
            

commands_thread = threading.Thread(target=manual_commands, name='Thread 1')
sensors_thread = threading.Thread(target=sensor_commands, name='Thread 2')
update_temp_thread = threading.Thread(target=update_sim_temp, name='Thread 3')
lcd_thread = threading.Thread(target=lcd_manager, name='Thread 4')
light_control_thread = threading.Thread(target=light_control, name='Thread 5')
web_commands_thread = threading.Thread(target=web_commands, name='Thread 6')

commands_thread.start()
sensors_thread.start()
update_temp_thread.start()
lcd_thread.start()
light_control_thread.start()
web_commands_thread.start()

    
