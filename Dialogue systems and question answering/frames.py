from frame_types import *
from slot import *

class Frame:

    def __init__(self):
        self.slots = {} 

    def add_slot(self, slot_name: str, type: Type, questions: SlotQuestions):
        self.slots[slot_name] = Slot(name=slot_name, type=type, questions=questions)

    @property
    def unfilled_slots(self):
        unfilled = []
        for _, slot in self.slots.items():
            if not slot.type.is_filled:
                unfilled.append(slot)
        return unfilled


def create_weather_forecast_frame():
    weather_frame = Frame()
    weather_frame.add_slot(
        slot_name="FORECAST LOCATION",
        type=City(),
        questions=SlotQuestions(
            texts=[
                "For what location would you like to see the weather forecast?",
                "What location?"
            ],
            patterns=[
                "in"
            ]
        )
    )
    weather_frame.add_slot(
        slot_name="FORECAST DAY",
        type=Day(),
        questions=SlotQuestions(
            texts=[
                "Which day would like to have forecasted?",
                "At what day do you want to see the forecast?"
            ],
            patterns=[
                "on"
            ]
        )
    )
    weather_frame.add_slot(
        slot_name="FORECAST TIME",
        type=Time(),
        questions=SlotQuestions(
            texts=[
                "At what time?",
                "At which time would you like to see the forecast?"
            ],
            patterns=[
                "at"
            ]
        )
    )
    return weather_frame


def create_find_a_restaurant_frame():
    rest_frame = Frame()
    rest_frame.add_slot(
        slot_name="LOCATION",
        type=City(),
        questions=SlotQuestions(
            texts=[
                "For which city?",
                "At what city?",
                "In which city?"
            ],
            patterns=[
                'in'
            ]
        )
    )
    rest_frame.add_slot(
        slot_name="TIME",
        type=Time(),
        questions=SlotQuestions(
            texts = [
                "When would you like to eat?",
                "At what time would you like to dine?"
            ],
            patterns=[
                "at"
            ]
        )
    )
    rest_frame.add_slot(
        slot_name="FOOD PREFERENCE",
        type=Food(),
        questions=SlotQuestions(
            texts=[
                "What type of food do you prefer?",
                "What would you like to eat?",
                "Any food preferences?"
            ],
            patterns=[
                "have",
                "eat",
            ]
        )
    )
    return rest_frame


def create_book_flight_frame():
    rest_frame = Frame()
    rest_frame.add_slot(
        slot_name="DEPARTURE LOCATION",
        type=City(),
        questions=SlotQuestions(
            texts=[
                "From which city do you want to go?",
                "From where are you traveling?"
            ],
            patterns=[
                "from"
            ]
        )
    )
    rest_frame.add_slot(
        slot_name="ARRIVAL LOCATION",
        type=City(),
        questions=SlotQuestions(
            texts=[
                "Which city do you want to go to?",
                "Where do you want to go traveling?"
            ],
            patterns=[
                "to"
            ]
        )
    )
    rest_frame.add_slot(
        slot_name="DEPARTURE TIME",
        type=Time(),
        questions=SlotQuestions(
            texts=[
                "When do you want to leave?",
                "At what time do you want to depart?",
                "Specify departure time."
            ],
            patterns=[
                "at"
            ]
        )
    )
    return rest_frame