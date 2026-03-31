from aiogram.fsm.state import StatesGroup, State


class AddPlant(StatesGroup):
    waiting_for_name = State()


class DeletePlant(StatesGroup):
    waiting_for_name = State


class WaterPlant(StatesGroup):
    waiting_for_name = State


class FeedPlant(StatesGroup):
    warning_for_name = State


class TransplantPlant(StatesGroup):
    waiting_for_name = State
