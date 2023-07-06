import user_interface
from bots import Bot_clever, Bot_random, bot_set_combination
COMBINATION_LENGTH = 4
ALLOWED_COLOURS = ["Red", "Purple", "Yellow", "Blue", "Green", "White"]
EMPTY_NOTATION = "Empty"  # literal used to denote an empty space
WHITE_PIN = "White"  # literal used to denote a white pin
RED_PIN = "Red"  # literal used to denote a red pin
OPTIONS = ["2 Players", "Easy AI", "Hard AI", "Rules"]
CONFIGURATIONS = [
    "No duplicates, no empty spaces",
    "No duplicates, empty spaces allowed",
    "Duplicates allowed, no empty spaces",
    "Duplicates and empty spaces allowed"
]
NO_OF_ROUNDS = 25
MODES = [0, 1, 2, 3]
# Mode 0 - Player 1 chooses the combination, Player 2 guesses it
# Mode 1 - AI chooses the combination, Player guesses it
# Mode 2 - Player chooses the combination, Easy AI guesses it
# Mode 3 - Player chooses the combination, Hard AI guesses it


class DuplicatesDetectedError(Exception):
    """
    Raised when unpermitted duplicates are detected
    """
    def __init__(self, combination):
        self._message = f"{combination} contains duplicates - not allowed"
        super().__init__(self._message)


class Game:
    """
    A class used to store elements of a game and run it

    Attributes:
        _mode (int): Running mode of the game
        _allowed_colours (list): Colours that can be picked
        _duplicates (bool): Information whether duplicates are allowed
        _combination (list): Correct combination
        _guesses (list): Guesses of the player
        _guess_correctness (list): Correctness of player's guesses
        _game_won (bool): Information whether correct combination was guessed

    Methods:
        __init__: creates game object
        allowed_colours: returns allowed colours
        _check_length: returns information whether combination has good length
        check_duplicates: checks for duplicates in a given combination
        set_combination: chooses combination and returns it
        check_colours: returns number of correct colours in a combination
        check_colours_and_place: returns number of red pins
        check_combination: returns list with correctness of combination
        guess_combination: guesses combination
        check_if_won: checks if game has been won in the last guess
        game_result: displays game results to player(s)
        guessing_phase: used for running guessing in the game
    """
    def __init__(self, mode, duplicates: bool, blanks: bool):
        """
        Creates game object

        Args:
            mode (int): Denotes mode that the game is running in
            duplicates (bool): Denotes whether duplicates are allowed
            blanks (bool): Denotes whether empty spaces are allowed
        """
        self._mode = mode
        self._allowed_colours = []
        self._allowed_colours.extend(ALLOWED_COLOURS)
        self._duplicates = duplicates
        if blanks is True:
            self._allowed_colours.append(EMPTY_NOTATION)
        if self._mode == MODES[1]:
            self._combination = bot_set_combination(self._allowed_colours,
                                                    self._duplicates,
                                                    COMBINATION_LENGTH)
        else:
            self._combination = self.set_combination()
        self._guesses = []
        self._guess_correctness = []
        self._game_won = False

    def allowed_colours(self):
        return self._allowed_colours

    def _check_length(self, combination):
        """
        Checks whether the combination has appropriate length

        Args:
            combination (list): Combination to be checked

        Returns:
            bool: True if length of combination is equal to COMBINATION_LENGTH.
            Otherwise False
        """
        try:
            return COMBINATION_LENGTH == len(combination)
        except TypeError:
            return False

    def check_duplicates(self, comb: list):
        """
        Checks whether there are duplicates in a given combination

        Args:
            comb (list): Combination to be checked

        Returns:
            bool: True if no duplicates were detected. Otherwise False
        """
        no_dupes = [i for n, i in enumerate(comb) if i not in comb[:n]]
        if no_dupes == comb:
            return True
        return False

    def set_combination(self):
        """
        Sets combination and checks for unpermitted duplicates

        Raises:
            DuplicatesDetectedError: If unpermitted duplicates were detected

        Returns:
            list: Chosen combination
        """
        choice = []
        while not self._check_length(choice):
            choice = user_interface.set_combination(self.allowed_colours(),
                                                    self._duplicates,
                                                    COMBINATION_LENGTH)
        if self._duplicates is False:
            if self.check_duplicates(choice) is False:
                raise DuplicatesDetectedError(choice)
        return choice

    def check_colours(self):
        """
        Checks number of correct colours in a last chosen combination

        Returns:
            int: Number of correct colours
        """
        white_count = 0
        if self._duplicates is False:
            for guess in self._guesses[-1]:
                if guess in self._combination:
                    white_count += 1
        if self._duplicates is True:
            combination_temp = []
            combination_temp.extend(self._combination)
            for guess in self._guesses[-1]:
                if guess in combination_temp:
                    white_count += 1
                    combination_temp.remove(guess)
        return white_count

    def check_colours_and_place(self):
        """
        Checks number of elements with correct colour and place
        in a last chosen combination

        Returns:
            int: Number of elements with correct colour and place
        """
        red_count = 0
        for guess, code in zip(self._guesses[-1], self._combination):
            if guess == code:
                red_count += 1
        return red_count

    def check_combination(self):
        """
        Checks correctness last chosen combination

        Returns:
            list: Red pins and white pins for last chosen combination
        """
        red_count = self.check_colours_and_place()
        white_count = self.check_colours() - red_count
        return [RED_PIN] * red_count + [WHITE_PIN] * white_count

    def guess_combination(self, ai):
        """
        Guesses combination (using Player input or AI) and
        appends it to table of guesses

        Args:
            ai (Bot): If None - Player is guessing the combination.
            Otherwise, AI is guessing it
        """
        guess = []
        if ai is None:
            while(not self._check_length(guess)):
                guess = user_interface.set_combination(self.allowed_colours(),
                                                       self._duplicates,
                                                       COMBINATION_LENGTH,
                                                       self._guesses,
                                                       self._guess_correctness)
        else:
            guess = ai.guess_combination()
        self._guesses.append(guess)

    def check_if_won(self):
        """
        Checks if the last guess was game-winning. If so, sets game_won to True
        """
        if len(self._guess_correctness[-1]) == COMBINATION_LENGTH:
            if WHITE_PIN not in self._guess_correctness[-1]:
                self._game_won = True

    def game_result(self):
        """
        Sends information about game result to user_interface to display it
        """
        if self._game_won:
            user_interface.game_won(len(self._guesses),
                                    self._combination,
                                    self._mode,
                                    MODES)
        else:
            user_interface.game_lost(self._combination,
                                     NO_OF_ROUNDS,
                                     self._mode,
                                     MODES)

    def guessing_phase(self):
        """
        Used for running guessing phase in the game.
        Creates AI Players if necessary, then runs guessing cycle
        (guessing and checking) until game is won or guess limit is reached
        """
        ai = None
        if self._mode == MODES[2]:
            ai = Bot_random(self._allowed_colours,
                            self._duplicates,
                            COMBINATION_LENGTH)
        if self._mode == MODES[3]:
            ai = Bot_clever(self._allowed_colours,
                            self._duplicates,
                            COMBINATION_LENGTH)
        while len(self._guesses) < NO_OF_ROUNDS:
            self.guess_combination(ai)
            self._guess_correctness.append(self.check_combination())
            if ai is not None:
                user_interface.ai_guess_printer(self._guesses,
                                                self._guess_correctness)
            self.check_if_won()
            if self._game_won:
                break
            if self._mode == MODES[3]:
                ai.update_possible_combinations(self._guess_correctness[-1],
                                                RED_PIN)
        self.game_result()


"""
TODO:
poniedziałek:
    napisz dokumentację (tego PDFa)
    daj licencję tego pick i zadbaj, żeby on się tam znalazł na tym githubie
"""
