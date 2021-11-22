from collections import Counter
import random
import re

EXIT_COMMAND = "exit"
BIGRAM_ELEMENTS_COUNT = 2

file_name = input("Please enter the file name: ")

corpus = open(file_name, "rt", encoding="utf-8")
tokens = corpus.read().split()
bigrams = [[tokens[i], tokens[i + 1]] for i in range(0, len(tokens) - 1)]
counting_helper_dictionary = {}
bigrams_dictionary = {}

for bigram in bigrams:
    counting_helper_dictionary.setdefault(bigram[0], []).append(bigram[1])

for bigram in counting_helper_dictionary.items():
    bigrams_dictionary[bigram[0]] = Counter(bigram[1])


def get_sentence():
    first_word_pattern = "^[A-Z].+[^.?!]$"
    last_word_pattern = ".+[.?!]$"
    sentence = []

    first_word = random.choice(tokens)

    while re.match(first_word_pattern, first_word) is None:
        first_word = random.choice(tokens)

    sentence.append(first_word)
    previous_word = first_word

    while True:
        word = random.choices(list(bigrams_dictionary[previous_word].keys()), weights=tuple(bigrams_dictionary[previous_word].values()))[0]
        previous_word = word
        sentence.append(word)

        if re.match(last_word_pattern, sentence[-1]) is not None and len(sentence) >= 5:
            break
        else:
            continue

    return sentence


for i in range(0, 10):
    print(" ".join(get_sentence()))

corpus.close()
