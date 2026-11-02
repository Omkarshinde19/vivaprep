# Practical 1: Simple Reflex Agent for the Vacuum Cleaner World

Syllabus reference: Part A, Assignment 1

---

## 1. The Problem and Its Solution

### Diagram 1: The vacuum cleaner world

```
        +---------------------+---------------------+
        |     Location A      |     Location B      |
        |                     |                     |
        |   [Vacuum]  * * *   |          * * *      |
        |             (dirt)  |          (dirt)     |
        +---------------------+---------------------+
             Move Right ------->
             <------- Move Left
```

### Diagram 2: How the agent works with the environment

```
   +--------------------------------------------------------+
   |                      ENVIRONMENT                       |
   |            Location A          Location B              |
   +--------------------------------------------------------+
          |                                      ^
          | percept                              | action
          | (location, status)                   | (Suck / Move)
          v                                      |
   +-------------+    +-------------------+    +-------------+
   |   SENSORS   | -> | CONDITION-ACTION  | -> |  ACTUATORS  |
   |             |    |       RULES       |    |             |
   +-------------+    +-------------------+    +-------------+
   |                         AGENT                          |
   +--------------------------------------------------------+
```

### Diagram 3: The decision rules

```
                 Read percept (location, status)
                               |
                               v
                       Is status Dirty?
                        /            \
                      Yes             No
                      /                \
                     v                  v
                   SUCK           Is location A?
                                   /          \
                                 Yes           No
                                 /              \
                                v                v
                           MOVE RIGHT        MOVE LEFT
```

### Diagram 4: Solution when both rooms are dirty

```
Start      [Vacuum, dirty] [dirty]         A = Dirty, B = Dirty
             |  Suck
             v
Step 1     [Vacuum, clean] [dirty]         A = Clean, B = Dirty
             |  Move Right
             v
Step 2     [clean] [Vacuum, dirty]         A = Clean, B = Dirty
             |  Suck
             v
Step 3     [clean] [Vacuum, clean]         A = Clean, B = Clean  (goal reached)
             |  Move Left
             v
Step 4     [Vacuum, clean] [clean]         A = Clean, B = Clean  (extra move)
```

### Explain the problem in words (viva answer)

The vacuum cleaner world has two rooms, A and B. Each room is either clean or dirty, and the vacuum is in one room at a time. The agent has to clean both rooms using three actions: Suck, Move Right and Move Left.

The agent can sense only which room it is in and whether that room is dirty. It cannot see the other room.

### Explain the solution in words (viva answer)

I solved this with a simple reflex agent, which chooses its action using only the current percept and has no memory. It follows three rules:

1. If the current room is dirty, Suck.
2. If the room is clean and the agent is in A, Move Right.
3. If the room is clean and the agent is in B, Move Left.

When both rooms are dirty and the agent starts in A, it sucks A, moves right and sucks B. Both rooms are clean after three actions.

### Analysis of rational behaviour

A rational agent chooses the action expected to give the best performance, based on what it has perceived so far. To test this, change the `rooms` line in the code. Each case below starts in A and runs for 4 steps:

| A and B at start | Actions taken | Result |
|---|---|---|
| Dirty, Dirty | Suck, Right, Suck, Left | Both clean, 1 extra move |
| Clean, Dirty | Right, Suck, Left, Right | Both clean, 2 extra moves |
| Dirty, Clean | Suck, Right, Left, Right | Both clean, 2 extra moves after checking B |
| Clean, Clean | Right, Left, Right, Left | Nothing to clean, the agent keeps moving |

- The agent sucks whenever it senses dirt, and it cleans both rooms in every case.
- Moving is rational given what it knows, because the other room might be dirty and it cannot see it.
- It has no memory, so it cannot know when everything is clean and keeps wasting energy. This is its main limitation.

---

## 2. Code Explanation

```python
rooms = {"A": "Dirty", "B": "Dirty"}
```
This is the environment. A dictionary links each room name to its status, so a room's status can be read directly by its name.

```python
location = "A"
```
Stores the room the agent is currently in. It starts in A.

```python
for step in range(4):
```
Repeats the sense-decide-act cycle 4 times. A fixed count is used because the agent cannot know when all rooms are clean. Three actions are enough to clean both rooms, and the fourth shows that the agent does not stop by itself.

```python
    if rooms[location] == "Dirty":
```
Rule 1. It reads only the current room, which is the percept. It is checked first because cleaning is the goal.

```python
        print("Room", location, "is Dirty: Suck")
```
Shows the percept and chosen action, so the behaviour can be followed.

```python
        rooms[location] = "Clean"
```
Performs Suck by changing the current room to Clean.

```python
    elif location == "A":
```
Rule 2. This line is reached only when the room is clean, and it checks if the agent is in A.

```python
        print("Room A is Clean: Move Right")
```
Shows the action being taken.

```python
        location = "B"
```
Performs Move Right. From A, the only other room is B.

```python
    else:
```
Rule 3. The room is clean and the agent is not in A, so it must be in B.

```python
        print("Room B is Clean: Move Left")
```
Shows the action being taken.

```python
        location = "A"
```
Performs Move Left, taking the agent back to A.

```python
print("Final rooms:", rooms)
```
This is outside the loop, so it runs once at the end and shows the final environment.

### Output

```
Room A is Dirty: Suck
Room A is Clean: Move Right
Room B is Dirty: Suck
Room B is Clean: Move Left
Final rooms: {'A': 'Clean', 'B': 'Clean'}
```

---

## 3. Write-up

### Problem Statement

Design and implement a simple reflex agent for the Vacuum Cleaner world and analyze its rational behavior in a given environment.

### Objectives

1. To understand the concept of an intelligent agent.
2. To understand the working of a simple reflex agent.
3. To implement a vacuum cleaner agent using Python.
4. To analyze the agent's actions for different environmental conditions.
5. To understand the concept of rational behavior of an AI agent.

### Theory

**Intelligent agent:** A system that perceives its environment through sensors and acts on it through actuators to achieve a goal.

**Vacuum cleaner world:** An environment with two locations, A and B. Each location is either clean or dirty. The agent can perform Suck, Move Right and Move Left.

**Simple reflex agent:** An agent that selects its action using only the current percept. It uses condition-action rules of the form IF condition THEN action, and it keeps no history of previous states.

| Condition | Action |
|---|---|
| Current location is Dirty | Suck |
| Current location is Clean and agent is at A | Move Right |
| Current location is Clean and agent is at B | Move Left |

**PEAS description:**

| Component | Vacuum cleaner agent |
|---|---|
| Performance measure | Maximum cleanliness, minimum unnecessary movement, minimum time and energy |
| Environment | Two-room environment, A and B |
| Actuators | Suck, Move Left, Move Right |
| Sensors | Current location and cleanliness status |

**Rational behavior:** A rational agent selects the action expected to maximize its performance measure, based on its percepts and built-in knowledge.

### Conclusion

A simple reflex agent for the vacuum cleaner world was designed and implemented in Python using condition-action rules. The agent cleaned both rooms in all four starting conditions. Its behavior is rational in choosing actions from the current percept. However, it has no memory, so it continues to move after both rooms are clean.

---

## 4. Viva Questions

**1. What is an intelligent agent?**
A system that perceives its environment through sensors and acts on it through actuators to achieve a goal.

**2. What is a simple reflex agent?**
An agent that chooses its action using only the current percept and condition-action rules, without any memory.

**3. What is the difference between an agent and an environment?**
The agent perceives and decides. The environment is the world it senses and acts upon. Here the vacuum is the agent and the two rooms are the environment.

**4. What are sensors and actuators?**
Sensors collect information from the environment, and actuators carry out actions on it. Here the sensors detect location and dirt, and the actuators suck and move.

**5. What is a percept?**
What the agent senses at a given moment. Here it is the pair (location, status), such as (A, Dirty).

**6. What are the possible percepts in this world?**
There are four: (A, Clean), (A, Dirty), (B, Clean) and (B, Dirty).

**7. What is PEAS?**
Performance measure, Environment, Actuators and Sensors. It is a way to describe an agent's task.

**8. What is the performance measure of a vacuum cleaner agent?**
Maximum cleanliness with minimum unnecessary movement, time and energy.

**9. What is meant by rational behavior?**
Choosing the action expected to maximize the performance measure, based on the percepts and knowledge the agent has.

**10. Is rational the same as perfect?**
No. A rational agent does the best it can with the information it has. A perfect agent would need to know the outcome in advance.

**11. Why is the vacuum cleaner considered an intelligent agent?**
It senses its environment and acts on it by itself to achieve the goal of cleaning.

**12. Can a simple reflex agent remember previous actions?**
No. It uses only the current percept, so it does not know what it did before.

**13. What are the limitations of a simple reflex agent?**
It has no memory, it cannot tell when the whole task is finished, and it works well only when the right action can be decided from the current percept.

**14. How is a model-based reflex agent different?**
It keeps an internal state about parts of the world it cannot currently see. It could remember that A is clean and stop after cleaning B.

**15. What happens if both rooms are clean?**
The agent keeps moving between the rooms, because it cannot know the other room is clean.

**16. Why is if-elif-else used in this implementation?**
Exactly one action must be chosen at each step, and if-elif-else makes sure only one rule fires. Checking Dirty first gives cleaning priority.

**17. Why is a dictionary used for the environment?**
It links each room name to its status, so `rooms[location]` directly gives the status of the current room.

**18. Why does the program use a fixed number of steps?**
The agent cannot know when all rooms are clean, so the loop decides how long the program runs.

**19. What are the properties of this environment?**
Partially observable, because the agent senses only its own room. It is also deterministic, static, discrete and single-agent.

**20. What is the time complexity of this program?**
O(n), where n is the number of steps, because each step does a constant amount of work.
