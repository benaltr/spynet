# importing the required packages
import datetime
import os
import time
import cv2
import numpy as np
import pyautogui

from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")
video_config = config["Video"]
duration = int(video_config["duration"])

curr_dir = os.getcwd()


def screenshot(website, date):
    try:
        os.mkdir(fr'{date}/{website}')
    except:
        pass

    now = str(datetime.datetime.now()).replace(' ', '_').replace(':', '_').replace('.', '_').replace('-', '_')
    time.sleep(10)
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(fr'{curr_dir}\{date}\{website}\{website}_{now}.png')


def record_video(website, date):
    try:
        os.mkdir(fr'{date}/{website}')
    except:
        pass
    now = str(datetime.datetime.now()).replace(' ', '_').replace(':', '_').replace('.', '_').replace('-', '_')

    # Set the screen resolution
    screen_size = (1920, 1080)

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(fr"{curr_dir}\{date}\{website}\{website}_{now}.avi", fourcc, 20.0, screen_size)

    # Get the start time
    start_time = time.time()

    # Start the screen recording
    while (time.time() - start_time) < duration:

        # Take a screenshot of the screen
        img = pyautogui.screenshot()

        # Convert the screenshot to an OpenCV image
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # Write the frame to the output video file
        out.write(frame)


    # Release the resources
    out.release()
    cv2.destroyAllWindows()


def check_time(start_time_str, end_time_str):
    now = datetime.datetime.now().time()
    start_time = datetime.datetime.strptime(start_time_str, "%H:%M").time()
    end_time = datetime.datetime.strptime(end_time_str, "%H:%M").time()
    
    if start_time <= end_time:
        return start_time <= now <= end_time
    else:  # Handles cases where the range spans across midnight
        return start_time <= now or now <= end_time
    
