from emotional_support_bot import EmotionalSupportBot

def test_emotional_support_bot():
    """
    Test the functionality of the EmotionalSupportBot with an extended conversation,
    including long inputs and diverse emotional scenarios.
    """
    # Create an instance of the bot
    bot = EmotionalSupportBot()

    # Simulate a long and varied conversation
    conversation = [
        "Hi, I'm feeling really down today. Everything seems to be going wrong in my life.",
        "I lost my job last week, and I have no idea how I'm going to pay my bills.",
        "On top of that, my best friend and I had a big argument, and we haven't spoken since.",
        "I just feel so alone and overwhelmed by everything happening right now.",
        "Do you have any advice on how to stay positive in tough times like these?",
        "I've tried to stay busy, but it just feels like I'm avoiding the real issues.",
        "My parents have been supportive, but I don't want to burden them with all my problems.",
        "Sometimes I feel like I'm failing at everything, and I don't know how to move forward.",
        "I tried meditation and journaling, but they don't seem to help anymore.",
        "Do you think talking to a therapist could make a difference for someone like me?",
        "How do I even start looking for a therapist who understands what I'm going through?",
        "I also feel like I have so much pent-up frustration that I don't know how to release.",
        "What are some healthy ways to deal with feelings of anger and frustration?",
        "Thank you for listening to me. It really means a lot to be able to talk to someone.",
        "I hope things get better soon. Do you think there's a way to rebuild my confidence?",
        "What if I try something new, like starting a side project or learning a new skill?",
        "Do you have any tips for staying motivated when everything feels so uncertain?",
        "Sometimes I just wish I could escape from all the stress and go somewhere peaceful.",
        "If you were in my position, what would you do to start feeling better?"
    ]

    # Interact with the bot using the simulated conversation
    print("=== Starting Test: EmotionalSupportBot ===\n")
    for idx, user_input in enumerate(conversation):
        print(f"Test Input {idx + 1}: {user_input}")
        response = bot.get_response(user_input)
        print(f"Bot Response {idx + 1}: {response}\n")

    # Final status: Log the conversation history and check summarization
    print("\n=== Final Conversation History ===")
    bot.log_history()

    print("\n=== Test Completed ===")


# Run the test function
# if __name__ == "__main__":
#     test_emotional_support_bot()



# Example Usage
if __name__ == "__main__":
    bot = EmotionalSupportBot()

    print("Welcome to the Emotional Support Chatbot! 🌟")
    print("Type 'quit' to end the chat.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            print("Chat ended. Take care! ❤️")
            break
        response = bot.get_response(user_input)
        print(f"Bot: {response}")
