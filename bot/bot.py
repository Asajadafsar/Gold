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
    while True:
        try:
            print("Starting the client...")
            await app.start()
            print("Bot is ready...")
            print(f"Using crypto library: {__crypto_version__}")  # نمایش کتابخانه مورد استفاده
            await app.idle()
        except Exception as e:
            print(f"Connection error: {e}. Retrying in 5 seconds...")
            traceback.print_exc()
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
