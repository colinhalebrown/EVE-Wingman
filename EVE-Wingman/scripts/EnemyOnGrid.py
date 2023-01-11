import pyautogui
import numpy as np
import time
import winsound
import json

# Open the JSON file for reading
with open("data\EnemyOnGridSettings.json", "r") as infile:
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
image_path = "data\zones\EnemyOnGridRegion.png"

# Initialize a variable to store the previous count of colored pixels
dead_pixel_count = 100

while True:
    # Get the screenshot of the zone
    screenshot = pyautogui.screenshot(region=zone)
    # Save the image to disk
    screenshot.save(image_path)

    # Convert the screenshot to a numpy array
    image = np.array(screenshot)

    # Get the shape of the image
    rows, cols, _ = image.shape
    # Initialize a counter for the number of color pixels
    color_pixels = 0

    # Iterate through the image and count the number of color pixels
    for row in range(rows):
        for col in range(cols):
            # Check if the pixel is within the range of colors
            if 255 >= image[row][col][0] >= 160 and 180 >= image[row][col][1] >= 121 and 25 >= image[row][col][2] >= 0:
                color_pixels += 1

    # Print the number of color pixels
    print(f'Enemy On Grid Count: {color_pixels}')
    
    # Check if the number of colored pixels has changed
    if color_pixels >= dead_pixel_count:
        # Make a beep sound
        winsound.Beep(frequency=4000, duration=240)
        time.sleep(0.025)
        winsound.Beep(frequency=4000, duration=240)
        time.sleep(0.025)
        winsound.Beep(frequency=4000, duration=240)
        time.sleep(0.025)
        winsound.Beep(frequency=4000, duration=240)
        time.sleep(0.025)
        winsound.Beep(frequency=4000, duration=240)
        time.sleep(2)
    else:
        time.sleep(0.1)
