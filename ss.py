# A regular expression library.
import re

# The sentence segmentation algorithm.
# For now, its inputs are taken as arguments to the function.
def tokenizeAndCompare(quote, textFileAsString):

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
            
                # Handles abbreviations and "normal" periods.
                prevToken = tokens[i - 1].split(" ")[-1]
                # check for match with abbreviation list???
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

        i += 1

    # At this point each token contains a single sentence from the text.
    # Two undeclared functions: weightedAverage and updateTopFive.
    # Out of bounds index checks are not currently implemented.

    j = 0
    while (j < len(tokens)):
        
        # Stores the results of comparisons between the quote and a token.
        score = 0
    
        # Compare each token with the entire quote.
        score = weightedAverage(tokens[j], quote)

        # Combine the current token with future ones until a lower score is returned.
        k = 1
        curr = tokens[j]
        final = ""
        while (1):

            # Append the next token.
            curr += tokens[j + k]
            final += tokens[j + k - 1]

            # Get the new score.
            newScore = weightedAverage(curr, quote)

            if newScore > score:
                score = newScore
            else:
                break

            k += 1

        updateTopFive(final, score)

        j += 1

    return tokens

tokenArray = tokenizeAndCompare("yep", "How do you do? I'm doing fine. It's good to see you!")
print(tokenArray)
