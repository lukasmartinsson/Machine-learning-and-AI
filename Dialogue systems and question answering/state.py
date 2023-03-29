from enum import Enum
from frames import create_find_a_restaurant_frame, create_weather_forecast_frame, create_book_flight_frame
from topic import Topic
from rules import KeywordMatchingRule

class DialogueState(Enum):
    SELECT_FRAME = "select_frame"
    FILL_FRAME = "fill_frame"


class StateManager:
    
    weather_topic_id = "weather"
    restaurant_topic_id = "restaurant"
    book_flight_topic_id = "flight"

    def __init__(self):
        self._state = DialogueState.SELECT_FRAME
        self._active_topic = None
        self._topics = self.create_topics()

    @staticmethod
    def create_topics():
        topics = {
            StateManager.weather_topic_id: Topic(
                topic_id=StateManager.weather_topic_id,
                description="Providing a weather forecast.", 
                rules=[
                    KeywordMatchingRule(keywords=['weather', 'forecast', 'temperature'])
                ],
                frame=create_weather_forecast_frame()
            ),
            StateManager.restaurant_topic_id: Topic(
                topic_id=StateManager.restaurant_topic_id,
                description="Finding a restaurant.", 
                rules=[
                    KeywordMatchingRule(keywords=['restaurant', 'food', 'dining','diner', 'eat'])
                ],
                frame=create_find_a_restaurant_frame()
            ),
            StateManager.book_flight_topic_id: Topic(
                topic_id=StateManager.book_flight_topic_id,
                description="Finding the next flight.", 
                rules=[
                    KeywordMatchingRule(keywords=['flight', 'travel', 'vacation', 'fly'])
                ],
                frame=create_book_flight_frame()
            )
        }
        return topics

    @property
    def topics(self):
        return self._topics

    @property
    def active_topic(self):
        return self._active_topic

    @property
    def current_state(self):
        return self._state

    def make_topic_selection(self, topic):
        if topic.topic_id not in self.topics:
            return
        else:
            self._active_topic = topic
            self._state = DialogueState.FILL_FRAME

    def get_unfilled_slot_for_current_topic(self):
        for slot in self.active_topic.frame.unfilled_slots:
            if not slot.type.is_filled:
                return slot
        return None