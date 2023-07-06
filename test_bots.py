from itertools import permutations
import bots
COMBINATION_LENGTH = 4
ALLOWED_COLOURS = ["Red", "Purple", "Yellow", "Blue", "Green", "White"]


def test_create_bot():
    bot = bots.Bot(ALLOWED_COLOURS, True, COMBINATION_LENGTH)
    assert bot._colours == ALLOWED_COLOURS
    assert bot._duplicates is True
    assert bot._comb_len == COMBINATION_LENGTH


def test_create_bot_random():
    bot = bots.Bot_random(ALLOWED_COLOURS, True, COMBINATION_LENGTH)
    assert bot._colours == ALLOWED_COLOURS
    assert bot._duplicates is True
    assert bot._comb_len == COMBINATION_LENGTH


def test_bot_random_guess_combination():
    bot = bots.Bot_random(ALLOWED_COLOURS, True, COMBINATION_LENGTH)
    combination = bot.guess_combination()
    assert len(combination) == COMBINATION_LENGTH
    for colour in combination:
        assert colour in ALLOWED_COLOURS


def test_create_bot_clever():
    bot = bots.Bot_clever(ALLOWED_COLOURS, False, COMBINATION_LENGTH)
    assert bot._colours == ALLOWED_COLOURS
    assert bot._duplicates is False
    assert bot._comb_len == COMBINATION_LENGTH
    assert bot._last_guess == []
    exp_length = len(list(permutations(ALLOWED_COLOURS, COMBINATION_LENGTH)))
    assert len(bot._possible_combinations) == exp_length


def test_bot_clever_guess_combination():
    bot = bots.Bot_clever(ALLOWED_COLOURS, False, COMBINATION_LENGTH)
    combination = bot.guess_combination()
    assert len(combination) == COMBINATION_LENGTH
    for colour in combination:
        assert colour in ALLOWED_COLOURS


def test_bot_clever_possible_colors_in_guess():
    bot = bots.Bot_clever(ALLOWED_COLOURS, False, COMBINATION_LENGTH)
    bot._last_guess = ["Red", "Green", "Blue", "White"]
    cor_len = 3
    result = bot._possible_cols_in_guess(cor_len)
    assert len(result) == 4


def test_bot_clever_possible_colors_not_in_guess():
    bot = bots.Bot_clever(ALLOWED_COLOURS, False, COMBINATION_LENGTH)
    bot._last_guess = ["Red", "Green", "Blue", "White"]
    cor_len = 3
    result = bot._possible_cols_not_in_guess(cor_len)
    assert len(result) == 2


def test_bot_clever_poss_col_combs():
    bot = bots.Bot_clever(ALLOWED_COLOURS, False, COMBINATION_LENGTH)
    bot._last_guess = ["Red", "Green", "Blue", "White"]
    cor_len = 3
    in_guess = bot._possible_cols_in_guess(cor_len)
    not_in_guess = bot._possible_cols_not_in_guess(cor_len)
    result = bot._poss_col_combs(in_guess, not_in_guess)
    assert len(result) == 8


def test_bot_clever_poss_combs():
    bot = bots.Bot_clever(ALLOWED_COLOURS, False, COMBINATION_LENGTH)
    bot._last_guess = ["Red", "Green", "Blue", "White"]
    cor_len = 3
    in_guess = bot._possible_cols_in_guess(cor_len)
    not_in_guess = bot._possible_cols_not_in_guess(cor_len)
    poss_col_combs = bot._poss_col_combs(in_guess, not_in_guess)
    result = bot._poss_combs(poss_col_combs)
    assert len(result) == 24*8


def test_bot_clever_remove_wrong_combs():
    bot = bots.Bot_clever(ALLOWED_COLOURS, False, COMBINATION_LENGTH)
    bot._last_guess = ["Red", "Green", "Blue", "White"]
    cor_len = 3
    in_guess = bot._possible_cols_in_guess(cor_len)
    not_in_guess = bot._possible_cols_not_in_guess(cor_len)
    poss_col_combs = bot._poss_col_combs(in_guess, not_in_guess)
    poss_combs = bot._poss_combs(poss_col_combs)
    result = bot._rem_wrong_combs(poss_combs, 3)
    assert len(result) == 8


def test_bot_clever_possibilities_no_dupes():
    bot = bots.Bot_clever(ALLOWED_COLOURS, False, COMBINATION_LENGTH)
    bot._last_guess = ["Red", "Green", "Blue", "White"]
    cor_len = 3
    in_guess = bot._possible_cols_in_guess(cor_len)
    not_in_guess = bot._possible_cols_not_in_guess(cor_len)
    poss_col_combs = bot._poss_col_combs(in_guess, not_in_guess)
    poss_combs = bot._poss_combs(poss_col_combs)
    poss_combs = bot._rem_wrong_combs(poss_combs, 3)
    result = bot._possibilities(["Red", "Red", "Red"], "Red")
    assert len(result) == 8


def test_bot_clever_possibilities_with_dupes():
    bot = bots.Bot_clever(ALLOWED_COLOURS, True, COMBINATION_LENGTH)
    bot._last_guess = ["Red", "Red", "Blue", "White"]
    result = bot._possibilities(["Red", "Red", "Red"], "Red")
    assert len(result) == 20


def test_bot_clever_update_possible_combinations():
    bot = bots.Bot_clever(ALLOWED_COLOURS, True, COMBINATION_LENGTH)
    bot._last_guess = ["Red", "Red", "Blue", "White"]
    bot.update_possible_combinations(["Red", "Red", "Red"], "Red")
    assert len(bot._possible_combinations) == 20


def test_bot_set_combination():
    combination = bots.bot_set_combination(ALLOWED_COLOURS,
                                           False,
                                           COMBINATION_LENGTH)
    assert len(combination) == COMBINATION_LENGTH
    for colour in combination:
        assert colour in ALLOWED_COLOURS
