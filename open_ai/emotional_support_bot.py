import os
from openai import OpenAI
import logging

# Constants for configuration
# MODEL = "gpt-3.5-turbo"  # AI model to use
# MODEL = "ft:gpt-3.5-turbo-0125:personal::AVbPQOc8";

class EmotionalSupportBot:
    def __init__(self):
        """
        Initialize the bot with an empty conversation history.
        """
        self.history = [
            {"role": "system", "content": "You are a kind and empathetic assistant providing emotional support."}
        ]

        # Initialize the OpenAI client
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.MODEL = os.environ.get("OPENAI_API_MODEL")
        self.MAX_TOKEN_LIMIT = 4096  # Maximum token limit for the model
        self.SUMMARIZATION_TRIGGER = 600  # Trigger summarization when history exceeds this token count
        self.MAX_RESPONSE_TOKENS = 400  # Maximum tokens for the assistant's response
        self.TEMPERATURE = 0.7  # Temperature for creative responses
        self.SUMMARY_TEMPERATURE = 0.5  # Temperature for concise summaries

    def log_history(self):
        """
        Log the current conversation history for debugging purposes.
        """
        logging.info("🗂️ Current Conversation History:")
        for message in self.history:
            logging.info(f"  - {message['role'].capitalize()}: {message['content']}")

    def log_openai_request(self, messages, request_type):
        """
        Log the messages sent to OpenAI for API calls.

        Args:
            messages (list): Messages sent to OpenAI API.
            request_type (str): Indicates whether it's for 'summary' or 'main chat'.
        """
        logging.info("=" * 50)
        logging.info(f"🚀 Sending Request to OpenAI ({request_type}):")
        for message in messages:
            logging.info(f"  - {message['role'].capitalize()}: {message['content']}")
        logging.info("=" * 50)

    def log_openai_response(self, response, request_type):
        """
        Log the response received from OpenAI.

        Args:
            response (str): The response content.
            request_type (str): Indicates whether the response is for 'summary' or 'main chat'.
        """
        logging.info("=" * 50)
        logging.info(f"✅ OpenAI Response for {request_type}:")
        logging.info(f"  {response}")
        logging.info("=" * 50)


    def call_openai_api(self, messages):
        """
        Call the OpenAI API with the current conversation history.

        Args:
            messages (list): List of messages (history) to send to the API.

        Returns:
            str: The assistant's response.
        """
        self.log_openai_request(messages, "main chat session")
        try:
            max_tokens = self.MAX_TOKEN_LIMIT - self.calculate_token_usage(messages)
            max_tokens = min(max_tokens, self.MAX_RESPONSE_TOKENS)

            response = self.client.chat.completions.create(
                model=self.MODEL,
                messages=messages,
                max_tokens=max_tokens,
                temperature=self.TEMPERATURE,
            )
            response_content = response.choices[0].message.content
            self.log_openai_response(response_content, "main chat session")
            return response_content
        except Exception as e:
            logging.error(f"❌ Error calling OpenAI API: {e} | Messages: {messages}")
            return "I'm sorry, something went wrong. Please try again later."



    def calculate_token_usage(self, messages):
        """
        Estimate the token usage of a list of messages.
        """
        return sum(len(message["content"].split()) for message in messages)

    def summarize_history(self):
        """
        Summarize the conversation history using the OpenAI API.
        """
        summary_prompt = "Summarize the following conversation to preserve key context and details:"
        history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.history])

        summarization_messages = [
            {"role": "system", "content": "You are a summarization assistant."},
            {"role": "user", "content": f"{summary_prompt}\n{history_text}"}
        ]

        self.log_openai_request(summarization_messages, "summary")
        try:
            summary_response = self.client.chat.completions.create(
                model=self.MODEL,
                messages=summarization_messages,
                max_tokens=300,
                temperature=self.SUMMARY_TEMPERATURE,
            )
            summary_content = summary_response.choices[0].message.content
            self.log_openai_response(summary_content, "summary")
            logging.info(f"📃 Summary Updated: {summary_content}")
            return [{"role": "assistant", "content": f"Summary: {summary_content}"}]
        except Exception as e:
            logging.error(f"❌ Error during summarization: {e}")
            return self.history  # Return unsummarized history on failure

    def get_response(self, user_input):
        """
        Generate an emotional support response for the given user input.

        Args:
            user_input (str): The user's input message.

        Returns:
            str: The assistant's response.
        """
        # Add the user's message to the history
        self.history.append({"role": "user", "content": user_input})

        # Log the history before summarization
        self.log_history()

        # Check if token usage exceeds the trigger point for summarization
        if self.calculate_token_usage(self.history) > self.SUMMARIZATION_TRIGGER:
            logging.info("⚡ Summarizing conversation history...")
            self.history = self.summarize_history()

        # Get the assistant's response
        assistant_response = self.call_openai_api(self.history)

        # Add the assistant's response to the history
        self.history.append({"role": "assistant", "content": assistant_response})

        # Log the updated history
        self.log_history()

        return assistant_response