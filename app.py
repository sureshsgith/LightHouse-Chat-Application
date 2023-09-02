# Import necessary modules and libraries from FastAPI and other Python libraries
from fastapi import FastAPI, WebSocket
from fastapi.websockets import WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import uvicorn
import aiofiles
import json
import chat # Import the chat module
agent = chat.getAgent() # Get the chat agent from the chat module
app = FastAPI()  # Create a FastAPI app instance


# List to store active WebSocket connections
active_connections = []

# Mount the "static" directory for serving static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Asynchronous function to write JSON data to a file
async def write_json_to_file(data: dict):
    async with aiofiles.open("chat_history.json", mode="a") as file:
        await file.write(json.dumps(data) + "\n")

# Asynchronous function to clear the chat history JSON file
async def clear_json():
    async with aiofiles.open("chat_history.json", mode="w") as file:
        await file.write("")


# Define a route for the home page, serving an HTML file
@app.get("/", response_class=FileResponse)
def home():
    htmlPath=Path("templates/index.html")
    return FileResponse(htmlPath)


# WebSocket endpoint for handling chat interactions
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            resp = agent.run(data)  # Use the chat agent to respond to messages
            # resp = "test"
            conversation = {
                "User": data,
                "LighthouseBot": resp
            }
            await write_json_to_file(conversation) # Write conversation data to a file  
            await websocket.send_text(f"{resp}")  # Send the response back to the WebSocket client
    except WebSocketDisconnect:
        await clear_json()  # Clear the chat history when WebSocket disconnects
        print("Web Socket Disconnected!")

    finally:
        active_connections.remove(websocket)

# Run the FastAPI application with Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80) # Start the FastAPI app
