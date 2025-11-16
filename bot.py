import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# === НАСТРОЙКИ ===
BOT_TOKEN = "8476199583:AAGIObszhz_ucZvAxlA25NW9f68d-ItUc4g"  
CHANNEL_LINK = "https://t.me/+9IlMf5BuCSQ0YTY6" 

# === СКРИПТЫ ПО ID (start/1, start/2...) ===
SCRIPTS = {
    "1": """
loadstring(game:HttpGet("https://raw.githubusercontent.com/VapeVoidware/VW-Add/main/nightsintheforest.lua", true))()
    """.strip(),
    "2": """
loadstring(game:HttpGet("https://raw.githubusercontent.com/adibhub1/99-nighit-in-forest/refs/heads/main/99 night in forest"))()
    """.strip(),
    "3": """
loadstring(game:HttpGet("https://raw.githubusercontent.com/m00ndiety/99-nights-in-the-forest/refs/heads/main/Main"))()
    """.strip(),
    "4": """
loadstring(game:HttpGet("https://raw.githubusercontent.com/GEC0/gec/refs/heads/main/Gec.Loader"))()
    """.strip(),
    "5": """
loadstring(game:HttpGet("https://raw.githubusercontent.com/collonroger/pigeonhub/refs/heads/main/autofarmdiamonds.lua"))()
    """.strip(),
    "6": """
loadstring(game:HttpGet("https://raw.githubusercontent.com/yoursvexyyy/VEX-OP/refs/heads/main/99 nights in the forest"))()
    """.strip()
}

# === ИЗОБРАЖЕНИЕ ===
IMAGE_URL = "https://polinka.top/pics2/uploads/posts/2024-01/1706579927_polinka-top-p-gigachad-risunok-vkontakte-1.jpg"  

# === СОСТОЯНИЯ ===
class Form(StatesGroup):
    waiting = State()

# === КЛАВИАТУРЫ ===
def get_sub_keyboard(script_id: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подписаться на канал", url=CHANNEL_LINK)],
        [InlineKeyboardButton(text="Я подписался", callback_data=f"check_{script_id}")]
    ])

# === БОТ ===
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# === /start и /start id (БЕЗ ПРОВЕРКИ ПОДПИСКИ) ===
@dp.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext):
    args = message.text.split()
    script_id = args[1] if len(args) > 1 else None

    if script_id and script_id in SCRIPTS:
        # По ссылке t.me/bot?start=1
        text = (
            f"Вы выбрали скрипт **#{script_id}**\n\n"
            f"Чтобы получить — **подпишитесь на канал**:\n"
            f"{CHANNEL_LINK}\n\n"
            f"После нажмите **'Я подписался'**"
        )
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=IMAGE_URL,
            caption=text,
            reply_markup=get_sub_keyboard(script_id),
            parse_mode="Markdown"
        )
        await state.update_data(script_id=script_id)
        await state.set_state(Form.waiting)
    else:
        # Обычный /start
        text = (
            "*Приветствую в NameBot!*\n\n"
            "Данный бот создан для **получения скриптов** на 99 Nights in the Forest!\n\n"
            "Поддержка: [t.me/namechannel](https://t.me/namechannel)\n\n"
            "Выберите скрипт:"
        )
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"Скрипт #{i}", url=f"https://t.me/{(await bot.get_me()).username}?start={i}")] 
            for i in SCRIPTS.keys()
        ])
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=IMAGE_URL,
            caption=text,
            reply_markup=kb,
            parse_mode="Markdown"
        )

# === Выдача скрипта (БЕЗ ПРОВЕРКИ) ===
@dp.callback_query(F.data.startswith("check_"))
async def send_script(callback: types.CallbackQuery, state: FSMContext):
    script_id = callback.data.split("_", 1)[1]
    data = await state.get_data()
    
    if data.get("script_id") != script_id:
        await callback.answer("Ошибка! /start", show_alert=True)
        return

    # ВЫДАЁМ СРАЗУ — БЕЗ ПРОВЕРКИ
    code = SCRIPTS.get(script_id, "-- Не найден")
    text = (
        f"**Скрипт #{script_id} выдан!**\n\n"
        f"```lua\n{code}\n```\n\n"
        f"Поддержка: {CHANNEL_LINK}"
    )
    await callback.message.edit_caption(
        caption=text,
        reply_markup=None,
        parse_mode="Markdown"
    )
    await state.clear()

# === ЗАПУСК ===
async def main():
    print("99 Nights Bot (без ID) запущен 24/7")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
