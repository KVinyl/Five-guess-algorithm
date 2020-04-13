from collections import Counter, namedtuple
from itertools import product
from random import randint

Feedback = namedtuple('Feedback', ['blacks', 'whites'])


class Mastermind():
    def __init__(self, code=None):
        self.pegs = 4
        self.colors = 6
        self.win = False

        if code is None:
            self._code = tuple(randint(1, self.colors)
                               for _ in range(self.pegs))
        else:
            self._code = code

        assert type(self._code) == tuple
        assert len(self._code) == self.pegs
        assert all(n >= 1 and n <= self.colors for n in self._code)

    def feedback(self, guess):
        """
        Return a namedtuple Feedback(blacks, whites) where
        blacks is the number of pegs from the guess that
        are correct in both color and position and
        whites is the number of pegs of the right color but wrong position.
        """
        blacks = sum(g == c for g, c in zip(guess, self._code))
        whites = sum((Counter(guess) & Counter(
            self._code)).values()) - blacks

        if blacks == self.pegs:
            self.win = True

        return Feedback(blacks, whites)

    def victory(self):
        """Return whether the secret code has been correctly guessed."""
        return self.win


def print_turn(guess, fb):
    """Print the guess and feedback of the turn."""
    blacks, whites = fb
    print("Guess: ", guess)
    print("Blacks: ", blacks)
    print("Whites: ", whites)
    print()


def reduce_possible_codes(possible_codes, guess, fb):
    """Return a set with all elements from possible_codes that would receive
    the same feedback as the actual feedback from guess, fb,
    if guess was the secret code."""
    test = Mastermind(guess)

    return {code for code in possible_codes if test.feedback(code) == fb}


def next_guess(possible_codes):
    raise NotImplementedError


def main():
    """
    Five-guess algorithm steps are directly from the Mastermind wikipedia page:
    https://en.wikipedia.org/wiki/Mastermind_(board_game)#Five-guess_algorithm
    """
    mastermind = Mastermind()

    # 1. Create the set S of 1296 possible codes
    # (1111, 1112 ... 6665, 6666)
    possible_codes = set(product([1, 2, 3, 4, 5, 6], repeat=4))

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
        possible_codes = reduce_possible_codes(possible_codes, guess, fb)

        # 6. Apply minimax technique to find a next guess.
        guess = next_guess(possible_codes)

        # 7. Repeat from step 3


if __name__ == "__main__":
    main()
