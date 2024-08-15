import subprocess
import evdev
import board
import digitalio
import time
import threading
import signal
import sys

# Path to the USB keyboard device
device_path = '/dev/input/event0'

# Command to be executed
footswitch = ['aplay', '-q', 'single-ring.wav']
# enter_button = ['pw-play', 'geneva-jacuzzi-cannibal_babies.opus']
# enter_button = ['pw-play', 'jermaine-lewis-take-our-clothes-off.mp3']
enter_button = ['aplay', '-q', 'wakeup.wav']

# Create an input device object
device = evdev.InputDevice(device_path)

button = digitalio.DigitalInOut(board.D4)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

subprocesses = []
stop_threads = False

# Loop to listen for events
def listen_for_keyboard():
    # print(f'Listening for "Enter" key press on {device_path}...')
    for event in device.read_loop():
        if stop_threads:
            break
        if event.type == evdev.ecodes.EV_KEY:
            key_event = evdev.categorize(event)
            if key_event.keystate == evdev.KeyEvent.key_down:
                if button.value == True:
                    if key_event.keycode == 'KEY_ENTER':
                        # print('Enter key pressed. Executing command...')
                        # kill last process here before opening a new one
                        if subprocesses:
                            subprocesses[-1].terminate()
                            subprocesses.pop()
                        proc = subprocess.Popen(enter_button)
                        # subprocess.run(enter_button)
                        subprocesses.append(proc)

def listen_for_button():
    # print(f'Listening for foot switch on GPIO {board.D4}...')
    while not stop_threads:
        if (button.value):
            # print("foot switch down")
            subprocess.run(footswitch)
        else:
            if subprocesses:
                subprocesses[-1].terminate()
                subprocesses.pop()
            time.sleep(0.1)

def signal_handler(sig, frame):
    global stop_threads
    print('Terminating subprocess...')
    stop_threads = True
    for proc in subprocesses:
        proc.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

keyboard_thread = threading.Thread(target=listen_for_keyboard)
button_thread = threading.Thread(target=listen_for_button)

keyboard_thread.start()
button_thread.start()

keyboard_thread.join()
button_thread.join()
