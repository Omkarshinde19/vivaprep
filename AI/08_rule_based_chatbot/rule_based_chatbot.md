# Practical 8: Simple Rule-Based Chatbot using Pattern Matching

Syllabus reference: Part B, Assignment 4

---

## 1. The Problem and Its Solution

### Diagram 1: How the chatbot works

```
              +---------------------------+
              |   Display welcome message |
              +---------------------------+
                            |
                            v
              +---------------------------+
      +-----> |      Read user message    |
      |       |    Convert to lowercase   |
      |       +---------------------------+
      |                     |
      |                     v
      |          Contains bye/exit/quit? ---Yes---> Say goodbye, STOP
      |                     | No
      |                     v
      |          Check rules from the top
      |                 /         \
      |          A rule matches   No rule matches
      |               |                  |
      |               v                  v
      |        Rule's response    Default response
      |               |                  |
      +---------------+------------------+
```

### Diagram 2: The rule table

```
   Input contains            Response
   ------------------------------------------------------------------
   hello, hi, hey       ->   Hello! How can I help you?
   name                 ->   I am a simple AI chatbot.
   how are you          ->   I am fine. Thank you for asking!
   course, subject      ->   I can provide basic information about your course.
   help                 ->   Sure! You can ask me about my name, course, ...
   thank, thanks        ->   You are welcome!
   bye, exit, quit      ->   Goodbye! Have a nice day. (program stops)
   nothing matches      ->   Sorry, I do not understand your question.
```

### Diagram 3: Example of matching

```
   User types:      "What is your NAME?"
                            |
   Lowercase:       "what is your name?"
                            |
   Rule 1 hello|hi|hey?     no match
   Rule 2 name?             MATCH  (stop checking)
                            |
   Chatbot says:    "I am a simple AI chatbot."
```

### Explain the problem in words (viva answer)

We have to build a simple chatbot that talks with a user through text. It must recognise keywords in the user's message and reply with a predefined response. It does not learn, and it stops when the user says goodbye.

### Explain the solution in words (viva answer)

I stored the chatbot's knowledge as a list of rules. Each rule is a pair of a pattern and a response, which works like an IF-THEN rule.

The program reads a message and converts it to lowercase so that capital letters do not matter. If the message has bye, exit or quit, it says goodbye and stops. Otherwise, it checks each pattern from the top using regular expressions. The first match gives the response. If none match, the chatbot gives a default response.

I used `\b`, which means a word boundary, so that patterns match only whole words. This way, a message like "What is this" does not wrongly match "hi".

---

## 2. Code Explanation

```python
import re
```
`re` is Python's regular expression module, used for pattern matching.

```python
rules = [(r"\b(hello|hi|hey)\b", "Hello! How can I help you?"),
```
The start of the rule list, and Rule 1. Each rule is a (pattern, response) pair. `|` means OR and `\b` means a word boundary. The `r` makes it a raw string, so Python leaves the backslash alone.

```python
         (r"\bname\b", "I am a simple AI chatbot."),
```
Rule 2 answers questions about the chatbot's name.

```python
         (r"\bhow are you\b", "I am fine. Thank you for asking!"),
```
Rule 3 matches a full phrase, not only a single word.

```python
         (r"\b(course|subject)\b", "I can provide basic information about your course."),
```
Rule 4 matches either keyword.

```python
         (r"\bhelp\b", "Sure! You can ask me about my name, course, or general information."),
```
Rule 5 tells the user what can be asked.

```python
         (r"\b(thank|thanks)\b", "You are welcome!")]
```
Rule 6 answers thanks, and the list ends here.

```python
print("Chatbot: Welcome! Type bye to exit.")
```
Greets the user and explains how to stop.

```python
while True:
```
Keeps the conversation going until the user exits. The number of messages is not known in advance.

```python
    message = input("You: ").lower()
```
Reads the message. User input is needed here, as a chatbot must respond to a user. `lower()` makes the matching case-insensitive.

```python
    if re.search(r"\b(bye|exit|quit)\b", message):
```
Checks for exit words first, so the chatbot stops even when other keywords are present. `re.search` looks for the pattern anywhere in the message.

```python
        print("Chatbot: Goodbye! Have a nice day.")
```
Gives the exit response.

```python
        break
```
Leaves the loop and ends the program.

```python
    response = "Sorry, I do not understand your question."
```
Sets the default response first. It is replaced only if a rule matches.

```python
    for pattern, answer in rules:
```
Goes through the rules in order, taking each pattern and its answer.

```python
        if re.search(pattern, message):
```
Checks if this rule's pattern is in the message.

```python
            response = answer
```
Selects this rule's response.

```python
            break
```
Stops at the first match, so the order of rules sets their priority.

```python
    print("Chatbot:", response)
```
Prints the matched or default response, then the loop asks for the next message.

### Output

```
Chatbot: Welcome! Type bye to exit.
You: Hi
Chatbot: Hello! How can I help you?
You: What is your name?
Chatbot: I am a simple AI chatbot.
You: How are you
Chatbot: I am fine. Thank you for asking!
You: Can you help me?
Chatbot: Sure! You can ask me about my name, course, or general information.
You: What is the subject?
Chatbot: I can provide basic information about your course.
You: Thank you
Chatbot: You are welcome!
You: Good morning
Chatbot: Sorry, I do not understand your question.
You: What is this
Chatbot: Sorry, I do not understand your question.
You: Bye
Chatbot: Goodbye! Have a nice day.
```

---

## 3. Write-up

### Problem Statement

Develop a simple chatbot using predefined rules and pattern matching. The chatbot should identify keywords or patterns in the user's input and generate an appropriate predefined response.

### Objectives

1. To understand the basic concept of chatbots in Artificial Intelligence.
2. To understand rule-based conversation systems.
3. To implement pattern matching for identifying user inputs.
4. To develop a simple chatbot using predefined rules and responses.

### Theory

**Chatbot:** A computer program that interacts with users through text or voice.

**Rule-based chatbot:** A chatbot controlled by a collection of IF-THEN rules. It does not learn from data. If a rule matches the input, its response is displayed. If not, a default response is given.

**Pattern matching:** Checking whether the input contains a particular word, phrase or pattern. For example, the word "hello" matches the greeting rule.

**Working of the chatbot:**

1. The user enters a message.
2. The chatbot converts it to lowercase.
3. It checks the input against predefined patterns.
4. If a pattern matches, the first applicable rule's response is selected.
5. If no pattern matches, it gives a default response.
6. The conversation continues until the user enters an exit command such as "bye".

**Advantages:** It is simple, easy to implement with IF-THEN rules, needs no training data, gives predictable responses, and suits FAQ and basic customer support.

**Limitations:** It cannot understand complex language or create new responses, it depends on the quality of its patterns, different wordings of a question may not match, and it does not learn from conversations.

**Algorithm:**

1. Define the patterns and responses.
2. Display a welcome message.
3. Accept the user's input and convert it to lowercase.
4. If it contains an exit pattern, display the exit response and stop.
5. Compare the input with each pattern.
6. If a pattern matches, display its response. Otherwise, display the default response.
7. Repeat from step 3.

### Conclusion

A simple rule-based chatbot was developed using predefined rules and pattern matching. It accepts user input, identifies keywords or phrases, and gives a predefined response. This practical shows the basic working of conversational AI and introduces more advanced techniques such as Natural Language Processing and machine learning based systems.

---

## 4. Viva Questions

**1. What is a chatbot?**
A program that interacts with users through text or voice.

**2. What is a rule-based chatbot?**
A chatbot that uses predefined IF-THEN rules to choose its responses, without learning from data.

**3. What is pattern matching?**
Checking whether the input contains a particular word, phrase or pattern.

**4. How are rules represented in your chatbot?**
As a list of (pattern, response) pairs.

**5. Why is the input converted to lowercase?**
So "HELLO", "Hello" and "hello" all match the same pattern.

**6. What happens when no pattern matches?**
The chatbot gives the default response: "Sorry, I do not understand your question."

**7. What is the purpose of a default response?**
It makes sure the user always gets a reply and knows the question was not understood.

**8. What is the difference between a rule-based chatbot and an AI/ML chatbot?**
A rule-based chatbot follows fixed, hand-written rules. An AI/ML chatbot learns from data and can handle wording it has not seen before.

**9. What are the advantages of a rule-based chatbot?**
It is simple, predictable and needs no training data.

**10. What are its limitations?**
It cannot handle complex language, cannot create new responses, and does not learn.

**11. What is a regular expression?**
A pattern that describes text to search for, written with special symbols.

**12. What does `\b` mean?**
A word boundary. It makes a pattern match a whole word, so "hi" does not match inside "this".

**13. What does `|` mean in a pattern?**
OR. `hello|hi|hey` matches any of the three.

**14. What does `re.search` do?**
It looks for the pattern anywhere in the text, and returns a match or None.

**15. Why is a raw string used for the patterns?**
With `r"..."`, Python does not treat the backslash specially, so `\b` reaches `re` as a word boundary.

**16. Why is `while True` used?**
The chatbot must keep replying until the user exits, however many messages there are.

**17. Why is the exit condition checked first?**
So that the chatbot stops even if the message also contains other keywords, such as "thanks, bye".

**18. What happens if a message matches two rules?**
Only the first one is used, because the loop breaks at the first match.

**19. Is this chatbot intelligent?**
Only in a limited way. It matches keywords and does not understand meaning, so it appears intelligent only within its rules.

**20. What is the name of an early chatbot of this type?**
ELIZA, created by Joseph Weizenbaum in the 1960s, which used pattern matching to imitate a therapist.
