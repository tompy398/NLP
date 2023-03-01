from nltk import word_tokenize
from nltk.util import ngrams
import pickle


def read_file(filename):
    with open(filename, 'r') as f:
        text = f.read()
    text = text.strip()
    tokenize = word_tokenize(text)
    unigrams = list(tokenize)
    bigrams = list(ngrams(tokenize, 2))

    unigram_dict = {t: unigrams.count(t) for t in set(unigrams)}
    bigram_dict = {t: bigrams.count(t) for t in set(bigrams)}

    return unigram_dict, bigram_dict


def main():
    # These are just placeholders -- The Langs need to be replaced
    uni1, bi1 = read_file('data/LangId.train.English')
    uni2, bi2 = read_file('data/LangId.train.French')
    uni3, bi3 = read_file('data/LangId.train.Italian')

    pickle.dump(uni1, open('langEnglish_uni.p', 'wb'))
    pickle.dump(bi1, open('langEnglish_bi.p', 'wb'))
    pickle.dump(uni2, open('langFrench_uni.p', 'wb'))
    pickle.dump(bi2, open('langFrench_bi.p', 'wb'))
    pickle.dump(uni3, open('langItalian_uni.p', 'wb'))
    pickle.dump(bi3, open('langItalian_bi.p', 'wb'))


if __name__ == "__main__":
    main()
