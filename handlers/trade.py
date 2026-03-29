from aiogram import Router
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from services.value_service import get_value, load_all_pets

router = Router()

trades = []
favorites = {}
current_index = {}

class TradeFSM(StatesGroup):
    adding_pets = State()
    adding_wishlist = State()

def browse_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️", callback_data="prev"),
            InlineKeyboardButton(text="➡️", callback_data="next")
        ],
        [InlineKeyboardButton(text="❤️", callback_data="fav")]
    ])

@router.callback_query(lambda c: c.data == "create_trade")
async def create_trade(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.update_data(pets=[], wishlist=[])
    await cb.message.answer("Вводи питомцев (по одному). Напиши 'done' когда закончил")
    await state.set_state(TradeFSM.adding_pets)
    await cb.answer()

@router.message(TradeFSM.adding_pets)
async def add_pet(msg: Message, state: FSMContext):
    if msg.text.lower() == "done":
        await msg.answer("Теперь введи, что хочешь получить:")
        await state.set_state(TradeFSM.adding_wishlist)
        return

    data = await state.get_data()
    pets = data["pets"]
    value = await get_value(msg.text)
    pets.append((msg.text, value))
    await state.update_data(pets=pets)
    await msg.answer(f"Добавлено: {msg.text} ({value})")

@router.message(TradeFSM.adding_wishlist)
async def add_wishlist(msg: Message, state: FSMContext):
    if msg.text.lower() == "done":
        data = await state.get_data()
        total = sum(v for _, v in data["pets"])
        result = "FAIR"
        if total > 500:
            result = "WIN"
        elif total < 200:
            result = "LOSE"

        trade = {
            "pets": data["pets"],
            "wish": data["wishlist"],
            "value": total,
            "result": result
        }
        trades.append(trade)
        await msg.answer(f"✅ Трейд создан!\n💰 {total} | {result}")
        await state.clear()
        return

    data = await state.get_data()
    wish = data["wishlist"]
    wish.append(msg.text)
    await state.update_data(wishlist=wish)
    await msg.answer(f"Хочешь: {msg.text}")

def format_trade(trade):
    text = "🐾 Ты даёшь:\n"
    for p, v in trade["pets"]:
        text += f"- {p} ({v})\n"
    text += "\n🎯 Хочешь:\n"
    for w in trade["wish"]:
        text += f"- {w}\n"
    text += f"\n💰 Value: {trade['value']}\n📊 {trade['result']}"
    return text

@router.callback_query(lambda c: c.data == "browse")
async def browse(cb: CallbackQuery):
    if not trades:
        await cb.message.answer("Нет трейдов")
        return
    user = cb.from_user.id
    current_index[user] = 0
    trade = trades[0]
    await cb.message.answer(format_trade(trade), reply_markup=browse_kb())

@router.callback_query(lambda c: c.data in ["next", "prev"])
async def navigate(cb: CallbackQuery):
    user = cb.from_user.id
    if user not in current_index:
        return
    current_index[user] += 1 if cb.data == "next" else -1
    current_index[user] %= len(trades)
    trade = trades[current_index[user]]
    await cb.message.edit_text(format_trade(trade), reply_markup=browse_kb())

@router.callback_query(lambda c: c.data == "fav")
async def add_fav(cb: CallbackQuery):
    user = cb.from_user.id
    idx = current_index.get(user, 0)
    favorites.setdefault(user, []).append(idx)
    await cb.answer("Добавлено в избранное ❤️")
