from aiogram.fsm.state import StatesGroup, State


class AddPlant(StatesGroup):
    waiting_for_name = State()
    waiting_for_duplicate_confirm = State()


class DeletePlant(StatesGroup):
    waiting_for_name = State()


class WaterPlant(StatesGroup):
    waiting_for_name = State()


class FeedPlant(StatesGroup):
    waiting_for_name = State()


class TransplantPlant(StatesGroup):
    waiting_for_name = State()
