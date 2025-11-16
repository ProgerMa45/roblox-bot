import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# === НАСТРОЙКИ ===
BOT_TOKEN = "8476199583:AAGIObszhz_ucZvAxlA25NW9f68d-ItUc4g"  # ← Замени
CHANNEL_1 = "https://t.me/+9IlMf5BuCSQ0YTY6"           # ← Замени
CHANNEL_2 = "https://t.me/+Onnhx5vtGpJmYjRi"           # ← Замени

# === БАЗА СКРИПТОВ (добавляй новые сюда!) ===
SCRIPTS = {
    "gym_league": {
        "name": "Gym League Auto Farm",
        "code": """
-- Gym League Keyless Auto Farm
loadstring(game:HttpGet("https://raw.githubusercontent.com/AhmadV99/Script-Games/main/Gym League.lua"))()
        """.strip()
    },
    "99nights": {
        "name": "99 Nights in the Forest AFK Win",
        "code": """
-- 99 Nights Auto Win + Diamonds
loadstring(game:HttpGet("https://raw.githubusercontent.com/m00ndiety/99-nights-in-the-forest/refs/heads/main/Main"))()
        """.strip()
    },
    "pet_sim_x": {
        "name": "Pet Simulator X Auto Egg",
        "code": """
loadstring(game:HttpGet("https://raw.githubusercontent.com/RegularVynixu/Vynixius/main/Pet%20Simulator%20X.lua"))()
        """.strip()
    },
    "mm2": {
        "name": "Murder Mystery 2 ESP + Speed",
        "code": """
loadstring(game:HttpGet("https://raw.githubusercontent.com/Ethanoj1/EclipseMM2/master/MM2Script.lua"))()
        """.strip()
    }
    # ← Добавляй новые: "kod": { "name": "...", "code": "..." }
}

# === СОСТОЯНИЯ ===
class Form(StatesGroup):
    waiting = State()

# === КЛАВИАТУРЫ ===
def get_main_menu():
    kb = [[InlineKeyboardButton(text=f"{SCRIPTS[k]['name']}", callback_data=f"get_{k}")] for k in SCRIPTS]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def get_sub_keyboard(code):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Канал 1", url=f"https://t.me/{CHANNEL_1[1:]}")],
        [InlineKeyboardButton(text="Канал 2", url=f"https://t.me/{CHANNEL_2[1:]}")],
        [InlineKeyboardButton(text="Я подписался", callback_data=f"check_{code}")]
    ])

# === БОТ ===
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# === ПРОВЕРКА ПОДПИСКИ ===
async def is_subscribed(user_id):
    try:
        return all((await bot.get_chat_member(ch, user_id)).status in ["member", "administrator", "creator"]
                   for ch in [CHANNEL_1, CHANNEL_2])
    except:
        return False

# === /start с кодом ===
@dp.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext):
    args = message.text.split(maxsplit=1)
    code = args[1] if len(args) > 1 else None

    if code and code in SCRIPTS:
        await message.answer(
            f"Ты хочешь: **{SCRIPTS[code]['name']}**\n\n"
            f"Подпишись на каналы:",
            reply_markup=get_sub_keyboard(code),
            parse_mode="Markdown"
        )
        await state.update_data(code=code)
        await state.set_state(Form.waiting)
    else:
        await message.answer("Выбери скрипт:", reply_markup=get_main_menu())

# === Выбор из меню ===
@dp.callback_query(F.data.startswith("get_"))
async def get_script(callback: types.CallbackQuery, state: FSMContext):
    code = callback.data.split("_", 1)[1]
    await callback.message.edit_text(
        f"Ты выбрал: **{SCRIPTS[code]['name']}**\n\nПодпишись:",
        reply_markup=get_sub_keyboard(code),
        parse_mode="Markdown"
    )
    await state.update_data(code=code)
    await state.set_state(Form.waiting)

# === Проверка и выдача ===
@dp.callback_query(F.data.startswith("check_"))
async def check_sub(callback: types.CallbackQuery, state: FSMContext):
    code = callback.data.split("_", 1)[1]
    data = await state.get_data()
    if data.get("code") != code:
        await callback.answer("Ошибка!", show_alert=True)
        return

    if await is_subscribed(callback.from_user.id):
        script = SCRIPTS[code]
        await callback.message.edit_text("Готово! Вот твой скрипт:")
        await bot.send_message(
            callback.from_user.id,
            f"**{script['name']}**\n\n```lua
            parse_mode="Markdown"
        )
        await state.clear()
    else:
        await callback.answer("Ты не подписался на оба канала!", show_alert=True)

# === ЗАПУСК ===
async def main():
    print("Бот запущен 24/7")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())