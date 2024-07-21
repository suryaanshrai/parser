import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red" | "quick" | "brown" | "lazy"
Adv -> "down" | "here" | "never" 
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word" | "dog" | "fox"
P -> "at" | "before" | "in" | "of" | "on" | "to" | "over"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were" | "jumps"
"""

NONTERMINALS = """
S -> NP VP | NP Adv VP | Adv S | S Adv | S Conj S | NP | VP
AdjP -> Adj | Adj AdjP
NP -> N | Det N | AdjP NP | PP NP | Det AdjP N
PP -> P | PP NP
VP -> V | VP NP | VP NP PP
"""

# 8 9

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = nltk.tokenize.word_tokenize(sentence)
    tokens = list()
    for i in words:
        i = i.lower()
        if i.isalpha():
            tokens.append(i)
    return tokens


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    noun_phrases = list()
    for i in tree.subtrees():
        if i.label() == "NP":
            noun_phrases.append(i)
    for i in noun_phrases.copy():
        for j in noun_phrases.copy():
            if i != j and i in j.subtrees():
                noun_phrases.remove(j)
    return noun_phrases


if __name__ == "__main__":
    main()
