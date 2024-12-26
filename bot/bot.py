from pyrogram import Client, filters
import asyncio
import traceback

api_id = "20767541"
api_hash = "f4dad8155eb71a32cd47a78a7c6be4e6"

source_channel = "@chaneltabantest"
target_channel = "@Getinfo_gold"

app = Client("my_session", api_id=api_id, api_hash=api_hash)

@app.on_message(filters.chat(source_channel) & filters.text)
async def forward_message(client, message):
    try:
        print(f"Received message: {message.text}")

        if message.text.startswith("💍تابان گوهر نفیس💍"):
            print(f"Forwarding message: {message.text}")
            try:
                sent_message = await client.send_message(target_channel, message.text)
                print(f"Message sent successfully: {sent_message.id}")
            except Exception as e:
                print(f"Error sending message: {e}")
                traceback.print_exc()
        else:
            print("Message does not match the condition.")
    except Exception as e:
        print(f"Error in message handler: {e}")
        traceback.print_exc()

async def main():
    try:
        print("Starting the client...")
        await app.start()
        print("Bot is ready...")

        # Instead of idle(), use an event loop to keep the bot running
        while True:
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Connection error: {e}. Retrying in 5 seconds...")
        traceback.print_exc()
        await asyncio.sleep(5)
    finally:
        await app.stop()

if __name__ == "__main__":
    # Use the default event loop to start the bot
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
