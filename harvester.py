import os
import time
from datetime import datetime
from threading import Thread
from PIL import ImageGrab
import win32gui
from pynput import mouse

# Global variables
capturing = False
object_name = input("Enter the object name for the dataset: ")
dataset_dir = os.path.join('dataset', object_name)
os.makedirs(dataset_dir, exist_ok=True)

def get_active_window_rect():
    """Get the bounding box of the currently active window"""
    window = win32gui.GetForegroundWindow()
    return win32gui.GetWindowRect(window)

def capture_screenshot():
    """Capture and save a screenshot of a 640x640 box centered on the display"""
    try:
        # Get the current screen size
        screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

        # Calculate the bounding box for a 640x640 area centered on the screen
        left = (screen_width - 640) // 2
        top = (screen_height - 640) // 2
        right = left + 640
        bottom = top + 640

        # Capture the screenshot with the defined bounding box
        img = ImageGrab.grab(bbox=(left, top, right, bottom))
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        img.save(os.path.join(dataset_dir, f"{object_name}_{timestamp}.png"))
        print(f"Captured: {object_name}_{timestamp}.png")
    except Exception as e:
        print(f"Error capturing screenshot: {str(e)}")
        
def on_click(x, y, button, pressed):
    """Mouse click event handler"""
    global capturing
    if button == mouse.Button.right:
        if pressed and not capturing:
            capturing = True
            # Start capture thread
            Thread(target=capture_loop).start()
        elif not pressed:
            capturing = False

def capture_loop():
    """Continuous capture loop while right mouse button is held"""
    while capturing:
        capture_screenshot()
        time.sleep(0.4)  # 400ms interval

def main():
    print(f"Dataset will be saved in: {dataset_dir}")
    print("Right-click and hold to start capturing...")
    
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

if __name__ == "__main__":
    main()
