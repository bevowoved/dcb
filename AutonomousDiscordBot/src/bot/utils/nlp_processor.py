import re
from collections import defaultdict

class NLPProcessor:
    def __init__(self):
        self.response_patterns = defaultdict(list)
        self.load_default_patterns()

    def load_default_patterns(self):
        self.response_patterns['greeting'].extend([
            (r'\b(hi|hello|hey)\b', "Hello! How can I assist you today?"),
            (r'\bhow are you\b', "I'm functioning well, thank you! How can I help you?"),
        ])
        self.response_patterns['farewell'].extend([
            (r'\b(bye|goodbye)\b', "Goodbye! Feel free to ask if you need anything else."),
            (r'\bsee you\b', "See you later! Don't hesitate to reach out if you need assistance."),
        ])
        # Add more default patterns as needed

    async def process_message(self, message):
        for category, patterns in self.response_patterns.items():
            for pattern, response in patterns:
                if re.search(pattern, message, re.IGNORECASE):
                    return response
        return None

    async def auto_respond(self, message):
        return await self.process_message(message)

    async def learn_response(self, trigger, response):
        self.response_patterns['learned'].append((re.escape(trigger), response))

    async def forget_response(self, trigger):
        self.response_patterns['learned'] = [
            (pattern, response) for pattern, response in self.response_patterns['learned']
            if pattern != re.escape(trigger)
        ]
