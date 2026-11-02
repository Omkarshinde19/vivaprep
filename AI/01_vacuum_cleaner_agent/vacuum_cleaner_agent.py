# Simple Reflex Agent for the Vacuum Cleaner World

rooms = {"A": "Dirty", "B": "Dirty"}
location = "A"

for step in range(4):
    if rooms[location] == "Dirty":
        print("Room", location, "is Dirty: Suck")
        rooms[location] = "Clean"
    elif location == "A":
        print("Room A is Clean: Move Right")
        location = "B"
    else:
        print("Room B is Clean: Move Left")
        location = "A"

print("Final rooms:", rooms)
