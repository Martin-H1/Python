import sys
from enum import Enum

def load_words(filename):
    with open(filename) as sourcefile:
        words = sourcefile.read().splitlines()
        return words

class Context:
    """
    A context block is used to hold search state between guesses
    """
    def __init__(self):
        self.must_contain = ""
        self.exclude = ""
        self.candidate_words = []

class Match:
    """
    An enum type to scores letters in a word.
    """
    Exclude = -10
    Miss = 0
    Partial = 1
    Exact = 2

def score_guess(guess, word, exclude):
    # Assume no matches
    retval = [Match.Miss, Match.Miss, Match.Miss, Match.Miss, Match.Miss]

    # Check for a match anywhere.
    for idx in range(5):
        gchar = "" + guess[idx]
        if word.find(gchar) != -1:
            retval[idx] = Match.Partial

    # Check for exact matches
    for idx in range(5):
        if guess[idx] == word[idx]:
            retval[idx] = Match.Exact

    # Check for excluded letters
    for idx in range(5):
        gchar = "" + word[idx]
        if exclude.find(gchar) != -1:
            retval[idx] = Match.Exclude

    return retval

def filter_words(guess, words, exclude):
    retval = []
    for word in words:
        score = sum(score_guess(guess, word, exclude))
        print(guess + " " + word + " " + str(score))
        # a nonzero score means the word is a candidate
        if (score > 0):
            retval.append(word)
    return retval

# Create a global with all words.
words = load_words("words.txt")

secret = "frost"

guess = "salet"
print(filter_words(guess, words, "y"))
