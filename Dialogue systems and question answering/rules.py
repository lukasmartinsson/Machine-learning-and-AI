from abc import ABC, abstractmethod

class AbstractRule(ABC):
    @abstractmethod
    def matches_input(self, processed_input: list) -> bool:
        pass

class KeywordMatchingRule(AbstractRule):
    
    def __init__(self, keywords: list):
        self._kws = keywords

    @property
    def keywords(self):
        return self._kws

    def matches_input(self, processed_input: list) -> bool:
        for word in processed_input:
            if word in self.keywords:
                return True
        return False
