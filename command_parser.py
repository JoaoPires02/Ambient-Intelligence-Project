import argparse
import serial

# Main parser definition:
parser = argparse.ArgumentParser(exit_on_error=False)

possible_commands = ['temp', 'light', 'proj']
parser.add_argument('command', type=str, choices = possible_commands,
                    help='Command to be executed')
parser.add_argument('args', type=str,
                    help='All arguments related to the command')

# Temperature parser definition:
temp_parser = argparse.ArgumentParser(exit_on_error=False)

temp_parser.add_argument('value', type=float,
                    help='Value to set temperature to')

# Light parser definition:
light_parser = argparse.ArgumentParser(exit_on_error=False)

light_parser.add_argument('light_nr', type=int,
                          help='Number of the light')
light_parser.add_argument('state', type=str, choices=['on', 'off'],
                          help='On or off')

# Projector parser definition:
proj_parser = argparse.ArgumentParser(exit_on_error=False)

proj_parser.add_argument('state', type=str, choices=['on', 'off'],
                          help='On or off')


def read_command():
    raw_arg = input('> ').split(' ', 1)
    try:
        args = parser.parse_args(raw_arg)
    except Exception as e:
        print("Error:", e)
    
    command = args.command
    args = args.args

    if command == 'temp':
        try:
            args = temp_parser.parse_args(args.split(' '))
        except argparse.ArgumentError as e:
            print("Error:", e)
        return (0, args.value)
    
    elif command == 'light':
        try:
            args = light_parser.parse_args(args.split(' '))
        except argparse.ArgumentError as e:
            print("Error:", e)
        return (1, args.light_nr, args.state == 'on')
    
    elif command == 'proj':
        try:
            args = proj_parser.parse_args(args.split(' '))
        except argparse.ArgumentError as e:
            print("Error:", e)
        return (2, args.state == 'on')
    

# Sensors Parser Definition
sensors_parser = argparse.ArgumentParser(exit_on_error=False)

sensors_parser.add_argument('sensor', type=str, help='Sensor type')
sensors_parser.add_argument('args', type=str, help='All arguments related to the command')

# Temperature Sensor Parser Definition
temp_sensor_parser = argparse.ArgumentParser(exit_on_error=False)

temp_sensor_parser.add_argument('value', type=float,
                    help='Temperature read by sensor')
temp_sensor_parser.add_argument('sensor_n', type=int,
                    help='Number of the sensor')

# Light Sensor Parser Definition
light_sensor_parser = argparse.ArgumentParser(exit_on_error=False)

light_sensor_parser.add_argument('value', type=int,
                    help='Light level read by sensor')
light_sensor_parser.add_argument('sensor_n', type=int,
                    help='Number of the sensor')

# Button Parser Definition
button_parser = argparse.ArgumentParser(exit_on_error=False)

button_parser.add_argument('button_n', type=int,
                    help='Number of the button pressed')


def read_sensor_info():
    ser = serial.Serial('/dev/ttyACM0')

    try:
        msg = ser.readline()
        print(msg)
    except Exception as err:
        print('Error: '.format(err.args))

    raw_arg = msg.split(' ', 1)
    args = sensors_parser.parse_args(raw_arg)
    sensor = args.sensor
    args = args.args

    if sensor == 'T':
        args = temp_sensor_parser.parse_args(args.split(' '))
        return (0, args.value, args.sensor_n)
    elif sensor == 'L':
        args = light_sensor_parser.parse_args(args.split(' '))
        return (1, args.value, args.sensor_n)
    elif sensor == 'B':
        args = button_parser.parse_args(args.split(' '))
        return (2, args.button_n)