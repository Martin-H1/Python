import sys
from enum import Enum

def load_words(filename):
    with open(filename) as sourcefile:
        words = sourcefile.read().splitlines()
        return words

class Match:
    """
    An enum type to scores letters in a word.
    """
    Exclude = -10
    Miss = 0
    Partial = 1
    Exact = 2

class Context:
    """
    A context block is used to hold search state between guesses
    """
    def __init__(self):
        self.contains = ""
        self.excludes = ""
        self.candidate_words = []
        self.word = [ '*', '*', '*', '*', '*' ]

    def __str__(self):
        retVal = ("contains=" + self.contains +
                  ", excludes=" + self.excludes +
                  ", word=" + str(self.word) +
                  ", candidate_words=" + str(self.candidate_words))
        return retVal

def score_guess(guess, context):
    # Assume no matches
    retval = [Match.Miss, Match.Miss, Match.Miss, Match.Miss, Match.Miss]

    # Check for a match anywhere.
    for idx in range(5):
        gchar = guess[idx]
        if secret.find(gchar) != -1:
            retval[idx] = Match.Partial

    # Check for exact matches
    for idx in range(5):
        if guess[idx] == secret[idx]:
            retval[idx] = Match.Exact

    return retval

def filter_word(word, context):
    retval = True

    # Check for excluded letters
    for gchar in word:
        if context.excludes.find(gchar) != -1:
            return False

    # Check that all contained letters are present.
    for c in context.contains:
        if word.find(c) == -1:
            return False

    # Check for any required letters.
    for idx in range(5):
        gchar = context.word[idx]
        if gchar != '*' and word[idx] != gchar:
            return False

    return retval

def filter_words(guess, words, context):
    print("Guess = " + guess + ", input number of words = " + str(len(words)))
    # First score the guess to enabling filtering
    score = score_guess(guess, context)
    print(score)

    # Add each letter's score to appropriate filter criteria.
    for idx in range(5):
        # Add any misses to excluded letters.
        if score[idx] == Match.Miss:
            context.excludes += guess[idx]

        # Add any partials to the contains list.
        if score[idx] == Match.Partial:
            context.contains += guess[idx]

        # Add any exact to the target word.
        if score[idx] == Match.Exact:
            context.word[idx] = guess[idx]

    # Now use the context to filter the word list.
    retval = []
    for word in words:
        if filter_word(word, context):
            retval.append(word)
    context.candidate_words = retval
    return retval

# Create a global with all words.
words = load_words("words.txt")

secret = "frost"

ctx = Context()
ctx.excludes = ""

guess = "salet"
filter_words(guess, words, ctx)
print(ctx)
filter_words(ctx.candidate_words[0], ctx.candidate_words, ctx)
print(ctx)
filter_words(ctx.candidate_words[0], ctx.candidate_words, ctx)
print(ctx)