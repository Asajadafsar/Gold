from telethon import TelegramClient, events

# Connection details
api_id = '20767541'
api_hash = 'f4dad8155eb71a32cd47a78a7c6be4e6'

# Channels
source_channel = '@chaneltabantest'
target_channel = '@send_mgoldbot'

# Create a Telegram client with a user account
client = TelegramClient('my_session', api_id, api_hash)

# Fetch messages from the source channel
@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    # دریافت متن پیام
    message_text = event.message.text
    
    # بررسی شروع پیام با "💍تابان گوهر نفیس💍"
    if message_text and message_text.startswith("💍تابان گوهر نفیس💍"):
        print(f'Forwarding message: {message_text}')
        
        # ارسال پیام به کانال هدف
        await client.send_message(target_channel, message_text)

print("Bot is ready...")
client.start()
client.run_until_disconnected()
