import json
import csv
import os
import collections
import plotly.express as px

KEYWORDS = {
    'asian',
    'indian',
    'japanese',
    'black',
    'ebony'
}

def documentToWords(document):
    document = document.lower()
    document = document.replace('.', '')
    document = document.replace(',', '')
    document = document.replace('<br /><br />', ' ')
    words = document.split(' ')
    return words

def documentToTuples(document):
    tuples = []
    words = documentToWords(document)
    num_words = len(words)
    for index in range(num_words):
        if index + 1 < len(words):
            tuples.append((words[index], words[index+1]))

    # print(tuples)
    return tuples


def createGoodWordsFrequency():
    all_words = []

    paths = [
        os.path.relpath('./data/good_words/pos'),
        os.path.abspath('./data/good_words/pos2'),
        os.path.abspath('./data/good_words/neg'),
        os.path.abspath('./data/good_words/neg1')
    ]
    for path in paths:
        for filename in os.listdir(path):
            with open(os.path.join(path, filename), 'r') as f:
                review = f.read()
                words = documentToTuples(review)
                all_words.extend(words)

    document_frequency = collections.Counter(all_words)
    return document_frequency

def createBadWordsFrequency():
    all_words = []

    path = os.path.abspath('/Users/isaac/Programming/BadWords/bad_words_code/data/bad_words/xnxx.json')
    with open(path, 'r') as f:
        data = json.loads(f.read())
    
    for datum in data.values():
        document = datum['title']
        words = documentToTuples(document)
        all_words.extend(words)

    document_frequency = collections.Counter(all_words)
    return document_frequency

def containsKeywords(words):
    if words[0] in KEYWORDS:
        return True
    if words[1] in KEYWORDS:
        return False

def compareFrequencies(first, second, limit=10000):
    compare_frequencies = []
    
    top_n = first.most_common(limit)

    total_first = sum(first.values())
    total_second = sum(second.values())

    for (word, total) in top_n:
        
        bad_freq = first[word] / total_first
        good_freq = second[word] / total_first

        if(containsKeywords(word)):
            group = 'racialized'
        else:
            group = 'non-racialized'

        compare_frequencies.append({
            "word": word,
            "bad_freq": bad_freq,
            "good_freq": good_freq,
            "group": group
        })

    return compare_frequencies


if __name__ == '__main__':
    good_freq = createGoodWordsFrequency()
    bad_freq = createBadWordsFrequency()

    df = compareFrequencies(bad_freq, good_freq)
    fig = px.scatter(df, x="bad_freq", y="good_freq", hover_data=['word'], color="group")
    fig.show()

