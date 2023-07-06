from game_logic import (
                        MODES,
                        Game,
                        COMBINATION_LENGTH,
                        ALLOWED_COLOURS,
                        EMPTY_NOTATION,
                        WHITE_PIN,
                        RED_PIN,
                        )
from bots import Bot_clever


def test_create_game(monkeypatch):  # ogarnąć jak testować z inputami rzeczy
    game = Game(MODES[1], False, False)
    assert game._mode == MODES[1]
    assert game._allowed_colours == ALLOWED_COLOURS
    assert game._duplicates is False
    assert game._guesses == []
    assert game._guess_correctness == []
    assert game._game_won is False
    assert len(game._combination) == COMBINATION_LENGTH
    for element in game._combination:
        assert element in ALLOWED_COLOURS


def test_check_duplicates_no_dupes():
    game = Game(MODES[1], False, False)
    combination = ["Red", "Blue", "Purple", "White"]
    assert game.check_duplicates(combination) is True


def test_check_duplicates_dupes():
    game = Game(MODES[1], False, False)
    combination = ["Red", "Blue", "Purple", "Red"]
    assert game.check_duplicates(combination) is False


def test_check_colours_no_dupes():
    game = Game(MODES[1], False, False)
    combination = ["Red", "Blue", "Purple", "Green"]
    game._combination = combination
    guess = ["Blue", "Purple", "White", "Yellow"]
    game._guesses.append(guess)
    assert game.check_colours() == 2


def test_check_colours_dupes():
    game = Game(MODES[1], True, False)
    combination = ["Red", "Blue", "Purple", "Blue"]
    game._combination = combination
    guess = ["Blue", "Purple", "White", "Yellow"]
    game._guesses.append(guess)
    assert game.check_colours() == 2


def test_check_colours_no_matching_colours():
    game = Game(MODES[1], True, False)
    combination = ["Red", "Red", "Red", "Red"]
    game._combination = combination
    guess = ["Blue", "Purple", "White", "Yellow"]
    game._guesses.append(guess)
    assert game.check_colours() == 0


def test_check_colours_and_place():
    game = Game(MODES[1], True, False)
    combination = ["Red", "Red", "Blue", "Yellow"]
    game._combination = combination
    guess = ["Blue", "Red", "White", "Yellow"]
    game._guesses.append(guess)
    assert game.check_colours_and_place() == 2


def test_check_colours_and_place_no_matching():
    game = Game(MODES[1], True, False)
    combination = ["Red", "Red", "Red", "Red"]
    game._combination = combination
    guess = ["Blue", "Purple", "White", "Yellow"]
    game._guesses.append(guess)
    assert game.check_colours_and_place() == 0


def test_check_combination():
    game = Game(MODES[1], True, False)
    combination = ["Red", "Red", "Blue", "Yellow"]
    game._combination = combination
    guess = ["Blue", "Red", "White", "Yellow"]
    game._guesses.append(guess)
    assert game.check_combination() == [RED_PIN, RED_PIN, WHITE_PIN]


def test_check_combination_no_matches():
    game = Game(MODES[1], True, False)
    combination = ["Red", "Red", "Red", "Red"]
    game._combination = combination
    guess = ["Blue", "Purple", "White", "Yellow"]
    game._guesses.append(guess)
    assert game.check_combination() == []


def test_guess_combination():
    game = Game(MODES[1], False, False)
    ai = Bot_clever(ALLOWED_COLOURS, False, COMBINATION_LENGTH)
    game.guess_combination(ai)
    assert len(game._guesses[-1]) == COMBINATION_LENGTH
    for element in game._guesses[-1]:
        assert element in ALLOWED_COLOURS


def test_check_if_won_win():
    game = Game(MODES[1], True, False)
    combination = ["Blue", "Red", "White", "Yellow"]
    game._combination = combination
    guess = ["Blue", "Red", "White", "Yellow"]
    game._guesses.append(guess)
    game._guess_correctness.append(game.check_combination())
    game.check_if_won()
    assert game._game_won is True


def test_check_if_won_no_win():
    game = Game(MODES[1], True, False)
    combination = ["Red", "Red", "Blue", "Yellow"]
    game._combination = combination
    guess = ["Blue", "Red", "White", "Yellow"]
    game._guesses.append(guess)
    game.check_combination()
    game.check_if_won
    assert game._game_won is False
