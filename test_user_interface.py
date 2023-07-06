import user_interface


def test_guess_printer():
    guess = [["Red", "Blue", "Red", "Blue"]]
    correctness = [["Red", "White"]]
    result = user_interface.guess_printer(guess, correctness)
    assert result == f"Guess: {guess[0]}. Result: {correctness[0]}\n"


def test_colorful_string_gen():
    array_to_colour = ["Red", "Purple", "Blue"]
    print("From test_colorful_string_gen:")
    print(user_interface.colourful_string_gen(array_to_colour))


def test_colorful_string_gen_color_not_in_range():
    array_to_colour = ["Red", "Purple", "Orange"]
    print("From test_colorful_string_gen_not_in_range:")
    print(user_interface.colourful_string_gen(array_to_colour))


def test_second_match(capsys, monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "")
    user_interface.second_match()
    result = capsys.readouterr()
    output = "Now the decoding player chooses the combination to be guessed\n"
    assert result.out == output


if __name__ == "__main__":
    test_colorful_string_gen()
    test_colorful_string_gen_color_not_in_range()
