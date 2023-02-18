import sys
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from random import seed
from random import randint


def process_text(preproc_tokens):
    """
    Does the bulk of Step 3 in this function and returns the requested tokens and nouns as specified
    """
    # Preprocess the Raw Text with Added Length Condition
    preproc_tokens = [t for t in preproc_tokens if len(t) > 5]
    # Lemma-tize the words
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in preproc_tokens]
    unique_lemmas = list(set(lemmas))
    lemmas_tagged = pos_tag(unique_lemmas)
    noun_list = []
    for lemma, tag in lemmas_tagged:
        if tag == 'NN':
            noun_list.append(lemma)

    print('Number of Tokens:', len(preproc_tokens))
    print('Number of Nouns:', len(noun_list))
    # I ASSUME tokens means the preprocessed tokens
    return preproc_tokens, noun_list


def begin_game(list_nouns):
    """
    The game takes the list of nouns that have already been processed and infinitely runs the game until the conditions
    are met
    """
    seed(170230)
    points = 5
    word_chosen = list_nouns[randint(0, 49)]
    guess_words = ''
    for i in range(len(word_chosen)):
        guess_words += '_'
    listed_words = list(guess_words)

    print('Let\'s play a word guessing game!')
    print('CHEAT: Chosen word is', word_chosen)
    print(' '.join(listed_words))
    print('Guess a letter: ', end='')
    user_input = str(input())
    if user_input == '!':  # Just in case they want to immediately exit
        print('Bye bye!')
        return

    while True:
        if user_input in word_chosen and not (user_input in guess_words) and not (user_input == '_'):
            indices = [i for i, x in enumerate(word_chosen) if x == user_input]  # Provides all indexes of the letter
            for index in indices:
                listed_words[index] = user_input
            points += 1
            print('Right! Score is', points)
            print(' '.join(listed_words))

        else:
            points -= 1
            if points < 0:
                print('Try again next time!')
                return
            print('Sorry!, guess again. Score is', points)

        num_blanks = listed_words.count('_')
        if not num_blanks:  # Basically when it reaches 0 '_'s
            print('You solved it!')
            print('Current score:', points)
            print('Let \'s play again!')
            # Now we just reuse the piece of code at the top
            word_chosen = list_nouns[randint(0, 49)]
            guess_words = ''
            for i in range(len(word_chosen)):
                guess_words += '_'
            listed_words = list(guess_words)
            print(' '.join(listed_words))
            print('CHEAT: Chosen word is', word_chosen)

        print('Guess a letter: ', end='')
        user_input = str(input())

        if user_input == '!':
            print('Bye bye!')
            return


def main():
    if len(sys.argv) > 1:
        file_input = sys.argv[1]
    else:
        print('ERROR: NO FILE PATH PROVIDED!')
        exit()
    with open(file_input, 'r') as f:
        text = f.read()

    # Lexical Diversity (Step 2)
    tokens = [t.lower() for t in word_tokenize(text)]
    preproc_tokens = [t for t in tokens if t.isalpha() and
                      t not in stopwords.words('english')]

    num_tokens = len(tokens)
    unique_tokens = len(set(tokens))

    lexical_diversity = unique_tokens / num_tokens
    print('Lexical Diversity: %.2f' % lexical_diversity)
    processed_tokens, nouns = process_text(preproc_tokens)

    # Step 4, Making a dictionary
    # To get an accurate count of nouns, I think I have to re-lemmatize them since
    # some would show up as 0 count
    wnl = WordNetLemmatizer()
    lemmas_token = [wnl.lemmatize(t) for t in preproc_tokens]
    dict_nouns = {t: lemmas_token.count(t) for t in nouns}
    dict_nouns_sorted = sorted(dict_nouns.items(), key=lambda item: item[1], reverse=True)
    print("50 most common words with counts:")
    print(dict_nouns_sorted[:50])
    dict_nouns_sorted = dict(dict_nouns_sorted)  # Technically a dictionary as requested
    list_nouns = sorted(dict_nouns, key=dict_nouns.get, reverse=True)

    # Step 5, Creating the guessing game
    begin_game(list_nouns[:50])


if __name__ == '__main__':
    main()
