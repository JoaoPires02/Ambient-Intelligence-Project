from RPLCD import CharLCD
import RPi.GPIO as GPIO
from time import sleep

# Pin configuration
lcd_rs = 26
lcd_en = 19
lcd_d4 = 13
lcd_d5 = 6
lcd_d6 = 5
lcd_d7 = 11

# Define LCD column and row size for 16x2 LCD
lcd_columns = 16
lcd_rows = 2

# Initialize LCD
lcd = CharLCD(
    cols=lcd_columns,
    rows=lcd_rows,
    pin_rs=lcd_rs,
    pin_e=lcd_en,
    pins_data=[lcd_d4, lcd_d5, lcd_d6, lcd_d7],
    numbering_mode=GPIO.BCM
)

def init_lcd():
    lcd.cursor_pos = (0, 0)
    lcd.write_string('Measuring...')
    lcd.cursor_pos = (1, 0)
    lcd.write_string('Room Code: RX5v')

def update_lcd(real_temp, ideal_temp, sim_temp):
    real_temp = str(format(real_temp, '.1f'))
    ideal_temp = str(format(ideal_temp, '.1f'))
    sim_temp = str(format(sim_temp, '.1f'))

    lcd.cursor_pos = (0, 0)
    lcd.write_string(real_temp + '-' + ideal_temp + '-' + sim_temp)

def close_lcd():
    lcd.close(clear=True)
    GPIO.cleanup()

def test_lcd():
    try:
        init_lcd()
        sleep(1)
        while True:
            update_lcd(15.4567, 20, 16.346367)
            sleep(0.5)
            update_lcd(15.4567, 20, 18.2587)
            sleep(0.5)
            update_lcd(15.4567, 20, 19.8867)
            sleep(0.5)
    
    except KeyboardInterrupt:
        pass
    finally:
        close_lcd()
