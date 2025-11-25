import random
from word_list import words


def scramble_order(length):
    new_order = list(range(length))
    random.shuffle(new_order)
    return new_order


def scramble_word(chosen_word, new_order):
    return ''.join(chosen_word[i] for i in new_order)


def main():
    print(f"\n{'=' * 60}")
    print("\nWelcome to Word Scramble - Food edition!")
    print(f"\n{'=' * 60}")

    print('\nInstractions:\nA scrambled food-related word will be presented to you.\nYour task is to guess the correct word.\nGood luck!\n')

    while True:
        chosen_word = random.choice(words)

        new_order = scramble_order(len(chosen_word))
        scrambled = scramble_word(chosen_word, new_order)

        print(f"Scrambled word: {scrambled}")
        attempts = 0

        while True:
            guess = input("\nYour guess: ").upper()
            attempts += 1

            if guess == chosen_word:
                print("\nCorrect! 👏")
                print(f"You solved it in {attempts} attempts.")
                break
            else:
                print("\nWrong...")
                if input("Try again? (y/n): ").lower() != 'y':
                    print(f"\nThe word was: {chosen_word}")
                    break

        play_again = input("\nDo you want to play another round? (y/n): ").lower()
        if play_again != 'y':
            print("\nThanks for playing! Goodbye :)")
            break


if __name__ == "__main__":
    main()
