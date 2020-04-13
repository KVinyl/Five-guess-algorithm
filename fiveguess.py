from itertools import product


def feedback(guess):
    pass


def print_turn(guess, blacks, whites):
    pass


def remove_codes(poss_codes):
    pass


def next_guess(poss_codes):
    pass


def main():
    # 1. Create the set S of 1296 possible codes
    # (1111, 1112 ... 6665, 6666)
    poss_codes = set(product([1, 2, 3, 4, 5, 6], repeat=4))

    # 2. Start with initial guess 1122
    guess = (1, 1, 2, 2)

    while True:
        # 3. Play the guess to get a response of coloured and white pegs.
        blacks, whites = feedback(guess)
        print_turn(guess, blacks, whites)

        # 4. If the response is four colored pegs,
        # the game is won, the algorithm terminates.
        if blacks == 4:
            break

        # 5. Otherwise, remove from S any code that would not give the same
        # response if it (the guess) were the code.
        poss_codes = remove_codes(poss_codes)

        # 6. Apply minimax technique to find a next guess.
        guess = next_guess(poss_codes)

        # 7. Repeat from step 3


if __name__ == "__main__":
    main()
