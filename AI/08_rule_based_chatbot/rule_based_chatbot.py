# Simple Chatbot using Predefined Rules and Pattern Matching
import re

rules = [(r"\b(hello|hi|hey)\b", "Hello! How can I help you?"),
         (r"\bname\b", "I am a simple AI chatbot."),
         (r"\bhow are you\b", "I am fine. Thank you for asking!"),
         (r"\b(course|subject)\b", "I can provide basic information about your course."),
         (r"\bhelp\b", "Sure! You can ask me about my name, course, or general information."),
         (r"\b(thank|thanks)\b", "You are welcome!")]

print("Chatbot: Welcome! Type bye to exit.")

while True:
    message = input("You: ").lower()
    if re.search(r"\b(bye|exit|quit)\b", message):
        print("Chatbot: Goodbye! Have a nice day.")
        break
    response = "Sorry, I do not understand your question."
    for pattern, answer in rules:
        if re.search(pattern, message):
            response = answer
            break
    print("Chatbot:", response)
