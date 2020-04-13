from collections import Counter, namedtuple
from itertools import product
from random import randint

Feedback = namedtuple('Feedback', ['blacks', 'whites'])


class Mastermind():
    def __init__(self):
        self.pegs = 4
        self.colors = 6
        self._code = tuple(randint(1, self.colors) for _ in range(self.pegs))
        self.win = False

    def feedback(self, guess):
        blacks = sum(g == c for g, c in zip(guess, self._code))
        whites = sum((Counter(guess) & Counter(
            self._code)).values()) - blacks

        if blacks == self.pegs:
            self.win = True

        return Feedback(blacks, whites)

    def victory(self):
        return self.win


def print_turn(guess, fb):
    """Print the guess and feedback of the turn"""
    blacks, whites = fb
    print("Guess: ", guess)
    print("Blacks: ", blacks)
    print("Whites: ", whites)
    print()


def remove_codes(poss_codes):
    pass


def next_guess(poss_codes):
    pass


def main():
    mastermind = Mastermind()

    # 1. Create the set S of 1296 possible codes
    # (1111, 1112 ... 6665, 6666)
    poss_codes = set(product([1, 2, 3, 4, 5, 6], repeat=4))

    # 2. Start with initial guess 1122
    guess = (1, 1, 2, 2)

    while True:
        # 3. Play the guess to get a response of coloured and white pegs.
        fb = mastermind.feedback(guess)
        print_turn(guess, fb)

        # 4. If the response is four colored pegs,
        # the game is won, the algorithm terminates.
        if mastermind.victory():
            break

        # 5. Otherwise, remove from S any code that would not give the same
        # response if it (the guess) were the code.
        poss_codes = remove_codes(poss_codes)

        # 6. Apply minimax technique to find a next guess.
        guess = next_guess(poss_codes)

        # 7. Repeat from step 3


if __name__ == "__main__":
    main()
