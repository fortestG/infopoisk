import os
import re

from bs4 import BeautifulSoup
import nltk
from collections import defaultdict
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context



nltk.download('stopwords')
nltk.download('punkt')
nltk.download('snowball_data')
nltk.download('perluniprops')
nltk.download('universal_tagset')
nltk.download('stopwords')
nltk.download('nonbreaking_prefixes')
nltk.download('wordnet')
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
sw = stopwords.words('english')

DIRECTORY = "output"


def get_tokens(s):
    tok = RegexpTokenizer('[A-Za-z]+')
    clean = tok.tokenize(s)
    clean = [w.lower() for w in clean if w != '']
    clean = [w for w in clean if w not in sw]
    return list(set(clean))


def get_lemmas(tokens):  
    lem = WordNetLemmatizer()
    lemmas = []
    for t in tokens:
        if re.match(r'[A-Za-z]', t):
            l = lem.lemmatize(t)
            lemmas.append(l)
    return lemmas


def get_lemmas_dict(tokens):
    lem = WordNetLemmatizer()
    lemmas = defaultdict(list)
    for t in tokens:
        if re.match(r'[A-Za-z]', t):
            l = lem.lemmatize(t)
            lemmas[l].append(t)
    return lemmas


def get_every_file():
    for root, dirs, files in os.walk(DIRECTORY):
        for file in files:
            if file.lower().endswith('.txt'):

                path_file = os.path.join(root, file)
                with open(path_file, encoding="utf-8") as f:
                    html_text = f.read()

                soup = BeautifulSoup(html_text, "html.parser")
                text = ' '.join(soup.stripped_strings)
                tokens = get_tokens(text)
                tokens_string = '\n'.join(tokens)

                path_result = f"output_clear/tokens_{file}"
                os.makedirs(os.path.dirname(path_result), exist_ok=True)
                with open(path_result, "w", encoding="utf-8") as file_result:
                    file_result.write(tokens_string)

                lemmas_dict = get_lemmas_dict(tokens)
                path_result = f"output_clear/lemmas_{file}"

                with open(path_result, "w", encoding="utf-8") as file_result:
                    for k, v in lemmas_dict.items():
                        file_result.write(k + ": ")
                        for word in v:
                            file_result.write(word + " ")
                        file_result.write("\n")


def get_common():
    tokens = []
    for root, dirs, files in os.walk(DIRECTORY):
        for file in files:

            if file.lower().endswith('.txt'):
                path_file = os.path.join(root, file)
                print(path_file)
                with open(path_file, encoding="utf-8") as f:
                    html_text = f.read()
                soup = BeautifulSoup(html_text, "html.parser")
                text = ' '.join(soup.stripped_strings)
                tokens += get_tokens(text)

    tokens = list(set(tokens))
    tokens_string = '\n'.join(tokens)

    path_result = f"../preprocessing/output_clear_all/tokens.txt"
    os.makedirs(os.path.dirname(path_result), exist_ok=True)
    with open(path_result, "w", encoding="utf-8") as file_result:
        file_result.write(tokens_string)

    lemmas_dict = get_lemmas_dict(tokens)
    path_result = f"../preprocessing/output_clear_all/lemmas.txt"
    with open(path_result, "w", encoding="utf-8") as file1_result:
        for k, v in lemmas_dict.items():
            print(k)
            file1_result.write(k + ": ")
            for word in v:
                file1_result.write(word + " ")
            file1_result.write("\n")


if __name__ == "__main__":
    get_every_file()
    get_common()
