from abc import ABC, abstractmethod
from datetime import datetime

class Type(ABC):

    @property
    @abstractmethod
    def type_name(self):
        pass

    @property
    @abstractmethod
    def content(self):
        pass

    @property
    @abstractmethod
    def is_filled(self):
        pass

    @abstractmethod
    def fill_content(self):
        pass

    @abstractmethod
    def parse_keyword(self, kw: str):
        pass
        


class City(Type):

    def __init__(self):
        self._city_name = None

    @property
    def type_name(self):
        return 'city'

    @property
    def content(self):
        return self._city_name

    @property
    def is_filled(self):
        return self._city_name is not None

    def fill_content(self, city_name: str):
        self._city_name = city_name

    def parse_keyword(self, kw: str): 
        city = kw.lower()
        available_cities = ['gothenburg', 'stockholm', 'london', 'new york']
        if city in available_cities:
            self.fill_content(city)
        else:
            return f"Did not find the city of '{city}'. Available cities: {available_cities}."


class Day(Type):

    def __init__(self):
        self._day = None

    @property
    def type_name(self):
        return 'day'

    @property
    def content(self):
        return self._day

    @property
    def is_filled(self):
        return self._day is not None

    def fill_content(self, day: str):
        self._day = day

    def parse_keyword(self, kw: str):
        day = kw.lower()
        available_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        if day in available_days:
            self.fill_content(day)
        else:
            return f"I could not understand which day '{day}' is. Available days: {available_days}."


class Time(Type):

    def __init__(self):
        self._hour = None
        self._minute = None

    @property
    def type_name(self):
        return 'time'

    @property
    def is_filled(self):
        return self._hour is not None and self._minute is not None

    def fill_content(self, hour=None, minute=None):
        self._hour = hour if hour is not None else self._hour
        self._minute = minute if minute is not None else self._minute

    @property
    def content(self):
        return {"hour": self._hour, "minute": self._minute}
    
    def parse_keyword(self, kw: str):
        try:
            time = datetime.strptime(kw.lower(), '%H:%M')
            self.fill_content(time.hour, time.minute)
        except:
            return f"I don't understand the time you provided. When talking about time to me please use 'HH:MM' format."



class Food(Type):

    def __init__(self):
        self._food = None

    @property
    def type_name(self):
        return 'food_preference'

    @property
    def is_filled(self):
        return self._food is not None

    def fill_content(self, food: str):
        self._food = food

    @property
    def content(self):
        return self._food

    def parse_keyword(self, kw: str):
        food_preference = kw
        available_preferences = ["no", "vegetarian", "chicken", "beef", "vegan", "fish"]
        if food_preference in available_preferences:
            self.fill_content(food_preference)
        else:
            return f"I'm sorry, '{food_preference}' is not an available preference. Please choose from: {available_preferences}."
