# A regular expression library.
import re

# The sentence segmentation algorithm.
# For now, its inputs are taken as arguments to the function.
def tokenize(quote, textFileAsString):

    # Set to true while processing an ellipsis.
    ellipsisFlag = 0

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
                continue

        # We need to detect if the period ends a sentence before knowing what to append.
        if i < len(tokens):
            if tokens[i] == '.':

                # Handles ellipses.
                if tokens[i + 1] == '.':
                    ellipsisFlag = 1
                    tokens[i - 1] += tokens[i]
                    tokens.pop(i)
                    continue
                if ellipsisFlag = 1:
                    tokens[i - 1] += tokens[i]
                    tokens.pop(i)
                    ellipsisFlag = 0
                    continue

                # Handles acronyms and decimal numbers.
                if tokens[i + 1][0].isalnum():
                    tokens[i] += tokens[i + 1]
                    tokens[i - 1] += tokens[i]
                    tokens.pop(i + 1)
                    tokens.pop(i)
                    continue
            
                # Handles abbreviations.
                prevToken = tokens[i - 1].split(" ")[-1]
                if prevToken.matches(abbreviationList):
                    if tokens[i + 1][1].isUpper():
                        tokens[i - 1] += tokens[i]
                        tokens.pop(i)
                        continue
                    else
                        tokens[i] += tokens[i + 1]
                        tokens[i - 1] += tokens[i]
                        tokens.pop(i + 1)
                        tokens.pop(i)
                        continue
                else
                    tokens[i - 1] += tokens[i]
                    tokens.pop(i)
                    continue

        i += 1

    return tokens

tokenArray = tokenize("yep", "How do you do? I'm doing fine. It's good to see you!")
print(tokenArray)
