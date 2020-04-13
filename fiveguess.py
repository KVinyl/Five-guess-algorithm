from itertools import product


def main():
    # 1. Create the set S of 1296 possible codes
    # (1111, 1112 ... 6665, 6666)
    s = set(product([1, 2, 3, 4, 5, 6], repeat=4))

    # 2. Start with initial guess 1122
    guessed_code = (1, 1, 2, 2)

    while True:
        pass
        # 3. Play the guess to get a response of coloured and white pegs.

        # 4. If he response is four colored pegs,
        # the game is won, the algorithm terminates.

        # 5. Otherwise, remove from S any code that would not give the same
        # response if it (the guess) were the code.

        # 6. Apply minimax technique to find a next guess.

        # 7. Repeat from step 3


if __name__ == "__main__":
    main()
