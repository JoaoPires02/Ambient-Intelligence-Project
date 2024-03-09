import argparse

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
                          help='On of off')

# Projector parser definition:
proj_parser = argparse.ArgumentParser(exit_on_error=False)

proj_parser.add_argument('state', type=str, choices=['on', 'off'],
                          help='On of off')


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