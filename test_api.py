from groq import Groq  # Import Groq library to access Meta's Llama model via API
import os  # For accessing environment variables securely
from dotenv import load_dotenv  # To load environment variables from a .env file

# Bot 1: BotIntroduction - provides a basic introduction and lists capabilities
class BotIntroduction:
    """A simple bot that introduces itself and shares its capabilities when prompted."""

    client = None  # Will hold the GROQ API client

    def __init__(self):
        # Initialize the API client, pulling the API key from the environment file
        load_dotenv('credentials.env')  # Load environment variables from credentials.env
        api_key = os.getenv("GROQ_API_KEY")  # Get the GROQ API key securely
        self.client = Groq(api_key=api_key)  # Set up the client with the API key

    def introduce(self):
        """Ask the bot to introduce itself and list its capabilities. Output is printed directly."""
        response = self.client.chat.completions.create(
            model="llama3-70b-8192",  # Specify which Llama model to use
            messages=[
                {"role": "user", "content": "Hi, who are you and what are your capabilities?"}
            ]
        )
        print(response.choices[0].message.content)  # Display the bot's response


# Bot 2: MemoryChatBot - retains memory of the conversation context for ongoing chats
class MemoryChatBot:
    """A chatbot with memory that keeps context of the conversation, allowing for ongoing, coherent interactions."""

    client = None  # Placeholder for the GROQ API client
    context = []  # Stores the chat history for contextual continuity
    max_tokens = 30000  # Token limit to manage the chat context size
    current_tokens = 0  # Track the current token count in the context

    def __init__(self):
        # Load environment variables and initialize the API client with the secure API key
        load_dotenv('credentials.env')  # Load .env file containing environment variables
        api_key = os.getenv("GROQ_API_KEY")  # Retrieve GROQ API key
        self.client = Groq(api_key=api_key)  # Initialize the API client

    def count_tokens(self, message):
        """Estimate token count for a message (1 token ≈ 4 characters)."""
        return len(message) // 4

    def add_message(self, role, content):
        """Add a message to the chat context and keep track of token usage.
        
        If the total token count exceeds max_tokens, older messages are dropped to stay within limits.
        """
        tokens = self.count_tokens(content)  # Get token count estimate for the message
        self.context.append({"role": role, "content": content})  # Add message to context
        self.current_tokens += tokens  # Update total token count

        # Manage token count by removing oldest messages if we exceed max_tokens
        while self.current_tokens > self.max_tokens:
            removed_message = self.context.pop(0)  # Drop the oldest message from context
            self.current_tokens -= self.count_tokens(removed_message["content"])  # Adjust token count

    def chat(self, user_input):
        """Handle user input and get a response from the bot based on conversation history.
        
        Args:
            user_input (str): The message input from the user.
        
        The assistant’s response is generated based on the accumulated context, then printed
        and added to the context for continuity.
        """
        self.add_message("user", user_input)  # Add user's message to context
        response = self.client.chat.completions.create(
            model="llama3-8b-8192",  # Specify model for generating response
            messages=self.context  # Send the full context for continuity
        )
        assistant_reply = response.choices[0].message.content  # Get the response content
        self.add_message("assistant", assistant_reply)  # Add response to context
        print(assistant_reply)  # Show response to the user


# Main Application
if __name__ == "__main__":
    # Set up both bots
    bot_intro = BotIntroduction()  # Bot that explains itself
    memory_chat_bot = MemoryChatBot()  # Memory-based bot for ongoing conversation

    print("Welcome! Type 'bot_intro' to see bot capabilities or 'exit' to end.")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        elif user_input.lower() == "bot_intro":
            # Trigger BotIntroduction to list capabilities
            bot_intro.introduce()
        else:
            # Send all other inputs to MemoryChatBot for a conversational response
            memory_chat_bot.chat(user_input)

