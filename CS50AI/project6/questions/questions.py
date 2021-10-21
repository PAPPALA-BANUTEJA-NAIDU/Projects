import nltk
import sys
import os, math, string

FILE_MATCHES = 2
SENTENCE_MATCHES = 3


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    
    ht = {}
    for text_file in os.listdir(directory):
        with open(os.path.join(directory, text_file), "r", encoding="utf-8") as file:
            ht[text_file] = file.read()
    return ht


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens = nltk.tokenize.word_tokenize(document.lower())
    word_list = [x for x in tokens if x not in string.punctuation and x not in nltk.corpus.stopwords.words("english")]

    return word_list


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idf_dict = {}
    length = len(documents)

    # Unique words
    vocab = set(sum(documents.values(), []))

    for word in vocab:
        count = 0
        for word_list in documents.values():
            if word in word_list:
                count += 1
        idf_dict[word] = math.log(length/count)
    return idf_dict


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    scores = dict()

    for filename, value in files.items():
        tf_idf = 0
        for word in query:
            if word in value:
                tf_idf += value.count(word) * idfs[word]
        if tf_idf != 0:
            scores[filename] = tf_idf
    sorted_score = [k for k, v in sorted(scores.items(), key=lambda x: x[1], reverse=True)]
    return sorted_score[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    scores = {}
    for sentence, words in sentences.items():
        score = 0
        for word in query:
            if word in words:
                score += idfs[word]

        if score != 0:
            density = sum([words.count(x) for x in query]) / len(words)
            scores[sentence] = (score, density)

    sorted_score = [k for k, v in sorted(scores.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)]

    return sorted_score[:n]


if __name__ == "__main__":
    main()
