import multiprocessing
from pyrogram import Client, filters
import asyncio
import json
from flask import Flask, jsonify
import traceback

# Telegram API connection details
api_id = "20767541"
api_hash = "f4dad8155eb71a32cd47a78a7c6be4e6"

source_channel = "@chaneltabantest"
target_channel = "@Getinfo_gold"

app = Client("my_session", api_id=api_id, api_hash=api_hash)

# Flask application for serving the API
flask_app = Flask(__name__)

# Path to save the price data
price_file_path = "price_data.json"  # Changed to JSON format

# Convert Persian/Arabic numbers to English numbers
def to_english_numbers(text):
    english_digits = {
        "۰": "0", "۱": "1", "۲": "2", "۳": "3", "۴": "4", "۵": "5", "۶": "6", "۷": "7", "۸": "8", "۹": "9"
    }
    return ''.join(english_digits.get(c, c) for c in text)

@app.on_message(filters.chat(source_channel) & filters.text)
async def forward_message(client, message):
    try:
        # Extracting prices from the message
        if message.text.startswith("💍تابان گوهر نفیس💍"):
            print(f"Received message: {message.text}")

            # Extract price data as a dictionary
            price_data = extract_price_data(message.text)

            # Save the data to file
            save_price_data_to_file(price_data)

            # Print status of successful extraction
            print("Price data extracted and saved.")

            # Forward the message to the target channel
            await send_price_message_to_channel(client, message.text)

        else:
            print("Message does not match the condition.")
    except Exception as e:
        print(f"Error in message handler: {e}")
        traceback.print_exc()

def extract_price_data(text):
    """
    Extracts prices from the message text and stores them in a dictionary.
    """
    data = {}

    # Extract the update time
    update_time = text.split("آخرین بروزرسانی:")[1].split("🕰")[0].strip()
    data["Last Update"] = to_english_numbers(update_time)  # Convert to English numbers

    # Extract price details
    price_lines = text.split("\n")
    
    for line in price_lines:
        # Ensure the line contains ":" before splitting
        if ":" in line:
            parts = line.split(":")
            key = parts[0].strip()
            value = parts[1].strip()

            # Convert price values to English numbers and remove any Persian/Arabic characters
            value = to_english_numbers(value)

            # Convert all price values to English numbers (in case the price includes words like "تومان")
            if "تومان" in value:
                value = value.replace("تومان", "Toman")
            elif "دلار" in value:
                value = value.replace("دلار", "Dollar")
            elif "یورو" in value:
                value = value.replace("یورو", "Euro")
            elif "درهم" in value:
                value = value.replace("درهم", "Dirham")

            # Convert keys to English
            if "گرم ۱۸ تهران" in key:
                data["18g Tehran"] = value
            elif "انس طلا" in key:
                data["Gold Ounce"] = value
            elif "یک گرم طلای ۲۴ عیار" in key:
                data["1g 24K Gold"] = value
            elif "مظنه تهران" in key:
                data["Tehran Mizan"] = value
            elif "انس نقره" in key:
                data["Silver Ounce"] = value
            elif "دلار" in key:
                data["Dollar"] = value
            elif "یورو" in key:
                data["Euro"] = value
            elif "درهم" in key:
                data["Dirham"] = value
            elif "ربع سکه" in key:
                data["Quarter Coin"] = value
            elif "نیم سکه" in key:
                data["Half Coin"] = value
            elif "سکه طرح جدید" in key:
                data["New Design Coin"] = value
            elif "سکه طرح قدیم" in key:
                data["Old Design Coin"] = value
            elif "سکه یک گرمی" in key:
                data["1g Coin"] = value

    return data

def save_price_data_to_file(data):
    """
    Save the extracted price data to a JSON file.
    """
    try:
        with open(price_file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Price data saved to file.")
    except Exception as e:
        print(f"Error saving price data to file: {e}")
        traceback.print_exc()

def load_price_data_from_file():
    """
    Read the price data from the JSON file.
    """
    try:
        with open(price_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading price data from file: {e}")
        traceback.print_exc()
        return None

async def send_price_message_to_channel(client, text):
    """
    Send the price message to the target channel in the same format.
    """
    try:
        # Forward the message to the target channel
        await client.send_message(target_channel, text)
        print("Message successfully forwarded to target channel.")
    except Exception as e:
        print(f"Error sending message to target channel: {e}")
        traceback.print_exc()

# Route for the Flask API
@flask_app.route('/api/price', methods=['GET'])
def get_price_data():
    """
    API endpoint to get the last extracted price data in JSON format.
    """
    price_data = load_price_data_from_file()

    if price_data:
        # Display JSON in a readable and formatted manner
        return jsonify(price_data)
    else:
        return jsonify({"error": "No price data available yet."})

def run_flask():
    # Run Flask without reloader (useful for multiprocessing)
    flask_app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)

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
    # This is needed for Windows to handle multiprocessing correctly
    multiprocessing.set_start_method('spawn')

    # Run the Flask API in a separate process
    flask_process = multiprocessing.Process(target=run_flask)
    flask_process.start()

    # Start the Telegram bot
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
