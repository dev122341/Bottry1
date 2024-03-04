
ChatGPT
Certainly! I'll integrate the logic from the code you provided into the appropriate command handlers:

python
Copy code
import asyncio
import logging
import subprocess
from aiogram import Bot, Dispatcher, types
import pandas as pd
import config

admin_id = int(config.info.admin.get_secret_value())
bot = Bot(token=config.info.telegram_bot_api.get_secret_value())
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

process = None

# Command handlers

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.from_user.id == admin_id:
        await message.reply('/start_bot - Start the bot\n'
                            '/stop_bot - Stop the bot\n'
                            '/info - Show current bot settings\n'
                            '/sol_usdt - Toggle between SOL and USDT\n'
                            '/raydium_jupiter - Toggle between Raydium and Jupiter\n'
                            'token <token_address> - Change token address\n'
                            'sleep_min <number> - Minimum time between transactions in seconds\n'
                            'sleep_max <number> - Maximum time between transactions in seconds\n'
                            'volume <number> - Volume in USDT\n'
                            'Sending a txt file adds wallet addresses to rotate volume\n')
    else:
        await message.reply('You are not authorized to use this bot.')

@dp.message_handler(commands=['start_bot'])
async def start_bot(message: types.Message):
    global process
    if message.from_user.id == admin_id:
        if process is None:
            process = subprocess.Popen(['python', 'models.py'])
            await message.reply('Bot started')
        else:
            await message.reply('Bot is already running')
    else:
        await message.reply('You are not authorized to use this bot.')

@dp.message_handler(commands=['stop_bot'])
async def stop_bot(message: types.Message):
    global process
    if message.from_user.id == admin_id:
        if process:
            process.terminate()
            process = None
            await message.reply('Bot stopped')
        else:
            await message.reply('Bot is not running')
    else:
        await message.reply('You are not authorized to use this bot.')

@dp.message_handler(commands=['sol_usdt'])
async def toggle_sol_usdt(message: types.Message):
    if message.from_user.id == admin_id:
        df = pd.read_csv('settings.csv')
        if df['usdt'][0]:
            df['usdt'][0] = False
            df.to_csv('settings.csv', index=False)
            await message.reply('Toggled to use SOL')
        else:
            df['usdt'][0] = True
            df.to_csv('settings.csv', index=False)
            await message.reply('Toggled to use USDT')
    else:
        await message.reply('You are not authorized to use this bot.')

@dp.message_handler(commands=['raydium_jupiter'])
async def toggle_raydium_jupiter(message: types.Message):
    if message.from_user.id == admin_id:
        df = pd.read_csv('settings.csv')
        if df['raydium'][0]:
            df['raydium'][0] = False
            df.to_csv('settings.csv', index=False)
            await message.reply('Toggled to use Jupiter')
        else:
            df['raydium'][0] = True
            df.to_csv('settings.csv', index=False)
            await message.reply('Toggled to use Raydium')
    else:
        await message.reply('You are not authorized to use this bot.')

@dp.message_handler(commands=['info'])
async def bot_info(message: types.Message):
    if message.from_user.id == admin_id:
        dct = pd.read_csv('settings.csv').to_dict('records')[0]
        value = 'USDT' if dct['usdt'] else 'SOL'
        dex = 'Raydium' if dct['raydium'] else 'Jupiter'

        await message.reply(f'Value usdt: {dct["value"]}\n'
                             f'Volume is rotating through {dex} in {value}\n'
                             f'Minimum delay between transactions: {dct["sleep_min"]}\n'
                             f'Maximum delay between transactions: {dct["sleep_max"]}\n')
    else:
        await message.reply('You are not authorized to use this bot.')

@dp.message_handler(commands=['token'])
async def change_token(message: types.Message):
    if message.from_user.id == admin_id:
        token = message.text.split()[1]
        df = pd.read_csv('settings.csv')
        df['token'][0] = str(token)
        df.to_csv('settings.csv', index=False)
        await message.reply(f'Token address changed to {token}')
    else:
        await message.reply('You are not authorized to use this bot.')

@dp.message_handler(commands=['sleep_min'])
async def change_sleep_min(message: types.Message):
    if message.from_user.id == admin_id:
        sleep_min = int(message.text.split()[1])
        df = pd.read_csv('settings.csv')
        df['sleep_min'][0] = sleep_min
        df.to_csv('settings.csv', index=False)
        await message.reply(f'Minimum delay between transactions changed to {sleep_min}')
    else:
        await message.reply('You are not authorized to use this bot.')

@dp.message_handler(commands=['sleep_max'])
async def change_sleep_max(message: types.Message):
    if message.from_user.id == admin_id:
        sleep_max = int(message.text.split()[1])
        df = pd.read_csv('settings.csv')
        df['sleep_max'][0] = sleep_max
        df.to_csv('settings.csv', index=False)
        await message.reply(f'Maximum delay between transactions changed to {sleep_max}')
    else:
        await message.reply('You are not authorized to use this bot.')

@dp.message_handler(commands=['volume'])
async def change_volume(message: types.Message):
    if message.from_user.id == admin_id:
        volume = int(message.text.split()[1])
        df = pd.read_csv('settings.csv')
        df['value'][0] = volume
        df.to_csv('settings.csv', index=False)
        await message.reply(f'Volume changed to {volume} USDT')
    else:
        await message.reply('You are not authorized to use this bot.')

@dp.message_handler(content_types=['document'])
async def handle_document(message: types.Message):
    if message.from_user.id == admin_id:
        file_id = message.document.file_id
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path
        await bot.download_file(file_path, 'private_keys.txt')
        await message.reply(f'Added new private keys')
    else:
        await message.reply('You are not authorized to use this bot.')

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
