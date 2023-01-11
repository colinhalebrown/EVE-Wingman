import pyautogui
import pytesseract
from PIL import Image
import time
import winsound
import os
import json

# Define PATH for your tesseract installation (default location: C:/Program Files/Tesseract-OCR/tesseract.exe)
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Open the JSON file for reading
with open("data\LocalMonitorSettings.json", "r") as infile:
    # Load the data from the file
    data = json.load(infile)

# You can access the variables like this:
zone_left = data["zone_left"]
zone_top = data["zone_top"]
zone_width = data["zone_width"]
zone_height = data["zone_height"]

# Define the zone of the screen to monitor
zone = (zone_left, zone_top, zone_width, zone_height)  # (left, top, width, height)

# Set the path to save the image
image_path = "data\zones\LocalMonitorRegion.png"

# Set the initial number to an empty string
prev_string = ""
null_string = ""

# Get a screenshot of the zone
screenshot = pyautogui.screenshot(region=zone)

# Save the image to disk
screenshot.save(image_path)

# Extract the text from the image using OCR
text = pytesseract.image_to_string(Image.open(image_path))
prev_string = text 
  
while True:
  # Get a screenshot of the zone
  screenshot = pyautogui.screenshot(region=zone)

  # Save the image to disk
  screenshot.save(image_path)

  # Extract the text from the image using OCR
  text = pytesseract.image_to_string(Image.open(image_path))

  # Print the extracted text
  print("Local Monitor: Prev: [" + prev_string + "] Current: [" + text + "]")
  
  
  # Check if the number has changed
  if text != prev_string:
    # Make the beep sound
    winsound.Beep(frequency=500, duration=300)
    prev_string = text
    
  elif text != null_string:
  
    
    time.sleep(5)