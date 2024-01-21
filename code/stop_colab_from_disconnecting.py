from pynput.keyboard import Controller, Key
import time

keyboard = Controller()

while True:
    keyboard.press(Key.space)
    time.sleep(600)
