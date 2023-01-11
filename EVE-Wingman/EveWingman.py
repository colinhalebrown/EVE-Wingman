from tkinter import *
from tkinter import ttk
import pyautogui
import subprocess
import json

# Define Color Palette
BackgroundColor = '#2d2d2d'
TextColor = '#bebebe'
ActiveColor = '#878683'

# Define Action Variables
proc1 = None
proc2 = None
proc3 = None

# Define Settings Placeholders
zone_left = 0
zone_top = 0
zone_width = 0
zone_height = 0

# Define Settings Editor Variables
FileLocal = ""
p_state = 0

# Define a function for the button 1's actions
def button1_script():
    global proc1

    if proc1 is not None and proc1.poll() is None:
        # Stop the script by terminating the process
        proc1.terminate()
        proc1 = None
        btn1.config(bg=BackgroundColor, fg=TextColor)

    else:
        # Start the script by creating a new process
        proc1 = subprocess.Popen(["python", "scripts\LocalMonitor.py"])
        btn1.config(bg=ActiveColor, fg=BackgroundColor)
        
# Define a function for the button 2's actions
def button2_script():
    global proc2

    if proc2 is not None and proc2.poll() is None:
        # Stop the script by terminating the process
        proc2.terminate()
        proc2 = None
        btn2.config(bg=BackgroundColor, fg=TextColor)

    else:
        # Start the script by creating a new process
        proc2 = subprocess.Popen(["python", "scripts\EnemyOnGrid.py"])
        btn2.config(bg=ActiveColor, fg=BackgroundColor)
        
# Define a function for the button 3's actions
def button3_script():
    global proc3

    if proc3 is not None and proc3.poll() is None:
        # Stop the script by terminating the process
        proc3.terminate()
        proc3 = None
        btn3.config(bg=BackgroundColor, fg=TextColor)

    else:
        # Start the script by creating a new process
        proc3 = subprocess.Popen(["python", "scripts\RatOnGrid.py"])
        btn3.config(bg=ActiveColor, fg=BackgroundColor)

def tool_selector():
  global active_menu
  global FileLocal

  # Check for an existing Popup
  if p_state == 1:
    popup_manager()

  # Import the current selection
  n = settingselect.get()
    
  if n == "Local Monitor":
    print("Local Monitor Settings Loaded")
    
    # Load The Settings For Local Monitor From JSON
    selected_tool.configure(text="Local Monitor Loaded")
    FileLocal = "data\LocalMonitorSettings.json"
    load_settings(FileLocal)

  elif n == "Enemy on Grid":
    print("Enemy on Grid Settings Loaded")
    
    # Load The Settings For Enemy On Grid From JSON
    selected_tool.configure(text="Enemy on Grid Loaded")
    FileLocal = "data\EnemyOnGridSettings.json"
    load_settings(FileLocal)

  elif n == "Rat on Grid":
    print("Rat on Grid Settings Loaded")
    
    # Load The Settings For Rat On Grid From JSON
    selected_tool.configure(text="Rat on Grid Loaded")
    FileLocal = "data\RatOnGridSettings.json"
    load_settings(FileLocal)

  else:
    print("Select an option to load.")

    # Reset Form
    selected_tool.configure(text="Select a Tool")
    clear_entries()
    disable_entry()

def save_settings():
  # Make sure a tool is selected before you import variables
  if settingselect.get() != "Select a Tool":
    # Import Variables From Form
    zone_left = Lentry.get()
    zone_top = Tentry.get()
    zone_width = Wentry.get()
    zone_height = Hentry.get()
    FileName = FileLocal

    # Construct Data For JSON File
    data = {
      "zone_left": zone_left,
      "zone_top": zone_top,
      "zone_width": zone_width,
      "zone_height": zone_height
    }
  
    with open(FileName, "w") as outfile:
      # Write the data to the file as JSON
      json.dump(data, outfile)

    # Reset Form and Close popup
    clear_entries()
    disable_entry()
    popup_manager()
    
def load_settings(FileDest):
  # Import Variable
  FileName = FileDest
  
  with open(FileName, "r") as infile:
    # Load the data from the file
    data = json.load(infile)

# You can access the variables like this:
  zone_left = data["zone_left"]
  zone_top = data["zone_top"]
  zone_width = data["zone_width"]
  zone_height = data["zone_height"]

# Enable Entires
  enable_entry()

# Clear Entries
  clear_entries()

# Insert Saved Values
  Lentry.insert(0, zone_left)
  Tentry.insert(0, zone_top)
  Wentry.insert(0, zone_width)
  Hentry.insert(0, zone_height)

def popup_manager():
  global p_state
  global popup
  
  if p_state == 0: 
    p_state = 1
  else:
    p_state = 0
    popup.destroy()

def preview_zone():
  if settingselect.get() != "Select a Tool":
    global popup

    zone_left = Lentry.get()
    zone_top = Tentry.get()
    zone_width = Wentry.get()
    zone_height = Hentry.get()

    # Define the zone of the screen to monitor
    zone = (zone_left, zone_top, zone_width, zone_height)  # (left, top, width, height)

    # Set the path to save the image
    image_path = "data\content\zonepreview.png"

    # Get the screenshot of the zone
    screenshot = pyautogui.screenshot(region=zone)
    # Save the image to disk
    screenshot.save(image_path)

    # Create popup window
    popup = Toplevel(window)
    popup.title("Zone Preview Window")
    popup.iconbitmap("data\content\icon.ico")
    popup['background'] = BackgroundColor
    popup['bd'] = 10
    popup_manager()

    # Create Header Frame
    popup_header = Frame(popup, bg=BackgroundColor)
    popup_title = Label(popup_header, text="Eve Wingman Zone Preview", bg=BackgroundColor, fg=TextColor, padx=6, pady=3, font=20)
    popup_title.grid(column=0, row=0)
    preview_screenshot = PhotoImage(file=image_path)
    preview_image= Label(popup_header, image=preview_screenshot, bd=6, bg=BackgroundColor)
    preview_image.image = preview_screenshot
    preview_image.grid(column=0, row=1)
    popup_header.pack(expand = False, fill = BOTH, side = TOP)

    # Create Options Menu
    options_menu = Frame(popup, bg=BackgroundColor)
    close_preview = Button(options_menu, text="Return", command=popup_manager, bg=BackgroundColor, fg=TextColor, padx=2, pady=1, bd=1)
    savebtn = Button(options_menu, text="Save", command=save_settings, bg=BackgroundColor, fg=TextColor, padx=2, pady=1, bd=1)
    spacer1 = Label(options_menu, text="", bg=BackgroundColor, padx=1)
    close_preview.grid(column=0, row=0)
    spacer1.grid(column=1, row=0)
    savebtn.grid(column=2 ,row=0)
    options_menu.pack(expand = False, fill = BOTH, side = BOTTOM)

def clear_entries():
  # Insert Saved Values
  Lentry.delete(0, 'end')
  Tentry.delete(0, 'end')
  Wentry.delete(0, 'end')
  Hentry.delete(0, 'end')

def disable_entry():
  # Config Entry Boxes
  Lentry.configure(state='disabled')
  Tentry.configure(state='disabled')
  Wentry.configure(state='disabled')
  Hentry.configure(state='disabled')

def enable_entry():
  # Config Entry Boxes
  Lentry.configure(state='normal')
  Tentry.configure(state='normal')
  Wentry.configure(state='normal')
  Hentry.configure(state='normal')

# Create the main window
window = Tk()
window.title("Eve Wingman")
window.iconbitmap("data\content\icon.ico")
#window.geometry('300x600')
window.resizable(width=False, height=False)
window['background'] = BackgroundColor
window['bd'] = 10

# Header
Header = Frame(window, bg=BackgroundColor)
# Header Content
title = Label(Header, text="Eve Wingman", bg=BackgroundColor, fg=TextColor, padx=6, pady=3, font=20)
btn1 = Button(Header, text="Local Monitor", command=button1_script, bg=BackgroundColor, fg=TextColor, padx=2, pady=1, bd=1)
btn2 = Button(Header, text="Enemy On Grid", command=button2_script, bg=BackgroundColor, fg=TextColor, padx=2, pady=1, bd=1)
btn3 = Button(Header, text="Rat On Grid", command=button3_script, bg=BackgroundColor, fg=TextColor, padx=2, pady=1, bd=1)
lbl1 = Label(Header, text="Settings", bg=BackgroundColor, fg=TextColor)
# Visualize Header Content
title.grid(column=1, row=0)
btn1.grid(column=0, row=1)
btn2.grid(column=1, row=1)
btn3.grid(column=2, row=1)
lbl1.grid(column=0, row=2)
# Header Packing
Header.pack(expand = False, fill = BOTH, side = TOP)

# Zone Editor Selector
Settings = Frame(window, bg=BackgroundColor)
# Zone Editor Selector Content
settingselect = ttk.Combobox(Settings, width=18)
settingselect['values'] = ("Select a Tool", "Local Monitor", "Enemy on Grid", "Rat on Grid")
settingselect.current(0) # Set default selection
selectbtn = Button(Settings, text="Load Profile", command=tool_selector, bg=BackgroundColor, fg=TextColor, padx=2, pady=1, bd=1)
spacer = Label(Settings, text="", bg=BackgroundColor, padx=4)
prevbtn = Button(Settings, text="Preview", command=preview_zone, bg=BackgroundColor, fg=TextColor, padx=2, pady=1, bd=1)
selected_tool = Label(Settings, text="Select a Tool", bg=BackgroundColor, fg=TextColor)
# Visualize Zone Editor Selector Content
settingselect.grid(column=0, row=0)
selectbtn.grid(column=1, row=0)
spacer.grid(column=2, row=0)
prevbtn.grid(column=3, row=0)
selected_tool.grid(column=0, row=1)
# Zone Editor Selector Packing
Settings.pack(expand = True, fill = BOTH, side = TOP)

# Form Settings
active_menu = Frame(window, bg=BackgroundColor)
# Form Settings Content
lbl2 = Label(active_menu, text="Zone Position", bg=BackgroundColor, fg=TextColor, font=14)
Llabel = Label(active_menu, text="Zone Left", bg=BackgroundColor, fg=TextColor)
Tlabel = Label(active_menu, text="Zone Top", bg=BackgroundColor, fg=TextColor)
lbl3 = Label(active_menu, text="Zone Size", bg=BackgroundColor, fg=TextColor, font=14)
Wlabel = Label(active_menu, text="Zone Width", bg=BackgroundColor, fg=TextColor)
Hlabel = Label(active_menu, text="Zone Height", bg=BackgroundColor, fg=TextColor)
Lentry = Entry(active_menu, width=15)
Tentry = Entry(active_menu, width=15)
Wentry = Entry(active_menu, width=15)
Hentry = Entry(active_menu, width=15)
lbl5 = Label(active_menu, text="px", bg=BackgroundColor, fg=TextColor)
lbl6 = Label(active_menu, text="px", bg=BackgroundColor, fg=TextColor)
lbl7 = Label(active_menu, text="px", bg=BackgroundColor, fg=TextColor)
lbl8 = Label(active_menu, text="px", bg=BackgroundColor, fg=TextColor)
# Visualize Form Settings Content
lbl2.grid(column=1, row=0)
Llabel.grid(column=0, row=1)
Tlabel.grid(column=0, row=2)
lbl3.grid(column=1, row=3)
Wlabel.grid(column=0, row=4)
Hlabel.grid(column=0, row=5)
Lentry.grid(column=1, row=1)
Tentry.grid(column=1, row=2)
Wentry.grid(column=1, row=4)
Hentry.grid(column=1, row=5)
lbl5.grid(column=2, row=1)
lbl6.grid(column=2, row=2)
lbl7.grid(column=2, row=4)
lbl8.grid(column=2, row=5)
# Form Settings Packing
active_menu.pack(expand = True, fill = BOTH, side = BOTTOM)

disable_entry()

# Run the main loop
window.mainloop()