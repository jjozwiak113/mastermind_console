from random import choice, sample, choices
from itertools import product, permutations, combinations


class Bot():
    """
    Base class for AI Players

    Attributes:
        _colours (list): List of allowed colours
        _duplicates (bool): True if duplicates are enabled, False otherwise
        _comb_len (int): Combination length

    Methods:
        __init__: creates bot object
        guess_combination: placeholder for inheriting classes
    """
    def __init__(self, colours, duplicates, le):
        """
        Creates bot object

        Args:
            colours (list): List of allowed colours
            duplicates (bool): True if duplicates are enabled, False otherwise
            le (int): Length of combination to be guessed
        """
        self._colours = colours
        self._duplicates = duplicates
        self._comb_len = le

    def guess_combination(self):
        """
        Placeholder for inheriting classes
        """
        pass


class Bot_random(Bot):
    """
    AI Player designed to randomly choose combination. Inherits from Bot

    Args:
        Bot (Bot): Base class, contains constructor

    Attributes:
        _colours (list): List of allowed colours (Inherited from Bot)
        _duplicates (bool): True if duplicates are enabled, False otherwise
        (Inherited from Bot)
        _comb_len (int): Combination length (Inherited from Bot)

    Methods:
        __init__: creates bot_random object (Inherited from Bot)
        guess_combination: returns randomly chosen combination from those
        allowed
    """
    def guess_combination(self):
        """
        Returns randomly chosen combination from those allowed, without
        consideration of previous guesses

        Returns:
            list: Chosen combination
        """
        return bot_set_combination(self._colours,
                                   self._duplicates,
                                   self._comb_len)


class Bot_clever(Bot):
    """
    AI Player designed to choose combination based on simple algorithm.
    Inherits from Bot

    Args:
        Bot (Bot): Base class

    Attributes:
        _colours (list): List of allowed colours (Inherited from Bot)
        _duplicates (bool): True if duplicates are enabled, False otherwise
        (Inherited from Bot)
        _comb_len (int): Combination length (Inherited from Bot)
        _last_guess (list): Last guess of the bot
        _possible_combinations (list): Contains possible combinations based
        on previous guesses

    Methods:
        __init__: creates bot_clever object (Inherited from Bot)
        guess_combination: returns randomly chosen combination from
        those possible based on previous guesses
        _possible_cols_in_guess: returns possible colours from those used
    in the guess (only for games without duplicates)
        _possible_cols_not_in_guess: returns possible colours from those
    not used in the guess (only for games without duplicates)
        _poss_col_combs: returns all possible combinations of colours
    (only for games without duplicates)
        _poss_combs: returns all possible combinations for given list of
    colours combination (only for games without duplicates)
        _rem_wrong_combs: returns a list of possible combinations based
    on number of red pins they would produce
        _possibilities: returns list of possible combinations according to
    previous guess
        update_possible_combinations: Updates internal variable containing
    possible combinations according to previous guesses
    """
    def __init__(self, colours, duplicates, le):
        """
        Creates bot_clever object

        Args:
            colours (list): List of allowed colours
            duplicates (bool): True if duplicates are enabled, False otherwise
            le (int): Length of combination to be guessed
        """
        super().__init__(colours, duplicates, le)
        self._last_guess = []
        self._possible_combinations = []
        if self._duplicates:
            self._possible_combinations = list(product(self._colours,
                                                       repeat=self._comb_len))
        else:
            self._possible_combinations = list(permutations(self._colours,
                                                            self._comb_len))

    def guess_combination(self):
        """
        Returns randomly chosen combination from those possible based
        on previous guesses

        Returns:
            list: Chosen combination
        """
        self._last_guess = choice(self._possible_combinations)
        return self._last_guess

    def _possible_cols_in_guess(self, cor_len):
        """
        Returns possible colours from those used in the guess
        (only for games without duplicates)
        Args:
            cor_len (int): Length of list with previous guess correctness

        Returns:
            list: Possible colours from those used in the guess
        """
        return list(combinations(self._last_guess,
                                 cor_len))

    def _possible_cols_not_in_guess(self, cor_len):
        """
        Returns possible colours from those not used in the guess
        (only for games without duplicates)
        Args:
            cor_len (int): Length of list with previous guess correctness

        Returns:
            list: Possible colours from those not used in the guess
        """
        colours_not_used = []
        for colour in self._colours:
            if colour not in self._last_guess:
                colours_not_used.append(colour)
        return list(combinations(colours_not_used,
                                 self._comb_len-cor_len))

    def _poss_col_combs(self, possible_from_comb, possible_not_from_comb):
        """
        Returns all possible combinations of colours
        (only for games without duplicates)

        Args:
            possible_from_comb (list): Possible colours combinations from guess
            possible_not_from_comb (list): Possible colours combinations
        not from guess

        Returns:
            list: Possible combinations of colours
        """
        possible_cols_combs = []
        for comb in possible_from_comb:
            for colours in possible_not_from_comb:
                temp = list(comb)
                temp.extend(list(colours))
                possible_cols_combs.append(temp)
        return possible_cols_combs

    def _poss_combs(self, possible_cols_combs):
        """
        Returns all possible combinations for given list of
        colours combination (only for games without duplicates)

        Args:
            possible_cols_combs (list): Possible combinations of colours

        Returns:
            list: Possible combinations
        """
        possible_combs = []
        for comb in possible_cols_combs:
            possible_combs.extend(list(permutations(comb,
                                                    self._comb_len)))
        return possible_combs

    def _rem_wrong_combs(self, possible_combs, no_of_red):
        """
        Returns a list of possible combinations based on their similarity
        to last_guess. For example, if previous guess produced 2 red pins,
        method return only combinations that have exactly 2 colours
        in the same positions as last guess

        Args:
            possible_combs (list): Possible combinations
            no_of_red (int): Number of red pins produced by previous guess

        Returns:
            list: Reduced list of possible combinations
        """
        temp = []
        for combination in possible_combs:
            red_count = 0
            for guess_el, comb_el in zip(self._last_guess, combination):
                if guess_el == comb_el:
                    red_count += 1
            if red_count == no_of_red:
                temp.append(combination)
        return temp

    def _possibilities(self, guess_correctness, RED_PIN):
        """
        Returns list of possible combinations according to previous guess

        Args:
            guess_correctness (list): Correctness of previous guess
            RED_PIN (str): Literal used to represent red pin

        Returns:
            list: Possible combinations according to previous guess
        """
        cor_len = len(guess_correctness)
        possible_combs = []
        if not self._duplicates:
            # Find possible colours from those that were used in the guess
            possible_from_comb = self._possible_cols_in_guess(cor_len)
            # Find possible colours from those that weren't used in the guess
            possible_not_from_comb = self._possible_cols_not_in_guess(cor_len)
            # Find all possible combinations of colours
            possible_cols_combs = self._poss_col_combs(possible_from_comb,
                                                       possible_not_from_comb)
            # Find all possible combinations for given colours
            possible_combs = self._poss_combs(possible_cols_combs)
            # Remove combinations that would produce wrong amount of red pins
            no_of_red = guess_correctness.count(RED_PIN)
            possible_combs = self._rem_wrong_combs(possible_combs, no_of_red)
        else:
            # Remove combinations that would produce wrong amount of red pins
            no_of_red = guess_correctness.count(RED_PIN)
            possible_combs = self._rem_wrong_combs(self._possible_combinations,
                                                   no_of_red)
        return possible_combs

    def update_possible_combinations(self, guess_correctness, RED_PIN):
        """
        Updates internal variable containing possible combinations according
        to previous guesses

        Args:
            guess_correctness (list): Correctness of previous guess
            RED_PIN (str): Literal used to represent red pin
        """
        temp = []
        possibilities = self._possibilities(guess_correctness, RED_PIN)
        for combination in self._possible_combinations:
            if combination in possibilities:
                temp.append(combination)
        self._possible_combinations = temp


def bot_set_combination(colours, duplicates, le):
    """
    Randomly generates a combination for given length, colours
    and duplicates allowance

    Args:
        colours (list): Allowed colours
        duplicates (bool): True if duplicates are enabled, False otherwise
        le (int): Length of combination to be generated

    Returns:
        list: Generated combination
    """
    if not duplicates:
        return sample(colours, le)
    else:
        return choices(colours, k=le)
