from pystray import Menu, Icon, MenuItem
import PIL.Image
import os

# Load the tray icon image
image = PIL.Image.open("jarvis.png")

# Function to start Jarvis
def start_jarvis(icon, item):
    os.system('python "C:/Users/akash/OneDrive/Desktop/coding/JARVIS/jarvis/s.py"')
    print("Jarvis started..")

# Function to exit the tray
def exit_jarvis(icon, item):
    icon.stop()

# Create a menu for the tray icon
menu = Menu(
    MenuItem('Start', start_jarvis),
    MenuItem('Exit', exit_jarvis)
)

if os._exit:
    exit

# Create and run the system tray icon
icon = Icon("Jarvis", image, "Jarvis", menu)
icon.run()
