import time
import requests
import pygame
from dotenv import load_dotenv
load_dotenv()
import os

# Initialize pygame
pygame.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# Define constants for input event types
JOYSTICK_EVENT_TYPE = "joystick"
QUIT_EVENT_TYPE = "quit"

# Define constants for number of events to send in a single request
EVENTS_PER_REQUEST = 10
EVENTS_PER_GROUP = 10

# Set up the server endpoint
url = os.environ.get("HOST_URL")

# Set up session for reusing connection
session = requests.Session()

# Define function to send input events to server
def send_events(events):
    payload = {"events": events}
    session.post(url, json=payload)

# Define function to get input events from pygame
def get_events():
    events = []
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            events.append({"type": QUIT_EVENT_TYPE})
        elif event.type == pygame.JOYAXISMOTION:
            x, y = joystick.get_axis(0), joystick.get_axis(1)
            
            events.append({"type": JOYSTICK_EVENT_TYPE, "x": x, "y": y})
    return events

# Main loop
while True:
    # Get input events from pygame
    events = get_events()
    # Group joystick events and average them
    grouped_events = []
    num_events = len(events)
    for i in range(0, num_events, EVENTS_PER_GROUP):
        group = events[i:i+EVENTS_PER_GROUP]
        joystick_events = [event for event in group if event["type"] == JOYSTICK_EVENT_TYPE]
        if len(joystick_events) > 0:
            x_avg = sum([event["x"] for event in joystick_events]) / len(joystick_events)
            y_avg = sum([event["y"] for event in joystick_events]) / len(joystick_events)
            grouped_events.append({"type": JOYSTICK_EVENT_TYPE, "x": x_avg, "y": y_avg})
    events = [event for event in events if event["type"] != JOYSTICK_EVENT_TYPE] + grouped_events
    
    # Send events to server in batches of EVENTS_PER_REQUEST
    num_events = len(events)
    for i in range(0, num_events, EVENTS_PER_REQUEST):
        batch = events[i:i+EVENTS_PER_REQUEST]
        print("Sent", events[0])
        send_events(batch)
    
    # Sleep for a short time to avoid overwhelming the server with requests
    time.sleep(0.01)