from collections import Counter, namedtuple
from itertools import product
from operator import attrgetter
from random import randint


init_possible_codes = set(product([1, 2, 3, 4, 5, 6], repeat=4))

Feedback = namedtuple('Feedback', ['blacks', 'whites'])
ScoreData = namedtuple('ScoreData', ['guess', 'score', 'is_possible_code'])


def feedback(code, guess):
    """
    Return a namedtuple Feedback(blacks, whites) where
    blacks is the number of pegs from the guess that
    are correct in both color and position and
    whites is the number of pegs of the right color but wrong position.
    """
    blacks = sum(g == c for g, c in zip(guess, code))
    whites = sum((Counter(guess) & Counter(code)).values()) - blacks

    return Feedback(blacks, whites)


def turn(guess, turn_num):
    """Input feedback of the turn."""
    def input_pegs(message):
        while True:
            try:
                user_input = int(input(message))
            except ValueError:
                print("Enter an integer from 0 to 4 inclusively. Try again.")
            else:
                if user_input >= 0 and user_input <= 4:
                    return user_input
                else:
                    print("Enter an integer from 0 to 4. Try again.")

    print()
    print("Turn", turn_num)
    print("Guess:", guess)
    blacks = input_pegs("Blacks: ")
    whites = input_pegs("Whites: ")

    return Feedback(blacks, whites)


def reduce_possible_codes(possible_codes, guess, fb):
    """Return a set with all elements from possible_codes that would receive
    the same feedback as the actual feedback from guess, fb,
    if guess was the secret code."""

    return {code for code in possible_codes if feedback(code, guess) == fb}


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
        fbs = [feedback(code, guess) for code in possible_codes]
        return len(possible_codes) - max(Counter(fbs).values())

    scores = [ScoreData(guess, score(guess), guess in possible_codes)
              for guess in sorted(init_possible_codes - past_guesses)]

    return max(scores, key=attrgetter('score', 'is_possible_code')).guess


def game():
    """
    Five-guess algorithm steps are directly from the Mastermind wikipedia page:
    https://en.wikipedia.org/wiki/Mastermind_(board_game)#Five-guess_algorithm
    """
    # 1. Create the set S of 1296 possible codes
    # (1111, 1112 ... 6665, 6666)
    possible_codes = init_possible_codes.copy()
    guesses = set()

    # 2. Start with initial guess 1122
    turn_num = 1
    guess = (1, 1, 2, 2)

    while True:
        # 3. Play the guess to get a response of coloured and white pegs.
        guesses.add(guess)
        fb = turn(guess, turn_num)

        # 4. If the response is four colored pegs,
        # the game is won, the algorithm terminates.
        if fb.blacks == 4:
            print()
            break

        # 5. Otherwise, remove from S any code that would not give the same
        # response if it (the guess) were the code.
        possible_codes = reduce_possible_codes(possible_codes, guess, fb)

        # 6. Apply minimax technique to find a next guess.
        guess = next_guess(possible_codes, guesses)

        # 7. Repeat from step 3
        turn_num += 1


def main():
    while True:
        game()

        again = ""
        while again not in ['y', 'n']:
            answer = input("Play again? (y/n) ")
            if answer:
                again = answer[0].lower()

        if again == 'n':
            break


if __name__ == "__main__":
    main()
