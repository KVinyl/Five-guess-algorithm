from collections import Counter, namedtuple
from itertools import product
from random import randint


init_possible_codes = set(product([1, 2, 3, 4, 5, 6], repeat=4))

Feedback = namedtuple('Feedback', ['blacks', 'whites'])


class Mastermind():
    def __init__(self, code=None):
        self.pegs = 4
        self.colors = 6
        self.guesses = set()
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
        Add guess to set of past guesses and
        return a namedtuple Feedback(blacks, whites) where
        blacks is the number of pegs from the guess that
        are correct in both color and position and
        whites is the number of pegs of the right color but wrong position.
        """
        self.guesses.add(guess)

        blacks = sum(g == c for g, c in zip(guess, self._code))
        whites = sum((Counter(guess) & Counter(
            self._code)).values()) - blacks

        if blacks == self.pegs:
            self.win = True

        return Feedback(blacks, whites)

    def past_guesses(self):
        """Return set of past guesses made."""
        return self.guesses

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


def next_guess(possible_codes, past_guesses):
    """
    Return the next guess.

    A score is calculated for each possible guess
    (any unguessed code in the original 1296 set).
    The score is the minimum number of possibilites it might
    eliminate from possible_guesses.

    The minimum eliminated is the count of elements in possible_codes
    minus the highest hit count (the count of the most frequent black/white peg
    feedback when passed through possible_codes)

    The next guess is the guess with the highest score and is in possible_set
    whenever possible.
    """
    def score(guess):
        fbs = [Mastermind(code).feedback(guess) for code in possible_codes]
        return len(possible_codes) - max(Counter(fbs).values())

    ScoreData = namedtuple('ScoreData', ['score', 'is_possible_code', 'guess'])
    scores = [ScoreData(score(guess), guess in possible_codes, guess)
              for guess in (init_possible_codes - past_guesses)]

    return max(scores).guess


def main():
    """
    Five-guess algorithm steps are directly from the Mastermind wikipedia page:
    https://en.wikipedia.org/wiki/Mastermind_(board_game)#Five-guess_algorithm
    """
    mastermind = Mastermind()

    # 1. Create the set S of 1296 possible codes
    # (1111, 1112 ... 6665, 6666)
    possible_codes = init_possible_codes.copy()

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
        guess = next_guess(possible_codes, mastermind.past_guesses())

        # 7. Repeat from step 3


if __name__ == "__main__":
    main()
