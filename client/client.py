from websockets.sync.client import connect
import os
import pygame
import json
import time
from loguru import logger
from dotenv import load_dotenv
load_dotenv()

# Initialize Pygame and the joystick
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(1)
joystick.init()


def joystick_data_message_producer(websocket):
    while True:
        pygame.event.pump()
        joystick_stats = {}

        # Axes
        axes = []
        for i in range(joystick.get_numaxes()):
            axis = joystick.get_axis(i)
            axes.append(axis)
        joystick_stats["axes"] = axes

        buttons = []
        for i in range(joystick.get_numbuttons()):
            button = joystick.get_button(i)
            buttons.append(button)
        joystick_stats["buttons"] = buttons

        hats = []
        for i in range(joystick.get_numhats()):
            hat = joystick.get_hat(i)
            hats.append(hat)
        joystick_stats["hats"] = hats

        logger.info(joystick_stats["hats"])

        # Convert the input data to JSON format
        json_data = json.dumps(joystick_stats)
        # Send the input data as a POST request to the server
        websocket.send(json_data)
        message = websocket.recv()
        # Print the response from the server
        logger.info(f"Received: {message}")


def send_joystick_data():
    HOST_URL = os.environ.get("HOST_URL")
    with connect(HOST_URL) as websocket:
        joystick_data_message_producer(websocket)


send_joystick_data()
