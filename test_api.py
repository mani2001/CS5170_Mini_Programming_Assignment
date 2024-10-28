from groq import Groq  # Import Groq library
import os  # Access environment variables
from dotenv import load_dotenv  # Load .env variables

# Bot 1: BotIntroduction - provides a basic introduction and capabilities
class BotIntroduction:
    client = None

    def __init__(self):
        # Initialize API client
        load_dotenv('credentials.env')
        api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=api_key)

    def introduce(self):
        # Provide an introduction and list of capabilities
        response = self.client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "user", "content": "Hi, who are you and what are your capabilities?"}
            ]
        )
        print(response.choices[0].message.content)  # Print the bot's response


# Bot 2: MemoryChatBot - retains memory of the conversation context
class MemoryChatBot:
    client = None
    context = []  # List to store chat history for context memory
    max_tokens = 30000  # Set the maximum token limit
    current_tokens = 0  # Track the current token count

    def __init__(self):
        # Initialize API client and load API key
        load_dotenv('credentials.env')
        api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=api_key)

    def count_tokens(self, message):
        # Rough token count approximation: 1 token ≈ 4 characters
        return len(message) // 4

    def add_message(self, role, content):
        # Add a message to the context and update token count
        tokens = self.count_tokens(content)
        self.context.append({"role": role, "content": content})
        self.current_tokens += tokens

        # Remove oldest messages if token limit is exceeded
        while self.current_tokens > self.max_tokens:
            removed_message = self.context.pop(0)
            self.current_tokens -= self.count_tokens(removed_message["content"])

    def chat(self, user_input):
        # Add user input to the context and request a response
        self.add_message("user", user_input)  # Add user message
        response = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=self.context  # Send entire context for continuity
        )
        assistant_reply = response.choices[0].message.content
        self.add_message("assistant", assistant_reply)  # Store assistant reply
        print(assistant_reply)  # Print response for user


# Main Application
if __name__ == "__main__":
    # Instantiate both bots
    bot_intro = BotIntroduction()
    memory_chat_bot = MemoryChatBot()

    print("Welcome! Type 'bot_intro' to see bot capabilities or 'exit' to end.")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        elif user_input.lower() == "bot_intro":
            # Trigger BotIntroduction for capabilities
            bot_intro.introduce()
        else:
            # Handle all other input with MemoryChatBot
            memory_chat_bot.chat(user_input)
