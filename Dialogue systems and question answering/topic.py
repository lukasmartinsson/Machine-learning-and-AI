from frames import Frame

class Topic:
    def __init__(self, topic_id, description, rules, frame: Frame):
        self._topic_id = topic_id
        self._description = description
        self._rules = rules
        self._frame = frame
    
    @property
    def topic_id(self):
        return self._topic_id

    @property
    def description(self):
        return self._description

    @property
    def rules(self):
        return self._rules

    @property
    def frame(self):
        return self._frame

    def matches_input(self, processed_input) -> bool:
        for rule in self.rules:
            if rule.matches_input(processed_input):
                return True
        return False 


    
    
