from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from services.value_service import ALL_PETS

router = Router()

user_data = {}

MODIFIERS = ["F", "R", "N", "M"]


# === старт создания трейда ===
@router.callback_query(F.data == "create_trade")
async def create_trade(call: CallbackQuery):
    user_data[call.from_user.id] = {
        "offer": [],
        "want": [],
        "current": None,
        "stage": "offer"
    }

    await call.message.edit_text(
        "📦 Выбирай питомца (что ТЫ даёшь):",
        reply_markup=get_pets_keyboard(0)
    )


# === список питомцев ===
def get_pets_keyboard(page):
    per_page = 5
    start = page * per_page
    end = start + per_page

    buttons = []

    for pet in ALL_PETS[start:end]:
        buttons.append([
            InlineKeyboardButton(
                text=f"{pet['name']} ({pet['value']})",
                callback_data=f"pet_{pet['name']}"
            )
        ])

    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="⬅️", callback_data=f"page_{page-1}"))
    nav.append(InlineKeyboardButton(text="➡️", callback_data=f"page_{page+1}"))

    buttons.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


# === выбор питомца ===
@router.callback_query(F.data.startswith("pet_"))
async def select_pet(call: CallbackQuery):
    pet_name = call.data.split("_")[1]

    user_data[call.from_user.id]["current"] = {
        "name": pet_name,
        "mods": []
    }

    await call.message.edit_text(
        f"⚙️ Выбери модификаторы для {pet_name}",
        reply_markup=get_mod_keyboard()
    )


# === модификаторы ===
def get_mod_keyboard():
    buttons = []

    for mod in MODIFIERS:
        buttons.append([
            InlineKeyboardButton(text=mod, callback_data=f"mod_{mod}")
        ])

    buttons.append([
        InlineKeyboardButton(text="✅ Готово", callback_data="mod_done")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.callback_query(F.data.startswith("mod_"))
async def add_mod(call: CallbackQuery):
    mod = call.data.split("_")[1]

    user_data[call.from_user.id]["current"]["mods"].append(mod)

    await call.answer(f"Добавлен {mod}")


# === завершили модификаторы ===
@router.callback_query(F.data == "mod_done")
async def mod_done(call: CallbackQuery):
    data = user_data[call.from_user.id]

    pet = data["current"]

    text = pet["name"] + "".join(pet["mods"])

    if data["stage"] == "offer":
        data["offer"].append(text)
    else:
        data["want"].append(text)

    data["current"] = None

    if data["stage"] == "offer":
        await call.message.edit_text(
            "➕ Добавлен! Теперь:\n\n"
            "➡️ Добавь ещё или перейди дальше",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="➕ Добавить ещё", callback_data="create_trade")],
                [InlineKeyboardButton(text="➡️ К WANT", callback_data="to_want")]
            ])
        )
    else:
        await call.message.edit_text(
            "🎯 Добавлено!\n\n"
            "Готово к публикации",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="📢 Опубликовать", callback_data="publish")]
            ])
        )


# === переход к WANT ===
@router.callback_query(F.data == "to_want")
async def to_want(call: CallbackQuery):
    user_data[call.from_user.id]["stage"] = "want"

    await call.message.edit_text(
        "🎯 Выбирай что ХОЧЕШЬ:",
        reply_markup=get_pets_keyboard(0)
    )


# === публикация ===
@router.callback_query(F.data == "publish")
async def publish(call: CallbackQuery):
    data = user_data[call.from_user.id]

    await call.message.answer(
        f"📢 ТРЕЙД ОПУБЛИКОВАН\n\n"
        f"📦 Даю: {', '.join(data['offer'])}\n"
        f"🎯 Хочу: {', '.join(data['want'])}"
    )
