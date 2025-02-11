import gensim
import gensim.models
from gensim.models import Word2Vec
import os
import zipfile
import numpy as np
from gensim.models import KeyedVectors

# Чтение текста из файла
input_file_path = '2.txt'

with open(input_file_path, 'r', encoding='utf-8') as infile:
    # Загрузка данных и разбиение на слова
    sentences = [line.strip().split() for line in infile if line.strip()]

# Параметры для моделей
window_size = 10
min_count = 2  # Исключаем слова, встречающиеся только 1 раз


# sg — используемый алгоритм обучения (0 — CBOW, 1 — Skip-gram)
#Обучение модели CBOW с размерностью векторов 500
cbow_model_500 = Word2Vec(sentences, vector_size=500, window=window_size, min_count=min_count, sg=0)
cbow_model_500.save("cbow_500.model")

# Обучение модели Skip-gram с размерностью векторов 300
skipgram_model_300 = Word2Vec(sentences, vector_size=300, window=window_size, min_count=min_count, sg=1)
skipgram_model_300.save("skipgram_300.model")

# Сравнение результатов: просто выводим информацию о количестве векторов
print("CBOW Model (500 dimensions):")
print("Vocabulary size:", len(cbow_model_500.wv.key_to_index))

print("\nSkip-gram Model (300 dimensions):")
print("Vocabulary size:", len(skipgram_model_300.wv.key_to_index))

query_words = ["эпоха_NOUN", "ночь_NOUN", "семантика_NOUN", "студент_NOUN", "студент_ADJ"]
for word in query_words:
    if word in cbow_model_500.wv.key_to_index:
        similar_words_cbow = cbow_model_500.wv.most_similar(word, topn=5)
        print(f"Most similar words to '{word}': {similar_words_cbow}")
    else:
        print(f"Word '{word}' not in vocabulary of CBOW model.")
        
print("\nSkip-gram Model Similar Words:")
for word in query_words:
    if word in skipgram_model_300.wv.key_to_index:
        similar_words_skipgram = skipgram_model_300.wv.most_similar(word, topn=5)
        print(f"Most similar words to '{word}': {similar_words_skipgram}")
    else:
        print(f"Word '{word}' not in vocabulary of Skip-gram model.")
#       
#print("\nCBOW Model Analogies:")
#cbow_analogy = cbow_model_500.wv.most_similar(positive=['студент_NOUN', 'женщина_NOUN'], negative=['мужчина_NOUN'], topn=5)
#print("CBOW analogy results:", cbow_analogy)
#
#print("\nSkip-gram Model Analogies:")
#skipgram_analogy = skipgram_model_300.wv.most_similar(positive=['студент_NOUN', 'женщина_NOUN'], negative=['мужчина_NOUN'], topn=5)
#print("Skip-gram analogy results:", skipgram_analogy)
#

# Загрузка модели из НКРЯ
nkr_model_path = '180.zip'

# Проверяем, существует ли файл
if not os.path.isfile(nkr_model_path):
    # Загружаем файл, если он отсутствует
    print("Downloading the NKRJ model...")
    import requests
    r = requests.get("http://vectors.nlpl.eu/repository/20/180.zip", allow_redirects=True)
    open(nkr_model_path, 'wb').write(r.content)

# Распаковка файла
\
# Загрузка модели NKRJ
nkr_model = KeyedVectors.load_word2vec_format("nkr_model/model.txt", binary=False)

# Слова, для которых нужно найти ближайших соседей
words_to_check = ["день_NOUN", "ночь_NOUN", "семантика_NOUN", "студент_NOUN", "студент_ADJ"]

# Поиск ближайших соседей и косинусной близости
for word in words_to_check:
    try:
        print(f"\nWord: {word}")
        similar_words = nkr_model.most_similar(word, topn=10)
        for similar_word, similarity in similar_words:
            print(f"{similar_word}, cosine similarity: {similarity:.4f}")
    except KeyError:
        print(f"Word '{word}' not found in the NKRJ model.")
        
#    в инструкции так было
        
#for word in words_to_check:
#   # есть ли слово в модели? Может быть, и нет
#   if word in nkr_model:
#       print(word)
#       # выдаем 10 ближайших соседей слова:
#       for i in nkr_model.most_similar(positive=[word], topn=10):
#           # слово + коэффициент косинусной близости
#           print(i[0], i[1])
#       print('\n')
#   else:
#       # Увы!
#       print(word + ' is not present in the model')