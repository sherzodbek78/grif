import asyncio
import wikipedia
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

TOKEN = '8474897063:AAEVjlMDNHQ37ba2RfusAftuoxwGhy4VE9E'
wikipedia.set_lang('uz')

dp = Dispatcher()

@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer("Salom! Mavzu yuboring, men Wikipedia'dan ma'lumot topib beraman.")

@dp.message()
async def wiki_search_handler(message: Message) -> None:
    try:
        respond = wikipedia.summary(message.text)
        await message.answer(respond)
    except:
        await message.answer("Bu mavzuga oid maqola topilmadi.")

async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
