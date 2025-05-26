import asyncio
import os
from chatterbox_io import ChatterBox

# Initialize the client with your API key
client = ChatterBox(
    authorization_token=os.getenv("CHATTERBOX_TOKEN")
)

async def handle_meeting_started(data):
    print(f"Meeting started: {data}")

async def handle_meeting_finished(data):
    print(f"Meeting finished: {data}")

async def handle_transcript(data):
    print(f"Transcript: {data['text']} (Speaker: {data['speaker']})")

async def main():
    try:
        # Send a bot to a Zoom meeting
        session = await client.send_bot(
            platform="zoom",
            meeting_id="1234567890",
            meeting_password="your_meeting_password_if_used", # Optional
            bot_name="Test Bot",  # Optional
            language="en",  # Optional: Set to English
            model="nova-3"  # Optional: Use Deepgram's nova-3 model
        )
        print(f"Bot started with session ID: {session.id}")

        # Connect to WebSocket for real-time events
        socket = client.connect_socket(session.id)
        
        # Register event handlers
        socket.on_meeting_started(handle_meeting_started)
        socket.on_meeting_finished(handle_meeting_finished)
        socket.on_transcript_received(handle_transcript)
        
        print("Connecting to WebSocket...")
        await socket.connect()
        print("Connected to WebSocket")
        
        # Keep the connection alive until interrupted
        try:
            await socket.wait_closed()
        except KeyboardInterrupt:
            print("\nShutting down...")
            await socket.disconnect()
            print("Disconnected from WebSocket")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        raise
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main()) 