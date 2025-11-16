import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# === НАСТРОЙКИ ===
BOT_TOKEN = "8476199583:AAGIObszhz_ucZvAxlA25NW9f68d-ItUc4g" 
CHANNEL_1_LINK = "https://t.me/Sigma4Script"
CHANNEL_2_LINK = "https://t.me/Xleb4ikScript2"
CHANNEL_1_USERNAME = "@Sigma4Script"
CHANNEL_2_USERNAME = "@Xleb4ikScript22"
TUTORIAL_LINK = "https://youtu.be/-SNisYqzKx4?si=tLw5kmmM9m_q8o4J"  

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
IMAGE_URL = "https://ih1.redbubble.net/image.5506461112.7176/bg,f8f8f8-flat,750x,075,f-pad,750x1000,f8f8f8.jpg" 

# === СОСТОЯНИЯ ===
class Form(StatesGroup):
    waiting = State()

# === КЛАВИАТУРЫ ===
def get_sub_keyboard(script_id: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Канал 1", url=CHANNEL_1_LINK)],
        [InlineKeyboardButton(text="Канал 2", url=,CHANNEL_2_LINK)],
        [InlineKeyboardButton(text="Я подписался", callback_data=f"check_{script_id}")]
    ])

# === БОТ ===
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# === ПРЕДСТАРТОВЫЙ ТЕКСТ ===
WELCOME_TEXT = (
    "*Приветствую в scriptmajproRB_bot!*\n\n"
    "Данный бот создан для **получения ключа и скрипта**\n\n"
    f"Туториал как получить ключ вы можете [перейти по ссылке]({TUTORIAL_LINK})"
)

# === ПРОВЕРКА ПОДПИСКИ ===
async def is_subscribed(user_id: int) -> bool:
    try:
        m1 = await bot.get_chat_member(CHANNEL_1_USERNAME, user_id)
        m2 = await bot.get_chat_member(CHANNEL_2_USERNAME, user_id)
        return (m1.status in ["member", "administrator", "creator"] and
                m2.status in ["member", "administrator", "creator"])
    except:
        return False

# === /start (только по ID) ===
@dp.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext):
    args = message.text.split(maxsplit=1)
    script_id = args[1] if len(args) > 1 else None

    if not script_id or script_id not in SCRIPTS:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=IMAGE_URL,
            caption=WELCOME_TEXT,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        return

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

# === Проверка ===
@dp.callback_query(F.data.startswith("check_"))
async def send_script(callback: types.CallbackQuery, state: FSMContext):
    script_id = callback.data.split("_", 1)[1]
    data = await state.get_data()
    
    if data.get("script_id") != script_id:
        await callback.answer("ошибка", show_alert=True)
        return

    if await is_subscribed(callback.from_user.id):
        code = SCRIPTS.get(script_id, "")
        text = (
            f"```lua\n{code}\n```"
        )
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
