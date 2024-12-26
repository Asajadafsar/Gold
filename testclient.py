from pyrogram import Client, filters
import asyncio
import traceback

# API credentials for the Telegram app
api_id = "20767541"  # Replace with your own API ID
api_hash = "f4dad8155eb71a32cd47a78a7c6be4e6"  # Replace with your own API hash

# Source and target channels
source_channel = "@chaneltabantest"  # Channel to monitor for messages
target_channel = "@Getinfo_gold"  # Channel to forward matching messages to

# Initialize the Pyrogram client
app = Client("my_session", api_id=api_id, api_hash=api_hash)

# Define a message handler to listen for specific messages from the source channel
@app.on_message(filters.chat(source_channel) & filters.text)
async def forward_message(client, message):
    try:
        print(f"Received message: {message.text}")  # Log the received message

        # Check if the message text starts with the specific string
        if message.text.startswith("💍تابان گوهر نفیس💍"):
            print(f"Forwarding message: {message.text}")  # Log the forwarding action
            try:
                # Forward the message to the target channel
                sent_message = await client.send_message(target_channel, message.text)
                print(f"Message sent successfully: {sent_message.id}")  # Log success
            except Exception as e:
                print(f"Error sending message: {e}")  # Log any error during forwarding
                traceback.print_exc()  # Print detailed traceback for debugging
        else:
            print("Message does not match the condition.")  # Log non-matching messages
    except Exception as e:
        print(f"Error in message handler: {e}")  # Log any error in the handler
        traceback.print_exc()  # Print detailed traceback for debugging

# Main function to start and manage the bot
async def main():
    while True:
        try:
            print("Starting the client...")  # Log the start of the client
            await app.start()  # Start the Pyrogram client
            print("Bot is ready...")  # Log when the bot is ready to operate
            await app.idle()  # Keep the bot running until stopped
        except Exception as e:
            print(f"Connection error: {e}. Retrying in 5 seconds...")  # Log connection errors
            traceback.print_exc()  # Print detailed traceback for debugging
            await asyncio.sleep(5)  # Wait for 5 seconds before retrying

# Entry point of the script
if __name__ == "__main__":
    asyncio.run(main())  # Run the main function asynchronously
