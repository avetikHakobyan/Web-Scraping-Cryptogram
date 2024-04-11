import random
from random import shuffle
import time
from string import ascii_uppercase
from QuotesParser import *
import urllib.request as req
from colorama import init, Fore

original = list(ascii_uppercase)
mixed = list(ascii_uppercase)


def get_quotes():
    url = "https://www.goodreads.com/quotes"
    with req.urlopen(url) as f:
        lines = list(line.decode("utf-8").strip() for line in f.readlines())

    parser = QuotesParser()

    for line in lines:
        parser.feed(line)

    return parser.get_quotes()


def encode_quote(string, original_arg, mixed_arg):
    shuffle(mixed_arg)
    encoded_string = []
    for char in string:
        if char in original_arg:
            encoded_string.append(mixed_arg[original_arg.index(char)])
        else:
            encoded_string.append(char)
    return encoded_string


def get_random_quote(quotes):
    shuffle(quotes)
    return quotes.pop(1)


def get_hidden_quote(selected_quote):
    return ["_" if char in original else char for char in selected_quote]


def quote_in_string(quote_list):
    return " ".join(quote_list)


def is_letter_used(letter_list, converted_letters):
    if letter_list[1] != "_":
        if converted_letters[letter_list[1]] != '':
            raise ReferenceError(f'{letter_list[1]} is already used! Convert another letter')


def update_converted_letters(letter_list, converted_letters):
    if letter_list[1] != "_":
        converted_letters[letter_list[1]] = letter_list[0]


def reset_alphabet_value(letter_list, hidden_quote, converted_letters, i):
    if letter_list[0] in converted_letters.values():
        converted_letters[hidden_quote[i]] = ""


def convert_letter(letter_list, hidden_quote, encoded_quote, converted_letters):
    is_letter_used(letter_list, converted_letters)
    reset_alphabet_value(letter_list, hidden_quote, converted_letters, encoded_quote.index(letter_list[0]))
    for i in range(len(encoded_quote)):
        if encoded_quote[i] == letter_list[0].upper():
            hidden_quote[i] = letter_list[1].upper()
    update_converted_letters(letter_list, converted_letters)
    return hidden_quote


def is_game_over(hidden_quote):
    return "_" in hidden_quote


def validate_input(command):
    message = "Invalid command, please try again"
    command_list = command.split()
    if command_list:
        if len(command_list) == 2:
            for item in command_list:
                if len(item) != 1:
                    raise ValueError(message)
                elif not item.isalpha() and item != "_":
                    raise ValueError(message)
        elif command_list[0] not in ["?", "!"]:
            raise IndexError(message)
        else:
            raise SyntaxError(message)
    else:
        raise SyntaxError(message)


def remove_all_mistakes(converted_letters, selected_quote, encoded_quote, hidden_quote):
    removed = False
    for i in range(len(hidden_quote)):
        if hidden_quote[i] != "_":
            if hidden_quote[i] != selected_quote[i]:
                removed = True
                reset_alphabet_value([encoded_quote[i], "_"],
                                     hidden_quote, converted_letters, encoded_quote.index(encoded_quote[i]))
                hidden_quote[i] = "_"
                print(f'{Fore.RED}{hidden_quote[i]}', end=' ')
            else:
                print(f'{hidden_quote[i]}', end=' ')
        else:
            print(f'{hidden_quote[i]}', end=' ')
    print()
    display_encoded_quote(encoded_quote)
    if removed:
        print('All the mistakes were removed.\n')
    else:
        print('No mistakes found! Keep solving!\n')
    return hidden_quote


def convert_random_letter(converted_letters, selected_quote, encoded_quote, hidden_quote):
    random_letter = random.choice([char for char in selected_quote if char.isalpha() and converted_letters[char] == ''])
    hidden_quote = convert_letter([encoded_quote[selected_quote.index(random_letter)], random_letter],
                                  hidden_quote, encoded_quote, converted_letters)
    for char in hidden_quote:
        if char == random_letter:
            print(f'{Fore.GREEN}{char}', end=' ')
        else:
            print(f'{char}', end=' ')
    print()
    display_encoded_quote(encoded_quote)
    return hidden_quote


def display_congrats_timing(start_time):
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = round(elapsed_time % 60)
    print(f'Congratulations! You won!', end=' ')
    message = f'{seconds} seconds to solve it!'
    if minutes != 0:
        message = f'{minutes} minutes and {message}'
    print(f'It took {message}')


def display_alphabet(converted_letters, encoded_quote):
    for key, value in converted_letters.items():
        print(Fore.BLUE + key, end=': ')
        if value in encoded_quote:
            print(Fore.YELLOW + value, end='  ')
        else:
            print("_", end='  ')
    print('\n')


def display_encoded_quote(encoded_quote):
    print(f'{Fore.YELLOW}{quote_in_string(encoded_quote)}\n')


def display_hidden_quote(hidden_quote):
    print(f'{quote_in_string(hidden_quote)}')


def play():
    start_time = time.time()
    converted_letters = {char: "" for char in original}
    is_hint_available = True
    quotes = get_quotes()
    selected_quote = get_random_quote(quotes).upper()
    encoded_quote = encode_quote(selected_quote, original, mixed)
    hidden_quote = get_hidden_quote(selected_quote)
    display_hidden_quote(hidden_quote)
    display_encoded_quote(encoded_quote)
    display_alphabet(converted_letters, encoded_quote)
    while True:
        input_string = input("Enter: ")
        print("————————————————————————————————————————————————————————————————————————————————————————————————————————"
              "————————————————————————————————————————————————\n")
        try:
            if input_string == "?":
                if is_hint_available:
                    is_hint_available = False
                    hidden_quote = convert_random_letter(converted_letters, selected_quote, encoded_quote, hidden_quote)
                else:
                    raise ValueError("You've already used a hint. Remember, you're entitled to just one hint per quote."
                                     " Keep solving, you've got this!")
            elif input_string == "!":
                hidden_quote = remove_all_mistakes(converted_letters, selected_quote, encoded_quote, hidden_quote)
            else:
                validate_input(input_string)
                letter_list = input_string.upper().split()
                hidden_quote = convert_letter(letter_list, hidden_quote, encoded_quote, converted_letters)
                display_hidden_quote(hidden_quote)
                display_encoded_quote(encoded_quote)

            display_alphabet(converted_letters, encoded_quote)

            if not is_game_over(hidden_quote):
                if "".join(hidden_quote) == selected_quote:
                    display_congrats_timing(start_time)
                    break
                else:
                    print("Oops! The quote is incorrect. Keep solving, you've got this!\n")
                    hidden_quote = remove_all_mistakes(converted_letters, selected_quote, encoded_quote, hidden_quote)
        except Exception as error:
            print(f'Error: {error}')


if __name__ == "__main__":
    init(autoreset=True)
    print("\n* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *\n")
    print("Welcome to Cryptogram!\n")
    print('A cryptogram game is a word puzzle or brainteaser that involves decoding a quote that has been encrypted or'
          ' encoded.')
    print('The encoded quote is shown as yellow.')
    print('For each quote, you have the option to get only one hint to convert a random letter in the quote.\n')
    print('Here is the available commands:\n')
    print('     • a b: Convert \'a\' to \'b\' (change \'a\' and \'b\' to your desired letters)')
    print('     • ?: Get a hint')
    print('     • !: Reveal all the mistakes')
    print('\nHave fun :)\n')
    while True:
        play()
        play_again = input("Do you want to play again? (Y/N)\n")
        if play_again.upper().strip() == "N":
            print("Thank you for playing! See you soon...")
            break
