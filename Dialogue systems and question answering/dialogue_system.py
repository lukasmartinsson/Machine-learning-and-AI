import time
from state import DialogueState, StateManager
import random


class DialogueSystem:
    response_time_s = 1

    def __init__(self):
        self.user_name = input("What is your name?: ").strip()
        self.state_manager = StateManager()
        self.current_slot = None
        self.prev_user_input = None

    def interact(self):

        # Make topic selection
        self.select_topic()

        # Get the first question regarding the topic
        self.current_slot = self.state_manager.get_unfilled_slot_for_current_topic()

        while self.current_slot:
            # Ask a question
            slot_questions = self.current_slot.questions
            question_text = random.choice(slot_questions.texts)
            print(f"\nSystem: {question_text}\n")

            # Get user answer
            user_input = input(f"{self.user_name}: ")
            processed_input = self.process_input(user_input)

            # Find the next word after a matching pattern for the asked question
            keyword = None
            for pattern in slot_questions.patterns:
                for i, word in enumerate(processed_input):
                    if len(processed_input) == 1:
                        keyword = word  # If user only supplies a single word, we also regard this as a keyword
                    if word == pattern:
                        keyword = processed_input[i + 1]
                        break

            if keyword:
                # Attempt to parse the keyword and fill up the current slot 
                error_response = self.current_slot.type.parse_keyword(kw=keyword)
                if error_response:
                    print(f"\nSystem: {error_response}\n")
            else:
                print(f"\nSystem: I didn't understand what you said.\n")

            # Get a new unfilled slot
            self.current_slot = self.state_manager.get_unfilled_slot_for_current_topic()

        print("\nSystem: Conversation over! Check that information is correct:")
        print(f"\tTopic: '{self.state_manager.active_topic.description}'")
        for _, slot in self.state_manager.active_topic.frame.slots.items():
            print(f"\t{slot.name}, [{slot.type.type_name}: {slot.type.content}]")
        print("\nSystem: I must now query an API to fill the request for you but we leave that for another time :)")

    def process_input(self, user_input):
        return [word.lower() for word in user_input.strip().split(" ")]

    def select_topic(self):
        print(f"\nSystem: Hi {self.user_name}.")
        time.sleep(DialogueSystem.response_time_s)
        print("I can help you with the following tasks: ")

        for topic in self.state_manager.topics.values():
            time.sleep(DialogueSystem.response_time_s)
            print(f"* {topic.description}")

        time.sleep(DialogueSystem.response_time_s)
        print("What would you like me to help you with?\n")

        while self.state_manager.current_state == DialogueState.SELECT_FRAME:
            user_input = input(f"{self.user_name}: ")
            processed_input = self.process_input(user_input)

            topic = self.determine_topic(processed_input)
            if topic is None:
                print("\nSystem: Unknown topic. Please repeat what you would like me to help you with.\n")
                continue
            self.state_manager.make_topic_selection(topic)

        for topic in self.state_manager.topics.values():
            if topic.topic_id == self.state_manager.active_topic.topic_id:
                print(f"\nSystem: I will now help you with {topic.description.lower()}")

        time.sleep(DialogueSystem.response_time_s)

    """
    Attempt to match the user input to one of the topics
    """

    def determine_topic(self, processed_input):
        for topic in self.state_manager.topics.values():
            if topic.matches_input(processed_input):
                return topic
        return None
