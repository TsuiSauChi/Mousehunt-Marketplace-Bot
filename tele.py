from summarizes import summarizes

import telegram
import asyncio
import time
import json

file_path = 'tele.txt'  # Change this to your file's path
with open(file_path, 'r') as file:
    # Read the entire content of the file
    file_content = file.read()

TOKEN = file_content
USER_ID = "335838693"

# Time interval between messages (in seconds)
INTERVAL = 1800

# Create the bot object
bot = telegram.Bot(token=TOKEN)

# Send the message
async def send_message():
    sb_summary, buy_summary, sell_summary = summarizes()

    print(sb_summary)
    print()
    print(buy_summary)
    print()
    print(sell_summary)

    await bot.send_message(chat_id=USER_ID, text=sb_summary, parse_mode="Markdown")

    if len(buy_summary) > 4096:
        truncated_message = buy_summary[:4093]
        await bot.send_message(chat_id=USER_ID, text=truncated_message, parse_mode="Markdown")
    else:
        if len(buy_summary) > 0:
             await bot.send_message(chat_id=USER_ID, text=buy_summary, parse_mode="Markdown")

    if len(sell_summary) > 4096:
        truncated_message = sell_summary[:4093]
        await bot.send_message(chat_id=USER_ID, text=truncated_message, parse_mode="Markdown")
    else:
        if len(sell_summary) > 0:
             await bot.send_message(chat_id=USER_ID, text=sell_summary, parse_mode="Markdown")

# Periodically send the message

loop = asyncio.get_event_loop()

while True:
    loop.run_until_complete(send_message())
    time.sleep(INTERVAL)