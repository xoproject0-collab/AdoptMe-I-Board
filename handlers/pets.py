from aiogram import Router, F
from aiogram.types import CallbackQuery
from services.value_service import get_pets
from keyboards.pets_keyboard import pets_page, modifiers_keyboard

router = Router()

user_selection = {}  # хранит текущий выбор пользователя

@router.callback_query(F.data.startswith("create_trade"))
async def start_trade(callback: CallbackQuery):
    pets = await get_pets()
    user_selection[callback.from_user.id] = {"give": [], "want": []}
    await callback.message.edit_text("Выберите питомца, которого вы даёте:", reply_markup=pets_page(pets, 0))

@router.callback_query(F.data.startswith("pet_"))
async def select_pet(callback: CallbackQuery):
    pet_id = int(callback.data.split("_")[1])
    user_selection[callback.from_user.id]["give"].append(pet_id)
    await callback.message.edit_text("Выберите модификаторы:", reply_markup=modifiers_keyboard())

@router.callback_query(F.data.startswith("mod_"))
async def select_modifier(callback: CallbackQuery):
    mod = callback.data.split("_")[1]
    if mod != "done":
        last_pet = user_selection[callback.from_user.id]["give"][-1]
        if isinstance(last_pet, dict):
            last_pet["mods"].append(mod)
        else:
            user_selection[callback.from_user.id]["give"][-1] = {"id": last_pet, "mods": [mod]}
        await callback.answer(f"{mod} применен")
    else:
        await callback.message.edit_text("Выбран питомец! Можете добавить еще или перейти к выбору желаемого.", reply_markup=None)
