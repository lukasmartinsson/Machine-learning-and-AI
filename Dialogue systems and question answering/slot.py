from frame_types import Type

class SlotQuestions:
    def __init__(self, texts: list, patterns: list):
        self._texts = texts
        self._patterns = patterns
    
    @property
    def texts(self):
        return self._texts
    
    @property
    def patterns(self):
        return self._patterns


class Slot:
    def __init__(self, name: str, type: Type, questions: SlotQuestions):
        self._name = name
        self._type = type
        self._questions = questions

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def questions(self):
        return self._questions

    