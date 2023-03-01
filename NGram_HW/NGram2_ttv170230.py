from nltk import word_tokenize
from nltk.util import ngrams
import pickle


def main():
    # Unpickling them here
    lang1_uni = pickle.load(open('lang1_uni.p', 'rb'))
    lang1_bi = pickle.load(open('lang1_bi.p', 'rb'))
    lang2_uni = pickle.load(open('lang2_uni.p', 'rb'))
    lang2_bi = pickle.load(open('lang2_bi.p', 'rb'))
    lang3_uni = pickle.load(open('lang3_uni.p', 'rb'))
    lang3_bi = pickle.load(open('lang3_bi.p', 'rb'))

    v = len(lang1_uni) + len(lang2_uni) + len(lang3_uni)
    print('Prob of this is:', compute_prob('Whatever', lang1_uni, lang2_bi, v))


def compute_prob(text, unigram_dict, bigram_dict, v):
    unigrams_text = word_tokenize(text)
    bigrams_text = list(ngrams(unigrams_text, 2))
    prob = 0

    for bigram in bigrams_text:
        b = bigram_dict[bigram] if bigram in bigram_dict else 0
        u = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0
        prob = (b + 1) / (u + v)

    return prob


if __name__ == "__main__":
    main()
