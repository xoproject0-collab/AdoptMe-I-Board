# trade.py
import json
import uuid
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

TRADES_FILE = "data/trades.json"  # файл для хранения всех трейдов пользователей

# -------------------- Вспомогательные функции --------------------
def load_trades():
    try:
        with open(TRADES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_trades(trades):
    with open(TRADES_FILE, "w", encoding="utf-8") as f:
        json.dump(trades, f, ensure_ascii=False, indent=2)

def format_trade(trade):
    give_list = ", ".join([f'{p["id"]}({" ".join(p["mods"])})' for p in trade["give"]])
    want_list = ", ".join([f'{p["id"]}({" ".join(p["mods"])})' for p in trade["want"]])
    return f"🔹 {trade['trade_id']}\nДаю: {give_list}\nХочу: {want_list}\n"

# -------------------- Создание трейда --------------------
@router.callback_query(F.data == "create_trade")
async def create_trade_start(callback: CallbackQuery):
    # Тут вызываем pets.py для выбора питомцев, например:
    await callback.message.edit_text(
        "Начинаем создание трейда!\nВыберите питомцев, которых отдаёте через кнопки.\nПосле выбора питомцев перейдите к выбору того, что хотите получить.",
    )
    # pets.py должен вызвать publish_trade после выбора питомцев

# -------------------- Публикация трейда --------------------
def publish_trade(user_id, give, want):
    trades = load_trades()
    trade_id = str(uuid.uuid4())[:8]  # уникальный id
    trades.append({
        "user_id": user_id,
        "give": give,
        "want": want,
        "trade_id": trade_id
    })
    save_trades(trades)
    return trade_id

# -------------------- Просмотр своих трейдов --------------------
@router.callback_query(F.data == "my_trades")
async def my_trades(callback: CallbackQuery):
    trades = load_trades()
    user_trades = [t for t in trades if t["user_id"] == callback.from_user.id]
    if not user_trades:
        await callback.message.answer("У тебя пока нет трейдов.")
        return

    for t in user_trades:
        text = format_trade(t)
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton("❌ Удалить трейд", callback_data=f"delete_{t['trade_id']}")]
        ])
        await callback.message.answer(text, reply_markup=kb)

# -------------------- Удаление трейда --------------------
@router.callback_query(F.data.startswith("delete_"))
async def delete_trade_callback(callback: CallbackQuery):
    trade_id = callback.data.split("_")[1]
    trades = load_trades()
    trades = [t for t in trades if not (t["user_id"] == callback.from_user.id and t["trade_id"] == trade_id)]
    save_trades(trades)
    await callback.message.answer(f"Трейд {trade_id} успешно удалён!")

# -------------------- Авто форматирование для ленты --------------------
def get_all_trades_for_feed():
    trades = load_trades()
    feed_list = []
    for t in trades:
        text = format_trade(t)
        feed_list.append(text)
    return feed_list
