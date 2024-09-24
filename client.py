import asyncio
import websockets
import json
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def get_distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance


async def send_address(file_path):
    # Read the address from the specified file
    try:
        with open(file_path, 'r') as file:
            address = file.read().strip()
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return

    # WebSocket connection
    uri = "ws://localhost:8080"
    async with websockets.connect(uri) as websocket:
        status = 'empty'  # Or other status as needed

        # loop

        while (True):
            # Create the message as a JSON object
            message = {
                'address': address,
                'status': status
            }

            # Send the message as a JSON string
            await websocket.send(json.dumps(message))
            print(f"Sent: {message}")

            # Optionally, receive a response from the server
            response = await websocket.recv()
            print(f"Server says: {response}")

            time.sleep(1)


# Run the client
file_path = 'address.txt'  # Replace with the path to your address file
# asyncio.run(send_address(file_path))

