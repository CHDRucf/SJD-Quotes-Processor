# A regular expression library.
import re

# The sentence segmentation algorithm.
# For now, its inputs are taken as arguments to the function.
def tokenize(quote, textFileAsString):

    # This tokenizes the text file based on punctuation,
    # but leaves the punctuation as their own tokens.
    tokens = re.split('([.?!])', textFileAsString)

    # The regex creates an element '' at the end of the array, so we want to remove it.
    tokens.pop()

    i = 0
    while i < len(tokens):

        # We need to append these punctuation marks to the previous sentence.
        if i < len(tokens):
            if tokens[i] == '?' or tokens[i] == '!':
                tokens[i - 1] += tokens[i]
                tokens.pop(i)

        # We need to detect if the period ended a sentence before knowing what to append.
        if i < len(tokens):
            if tokens[i] == '.':
                # Implement period detection algorithm here
                placeholder = 0

        i += 1

    return tokens

tokenArray = tokenize("yep", "How do you do? I'm doing fine. It's good to see you!")
print(tokenArray)
