import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# === НАСТРОЙКИ ===
BOT_TOKEN = "8476199583:AAGIObszhz_ucZvAxlA25NW9f68d-ItUc4g"  
CHANNEL_1_LINK = "https://t.me/Xleb4ikScript"
CHANNEL_2_LINK = "https://t.me/Sigma4Script"
CHANNEL_1_USERNAME = "@Xleb4ikScript"
CHANNEL_2_USERNAME = "@Sigma4Script"
TUTORIAL_LINK = "https://youtu.be/-SNisYqzKx4?si=uNAFUjhi-X6F1sDq"  

# === СКРИПТЫ ПО ID ===
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
IMAGE_URL = "data:image/jpeg;base64,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"  

# === СОСТОЯНИЯ ===
class Form(StatesGroup):
    waiting = State()

# === ПРИВЕТСТВЕННЫЙ ТЕКСТ ===
WELCOME_TEXT = (
    "*Приветствую в scriptmajproRB_bot!*\n\n"
    "Данный бот создан для **получения ключа и скрипта**\n\n"
    f"Туториал как получить ключ вы можете [перейти по ссылке]({TUTORIAL_LINK})"
)

# === КЛАВИАТУРЫ ===
def get_sub_keyboard(script_id: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Канал 1", url=CHANNEL_1_LINK)],
        [InlineKeyboardButton(text="Канал 2", url=CHANNEL_2_LINK)],
        [InlineKeyboardButton(text="Я подписался", callback_data=f"check_{script_id}")]
    ])

# === БОТ ===
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# === ПРОВЕРКА ПОДПИСКИ ===
async def is_subscribed(user_id: int) -> bool:
    try:
        m1 = await bot.get_chat_member(CHANNEL_1_USERNAME, user_id)
        m2 = await bot.get_chat_member(CHANNEL_2_USERNAME, user_id)
        return (m1.status in ["member", "administrator", "creator"] and
                m2.status in ["member", "administrator", "creator"])
    except:
        return False

# === /start ===
@dp.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext):
    args = message.text.split(maxsplit=1)
    script_id = args[1] if len(args) > 1 else None

    if script_id and script_id in SCRIPTS:
        # По ID — сразу подписка
        text = (
            f"**Скрипт #{script_id}**\n\n"
            f"Подпишитесь на каналы:\n\n"
            f"1. {CHANNEL_1_LINK}\n"
            f"2. {CHANNEL_2_LINK}\n\n"
            f"Нажмите **'Я подписался'**"
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
        # Просто /start — приветствие
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=IMAGE_URL,
            caption=WELCOME_TEXT,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

# === Проверка подписки и выдача ===
@dp.callback_query(F.data.startswith("check_"))
async def send_script(callback: types.CallbackQuery, state: FSMContext):
    script_id = callback.data.split("_", 1)[1]
    data = await state.get_data()
    
    if data.get("script_id") != script_id:
        await callback.answer("ошибка", show_alert=True)
        return

    if await is_subscribed(callback.from_user.id):
        code = SCRIPTS.get(script_id, "")
        text = f"```lua\n{code}\n```"
        await callback.message.edit_caption(
            caption=text,
            reply_markup=None,
            parse_mode="Markdown"
        )
        await state.clear()
    else:
        await callback.answer("ошибка", show_alert=True)

# === ЗАПУСК ===
async def main():
    print("scriptmajproRB_bot запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
