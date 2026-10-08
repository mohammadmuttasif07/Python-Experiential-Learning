"""
Dice Rolling Simulator
----------------------
Simulates rolling one or more standard six-sided dice.

Features:
  - Roll 1-10 dice at a time (random numbers from 1 to 6)
  - Roll multiple times in a row
  - View history of previous rolls
  - Statistics (frequency of each face, average)
  - Save history to a text file
  - Input validation with exception handling
"""

import random
from datetime import datetime

SIDES = 6
MAX_DICE = 10
MAX_ROLLS = 100

# Unicode faces for a nicer display
DICE_FACES = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}

history = []  # each entry: {"time": str, "dice": [ints], "total": int}


# ---------------------------------------------------------------- core logic
def roll_die():
    """Roll a single six-sided die and return a number from 1 to 6."""
    return random.randint(1, SIDES)


def roll_dice(count):
    """Roll `count` dice and return the list of results."""
    return [roll_die() for _ in range(count)]


def record_roll(results):
    """Save a roll in the history list."""
    history.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "dice": results,
        "total": sum(results),
    })


# ------------------------------------------------------------------- input
def get_int(prompt, minimum, maximum):
    """Keep asking until the user enters an integer within [minimum, maximum]."""
    while True:
        try:
            value = int(input(prompt))
            if minimum <= value <= maximum:
                return value
            print(f"  Please enter a number between {minimum} and {maximum}.")
        except ValueError:
            print("  Invalid input. Please enter a whole number.")


# ----------------------------------------------------------------- display
def show_roll(number, results):
    faces = " ".join(DICE_FACES[r] for r in results)
    values = ", ".join(str(r) for r in results)
    print(f"  Roll {number}: {faces}  ->  [{values}]  Total = {sum(results)}")


def show_history():
    if not history:
        print("\n  No rolls in history yet.")
        return
    print("\n" + "=" * 50)
    print("  ROLL HISTORY")
    print("=" * 50)
    for i, entry in enumerate(history, start=1):
        values = ", ".join(str(d) for d in entry["dice"])
        print(f"  {i:>3}. {entry['time']}  [{values}]  Total = {entry['total']}")


def show_statistics():
    if not history:
        print("\n  No data yet. Roll some dice first!")
        return

    all_dice = [d for entry in history for d in entry["dice"]]
    total_dice = len(all_dice)

    print("\n" + "=" * 50)
    print("  STATISTICS")
    print("=" * 50)
    print(f"  Total rolls (turns)  : {len(history)}")
    print(f"  Total dice rolled    : {total_dice}")
    print(f"  Average die value    : {sum(all_dice) / total_dice:.2f}")
    print(f"  Highest / Lowest     : {max(all_dice)} / {min(all_dice)}")
    print("\n  Face frequency:")
    for face in range(1, SIDES + 1):
        count = all_dice.count(face)
        percent = count / total_dice * 100
        bar = "█" * int(percent // 2)
        print(f"   {DICE_FACES[face]} {face}: {count:>3} ({percent:5.1f}%) {bar}")


def save_history(filename="dice_history.txt"):
    if not history:
        print("\n  Nothing to save yet.")
        return
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("Dice Rolling Simulator - History\n")
            f.write("=" * 40 + "\n")
            for i, entry in enumerate(history, start=1):
                values = ", ".join(str(d) for d in entry["dice"])
                f.write(f"{i}. {entry['time']} [{values}] Total = {entry['total']}\n")
        print(f"\n  History saved to '{filename}'.")
    except OSError as error:
        print(f"\n  Could not save file: {error}")


# ----------------------------------------------------------------- actions
def roll_action():
    num_dice = get_int(f"\n  How many dice? (1-{MAX_DICE}): ", 1, MAX_DICE)
    num_rolls = get_int(f"  How many times to roll? (1-{MAX_ROLLS}): ", 1, MAX_ROLLS)

    print()
    for n in range(1, num_rolls + 1):
        results = roll_dice(num_dice)
        record_roll(results)
        show_roll(n, results)


def clear_history():
    if not history:
        print("\n  History is already empty.")
        return
    confirm = input("\n  Clear all history? (y/n): ").strip().lower()
    if confirm == "y":
        history.clear()
        print("  History cleared.")
    else:
        print("  Cancelled.")


# -------------------------------------------------------------------- menu
def show_menu():
    print("\n" + "=" * 50)
    print("        🎲  DICE ROLLING SIMULATOR  🎲")
    print("=" * 50)
    print("  1. Roll dice")
    print("  2. View history")
    print("  3. View statistics")
    print("  4. Save history to file")
    print("  5. Clear history")
    print("  6. Exit")


def main():
    actions = {
        "1": roll_action,
        "2": show_history,
        "3": show_statistics,
        "4": save_history,
        "5": clear_history,
    }

    while True:
        show_menu()
        try:
            choice = input("\n  Enter your choice (1-6): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  Goodbye! 👋")
            break

        if choice == "6":
            print("\n  Thanks for playing. Goodbye! 👋")
            break
        elif choice in actions:
            try:
                actions[choice]()
            except KeyboardInterrupt:
                print("\n  Action interrupted.")
        else:
            print("\n  Invalid choice. Please select 1-6.")


if __name__ == "__main__":
    main()