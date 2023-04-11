import math

from search_index.task_03 import get_inverted_index
from preprocessing.task_02 import get_tokens, get_lemmas
from tfidf_counter.task_04 import get_tf_terms


inverted_idx = get_inverted_index()
tf_idf_dicts_lemmas, idf_lemmas = get_tf_terms("lemmas")
ALL_DOCS_COUNT = 100


def vector_norm(vec):
    return sum([el ** 2 for el in vec]) ** 0.5


def parse_index():
    with open('index.txt') as f:
        return {int(s.split()[0]): s.split()[1] for s in f.readlines()}


def calculate_tfidf(term, document_tokens_list, documents_count, documents_with_term_count):

    tf = document_tokens_list.count(term) / len(document_tokens_list)
    if documents_with_term_count == 0:
        idf = 0
    else:
        idf = math.log(documents_count / documents_with_term_count)

    return round(tf, 6), round(idf, 6), round(tf * idf, 6)


def count_cosine_similarity(vec1, vec2):
    dot = 0
    for x1, x2 in zip(vec1, vec2):
        dot += x1 * x2
    if dot == 0:
        return 0
    return dot / (vector_norm(vec1) * vector_norm(vec2))


def search(query):
    print("SEARCHING: {}".format(query))
    tokens = get_lemmas(get_tokens(query))
    index_dict = parse_index()
    if len(tokens) == 0:
        print("Empty query")
        return

    query_vector = []

    for token in tokens:
        doc_with_terms_count = sum(token in tf_idf_dict for tf_idf_dict in tf_idf_dicts_lemmas)
        _, _, tf_idf = calculate_tfidf(token,
                                 tokens,
                                 ALL_DOCS_COUNT,
                                 doc_with_terms_count)
        query_vector.append(tf_idf)

    distances = {}

    for index in range(ALL_DOCS_COUNT):
        document_vector = []

        for token in tokens:
            try:
                tf_idf = tf_idf_dicts_lemmas[index][token]
                document_vector.append(tf_idf)
            except KeyError:
                document_vector.append(0.0)

        distances[index] = count_cosine_similarity(query_vector, document_vector)

    searched_indices = sorted(distances.items(), key=lambda x: x[1], reverse=True)
    print(searched_indices)
    result_data = []
    for index in searched_indices:
        try:
            doc_id, tf_idf = index
            if tf_idf < 0.01:
                continue

            print("Document: {} ({})\nCosine_similarity: {}\n".format(doc_id, index_dict[doc_id], tf_idf))
            result_data.append({'doc_id': doc_id, 'link': index_dict[doc_id], 'cosine_sim': tf_idf})
        except KeyError:
            pass
    return result_data


if __name__ == "__main__":
    query = input()
    search(query)
