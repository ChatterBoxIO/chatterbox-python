python: `import asyncio
from chatterbox_io import ChatterBox

client = ChatterBox(authorization_token="******************")

async def handle_meeting_started(data):
    print("Meeting started:", data)

async def handle_meeting_finished(data):
    print("Meeting finished:", data)

async def handle_transcript(data):
    print(f"Transcript: {data['text']} (Speaker: {data['speaker']}")

async def main():
    try:
        # Send a bot to a Zoom meeting
        session = await client.send_bot(
            platform="zoom",
            meeting_id="9882112233",
            meeting_password="******************",
            bot_name="ChatterBox"
        )
        print(f"Bot started successfully! Session ID: {session.id}")

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
            print("\\nShutting down...")
            await socket.disconnect()
    
    except Exception as e:
        print(f"Failed to start the bot: {str(e)}")
        raise
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())` 