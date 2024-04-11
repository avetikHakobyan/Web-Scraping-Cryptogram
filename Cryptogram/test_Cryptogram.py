import unittest
from Cryptogram import *
from colorama import init


class QuotesParserTests(unittest.TestCase):

    def __init__(self, method_name: str = "runTest") -> None:
        super().__init__(method_name)
        self.test_selected_quote = "BE YOURSELF; EVERYONE ELSE IS ALREADY TAKEN."
        self.test_encoded_quote = ['T', 'Z', ' ', 'O', 'R', 'S', 'H', 'D', 'Z', 'Y', 'A', ';', ' ', 'Z', 'J', 'Z', 'H',
                                   'O', 'R', 'P', 'Z', ' ', 'Z', 'Y', 'D', 'Z', ' ', 'N', 'D', ' ', 'F', 'Y', 'H', 'Z',
                                   'F', 'X', 'O', ' ', 'I', 'F', 'U', 'Z', 'P', '.']
        self.test_hidden_quote = ['_', '_', ' ', '_', '_', '_', '_', '_', '_', '_', '_', ';', ' ', '_', '_', '_', '_',
                                  '_', '_',
                                  '_', '_', ' ', '_', '_', '_', '_', ' ', '_', '_', ' ', '_', '_', '_', '_', '_', '_',
                                  '_', ' ',
                                  '_', '_', '_', '_', '_', '.']
        self.test_original = list(ascii_uppercase)
        self.test_mixed = list(ascii_uppercase)

    def test_valid_get_quotes(self):
        self.assertEqual(len(get_quotes()), 30)

    def test_valid_encode_quote(self):
        self.assertNotEqual(encode_quote(self.test_selected_quote, self.test_original, self.test_mixed),
                            encode_quote(self.test_selected_quote, self.test_original, self.test_mixed))

    def test_valid_get_random_quote(self):
        self.assertNotEqual(get_random_quote(get_quotes()), get_random_quote(get_quotes()))

    def test_valid_get_hidden_quote(self):
        self.assertEqual(get_hidden_quote(self.test_selected_quote), self.test_hidden_quote)

    def test_valid_quote_in_string(self):
        self.assertEqual(quote_in_string(get_hidden_quote(self.test_selected_quote)),
                         "_ _   _ _ _ _ _ _ _ _ ;   _ _ _ _ _ _ _ _   _ _ _ _   _ _   _ _ _ _ _ _ _   _ _ _ _ _ .")

    def test_valid_is_letter_used(self):
        converted_letters = {char: "" for char in original}
        converted_letters["A"] = "X"
        self.assertRaises(ReferenceError, lambda: is_letter_used(["B", "A"], converted_letters))

    def test_valid_validate_input(self):
        self.assertRaises(ValueError, lambda: validate_input("1 _"))

    def test_valid_validate_input_underscore(self):
        validate_input("a _")
        self.assertTrue(True)

    def test_valid_convert_letter(self):
        converted_letters = {char: "" for char in original}
        hidden_quote = convert_letter(["T", "B"], self.test_hidden_quote, self.test_encoded_quote, converted_letters)
        self.assertEqual(hidden_quote[0], "B")

    def test_valid_remove_all_mistakes(self):
        converted_letters = {char: "" for char in original}
        hidden_quote = ['A', 'B', ' ', '_', '_', '_', '_', '_', '_', '_', '_', ';', ' ', '_', '_', '_', '_', '_', '_',
                        '_', '_', ' ', '_', '_', '_', '_', ' ', '_', '_', ' ', '_', '_', '_', '_', '_', '_', '_', ' ',
                        '_', '_', '_', '_', '_', '.']
        converted_letters['A'] = 'T'
        converted_letters['E'] = 'Z'
        hidden_quote = remove_all_mistakes(converted_letters, self.test_selected_quote, self.test_encoded_quote,
                                           hidden_quote)
        self.assertEqual(hidden_quote, self.test_hidden_quote)

    def test_valid_convert_random_letter(self):
        converted_letters = {char: "" for char in original}
        hidden_quote = convert_random_letter(converted_letters, self.test_selected_quote, self.test_encoded_quote,
                                             self.test_hidden_quote)
        self.assertLess(hidden_quote.count("_"), 36)

    def test_invalid_get_quotes(self):
        self.assertNotEqual(len(get_quotes()), 0)

    def test_invalid_validate_input_one_letter(self):
        self.assertRaises(IndexError, lambda: validate_input("a "))

    def test_invalid_validate_input_random_string(self):
        self.assertRaises(IndexError, lambda: validate_input("J5sPqRw8"))

    def test_invalid_validate_input_not_letter(self):
        self.assertRaises(ValueError, lambda: validate_input("123 abc"))

    def test_invalid_is_letter_used(self):
        converted_letters = {char: "" for char in original}
        converted_letters["B"] = "X"
        is_letter_used(["B", "A"], converted_letters)
        self.assertTrue(True)

    def test_invalid_convert_letter(self):
        converted_letters = {char: "" for char in original}
        converted_letters['B'] = 'T'
        hidden_quote = ['B', '_', ' ', '_', '_', '_', '_', '_', '_', '_', '_', ';', ' ', '_', '_', '_', '_', '_', '_',
                        '_', '_', ' ', '_', '_', '_', '_', ' ', '_', '_', ' ', '_', '_', '_', '_', '_', '_', '_', ' ',
                        '_', '_', '_', '_', '_', '.']
        self.assertRaises(ReferenceError,
                          lambda: convert_letter(["T", "B"], hidden_quote, self.test_encoded_quote, converted_letters))


if __name__ == '__main__':
    init(autoreset=True)
    unittest.main(verbosity=2)
