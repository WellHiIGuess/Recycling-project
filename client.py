import asyncio
import websockets
import json

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

# Run the client
file_path = 'address.txt'  # Replace with the path to your address file
asyncio.run(send_address(file_path))

