"""Two-room rule-based cleaning agent (with optional three-room extension).
Run: python TA2_Santos.py
No external packages are required.
"""
import random


class CleaningAgent:
    """Perceive the current room and clean it or move to a dirty room."""

    def __init__(self, environment, location="A"):
        self.environment = environment
        self.location = location

    def move(self, destination):
        """Move to another room in the environment."""
        if destination not in self.environment:
            raise ValueError(f"Unknown room: {destination}")
        self.location = destination

    def perceive_and_act(self):
        """Apply the rules once and return a description of the action."""
        if self.environment[self.location] == "Dirty":
            self.environment[self.location] = "Clean"
            return f"Room {self.location} has been cleaned."

        dirty_rooms = [
            room for room, condition in self.environment.items()
            if condition == "Dirty" and room != self.location
        ]
        if dirty_rooms:
            destination = random.choice(dirty_rooms)
            self.move(destination)
            return f"Moving to room {destination}."

        return "All rooms are clean. Agent is idle."


def ask_room_condition(room):
    """Ask for a room state and validate the answer."""
    while True:
        answer = input(f"Is room {room} Dirty or Clean? ").strip().lower()
        if answer in ("dirty", "clean"):
            return answer.title()
        print("Please enter Dirty or Clean.")


def ask_room_count():
    """Choose the required two-room task or the optional three-room extension."""
    while True:
        answer = input("Number of rooms (2 or 3) [2]: ").strip()
        if not answer:
            return 2
        if answer in ("2", "3"):
            return int(answer)
        print("Please enter 2 or 3.")


def ask_steps():
    """Read a non-negative number of simulation steps."""
    while True:
        answer = input("How many steps should the agent run? ").strip()
        try:
            steps = int(answer)
            if steps >= 0:
                return steps
        except ValueError:
            pass
        print("Please enter a whole number zero or greater.")


def show_environment(environment, agent):
    """Print a text-based room grid and the complete room-state dictionary."""
    cells = []
    for room, condition in environment.items():
        label = f"{room}-Agent" if room == agent.location else f"{room}-{condition}"
        cells.append(f"[{label}]")
    print(" ".join(cells))
    print(f"Environment state: {environment}")


def main():
    print("Rule-Based Room Cleaning Agent")
    room_count = ask_room_count()
    room_names = ["A", "B", "C"][:room_count]
    environment = {room: ask_room_condition(room) for room in room_names}
    steps = ask_steps()

    # Fixed seed makes the random destination choice reproducible.
    random.seed(7)
    agent = CleaningAgent(environment, location="A")
    print("\nInitial environment:")
    show_environment(environment, agent)

    for step_number in range(1, steps + 1):
        print(f"\nStep {step_number}: Agent is in room {agent.location}")
        action = agent.perceive_and_act()
        print(action)
        show_environment(environment, agent)
        if action == "All rooms are clean. Agent is idle.":
            break

    print("\nSimulation complete.")
    print(f"Final location: room {agent.location}")
    print(f"Final environment: {environment}")


if __name__ == "__main__":
    main()
