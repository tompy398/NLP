from nltk import word_tokenize
from nltk.util import ngrams
import pickle


def main():
    # Unpickling them here
    langEng_uni = pickle.load(open('langEnglish_uni.p', 'rb'))
    langEng_bi = pickle.load(open('langEnglish_bi.p', 'rb'))
    langFr_uni = pickle.load(open('langFrench_uni.p', 'rb'))
    langFr_bi = pickle.load(open('langFrench_bi.p', 'rb'))
    langIt_uni = pickle.load(open('langItalian_uni.p', 'rb'))
    langIt_bi = pickle.load(open('langItalian_bi.p', 'rb'))

    v = len(langEng_uni) + len(langFr_uni) + len(langIt_uni)

    new_file = open('results_file.txt', 'w')

    # Index 0 - English, Index 1 - French, Index 2 - Italian
    text_line = 1
    prob_list = [0, 0, 0]
    with open('data/LangId.test', encoding='utf-8') as test_file:
        file_text = test_file.read()
        file_text = file_text.split('\n')
        for line in file_text:
            if line == '':  # Just for the test file's last line
                continue
            eng_prob = compute_prob(line, langEng_uni, langEng_bi, v)
            fr_prob = compute_prob(line, langFr_uni, langFr_bi, v)
            it_prob = compute_prob(line, langIt_uni, langIt_bi, v)

            lang_prob = {'English': eng_prob,
                         'French': fr_prob,
                         'Italian': it_prob}
            max_lang = max(lang_prob, key=lang_prob.get)  # Grabs the key with the highest prob value
            new_file.write(str(text_line) + ' ' + str(max_lang) + '\n')
            text_line += 1

            prob_list[0] += eng_prob
            prob_list[1] += fr_prob
            prob_list[2] += it_prob
    max_prob = max(prob_list)
    max_index = prob_list.index(max_prob)
    hi_prob_file = open('highest_prob.txt', 'w')
    if max_index == 0:
        hi_prob_file.write('Highest Probability Language for File is ' + 'English')
    elif max_index == 1:
        hi_prob_file.write('Highest Probability Language for File is ' + 'French')
    elif max_index == 2:
        hi_prob_file.write('Highest Probability Language for File is ' + 'Italian')
    # Have to close and Reopen the file to read it
    new_file.close()
    new_file = open('results_file.txt', 'r')
    results = new_file.read()
    test_file = open('data/LangId.sol', 'r')
    test_file = test_file.read()

    my_results = results.split('\n')
    test_results = test_file.split('\n')
    correct = 0
    incorrect_lines = []
    for i in range(0, 300):
        if my_results[i] == test_results[i]:
            correct += 1
        else:
            incorrect_lines.append(i)
    print("Accuracy:", str((correct / 300) * 100) + '%')
    print("Incorrect Lines:", incorrect_lines)


def compute_prob(text, unigram_dict, bigram_dict, v):
    unigrams_text = word_tokenize(text)
    bigrams_text = list(ngrams(unigrams_text, 2))
    prob_laplace = 1

    for bigram in bigrams_text:
        b = bigram_dict[bigram] if bigram in bigram_dict else 0
        u = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0
        prob_laplace = prob_laplace * (b + 1) / (u + v)

    return prob_laplace


if __name__ == "__main__":
    main()
