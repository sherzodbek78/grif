import asyncio
import wikipedia
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

TOKEN = '474897063:AAEVjlMDNHQ37ba2RfusAftuoxwGhy4VE9E'
wikipedia.set_lang('uz')

dp = Dispatcher()


# Command handler
@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer("salom")
    try:
        respond = wikipedia.summary(message.text)
        await message.answer(respond)
    except:  
        await message.answer("bu mavzuga oid maqola top")


# Run the bot
async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
          
