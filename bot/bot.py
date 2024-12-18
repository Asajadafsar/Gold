from telethon import TelegramClient, events

# Connection details
api_id = 'Your_API_ID'
api_hash = 'Your_API_HASH'

# Source channel
source_channel = 'username@source_channel'

# Create a Telegram client with a user account
client = TelegramClient('my_session', api_id, api_hash)

# Fetch messages from the source channel
@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    print(f'New message from {source_channel}: {event.message.text}')

print("Bot is ready...")
client.start()
client.run_until_disconnected()
