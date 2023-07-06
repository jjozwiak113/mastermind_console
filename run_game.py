from game_logic import Game, OPTIONS, MODES, CONFIGURATIONS
import user_interface


def run_game(mode, settings):
    """
    Runs one round of a game with given parameters

    Args:
        mode (int): Stores information about game mode to be used
        settings (tuple): Stores information about game parameters:
        whether blanks and / or duplicates are allowed
        )
    """
    game = Game(mode, settings[0], settings[1])
    user_interface.switch_message(mode, MODES)
    game.guessing_phase()


def main_menu():
    """
    Starting function of the game. Handles proper setup of the game,
    as well as running it
    """
    end_game = False
    while not end_game:
        selected = user_interface.main_menu(OPTIONS)
        if selected == OPTIONS[0]:  # 2 Players
            settings = choose_settings()
            run_game(MODES[0], settings)
            user_interface.second_match()
            run_game(MODES[0], settings)
        elif selected == OPTIONS[1]:  # Player vs Easy AI
            settings = choose_settings()
            run_game(MODES[1], settings)
            user_interface.second_match()
            run_game(MODES[2], settings)
        elif selected == OPTIONS[2]:  # Player vs Hard AI
            settings = choose_settings()
            run_game(MODES[3], settings)
            user_interface.second_match()
            run_game(MODES[3], settings)
        else:
            rules()
        end_game = user_interface.what_next()


def choose_settings():
    """
    Allows for choice of game settings (duplicates and blanks)

    Returns:
        tuple: 2-elements long, both are bools.
        First one is for duplicates (whether they are allowed)
        Second one is for empty spaces (whether they are allowed)
    """
    selected = user_interface.choose_settings(CONFIGURATIONS)
    if selected == 0:
        settings = (False, False)
    elif selected == 1:
        settings = (False, True)
    elif selected == 2:
        settings = (True, False)
    elif selected == 3:
        settings = (True, True)
    return settings


def rules():
    """
    Prints out rules of the game
    """
    user_interface.rules()
    main_menu()


if __name__ == "__main__":
    main_menu()
