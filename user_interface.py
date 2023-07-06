from pick import pick
import os
CURSOR = "=>"  # Cursor for pick method
path_to_file = os.path.dirname(__file__)
instructions_path = os.path.join(path_to_file, './instructions.txt')


def clear_screen():
    """
    Clears terminal
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def rules():
    """
    Prints instruction file to terminal.
    If not possible, shows appropriate message
    """
    clear_screen()
    try:
        with open(instructions_path, 'r') as filehandle:
            text = filehandle.readlines()
            text_string = ""
            for line in text:
                text_string += line
            print(text_string)
    except FileNotFoundError:
        print("It looks like instructions file got lost")
        print("Good luck then ;)")
    input("Press enter to proceed")


def choose_settings(configurations):
    """
    Allows player to choose desired settings regarding duplicates and blanks

    Args:
        configurations (list): Possible game configurations

    Returns:
        int: Number representing chosen option
    """
    title = "Please choose the game preset:"
    result = pick(configurations, title, CURSOR)
    return result[1]


def main_menu(options):
    """
    Allows player to choose game mode

    Args:
        options (list): Possible game modes

    Returns:
        str: Chosen game mode
    """
    title = "Welcome to the Mastermind. Please choose the option (with Enter):"
    result = pick(options, title, CURSOR)
    return result[0]


def switch_message(mode, modes):
    """
    Displays message annoncing the beginning of guessing phase.
    Message changes depending on game mode

    Args:
        mode (int): Current game mode
        MODES (list): List of possible modes
    """
    clear_screen()
    if mode == modes[0]:
        input("Please sit the other player at the computer and press Enter")
    elif mode == modes[1]:
        input("AI chose the combination. Press Enter")
    else:
        input("AI will now try to guess the combination. Press Enter")


def guess_printer(guesses, correctness):
    """
    Creates a string with information about guesses and their correctness

    Args:
        guesses (list): Guesses
        correctness (list): Correctness of guesses

    Returns:
        str: Guesses and their correctness in string form
    """
    guess_info = ""
    for guess, result in (zip(guesses, correctness)):
        guess_info += f"Guess: {guess}. Result: {result}\n"
    return guess_info


def set_combination(cols, dupes, le, guesses=None, correctness=None):
    """
    Allows player to choose combination to be guessed / guess the combination.
    Displays previous guesses and their correctness if necessary

    Args:
        cols (list): Allowed colours
        dupes (bool): Denotes whether duplicates are allowed
        le (int): Length of combination
        guesses (list, optional): Guesses to be shown. Defaults to None.
        correctness (list, optional): Correctness of guesses. Defaults to None.

    Returns:
        [type]: [description]
    """
    title = f"Choose a {le} elements long combination\n"
    title += "Press Space to add selection, Enter to submit a combination"
    if (guesses is not None and correctness is not None):
        title += "\nGuesses so far:\n"
        title += guess_printer(guesses, correctness)
    opts = []
    if dupes is True:
        for colour in cols:
            opts.extend([colour]*le)
    else:
        opts = cols
    comb = pick(opts, title, CURSOR, multiselect=True, min_selection_count=le)
    return [element[0] for element in comb]


def ai_guess_printer(guesses, correctness):
    """
    Displays guesses if AI is guessing

    Args:
        guesses (list): Previous guesses
        correctness (list): Correctness of previous guesses
    """
    clear_screen()
    print(f"AI Guesses:\n{guess_printer(guesses, correctness)}")
    input("Press Enter for next guess")


def colourful_string_gen(array):
    """
    Generates a string of colours with ANSI colour literals for given array.
    If colour is not in the internal dictionary, returns colour literal.

    Args:
        array (list): Colours to be printed in colours

    Returns:
        str: Literal with ANSI colours. For display purposes only
    """
    colourful_string = ""
    colours_prefix = "\033["
    colours = {
        "Red": f"{colours_prefix}0;31m",
        "Purple": f"{colours_prefix}0;35m",
        "White": f"{colours_prefix}0;37m",
        "Blue": f"{colours_prefix}0;36m",
        "Green": f"{colours_prefix}0;32m",
        "Yellow": f"{colours_prefix}0;33m",
        "End": f" {colours_prefix}0m"
    }
    end = colours["End"]
    for colour in array:
        if colour in colours:
            colourful_string += colours[colour]+colour+end
        else:
            colourful_string += colour + " "
    return colourful_string


def game_won(moves, combination, mode, modes):
    """
    Prints a message informing about victory

    Args:
        moves (int): Number of attempts that were needed
        combination (list): Correct combination
        mode (int): Current game mode
        MODES (list): List of possible modes
    """
    clear_screen()
    attempts = "attempts"
    if (moves == 1):
        attempts = "attempt"
    plr = "AI"
    if mode == modes[0] or mode == modes[1]:
        plr = "Congratulations, you"
    print(f"{plr} guessed the code in {moves} {attempts}")
    print(f"The correct combination was: {colourful_string_gen(combination)}")
    input("Press Enter to continue")
    print("\n")


def game_lost(combination, NO_OF_ROUNDS, mode, modes):
    """
    Prints message informing about defeat

    Args:
        combination (list): Correct combination
        NO_OF_ROUNDS (int): Number of round played without success
        mode (int): Current game mode
        MODES (list): List of possible modes
    """
    clear_screen()
    plr = "AI "
    if mode == modes[0] or mode == modes[1]:
        plr = "You "
    print(f"{plr}lost. {plr}didn't guess the code in {NO_OF_ROUNDS} attempts")
    print(f"The correct combination was: {colourful_string_gen(combination)}")
    input("Press Enter to continue")
    print("\n")


def what_next():
    """
    Allows players to choose what to do next

    Returns:
        bool: If True - end game. Otherwise return to main menu
    """
    title = "What do you want to do next?"
    options = ["Return to main menu", "Exit the game"]
    result = pick(options, title, CURSOR)
    if result[0] == options[1]:
        return True
    return False


def second_match():
    """
    Prints a message informing players that roles are switching
    """
    print("Now the decoding player chooses the combination to be guessed")
    input("Press Enter to continue")
